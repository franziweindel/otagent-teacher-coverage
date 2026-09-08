#!/usr/bin/env python3
"""Sweep the candidate repos, hash every instruction.md, print the tables.

Hashes every task's instruction.md across the repos
`find_candidate_repos.py` marked `candidate=True` (never joining by task id,
see `hash_sft10k_tasks.py`), then answers:

1. Joined with the OpenThoughts-Agent-SFT-10K tasks: to re-SFT the dataset
   with teacher X, how many trajectories must still be generated? The
   generation-gap table.
2. Extracts each task's data source, filters to the OT-Agent SFT-10K
   sources (swesmith, superuser, tezos, issue), and prints per teacher
   combination two overlaps: the tasks all its teachers share exactly
   (same instruction.md), and the tasks usable when they only need to come
   from the same source. There a comparison can use as many of a source's
   tasks as the combination's weakest teacher covers, summed over sources.
3. The same combination tables without the source filter, over everything
   swept.

Files under the cache dir (default
/data/cat/ws/frwe188h-otagent/tmp/agenttrove_cache). "in" = read here, the
script in parentheses creates it; "tmp" = this script's own resumable
cache; "out" = written here:

    sft_text.parquet        in   SFT-10K task hashes  (hash_sft10k_tasks.py)
    sweep/candidates.csv    in   the worklist         (find_candidate_repos.py)
    tasktrove_hashes/       in   task -> source registry (hash_tasktrove.py)
    sweep/hashes/<repo>.pq  tmp  every instruction hash + teacher per repo,
                                 unfiltered; a run resumes from these
    teacher_coverage.csv    out  teachers + trace repos per SFT-10K task
    sweep/sweep_status.csv  out  per repo: read or skipped, tasks matched
    sweep/instructions_by_teacher.csv
                            out  every instruction seen anywhere, its
                                 teachers, sources, and whether in SFT-10K

`--refresh` ignores the cached hashes. `--cached-only` skips repos not yet
fetched, for a fast re-report. `--sets-only` rebuilds only the combination
tables from the csv above, no fetch.

Caveat for question 1: every SFT-10K row is itself a GLM-4.7 trace, so a
GLM-4.7 rerun needs no generation at all; the tables count only traces found
in the swept repos.
"""

from __future__ import annotations

import argparse
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem

from find_candidate_repos import TEACHER_TOKENS, teacher_from_text
from hash_sft10k_tasks import (DEFAULT_CACHE, extract_task_text,
                               first_user_message, hashes_path, load_tasks,
                               text_hash)

#: Sources whose teacher is a per-row column rather than the repo name — the
#: concatenated dumps, where one repo holds many teachers.
TEACHER_COLUMNS = {"open-thoughts/AgentTrove": "original_teacher"}

#: Teacher precedence, per row: TEACHER_OVERRIDES for the repo, else the
#: `original_teacher` column where a repo has one (TEACHER_COLUMNS), else the
#: `model` column, else `resolve_bare_glm` (run_id evidence), else the
#: repo name, else "<unknown>".
#:
#: `model` usually wins: `moonshotai/Kimi-K2-Thinking`, `QuantTrio/GLM-4.6-AWQ`
#: and `gpt-5-nano-2025-08-07` are exact where the name is vague or silent. It
#: is only useless when it holds a numeric vLLM id
#: (`hosted_vllm/1774312518071260`) or a version-less `hosted_vllm/glm` — both
#: resolve to nothing, leaving the task under "<unknown>" rather than under a
#: guessed version.
#:
#: Bare `hosted_vllm/glm` rows are resolved by `resolve_bare_glm` from the
#: `run_id` column instead (evidence recorded in sweep_status.csv). What that
#: cannot decide stays "<unknown>" unless this map asserts a teacher, with the
#: reasoning here:
#: - `a1_issue_tasks` is the renamed `exp_rpt_issue_10k_glm_4.7_traces_jupiter`
#:   (HF redirects the old name). Its rows are bare `hosted_vllm/glm` and share
#:   no run_id with SFT-10K, so it is not the source of SFT-10K's issue traces,
#:   but the old name fixes the teacher.
#: - `a1_swesmith` is bare `hosted_vllm/glm` dated 2026-01-16, after the
#:   GLM-4.7 release (2025-12-22) and before the GLM-5 release (2026-02-11);
#:   assuming the shared endpoint runs the newest GLM that is GLM-4.7. A
#:   judgment call, not proof, hence here and not in the code. Its one
#:   cross-check agrees: `a1_stackexchange_tezos` (2025-12-25, same window) is
#:   pinned to GLM-4.7 by run_id.
#: Still open: `stackexchange-tezos-sandboxes_glm_traces_blah` (2025-12-20,
#: before GLM-4.7 shipped) is 4.6 or 4.7, undecidable, stays "<unknown>".
TEACHER_OVERRIDES = {
    "DCAgent/a1_issue_tasks": "GLM-4.7",
    "DCAgent/a1_swesmith": "GLM-4.7",
}

#: One model, two spellings: AgentTrove's hand-typed `original_teacher` says
#: "GPT 5.1 Nano" where every such row's `model` is `gpt-5-nano-2025-08-07`,
#: the id that resolves to "GPT-5-nano" everywhere else. Applied to every
#: teacher label after resolution, so cached values are normalised too.
TEACHER_ALIASES = {"GPT 5.1 Nano": "GPT-5-nano"}


def canon_teacher(t: str) -> str:
    return TEACHER_ALIASES.get(t, t)


#: The teacher SFT-10K was generated with. Its `model` column is the same bare
#: `hosted_vllm/glm`, so this is asserted, not read (paper + repo card).
SFT10K_TEACHER = "GLM-4.7"

def task_prefix(task: object) -> object:
    """The source family off a task id: "tezos-0561" -> "tezos".

    The one in-row source signal that travels with the task itself (same id
    scheme as SFT-10K's families). AgentTrove's `original_source` column is
    assembly-time metadata regexed from source repo names and measurably
    wrong (superuser rows labelled swesmith, tezos labelled exp_tas), so the
    prefix is used instead. Generic ids ("task_0") carry no source: NA.
    """
    if not isinstance(task, str) or not task:
        return pd.NA
    pre = re.sub(r"[-_]*\d+$", "", task.strip()).lower()
    return pre if len(pre) >= 3 and pre not in ("task", "tasks") else pd.NA


#: Columns kept for rows whose model id resolves to nothing: `run_id` feeds
#: `resolve_bare_glm`, `model` and `date` stay cached for manual checks (the
#: date reasoning behind TEACHER_OVERRIDES), all without a refetch.
EVIDENCE_COLUMNS = ("model", "run_id", "date")


def resolve_bare_glm(found: pd.DataFrame, sft_runs: set[str]
                     ) -> tuple[pd.DataFrame, dict[str, int]]:
    """Fill the teacher of version-less `hosted_vllm/glm` rows by run_id.

    A row from the same generation run as an SFT-10K trajectory has SFT-10K's
    teacher: a run is one batch job driven by one model, and SFT-10K's runs
    are known SFT10K_TEACHER runs. Exact, so it is the only rule in code;
    weaker date reasoning lives in TEACHER_OVERRIDES as asserted judgment.

    Only touches rows whose model id contains ``glm`` and resolved to nothing;
    anything else keeps its value. Returns the frame and how many rows were
    decided, for the status table. A cache written before the evidence columns
    existed passes through untouched.
    """
    n = {"by_run_id": 0}
    if not all(c in found.columns for c in EVIDENCE_COLUMNS):
        return found, n
    found = found.copy()
    open_glm = (found["teacher"].isna()
                & found["model"].astype("string").str.contains("glm", case=False,
                                                              na=False))
    by_run = open_glm & found["run_id"].isin(sft_runs)
    found.loc[by_run, "teacher"] = SFT10K_TEACHER
    n["by_run_id"] = int(by_run.sum())
    return found, n


def repo_task_hashes(repo: str, parts_dir: Path | None = None) -> pd.DataFrame:
    """Instruction-text hash of every task a repo holds, and its teacher.

    Bare ``instruction`` column where present, else the first user message of
    ``conversations`` or ``messages`` stripped of the terminus-2 wrapper. The
    fallbacks are per row, since one repo can mix shapes.

    Every row is read. Nothing is filtered here, so the cache means the same
    thing for every repo and any later question is a join against it rather
    than a refetch. Row groups are read one at a time to bound memory, since
    AgentTrove's text sits in 18.8 GB of ``conversations``.

    ``parts_dir``: each finished shard is cached there, so a killed process
    loses at most one shard of a big repo instead of the whole repo. The
    caller deletes the directory once the combined result is cached.

    Raises if a repo yields no task text: an empty result is indistinguishable
    from "shares no task with SFT-10K", and that silent zero is the one failure
    that would corrupt the tables.
    """
    fs = HfFileSystem()
    teacher_col = TEACHER_COLUMNS.get(repo)
    frames: list[pd.DataFrame] = []
    n_rows = 0
    cols: list[str] = []
    paths = sorted(fs.glob(f"datasets/{repo}/**/*.parquet"))
    if not paths:
        raise ValueError("no parquet files (empty or non-parquet repo)")
    for pi, path in enumerate(paths):
        part = (parts_dir / f"{pi:05d}.parquet") if parts_dir else None
        if part is not None and part.exists():
            cached_part = pd.read_parquet(part)
            n_rows += len(cached_part) or 1     # count>=1: shard was readable
            frames.append(cached_part)
            continue
        shard_frames: list[pd.DataFrame] = []
        with fs.open(path) as fh:
            pf = pq.ParquetFile(fh)
            names = set(pf.schema_arrow.names)
            cols = [c for c in ("instruction", "conversations", "messages")
                    if c in names]
            if not cols:
                raise ValueError(f"no task-text column in {sorted(names)}")
            label_col = teacher_col if teacher_col in names else (
                "model" if "model" in names else None)
            if label_col:
                cols = cols + [label_col]
            evidence = [c for c in EVIDENCE_COLUMNS
                        if c in names and c not in cols]
            cols = cols + evidence
            if "task" in names and "task" not in cols:
                cols = cols + ["task"]
            for rg in range(pf.metadata.num_row_groups):
                df = pf.read_row_group(rg, columns=cols).to_pandas()
                n_rows += len(df)
                text = pd.Series(pd.NA, index=df.index, dtype="object")
                if "instruction" in df:
                    text = df["instruction"].where(
                        df["instruction"].map(
                            lambda v: isinstance(v, str) and bool(v)), pd.NA)
                for turns in ("conversations", "messages"):
                    need = text.isna()
                    if need.any() and turns in df:
                        text.loc[need] = (df.loc[need, turns]
                                          .map(first_user_message)
                                          .map(extract_task_text))
                out = pd.DataFrame({"hash": text.map(text_hash)})
                if not label_col:                 # repo names no model at all
                    out["teacher"] = pd.NA
                elif label_col == teacher_col:    # already a teacher name
                    out["teacher"] = df[label_col]
                else:                             # a model id, resolve it
                    out["teacher"] = df[label_col].map(teacher_from_text)
                out["teacher"] = out["teacher"].replace("", pd.NA)
                out["source_prefix"] = (df["task"].map(task_prefix)
                                        if "task" in df else pd.NA)
                # evidence only where it is needed, so the cache stays one row
                # per (hash, teacher) for resolved rows
                for c in EVIDENCE_COLUMNS:
                    val = df[c] if c in df else pd.Series(pd.NA, index=df.index)
                    if c == "date":
                        val = val.astype("string").str.slice(0, 10)
                    out[c] = val.where(out["teacher"].isna(), pd.NA)
                shard_frames.append(
                    out.dropna(subset=["hash"]).drop_duplicates())
        shard = (pd.concat(shard_frames, ignore_index=True).drop_duplicates()
                 if shard_frames else pd.DataFrame(
                     columns=["hash", "teacher", *EVIDENCE_COLUMNS]))
        if part is not None:
            part.parent.mkdir(parents=True, exist_ok=True)
            shard.to_parquet(part, index=False)
        frames.append(shard)
    hashes = (pd.concat(frames, ignore_index=True).drop_duplicates()
              if frames else pd.DataFrame(
                  columns=["hash", "teacher", *EVIDENCE_COLUMNS]))
    if n_rows and hashes.empty:
        raise ValueError(f"{n_rows} rows but no task text extracted from {cols}")
    for c in EVIDENCE_COLUMNS:
        hashes[c] = hashes[c].astype("string")
    return hashes


def repo_hashes(repo: str, cache: Path,
                refresh: bool) -> tuple[pd.DataFrame, str]:
    """Every instruction hash this repo holds, with its teacher, plus a status.

    Caching the whole hash set rather than only the SFT-10K matches is what
    lets a second question ("which instructions have traces from several
    teachers?") be answered without refetching 232 repos. ``teacher`` is null
    unless the repo carries a per-row teacher column; the caller then falls
    back to the repo-level label.

    ``status`` is "read" or the reason the repo was unusable, so the report can
    name the skipped repos instead of counting them. Failures are never cached.
    """
    cached = hashes_path(cache, repo)
    if cached.exists() and not refresh:
        return pd.read_parquet(cached), "read"
    t0 = time.time()
    parts_dir = cached.parent / "parts" / cached.stem
    try:
        found = repo_task_hashes(repo, parts_dir)
    except Exception as exc:                     # unreadable: never cache it,
        why = f"{type(exc).__name__}: {exc}"
        print(f"  !! SKIPPED {repo}: {why}", flush=True)   # never count as 0
        return pd.DataFrame(columns=["hash", "teacher"]), why
    cached.parent.mkdir(parents=True, exist_ok=True)
    found.to_parquet(cached, index=False)
    shutil.rmtree(parts_dir, ignore_errors=True)
    print(f"  fetched in {time.time() - t0:.0f}s ({len(found):,} hashes)",
          flush=True)
    return found, "read"


def multiplicity(by_hash: dict[str, set[str]], by_src: dict[str, set[str]],
                 canon: dict[str, str], sft_hashes: set[str],
                 cache: Path) -> pd.DataFrame:
    """One row per distinct instruction: its teachers and data sources.

    Counted over distinct instruction text, so the tezos upsampler writing
    the same question 458 times counts once. ``datasources`` is the union of
    every label layer (lookup convenience); ``source`` is the one canonical
    label per instruction (task-id prefix, else TaskTrove dataset, else repo
    name) - a partition, so per-source counts never count a task twice.
    """
    df = pd.DataFrame({"hash": list(by_hash)})
    df["teachers"] = df["hash"].map(lambda h: ";".join(sorted(by_hash[h])))
    df["n_teachers"] = df["hash"].map(lambda h: len(by_hash[h]))
    df["in_sft10k"] = df["hash"].isin(sft_hashes)
    df["datasources"] = df["hash"].map(
        lambda h: ";".join(sorted(by_src.get(h, ()))))
    df["source"] = df["hash"].map(lambda h: canon.get(h, ""))
    df.sort_values(["n_teachers", "teachers"], ascending=[False, True]).to_csv(
        cache / "sweep" / "instructions_by_teacher.csv", index=False)
    return df


def mult_rows_of(df: pd.DataFrame) -> list[list]:
    """[n_teachers, instructions, in SFT-10K, outside] rows, most teachers first."""
    rows = []
    for n, g in df.groupby("n_teachers"):
        rows.append([n, len(g), int(g["in_sft10k"].sum()),
                     int((~g["in_sft10k"]).sum())])
    return sorted(rows, reverse=True)


def combo_tables(ibt: pd.DataFrame, ot_only: bool = False,
                 top: int = 12) -> dict[int, list[list]]:
    """Per n, the teacher combinations with the largest task overlap.

    Combinations containing "<unknown>" (traces no rule could attribute to a
    teacher) are excluded: they are not actionable. The CSV keeps them.

    Row = one combination of n teachers, counted twice:
    - exact task overlap: tasks (same instruction.md hash) every teacher in
      the combination has a trace for. Extra teachers do not disqualify a
      task, so one task counts for every combination it serves.
    - same-source overlap: tasks a comparison could use if they only need to
      come from the same data source, not be identical. Per source the
      usable count is the SMALLEST per-source task count among the n
      teachers; the total sums that over sources, the parenthesis names the
      biggest ones. Uses the canonical ``source`` column (one label per
      task), so no task is counted under two labels.

    ``ot_only`` restricts both counts to the OT-Agent data sources.
    """
    from itertools import combinations
    from find_candidate_repos import DATASOURCE_TOKENS
    df = ibt
    if ot_only:
        ot = set(DATASOURCE_TOKENS)
        df = df[df["source"].isin(ot)]

    # strict: superset counting via the exact sets present
    exact = df.groupby("teachers")["hash"].size()
    strict: dict[int, dict[tuple, int]] = {}
    for tstr, c in exact.items():
        members = sorted(m for m in tstr.split(";") if m != "<unknown>")
        for n in range(2, len(members) + 1):
            cnt = strict.setdefault(n, {})
            for sub in combinations(members, n):
                cnt[sub] = cnt.get(sub, 0) + int(c)

    # relaxed: per (teacher, source) distinct-task counts, source = partition
    ex = (df[df["source"] != ""]
          .assign(teacher=df["teachers"].str.split(";"))
          .explode("teacher"))
    per_ts = ex.groupby(["teacher", "source"])["hash"].size()

    def relaxed(combo: tuple) -> str:
        mins = {}
        counts = [per_ts.get(t, pd.Series(dtype=int)) for t in combo]
        shared = set.intersection(*(set(c.index) for c in counts))             if counts else set()
        for src in shared:
            mins[src] = min(int(c[src]) for c in counts)
        if not mins:
            return "0"
        total = sum(mins.values())
        tops = sorted(mins.items(), key=lambda kv: -kv[1])[:3]
        more = len(mins) - len(tops)
        inner = "; ".join(f"{k} {v:,}" for k, v in tops) + (
            f"; +{more} more" if more > 0 else "")
        return f"{total:,} ({inner})"

    out: dict[int, list[list]] = {}
    for n, cnt in sorted(strict.items()):
        rows = sorted(cnt.items(), key=lambda kv: -kv[1])[:top]
        out[n] = [[";".join(combo), f"{c:,}", relaxed(combo)]
                  for combo, c in rows]
    return out


SET_HEADER = ["teachers", "exact task overlap", "same-source overlap"]


def source_label(repo: str, datasources: str) -> str:
    """The task set a trace repo covers, as a short label.

    OT-Agent source labels from the repo name where present. Else derived
    from the datagen naming convention `<task-dataset>-<teacher>-<ctx>-traces`
    by cutting the name at the first teacher token, so the same task set gets
    one label across its per-teacher dumps. Falls back to the bare repo name.
    """
    if datasources:
        return datasources
    name = repo.split("/", 1)[-1].lower()
    cuts = [i for _, toks in TEACHER_TOKENS
            for i in (name.find(t) for t in toks) if i > 0]
    return (name[:min(cuts)].rstrip("-_.") or name) if cuts else name


def tasktrove_sources(cache: Path) -> dict[str, set[str]]:
    """hash -> TaskTrove dataset names holding it, from hash_tasktrove.py.

    The exact source of a task, independent of what any trace repo's name or
    columns claim. Mixed dumps (AgentTrove holds many sources in one repo)
    and AgentTrove's known-wrong `original_source` column make the repo side
    unreliable; the task registry is not. Empty when hash_tasktrove.py has
    not run.
    """
    out: dict[str, set[str]] = {}
    for f in sorted((cache / "tasktrove_hashes").glob("*.parquet")):
        label = f.stem.split("_", 1)[-1]         # drop the org prefix
        for h in pd.read_parquet(f)["hash"].dropna():
            out.setdefault(h, set()).add(label)
    return out


def worklist(cache: Path) -> list[tuple[str, str, str]]:
    """(repo, teacher, datasources) per candidate find_candidate_repos.py found.

    ``datasources`` is the ;-joined OT-Agent source labels the repo name
    mentions ("" for a trace dump over other task sources), so the teachers-
    per-instruction tables can be split into OT-Agent-sources vs everything.
    """
    path = cache / "sweep" / "candidates.csv"
    if not path.exists():
        raise SystemExit(f"{path} missing — run find_candidate_repos.py first")
    df = pd.read_csv(path)
    df = df[df["candidate"].astype(str).str.lower() == "true"]
    return [(r.repo, TEACHER_OVERRIDES.get(r.repo, r.teacher if isinstance(
        r.teacher, str) and r.teacher else "<unknown>"),
        r.datasources if isinstance(r.datasources, str) else "")
        for r in df.itertuples()]


def gap_table(tasks: pd.DataFrame, teachers: dict[str, set[str]],
              all_teachers: list[str]) -> list[list]:
    """Rows of [family, tasks, *per-teacher missing counts], TOTAL last."""
    rows, totals = [], [0] * len(all_teachers)
    for fam, n in tasks.groupby("family")["base_id"].nunique().items():
        fam_ids = tasks.loc[tasks["family"] == fam, "base_id"]
        counts = []
        for i, t in enumerate(all_teachers):
            v = n - sum(t in teachers[b] for b in fam_ids)
            counts.append(v)
            totals[i] += v
        rows.append([fam, n, *counts])
    rows.append(["TOTAL", len(tasks), *totals])
    return rows


def as_markdown(header: list[str], rows: list[list]) -> str:
    """Markdown table; < and > escaped so GitHub does not eat "<unknown>"."""
    def esc(v: object) -> str:
        txt = f"{v:,}" if isinstance(v, int) else str(v)
        return txt.replace("<", "\\<").replace(">", "\\>")
    header = [esc(h) for h in header]
    rows = [[esc(v) for v in r] for r in rows]
    out = ["| " + " | ".join(header) + " |",
           "|" + "---|" * len(header)]
    for r in rows:
        cells = [f"**{r[0]}**" if r[0] == "TOTAL" else str(r[0])]
        cells += [f"{v:,}" if isinstance(v, int) else str(v) for v in r[1:]]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def print_table(title: str, header: list[str], rows: list[list]) -> None:
    print(f"\n== {title} ==")
    print("".join(f"{h:>20}" if i else f"{h:<12}" for i, h in enumerate(header)))
    for r in rows:
        print("".join(f"{v:>20,}" if i and isinstance(v, int) else
                      f"{str(v):<12}" if not i else f"{str(v):>20}"
                      for i, v in enumerate(r)))


def write_report(results: Path, header: list[str], gap_rows: list[list],
                 swept: list[tuple[str, str, int, str, str]],
                 combo_all: dict[int, list[list]],
                 combo_ot: dict[int, list[list]]) -> Path:
    """One directory per run, one table per file, nothing else.

    results/<stamp>/generation_gap.md          question 1
    results/<stamp>/n<k>.md                    combinations, all data sources
    results/<stamp>/n<k>_top-4-datasources.md  combinations, OT-Agent sources
    results/<stamp>/repos.md                   repos read / skipped
    """
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out = results / stamp
    out.mkdir(parents=True, exist_ok=True)
    (out / "generation_gap.md").write_text("\n".join([
        "# Generation gap: SFT-10K tasks still needing a trajectory", "",
        as_markdown(header, gap_rows), ""]))
    for tables, suffix in ((combo_all, ""), (combo_ot, "_top-4-datasources")):
        for n, rows in tables.items():
            (out / f"n{n}{suffix}.md").write_text("\n".join([
                f"# {n}-teacher combinations"
                + (", OT-Agent data sources only" if suffix else ""), "",
                as_markdown(SET_HEADER, rows), ""]))
    read = [r for r in swept if r[3] == "read"]
    skipped = [r for r in swept if r[3] != "read"]
    (out / "repos.md").write_text("\n".join([
        "# Repos read", "",
        as_markdown(["repo", "teacher", "tasks matched"],
                    [[r, t, n]
                     for r, t, n, _, _ in sorted(read, key=lambda x: -x[2])]),
        "", "# Repos skipped", "",
        as_markdown(["repo", "why"],
                    [[r, w]
                     for r, _, _, w, _ in sorted(skipped, key=lambda x: x[3])]),
        ""]))
    print(f"wrote {out}/")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    ap.add_argument("--refresh", action="store_true",
                    help="re-fetch every repo instead of using cached hits")
    ap.add_argument("--cached-only", action="store_true",
                    help="skip repos with no cached hits (fast re-report)")
    ap.add_argument("--max-repos", type=int, default=0,
                    help="stop after N uncached repos (0 = no limit)")
    ap.add_argument("--sets-only", action="store_true",
                    help="no fetch: rebuild the teacher-set tables from "
                         "<cache>/sweep/instructions_by_teacher.csv into "
                         "results/<stamp>_teacher_sets.md")
    ap.add_argument("--workers", type=int, default=8,
                    help="repos fetched concurrently; the work is network-bound")
    args = ap.parse_args()
    if args.sets_only:
        ibt = pd.read_csv(args.cache / "sweep" / "instructions_by_teacher.csv",
                          keep_default_na=False)
        if "source" not in ibt.columns:
            raise SystemExit("csv has no canonical source column - "
                             "regenerate it (--cached-only suffices)")
        ibt["in_sft10k"] = ibt["in_sft10k"].astype(str) == "True"
        ibt["teachers"] = ibt["teachers"].map(lambda ts: ";".join(
            sorted({canon_teacher(t) for t in ts.split(";")})))
        ibt["n_teachers"] = ibt["teachers"].str.count(";") + 1
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        out = Path(__file__).resolve().parent / "results" / stamp
        out.mkdir(parents=True, exist_ok=True)
        for suffix, ot in (("", False), ("_top-4-datasources", True)):
            tables = combo_tables(ibt, ot)
            for n, rows in sorted(tables.items(), reverse=True):
                (out / f"n{n}{suffix}.md").write_text("\n".join([
                    f"# {n}-teacher combinations"
                    + (", OT-Agent data sources only" if suffix else ""),
                    "", as_markdown(SET_HEADER, rows), ""]))
                print_table(f"{n}-TEACHER COMBINATIONS"
                            + (" (OT-Agent sources)" if suffix else ""),
                            SET_HEADER, rows)
        print(f"wrote {out}/")
        return

    tasks = load_tasks(args.cache)
    teachers: dict[str, set[str]] = {b: set() for b in tasks["base_id"]}
    trace_repos: dict[str, set[str]] = {b: set() for b in tasks["base_id"]}

    todo = []
    fetched = 0
    for repo, label, sources in worklist(args.cache):
        cached = hashes_path(args.cache, repo).exists()
        if args.cached_only and not cached:
            continue
        if not cached:
            if args.max_repos and fetched >= args.max_repos:
                continue
            fetched += 1
        todo.append((repo, label, sources))
    print(f"{len(todo)} repos to read ({len(todo) - fetched} cached), "
          f"{args.workers} workers", flush=True)

    sft = tasks[["base_id", "hash"]]
    sft_runs = set(tasks["run_id"].dropna()) if "run_id" in tasks else set()
    by_hash: dict[str, set[str]] = {}          # every instruction seen anywhere
    by_src: dict[str, set[str]] = {}           # union of its source labels
    by_pre: dict[str, str] = {}                # its in-row task-id prefix
    by_repo_label: dict[str, str] = {}         # a repo-name-derived label
    tt_src = tasktrove_sources(args.cache)     # exact hash -> task dataset
    print(f"TaskTrove source map: {len(tt_src):,} hashes", flush=True)

    def read(job):
        repo, label, sources = job
        return repo, label, sources, repo_hashes(repo, args.cache, args.refresh)

    swept: list[tuple[str, str, int, str, str]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for repo, label, sources, (found, status) in pool.map(read, todo):
            srcs = set(source_label(repo, sources).split(";"))
            found, resolved = resolve_bare_glm(found, sft_runs)
            evidence = ";".join(f"{k}={v}" for k, v in resolved.items() if v)
            if evidence:
                print(f"  {repo}: bare-GLM rows resolved {evidence}", flush=True)
            # a human-asserted override wins; else the data; else the name;
            # else the raw model string (hosted_vllm/glm still says "a GLM")
            models = (found["model"] if "model" in found.columns
                      else pd.Series(pd.NA, index=found.index))
            teacher = pd.Series(
                [canon_teacher(TEACHER_OVERRIDES.get(repo) or (
                    v if isinstance(v, str) and v else
                    label if label != "<unknown>" else
                    m if isinstance(m, str) and m else "<unknown>"))
                 for v, m in zip(found["teacher"], models)],
                index=found.index)
            prefixes = (found["source_prefix"]
                        if "source_prefix" in found.columns
                        else pd.Series(pd.NA, index=found.index))
            for h, t, pre in zip(found["hash"], teacher, prefixes):
                by_hash.setdefault(h, set()).add(t)
                by_src.setdefault(h, set()).update(srcs)
                by_repo_label.setdefault(h, min(srcs))
                if isinstance(pre, str):
                    by_src.setdefault(h, set()).add(pre)
                    by_pre.setdefault(h, pre)
            hit = sft.merge(found.assign(teacher=teacher), on="hash")
            swept.append((repo, label, hit["base_id"].nunique(), status,
                          evidence))
            for row in hit.itertuples():
                teachers[row.base_id].add(row.teacher)
                trace_repos[row.base_id].add(repo)
            if len(hit):
                print(f"{hit['base_id'].nunique():>6} tasks  {label:<18} {repo}",
                      flush=True)

    pd.DataFrame(swept, columns=["repo", "teacher", "tasks_matched", "status",
                                 "glm_resolved_by"]
                 ).sort_values(["status", "tasks_matched"],
                               ascending=[True, False]).to_csv(
        args.cache / "sweep" / "sweep_status.csv", index=False)

    out = tasks[["base_id", "family"]].copy()
    out["teachers"] = out["base_id"].map(lambda b: ";".join(sorted(teachers[b])))
    out["trace_repos"] = out["base_id"].map(
        lambda b: ";".join(sorted(trace_repos[b])))
    out.to_csv(args.cache / "teacher_coverage.csv", index=False)

    covered = sum(bool(v) for v in teachers.values())
    print(f"\nUnion: {covered:,}/{len(tasks):,} tasks have >=1 located trace")
    print(f"wrote {args.cache / 'teacher_coverage.csv'}")
    print(f"wrote {args.cache / 'sweep' / 'sweep_status.csv'}")

    all_teachers = sorted({t for s in teachers.values() for t in s}
                          - {"<unknown>"})
    header = ["data source", "tasks", *all_teachers]
    gap_rows = gap_table(tasks, teachers, all_teachers)
    print_table("GENERATION GAP: tasks still needing a trajectory",
                header, gap_rows)
    canon: dict[str, str] = {}                 # one source per hash, by trust:
    for h in by_hash:                          # prefix > registry > repo name
        if h in tt_src:
            by_src.setdefault(h, set()).update(tt_src[h])
        canon[h] = by_pre.get(h) or (
            min(tt_src[h], key=len) if h in tt_src else
            by_repo_label.get(h, ""))
    print(f"datasources: {sum(1 for v in canon.values() if v):,} of "
          f"{len(by_hash):,} hashes labelled", flush=True)
    ibt = multiplicity(by_hash, by_src, canon, set(tasks["hash"]), args.cache)
    print_table("INSTRUCTIONS BY NUMBER OF TEACHERS",
                ["teachers", "instructions", "in SFT-10K",
                 "outside SFT-10K"], mult_rows_of(ibt))
    combo_all, combo_ot = combo_tables(ibt, False), combo_tables(ibt, True)
    for tag, tables in (("all data sources", combo_all),
                        ("OT-Agent data sources only", combo_ot)):
        for n, rows in sorted(tables.items(), reverse=True):
            print_table(f"{n}-TEACHER COMBINATIONS ({tag})",
                        SET_HEADER, rows)
    print(f"wrote {args.cache / 'sweep' / 'instructions_by_teacher.csv'}")

    write_report(Path(__file__).resolve().parent / "results", header,
                 gap_rows, swept, combo_all, combo_ot)


if __name__ == "__main__":
    main()
