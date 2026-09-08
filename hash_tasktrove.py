#!/usr/bin/env python3
"""Hash every TaskTrove task's instruction.md, for exact joins per source.

`open-thoughts/TaskTrove` holds one folder per task dataset; each row is one
task packed as a tar.gz (`task_binary`). This unpacks every task, extracts
its instruction.md, and hashes it exactly like `hash_sft10k_tasks.py` hashes
SFT-10K and `teacher_coverage.py` hashes the trace repos, so TaskTrove tasks
join against everything else on the same key.

One parquet per dataset under `<cache>/tasktrove_hashes/<dataset>.parquet`
(columns: task_path, hash), skipped when it already exists: hash once, saved
forever. Datasets are processed ``--workers`` at a time. Retired dataset
versions under TaskTrove's `deprecated/` are skipped unless
``--include-deprecated`` is passed.

    uv run --no-project --with pandas --with pyarrow --with huggingface_hub \\
      python hash_tasktrove.py --workers 100
"""

from __future__ import annotations

import argparse
import io
import re
import tarfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem

from hash_sft10k_tasks import DEFAULT_CACHE, text_hash

TASKTROVE = "open-thoughts/TaskTrove"


def instruction_text(task_binary: bytes) -> object:
    """The instruction.md inside one task's tar.gz, or NA."""
    try:
        with tarfile.open(fileobj=io.BytesIO(task_binary), mode="r:gz") as tar:
            names = [n for n in tar.getnames()
                     if n.lower().endswith("instruction.md")]
            if not names:
                return pd.NA
            member = min(names, key=len)         # top-level one over nested
            fh = tar.extractfile(member)
            return fh.read().decode("utf-8", errors="replace") if fh else pd.NA
    except Exception:
        return pd.NA


def hash_dataset(parquet_path: str, out: Path) -> tuple[str, int, int]:
    """Hash one TaskTrove dataset's tasks into ``out``. Returns counts."""
    dataset = parquet_path.split("/")[-2]
    if out.exists():
        done = pd.read_parquet(out)
        return dataset, len(done), int(done["hash"].isna().sum())
    t0 = time.time()
    frames = []
    with HfFileSystem().open(parquet_path) as fh:
        pf = pq.ParquetFile(fh)
        for rg in range(pf.metadata.num_row_groups):
            df = pf.read_row_group(rg, columns=["path", "task_binary"]
                                   ).to_pandas()
            frames.append(pd.DataFrame({
                "task_path": df["path"],
                "hash": df["task_binary"].map(instruction_text).map(text_hash),
            }))
    res = pd.concat(frames, ignore_index=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    res.to_parquet(out, index=False)
    misses = int(res["hash"].isna().sum())
    print(f"  {dataset}: {len(res):,} tasks, {misses} without instruction.md, "
          f"{time.time() - t0:.0f}s", flush=True)
    return dataset, len(res), misses


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--only", default="",
                    help="only datasets whose folder name contains this")
    ap.add_argument("--include-deprecated", action="store_true",
                    help="also hash TaskTrove's retired dataset versions")
    args = ap.parse_args()
    paths = sorted(HfFileSystem().glob(f"datasets/{TASKTROVE}/**/*.parquet"))
    if not args.include_deprecated:
        paths = [p for p in paths if "/deprecated/" not in p]
    if args.only:
        paths = [p for p in paths if args.only.lower() in p.lower()]
    print(f"{len(paths)} TaskTrove datasets, {args.workers} workers",
          flush=True)
    hdir = args.cache / "tasktrove_hashes"
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(
            lambda p: hash_dataset(
                p, hdir / (re.sub(r"[^A-Za-z0-9]+", "_",
                                  p.split("/")[-2]) + ".parquet")), paths))
    total = sum(n for _, n, _ in results)
    print(f"hashed {total:,} tasks across {len(results)} datasets "
          f"-> {hdir}")


if __name__ == "__main__":
    main()
