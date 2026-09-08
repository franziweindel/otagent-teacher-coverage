#!/usr/bin/env python3
"""Per-teacher trace counts for one data source.

Call with a source label (`python relaxed_coverage.py nl2bash`) and get, for
every teacher the sweep found, how many tasks of this source it has a trace
for, plus how many tasks the source has at all, one row per matching
`open-thoughts/TaskTrove` dataset. Retired dataset versions (TaskTrove's
`deprecated/` folder) are marked deprecated in the status column. The
teachers are not a fixed list: they are whatever labels
`teacher_coverage.py` resolved from the swept repos (model columns, repo
names, the run_id rule).

Tasks are matched by instruction.md hash against TaskTrove where
`hash_tasktrove.py` ran (exact; deprecated dataset versions join only with
``--include-deprecated``), else by the sweep's data-source labels. Substring
matching, so `nl2bash` also finds `nl2bash-tasks-cleaned-oracle-v2`.
``--list`` prints every TaskTrove dataset.

    uv run --no-project --with pandas --with pyarrow --with huggingface_hub \
      python relaxed_coverage.py nl2bash
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from hash_sft10k_tasks import DEFAULT_CACHE
from teacher_coverage import canon_teacher, print_table

TASKTROVE = "open-thoughts/TaskTrove"


def tasktrove_counts(cache: Path) -> pd.DataFrame:
    """dataset -> tasks for every TaskTrove folder, from parquet metadata.

    TaskTrove keeps retired dataset versions under `deprecated/`; they are
    listed too (old trace campaigns join against them), flagged in the
    ``deprecated`` column.
    """
    out = cache / "tasktrove_counts.csv"
    if out.exists():
        df = pd.read_csv(out)
        if "deprecated" in df.columns:      # else: cache predates the column
            return df
    from huggingface_hub import HfFileSystem
    import pyarrow.parquet as pq
    fs = HfFileSystem()
    rows = []
    for path in sorted(fs.glob(f"datasets/{TASKTROVE}/**/*.parquet")):
        dataset = path.split("/")[-2]
        with fs.open(path) as fh:
            rows.append({"dataset": dataset,
                         "tasks": pq.ParquetFile(fh).metadata.num_rows,
                         "deprecated": "/deprecated/" in path})
        print(f"  {dataset}: {rows[-1]['tasks']:,}", flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)
    return df


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", nargs="?", default="",
                    help="source label substring, e.g. nl2bash")
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    ap.add_argument("--no-tasktrove", action="store_true",
                    help="skip the TaskTrove task counts (no network)")
    ap.add_argument("--list", action="store_true",
                    help="print every TaskTrove dataset and exit")
    ap.add_argument("--include-deprecated", action="store_true",
                    help="also hash-join TaskTrove's retired dataset "
                         "versions (needs hash_tasktrove.py "
                         "--include-deprecated)")
    args = ap.parse_args()
    if args.list:
        tt = tasktrove_counts(args.cache)
        print_table("TASKTROVE DATASETS", ["dataset", "tasks", "status"],
                    [[r.dataset, f"{r.tasks:,}",
                      "deprecated" if r.deprecated else "active"]
                     for r in tt.itertuples()])
        return
    if not args.source:
        raise SystemExit("pass a source label (or --list)")
    needle = args.source.lower()

    matched: list[str] = []
    tt = pd.DataFrame()
    if not args.no_tasktrove:
        tt = tasktrove_counts(args.cache)
        hit = tt[tt["dataset"].str.lower().str.contains(needle)]
        keep = hit if args.include_deprecated else hit[~hit["deprecated"]]
        matched = keep["dataset"].tolist()
        print_table(f"TASKTROVE DATASETS MATCHING '{args.source}'",
                    ["dataset", "tasks", "status"],
                    [[r.dataset, f"{r.tasks:,}",
                      "deprecated" if r.deprecated else "active"]
                     for r in hit.itertuples()] or [["(none)", "", ""]])

    ibt = pd.read_csv(args.cache / "sweep" / "instructions_by_teacher.csv",
                      keep_default_na=False)
    ibt["teachers"] = ibt["teachers"].map(lambda ts: ";".join(
        sorted({canon_teacher(t) for t in ts.split(";")})))

    hashed = {ds: args.cache / "tasktrove_hashes"
              / (re.sub(r"[^A-Za-z0-9]+", "_", ds) + ".parquet")
              for ds in matched}
    hashed = {ds: f for ds, f in hashed.items() if f.exists()}
    if hashed:
        seen = set(ibt["hash"])
        dep = set(tt[tt["deprecated"]]["dataset"]) if len(tt) else set()
        task_hashes: set = set()
        rows = []
        for ds, f in hashed.items():
            th = pd.read_parquet(f)["hash"].dropna()
            task_hashes |= set(th)
            rows.append([ds, f"{len(th):,}", f"{th.isin(seen).sum():,}",
                         "deprecated" if ds in dep else "active"])
        print_table("EXACT JOIN: tasks with >=1 trace, per dataset",
                    ["dataset", "tasks", "traced", "status"], rows)
        df = ibt[ibt["hash"].isin(task_hashes)]
        scope = "exact hash join with TaskTrove"
    else:
        if "datasources" not in ibt.columns:
            raise SystemExit("no TaskTrove hashes for the matched datasets "
                             "and instructions_by_teacher.csv has no "
                             "datasources column - run hash_tasktrove.py, or "
                             "regenerate the csv (--cached-only suffices)")
        df = ibt[ibt["datasources"].str.lower().str.contains(needle)]
        scope = "repo-name labels (run hash_tasktrove.py for the exact join)"
    if df.empty:
        raise SystemExit(f"no swept instruction matches '{args.source}'")

    print(f"\n'{args.source}': {len(df):,} distinct tasks with >=1 trace "
          f"({scope})")
    per_teacher = (df.assign(teacher=df["teachers"].str.split(";"))
                     .explode("teacher").groupby("teacher")["hash"].size()
                     .sort_values(ascending=False))
    print_table("PER TEACHER: tasks of this source with >=1 trace "
                "(need not be the same tasks)",
                ["teacher", "tasks"],
                [[t, f"{n:,}"] for t, n in per_teacher.items()])
    print("Exact same-task overlap per teacher combination: "
          "teacher_coverage.py's combination tables.")


if __name__ == "__main__":
    main()
