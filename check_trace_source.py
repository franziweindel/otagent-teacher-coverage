#!/usr/bin/env python3
"""Find cached repos whose `trace_source` rows an earlier sweep dropped.

Until 2026-09-10 14:45 the sweep kept only rows with `trace_source` null or
`main`: `summarization-k-summary` / `-answers` segments (trajectories) and
dataset labels (`exp_rpt_issue_10k`) were dropped, repos with only such
rows failed outright. This reads the column alone from every cached repo
that has it and reports rows whose value is neither null nor `main`
(`-questions` helper rows excepted, those stay dropped). With `--fix` the
affected cache files are deleted so the next sweep refetches them.

    uv run --no-project --with pandas --with pyarrow --with huggingface_hub \\
      python check_trace_source.py --cache <cache> [--fix] [--workers 16]
"""
from __future__ import annotations

import argparse
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hash_sft10k_tasks import DEFAULT_CACHE, hashes_path  # noqa: E402
from teacher_coverage import worklist  # noqa: E402


def check(repo: str, attempts: int = 8) -> tuple[str, int, int, list[str]]:
    """(repo, rows, rows with a non-main label, labels); retried on 429."""
    for attempt in range(attempts):
        try:
            return _check(repo)
        except Exception as exc:
            msg = str(exc)
            if "429" not in msg or attempt == attempts - 1:
                raise
            m = re.search(r"Retry after (\d+) seconds", msg)
            wait = (int(m.group(1)) if m else 60) + random.uniform(5, 60)
            print(f"  {repo}: 429, retry in {wait:.0f}s", flush=True)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def _check(repo: str) -> tuple[str, int, int, list[str]]:
    fs = HfFileSystem()
    n = bad = 0
    labels: set[str] = set()
    for path in fs.glob(f"datasets/{repo}/**/*.parquet"):
        with fs.open(path) as fh:
            pf = pq.ParquetFile(fh)
            if "trace_source" not in pf.schema_arrow.names:
                return repo, 0, 0, []
            col = pf.read(columns=["trace_source"]).column(0).to_pylist()
        n += len(col)
        for v in col:
            if v is None or v == "main" or str(v).endswith("-questions"):
                continue
            bad += 1
            labels.add(str(v))
    return repo, n, bad, sorted(labels)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    ap.add_argument("--fix", action="store_true",
                    help="delete the cache file of every affected repo")
    ap.add_argument("--workers", type=int, default=6,
                    help="keep low: the Hub allows 1,000 api calls per 5 min")
    args = ap.parse_args()
    repos = [r for r, _, _ in worklist(args.cache)
             if hashes_path(args.cache, r).exists()]
    print(f"{len(repos)} cached repos", flush=True)
    affected = []
    with ThreadPoolExecutor(args.workers) as pool:
        for repo, n, bad, labels in pool.map(check, repos):
            if bad:
                affected.append(repo)
                print(f"  {bad:>7,} of {n:>8,} rows  {repo}  {labels[:4]}",
                      flush=True)
    print(f"{len(affected)} affected repos")
    if args.fix:
        for repo in affected:
            hashes_path(args.cache, repo).unlink()
        print(f"deleted {len(affected)} cache files; rerun the sweep")


if __name__ == "__main__":
    main()
