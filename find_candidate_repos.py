#!/usr/bin/env python3
"""Take all datasets posted under the organisations in ORGS and filter by name.

Without a flag, keep only repos whose name contains an
SFT-10K data-source token (case-insensitive substring match against
DATASOURCE_TOKENS: `swesmith`, `superuser`, `tezos`, `issue`, and spelling
variants like `swe-smith`), which covers questions 1 and 2. With `--all`,
keep every repo with a `traces` token in the name (the datagen convention for
a trajectory dump), a superset, for question 3. Either way, drop repos whose
name marks an eval result (a benchmark from BENCHMARKS: `terminal_bench`,
`swebench-verified`, `aider`, `bfcl`, `gaia`, ...; or a leading `eval-`), and
always keep ALWAYS_CANDIDATE (AgentTrove). Names only decide what is worth
hash-joining; the join in `teacher_coverage.py` decides what a repo actually
holds.

Each name is also tagged with the teacher it implies, by the same substring
matching against TEACHER_TOKENS (`glm-4.7` in the name -> GLM-4.7; "" when
the name says nothing).

Writes one row per dataset, rejected ones included, to
`<cache>/sweep/candidates.csv`. `<cache>` defaults to
`/data/cat/ws/frwe188h-otagent/tmp/agenttrove_cache`; pass `--cache <dir>`
to keep it somewhere durable. Two
boolean columns say where each repo stands:

- `candidate`: did the filter keep it? `teacher_coverage.py` fetches exactly
  the `candidate=True` rows, so making this script mark a repo `True` is how
  it gets tested.
- `swept`: has `teacher_coverage.py` already fetched it, i.e. does its hash
  cache exist under `<cache>/sweep/hashes/`?

The "untested" count printed at the end is candidate-and-not-swept: how many
repos the next `teacher_coverage.py` run will actually download.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
from huggingface_hub import HfApi

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hash_sft10k_tasks import DEFAULT_CACHE, hashes_path  # noqa: E402

#: Accounts publishing OT-Agent datagen output.  SankalpKJ builds the source
#: *task* sets, whose slugs appear inside downstream trace-repo names.
ORGS = ["DCAgent", "DCAgent2", "penfever", "mlfoundations-dev", "open-thoughts",
        "marin-community", "laion", "SankalpKJ", "open-athena", "EtashGuha",
        "RZ412", "marianna13"]

#: Repos to sweep regardless of what their name says. The name rules key on a
#: task family, which the big concatenated dumps do not mention: AgentTrove
#: holds traces for every family and says so nowhere in its name.
ALWAYS_CANDIDATE = {"open-thoughts/AgentTrove"}

#: Benchmarks we eval on.  A repo whose name contains one is an eval result
#: (`<benchmark>_<student checkpoint>_<timestamp>`), not a trace repo: the
#: checkpoint is named after its training traces, so the name carries family
#: and teacher tokens either way.  Source: the ID/OOD master list in
#: `.agents/skills/crud-otagent-supabase/SKILL.md`.  Checked 2026-08-20 by
#: hash-joining 20 sampled excluded repos against SFT-10K: all 0 matches.
BENCHMARKS = {
    # name as it appears in repo names        # tasks
    "dev_set": ["dev[-_]set"],                                     # partial credit
    "terminal_bench_2": ["terminal[-_]bench[-_]?2", "tb2"],                  #  89
    "swebench-verified": ["swebench[-_]verified", "swe[-_]bench[-_]verified"],  # 100/500
    "terminal_bench": ["terminal[-_]bench", "tbench", "OpenThoughts[-_]TB"],  # retired
    "aider_polyglot": ["aider[-_]polyglot", "aider"],                        # 225
    "bfcl": ["bfcl"],                                                        # 123
    "gaia": ["gaia[-_]?127"],                                                # 127
    "medagentbench": ["medagentbench"],                                      # 300
    "financeagent": ["financeagent"],                                        #  50
}

#: The eval job also writes repos naming no benchmark at all (`eval-<model>-
#: <timestamp>`). 
EVAL_MARKERS = {"eval-pipeline": [r"^eval[-_]"]}

#: The two dicts above, compiled once into one regex per label, so `classify`
#: can report which label matched instead of just "yes".
_EVAL_PATTERNS = {label: re.compile("|".join(pats), re.I)
                  for label, pats in {**BENCHMARKS, **EVAL_MARKERS}.items()}

#: The five data sources SFT-10K's 8,360 tasks come from, i.e. the task-id prefix
#: (`swesmith-13674`, `tezos-issue-02837`).  Lowercased substring match, so
#: `issue` also covers `IssueTasks`, `issue-tasks`, `issues_glm`.  Deliberately
#: generic: over-matching costs a wasted hash join, under-matching loses
#: coverage silently.
DATASOURCE_TOKENS = {
    "swesmith": ["swesmith", "swe-smith", "swe_smith"],
    "superuser": ["superuser"],
    "tezos": ["tezos"],
    "issue": ["issue"],
    "tezos-issue": ["tezos-issue", "tezos_issue"],
}

#: Teacher tokens, first match wins, longer tokens first (`kimi-k2t` before
#: `kimi`, `glm-5.2` before `glm5`).  Minor versions stay distinct: GLM-5.1 and
#: GLM-5.2 are different teachers.  A bare `glm5` stays `GLM-5.x`: resolve it
#: from the campaign, not the name.  `GLM_5_20260505` is a timestamp, not 5.2.
TEACHER_TOKENS = [
    ("Kimi K2.0 Thinking", ["kimi-k2t", "kimi-k2", "kimi_k2", "k2t", "k2-thinking"]),
    ("Kimi-2.6", ["kimi-2.6", "kimi2.6", "kimi-26"]),
    ("Kimi-2.5", ["kimi-2.5", "kimi2.5", "kimi-25"]),
    ("MiniMax-M2.7", ["minimax", "m2.7", "m27"]),
    ("Qwen3.5-122B", ["qwen3.5-122b", "qwen35-122b"]),
    ("Gemma4-31B", ["gemma4", "gemma-4"]),
    ("GLM-5.3", ["glm-5.3", "glm5.3", "glm53", "glm-5_3"]),
    ("GLM-5.2", ["glm-5.2", "glm5.2", "glm52", "glm-5_2"]),
    ("GLM-5.1", ["glm-5.1", "glm5.1", "glm51", "glm-5_1"]),
    ("GLM-5.x", ["glm5", "glm-5", "glm_5"]),
    ("GLM-4.7", ["glm-4.7", "glm_4.7", "glm47", "glm-4_7", "glm_4_7"]),
    ("GLM-4.6", ["glm-4.6", "glm_4.6", "glm46", "glm-4_6", "glm_4_6"]),
    ("GPT-5-nano", ["gpt-5-nano", "gpt5nano", "gpt5-nano", "gpt_5_nano"]),
    ("GPT-5-mini", ["gpt-5-mini", "gpt5mini", "gpt5-mini"]),
    ("GPT-OSS", ["gptoss", "gpt-oss"]),
    ("Qwen3-Coder-480B", ["qwen3-coder-480b", "qwen3_coder_480b",
                          "480b-a35b"]),
    ("Qwen3-Coder-30B", ["qwen3-coder-30b", "30b-a3b"]),
    ("Qwen3", ["qwen3", "qwen-3"]),
]


def teacher_from_text(text: object) -> str:
    """First teacher token appearing in a repo name or a `model` value.

    "" when nothing matches: a numeric vLLM id (`hosted_vllm/1774312518071260`)
    or a version-less `hosted_vllm/glm` names no teacher we can act on.
    """
    if not isinstance(text, str) or not text:
        return ""
    low = text.lower()
    return next((label for label, toks in TEACHER_TOKENS
                 if any(t in low for t in toks)), "")


def classify(name: str) -> tuple[list[str], str, str]:
    """Read three labels off an HF repo name, without opening the repo.

    In:  an HF dataset id, e.g.
         "DCAgent2/dev_set_v2_exp_psu_swesmith_10K_glm_4_7_traces_jupiter"
    Out: (["swesmith"], "GLM-4.7", "dev_set")

      datasources     SFT-10K data sources the name mentions ([] if none)
      teacher         teacher the name implies ("" if none)
      eval_benchmark  benchmark the name mentions, so it is an eval result
                      rather than a trace repo ("" if none)

    ``is_candidate`` turns these into the keep/skip decision.
    """
    low = name.lower()
    datasources = [d for d, toks in DATASOURCE_TOKENS.items()
                   if any(t in low for t in toks)]
    teacher = teacher_from_text(name)
    bench = next((label for label, pat in _EVAL_PATTERNS.items()
                  if pat.search(name.split("/", 1)[-1])), "")
    return datasources, teacher, bench


#: The datagen pipelines name every trajectory dump `...traces...`
#: (`<task-dataset>-<teacher>-<ctx>-traces`, `..._traces_jupiter`), so the
#: token marks a trace repo even when the task source is not one of SFT-10K's.
#: Those repos cannot hold SFT-10K tasks, so the default (SFT-10K coverage)
#: sweep skips them; `--all` keeps them, for the teachers-per-instruction
#: question over every task set. Their registry is marin issue #6191 (all
#: under open-athena since 2026-09-04, private - sweeping them needs
#: `hf auth login` by a member of the org).
_TRACES = re.compile(r"(^|[-_])traces?([-_]|$)")


def is_candidate(repo: str, datasources: list[str], eval_benchmark: str,
                 include_traces: bool = False) -> bool:
    """Worth hash-joining: names an SFT-10K data source (or, with
    ``include_traces``, any trace dump) and is not an eval."""
    if repo in ALWAYS_CANDIDATE:
        return True
    if eval_benchmark:
        return False
    if datasources:
        return True
    return include_traces and bool(
        _TRACES.search(repo.split("/", 1)[-1].lower()))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    ap.add_argument("--all", action="store_true",
                    help="also keep trace dumps over non-SFT-10K task sources "
                         "(any `traces` in the name); default is repos that "
                         "could hold SFT-10K tasks only")
    args = ap.parse_args()

    api = HfApi()
    rows = []
    for org in ORGS:
        try:
            names = [d.id for d in api.list_datasets(author=org)]
        except Exception as exc:                      # account may not exist
            print(f"{org}: skipped ({exc})")
            continue
        print(f"{org}: {len(names)} datasets")
        for name in names:
            datasources, teacher, bench = classify(name)
            rows.append({
                "repo": name, "org": org, "datasources": ";".join(datasources),
                "teacher": teacher, "eval_benchmark": bench,
                "candidate": is_candidate(name, datasources, bench,
                                          include_traces=args.all),
                "swept": hashes_path(args.cache, name).exists(),
            })

    df = pd.DataFrame(rows).sort_values("repo")
    out = args.cache / "sweep" / "candidates.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    results = Path(__file__).resolve().parent / "results"
    df.to_csv(results / "candidates.csv", index=False)   # cache is scratch,
    df[df["candidate"]].drop(columns=["candidate"]).to_csv(   # results is not
        results / "candidates_swept.csv", index=False)   # the sweep worklist

    named = df[df["datasources"] != ""]
    cand = df[df["candidate"]]
    todo = cand[~cand["swept"]]
    print(f"\ntotal datasets listed        {len(df)}")
    print(f"  naming a data source       {len(named)}")
    print(f"  ... eval results (excl.)   {int((named['eval_benchmark'] != '').sum())}")
    print(f"  ... CANDIDATE UNIVERSE     {len(cand)}")
    print(f"      already swept          {int(cand['swept'].sum())}")
    print(f"      UNTESTED               {len(todo)}")
    print("\nexcluded as eval results, by benchmark:")
    print(named.loc[named["eval_benchmark"] != ""]
          .groupby("eval_benchmark").size().sort_values(ascending=False).to_string())
    print("\nuntested candidates by implied teacher:")
    print(todo.groupby(todo["teacher"].replace("", "<none in name>"))
          .size().sort_values(ascending=False).to_string())
    print(f"\nfull inventory: {out}")


if __name__ == "__main__":
    main()
