#!/usr/bin/env python3
"""List the repos and task ids behind one cell of a teacher-combination table.

Pick a row (the teachers) and a column of an `n<k>.md` table written by
`teacher_coverage.py`, and get the tasks that number counts: instruction
hash, data source, SFT-10K id and TaskTrove id where the task is registered
there, and per teacher the repos holding a trace of it. The number is
recomputed from the same cache the table came from and printed next to the
table's value, so a stale cache shows up as a mismatch.

    uv run --no-project --with pandas --with pyarrow python overlap_members.py \\
      GLM-4.7 GPT-5-nano --column exact-tasks --ot-only --cache <cache>

Teachers: separate arguments or one comma/semicolon-separated string, spelled
as in the table. `--column`: `exact-tasks` (default), `exact-trajectories`,
`same-source-tasks`, `same-source-trajectories`. `--ot-only` selects the
`_top-4-datasources` table (OT-Agent sources only).

Exact columns: one row per task every teacher covers, per teacher. `n_traj`
is the sweep's trajectory count for (task, teacher); the column's number is
the distinct-task count, or the per-task minimum over teachers summed.

Same-source columns: per shared source, per teacher, every task that teacher
has there. `binding=True` marks the teacher whose task count is the source's
minimum: those rows add up to the same-source tasks number.
`binding_traj=True` does the same for trajectories (can be a different
teacher).

Task ids: `task_id` is the id the trace repo itself gives the task (its
`task` column, else another id column, else `<file>#<rowgroup>:<row>`; see
ID_COLUMNS in teacher_coverage.py), `;`-joined when one repo holds the text
under several ids (tezos `_copy` duplicates). Ids only name a row inside
their own dataset; across datasets the hash is the join key. `sft10k_id`
and `tasktrove_task` (`<dataset>:<task_path>`) are filled where the task is
registered there.

`--outcome <value>[,<value>...]` keeps only trajectories whose cached
outcome is one of the given values, spelled exactly as in the cache (the
run's `outcomes.md` lists every value with its count; see `--help`). The
listing shrinks to tasks that still qualify and the summary prints the
filtered number next to the table's unfiltered one. Per row the csv
carries the outcome split of that repo's trajectories (`outcomes`, e.g.
`unscored 3; error:AgentTimeoutError 1`).
Trajectory counts are over distinct conversation hashes, so a mirror's copy
of a trajectory is not counted twice.

Output: one row per (task, teacher, repo) to
`results/overlaps/<teachers>__<column>[__ot].csv` (or `--out`), and a summary
on stdout: recomputed vs table number, id coverage, per teacher the repos
holding the listed tasks with how many of them each holds.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from find_candidate_repos import DATASOURCE_TOKENS          # noqa: E402
from hash_sft10k_tasks import DEFAULT_CACHE, hashes_path, load_tasks  # noqa: E402
from teacher_coverage import (SET_HEADER, canon_outcome,    # noqa: E402
                              canon_teacher, resolve_bare_glm,
                              resolve_repo_teachers, worklist)


COLUMNS = {"exact-tasks": "exact tasks",
           "exact-trajectories": "exact trajectories",
           "same-source-tasks": "same-source tasks",
           "same-source-trajectories": "same-source trajectories"}
RESULTS = Path(__file__).resolve().parent / "results"


def parse_teachers(args: list[str]) -> list[str]:
    seen: list[str] = []
    for a in args:
        for t in re.split(r"[,;]", a):
            t = canon_teacher(t.strip())
            if t and t not in seen:
                seen.append(t)
    if len(seen) < 2:
        raise SystemExit("give at least two teachers")
    if "<unknown>" in seen:
        raise SystemExit("<unknown> is never part of a table row")
    return sorted(seen)


def teacher_regex(t: str) -> str:
    return rf"(?:^|;){re.escape(t)}(?:;|$)"


def load_ibt(cache: Path, combo: list[str], any_of: bool) -> pd.DataFrame:
    """Rows of instructions_by_teacher.csv holding all (or any) combo teachers,
    with `traj`: teacher -> n_traj for the combo teachers present."""
    ibt = pd.read_csv(cache / "sweep" / "instructions_by_teacher.csv",
                      keep_default_na=False, dtype=str,
                      usecols=["hash", "teachers", "n_traj", "in_sft10k",
                               "source"])
    masks = [ibt["teachers"].str.contains(teacher_regex(t)) for t in combo]
    mask = masks[0]
    for m in masks[1:]:
        mask = (mask | m) if any_of else (mask & m)
    ibt = ibt[mask].copy()
    want = set(combo)

    def traj(row) -> dict[str, int]:
        out: dict[str, int] = {}
        for t, k in zip(row.teachers.split(";"), row.n_traj.split(";")):
            t = canon_teacher(t)
            if t in want:
                out[t] = max(out.get(t, 0), int(k))
        return out
    ibt["traj"] = [traj(r) for r in ibt.itertuples()]
    return ibt


def exact_members(ibt: pd.DataFrame, combo: list[str]
                  ) -> tuple[pd.DataFrame, int, int]:
    rows = [(r.hash, r.source, t, r.traj[t])
            for r in ibt.itertuples() for t in combo]
    mem = pd.DataFrame(rows, columns=["hash", "source", "teacher", "n_traj"])
    n_tasks = len(ibt)
    n_traj = int(sum(min(r.traj[t] for t in combo) for r in ibt.itertuples()))
    return mem, n_tasks, n_traj


def same_source_members(ibt: pd.DataFrame, combo: list[str]
                        ) -> tuple[pd.DataFrame, int, int]:
    ibt = ibt[ibt["source"] != ""]
    rows = [(r.hash, r.source, t, k)
            for r in ibt.itertuples() for t, k in r.traj.items()]
    ex = pd.DataFrame(rows, columns=["hash", "source", "teacher", "n_traj"])
    per = ex.groupby(["source", "teacher"]).agg(tasks=("hash", "size"),
                                                traj=("n_traj", "sum"))
    shared = [s for s, g in per.groupby(level="source")
              if set(g.index.get_level_values("teacher")) >= set(combo)]
    ex = ex[ex["source"].isin(shared)].copy()
    ex["binding"] = False
    ex["binding_traj"] = False
    n_tasks = n_traj = 0
    for s in shared:
        g = per.loc[s]
        bt, btj = g["tasks"].idxmin(), g["traj"].idxmin()
        n_tasks += int(g["tasks"].min())
        n_traj += int(g["traj"].min())
        sel = ex["source"] == s
        ex.loc[sel & (ex["teacher"] == bt), "binding"] = True
        ex.loc[sel & (ex["teacher"] == btj), "binding_traj"] = True
    return ex, n_tasks, n_traj


def sft10k_ids(cache: Path, hashes: set[str]) -> pd.Series:
    tasks = load_tasks(cache)
    tasks = tasks[tasks["hash"].isin(hashes)]
    return tasks.groupby("hash")["base_id"].apply(
        lambda s: ";".join(sorted(set(s))))


def tasktrove_ids(cache: Path, hashes: set[str]) -> pd.Series:
    parts = []
    for f in sorted((cache / "tasktrove_hashes").glob("*.parquet")):
        label = f.stem.split("_", 1)[-1]
        df = pd.read_parquet(f)
        df = df[df["hash"].isin(hashes)]
        if len(df):
            parts.append(pd.DataFrame({"hash": df["hash"],
                                       "id": label + ":" + df["task_path"]}))
    if not parts:
        return pd.Series(dtype="object", name="tasktrove_task")
    return (pd.concat(parts).groupby("hash")["id"]
            .apply(lambda s: ";".join(sorted(set(s)))))


def repos_holding(cache: Path, hashes: set[str], combo: list[str],
                  sft_runs: set[str]) -> pd.DataFrame:
    """Every cached trajectory row of the wanted tasks: (hash, teacher, repo,
    task, traj_hash, outcome, n), teachers resolved exactly as the sweep
    resolved them."""
    parts = []
    for repo, label, _ in worklist(cache):
        path = hashes_path(cache, repo)
        if not path.exists():
            continue
        found = pd.read_parquet(path)
        found = found[found["hash"].isin(hashes)]
        if found.empty:
            continue
        if "traj_hash" in found.columns:          # a task without a trace
            found = found[found["traj_hash"].notna()]   # is not a trajectory
        found, _ = resolve_bare_glm(found, sft_runs)
        found = found.assign(teacher=resolve_repo_teachers(repo, label, found))
        found = found[found["teacher"].isin(combo)]
        if found.empty:
            continue
        for c in ("task", "traj_hash", "outcome", "trace_source"):
            if c not in found.columns:                  # pre-schema caches
                found[c] = pd.NA
        n = found["n_traj"] if "n_traj" in found.columns else 1
        parts.append(pd.DataFrame({
            "hash": found["hash"].astype(str), "teacher": found["teacher"],
            "repo": repo, "task": found["task"].astype("string"),
            "traj_hash": found["traj_hash"].astype("string"),
            "outcome": found["outcome"].map(canon_outcome).astype("string")
                       .fillna("unscored"),
            "trace_source": found["trace_source"].astype("string")
                            .fillna("<none>"),
            "n": pd.Series(n, index=found.index).astype(int)}))
    if not parts:
        return pd.DataFrame(columns=["hash", "teacher", "repo", "task",
                                     "traj_hash", "outcome", "trace_source",
                                     "n"])
    return pd.concat(parts, ignore_index=True)


def per_repo(det: pd.DataFrame) -> pd.DataFrame:
    """(hash, teacher, repo) rows: task ids, distinct trajectories, outcome split."""
    d = det.drop_duplicates(["hash", "teacher", "repo", "traj_hash"]).copy()
    d["k"] = d["n"]
    g = d.groupby(["hash", "teacher", "repo"])
    out = g.agg(task_id=("task", lambda s: ";".join(
                    sorted({v for v in s if isinstance(v, str)}))),
                n_traj_in_repo=("k", "sum")).reset_index()
    for col, name in (("outcome", "outcomes"),
                      ("trace_source", "trace_sources")):
        split = (d.groupby(["hash", "teacher", "repo", col])["k"].sum()
                 .reset_index())
        split["part"] = split[col] + " " + split["k"].astype(str)
        split = (split.groupby(["hash", "teacher", "repo"])["part"]
                 .apply("; ".join).rename(name).reset_index())
        out = out.merge(split, on=["hash", "teacher", "repo"], how="left")
    return out


def dedup_counts(det: pd.DataFrame) -> pd.Series:
    """(hash, teacher) -> trajectories summed across repos, identical
    conversations counted once."""
    return (det.drop_duplicates(["hash", "teacher", "traj_hash"])
            .groupby(["hash", "teacher"])["n"].sum().astype(int))


def table_value(combo: list[str], column: str, ot_only: bool,
                results_dir: Path | None) -> tuple[str, str]:
    """The cell as the newest results table prints it, and where it came from."""
    name = f"n{len(combo)}{'_top-4-datasources' if ot_only else ''}.md"
    dirs = [results_dir.resolve()] if results_dir else sorted(
        (d for d in RESULTS.iterdir() if (d / name).exists()), reverse=True)
    if not dirs or not (dirs[0] / name).exists():
        return "n/a", "no results table found"
    path = dirs[0] / name
    key = ";".join(combo)
    col = SET_HEADER.index(COLUMNS[column])
    for line in path.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == key:
            return cells[col].split(" (")[0], _rel(path)
    return "no row", _rel(path)


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(RESULTS))
    except ValueError:
        return str(path)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("teachers", nargs="+",
                    help="teacher names, separate or comma-separated")
    ap.add_argument("--column", choices=list(COLUMNS), default="exact-tasks")
    ap.add_argument("--ot-only", action="store_true",
                    help="the _top-4-datasources table (OT-Agent sources only)")
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    ap.add_argument("--outcome", default="", metavar="VALUE[,VALUE...]",
                    help="count only trajectories whose cached outcome is one "
                         "of these values, spelled exactly as stored: "
                         "`unscored` (no result recorded; most of the data, "
                         "all of AgentTrove), `pass` / `partial` / `fail` "
                         "(a numeric result: >=1, between 0 and 1, 0), or "
                         "`error:<class>` for a run that ended in that "
                         "exception, e.g. error:AgentTimeoutError, "
                         "error:DaytonaError, "
                         "error:AgentEnvironmentTimeoutError, "
                         "error:DaytonaNotFoundError, error:CancelledError, "
                         "error:ContextLengthExceededError. The run's "
                         "results/<stamp>/outcomes.md lists every value in "
                         "the cache with its count. Whether an errored or "
                         "unscored trajectory is useful is your call, so "
                         "nothing is grouped or excluded by default.")
    ap.add_argument("--trace-source", default="", metavar="VALUE[,VALUE...]",
                    help="count only rows whose cached trace_source is one of "
                         "these values, spelled exactly as stored: `main` for "
                         "the run itself (some repos write a dataset label "
                         "such as exp_rpt_issue_10k there instead, and repos "
                         "without the column show as `<none>`), "
                         "`summarization-1-summary` / "
                         "`summarization-1-answers` (and 2, 3, ...) for the "
                         "agent's conversation segments before and after its "
                         "k-th context reset. To count runs only, pass "
                         "`main,<none>` plus whatever dataset labels the "
                         "run's results/<stamp>/outcomes.md lists; a value "
                         "missing for one teacher drops that teacher's rows.")
    ap.add_argument("--results-dir", type=Path,
                    help="results/<stamp> to compare against (default: newest)")
    ap.add_argument("--out", type=Path,
                    help="csv path (default results/overlaps/<auto>.csv)")
    args = ap.parse_args()

    combo = parse_teachers(args.teachers)
    exact = args.column.startswith("exact")
    ibt = load_ibt(args.cache, combo, any_of=not exact)
    if args.ot_only:
        ibt = ibt[ibt["source"].isin(set(DATASOURCE_TOKENS))]
    mem, n_tasks, n_traj = (exact_members if exact
                            else same_source_members)(ibt, combo)
    number = n_tasks if args.column.endswith("tasks") else n_traj

    hashes = set(mem["hash"])
    tasks = load_tasks(args.cache)
    sft_runs = set(tasks["run_id"].dropna()) if "run_id" in tasks else set()
    sft = sft10k_ids(args.cache, hashes).rename("sft10k_id")
    tt = tasktrove_ids(args.cache, hashes).rename("tasktrove_task")
    det = repos_holding(args.cache, hashes, combo, sft_runs)

    wanted = [o.strip() for o in args.outcome.split(",") if o.strip()]
    wanted_src = [o.strip() for o in args.trace_source.split(",") if o.strip()]
    filtered = None
    for col, vals in (("outcome", wanted), ("trace_source", wanted_src)):
        if not vals:
            continue
        have = set(det[col].dropna().unique())
        unknown = [o for o in vals if o not in have]
        if unknown:
            print(f"  note: {col} {unknown} occur in none of these tasks' "
                  f"trajectories; values present: {sorted(have)}")
        det = det[det[col].isin(vals)]
    if wanted or wanted_src:
        counts = dedup_counts(det)
        by_hash: dict[str, dict[str, int]] = {}
        for (h, t), k in counts.items():
            by_hash.setdefault(h, {})[t] = int(k)
        ibt_f = ibt[ibt["hash"].isin(by_hash)].copy()
        ibt_f["traj"] = ibt_f["hash"].map(by_hash)
        if exact:
            ibt_f = ibt_f[ibt_f["traj"].map(lambda d: all(t in d for t in combo))]
        mem, n_tasks_f, n_traj_f = (exact_members if exact
                                    else same_source_members)(ibt_f, combo)
        filtered = n_tasks_f if args.column.endswith("tasks") else n_traj_f
        hashes = set(mem["hash"])
    repos = per_repo(det)

    out = (mem.merge(sft, left_on="hash", right_index=True, how="left")
           .merge(tt, left_on="hash", right_index=True, how="left")
           .merge(repos, on=["hash", "teacher"], how="left"))
    out["sft10k_id"] = out["sft10k_id"].fillna("")
    out["tasktrove_task"] = out["tasktrove_task"].fillna("")
    out["task_id"] = out["task_id"].fillna("")
    out["repo"] = out["repo"].fillna("")
    out["outcomes"] = out["outcomes"].fillna("")
    out["trace_sources"] = out["trace_sources"].fillna("")
    out["n_traj_in_repo"] = out["n_traj_in_repo"].fillna(0).astype(int)
    cols = ["hash", "source", "sft10k_id", "tasktrove_task", "teacher",
            "n_traj"]
    if not exact:
        cols += ["binding", "binding_traj"]
    cols += ["repo", "task_id", "n_traj_in_repo", "outcomes", "trace_sources"]
    out = out[cols].sort_values(["source", "hash", "teacher", "repo"])

    if args.out:
        path = args.out
    else:
        slug = "+".join(re.sub(r"[^A-Za-z0-9.]+", "-", t) for t in combo)
        path = RESULTS / "overlaps" / (
            f"{slug}__{args.column}{'__ot' if args.ot_only else ''}"
            f"{'__' + '-'.join(wanted).replace(':', '.') if wanted else ''}"
            f"{'__' + '-'.join(wanted_src) if wanted_src else ''}.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False)

    tv, where = table_value(combo, args.column, args.ot_only, args.results_dir)
    per_task = out.drop_duplicates("hash")
    print(f"{';'.join(combo)}  |  {COLUMNS[args.column]}"
          f"{'  |  OT-Agent data sources only' if args.ot_only else ''}")
    print(f"  recomputed: {number:,}    table: {tv} ({where})")
    if filtered is not None:
        print(f"  with outcome in {wanted or 'any'} and trace_source in "
              f"{wanted_src or 'any'}: {filtered:,}")
    print(f"  distinct tasks listed: {len(per_task):,}   with SFT-10K id: "
          f"{(per_task['sft10k_id'] != '').sum():,}   with TaskTrove id: "
          f"{(per_task['tasktrove_task'] != '').sum():,}   neither: "
          f"{((per_task['sft10k_id'] == '') & (per_task['tasktrove_task'] == '')).sum():,}")
    src = per_task["source"].replace("", "<none>").value_counts()
    top = "; ".join(f"{s} {n:,}" for s, n in src.head(8).items())
    more = f"; +{len(src) - 8} more" if len(src) > 8 else ""
    print(f"  by source ({len(src)}): {top}{more}")
    for t in combo:
        sub = out[(out["teacher"] == t) & (out["repo"] != "")]
        if not exact:
            b = out[(out["teacher"] == t) & out["binding"]]["hash"].nunique()
            tag = f", binding for {b:,} tasks" if b else ""
        else:
            tag = ""
        held = sub.groupby("repo")["hash"].nunique().sort_values(ascending=False)
        print(f"  {t}: {sub['hash'].nunique():,} tasks in {len(held)} repos{tag}")
        for repo, n in held.items():
            print(f"    {n:>8,}  {repo}")
        missing = out[(out["teacher"] == t) & (out["repo"] == "")]["hash"].nunique()
        if missing:
            print(f"    {missing:>8,}  <no repo in cache resolves to {t}>")
    print(f"wrote {path} ({len(out):,} rows)")


if __name__ == "__main__":
    main()
