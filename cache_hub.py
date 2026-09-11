#!/usr/bin/env python3
"""Share the sweep cache through the Hub, so nobody has to re-hash 977 repos.

    uv run --no-project --with huggingface_hub python cache_hub.py download --cache <dir>
    uv run --no-project --with huggingface_hub python cache_hub.py upload   --cache <dir>

`download` fills `<cache>` (default: DEFAULT_CACHE of hash_sft10k_tasks.py)
from HUB_REPO; afterwards `teacher_coverage.py --cache <dir>` reports without
fetching anything, and `overlap_members.py --cache <dir>` works as is. Pass
`--only-hashes` to skip the derived tables.

`upload` pushes the cache files listed in SHARED (hashes, ids, counts and
csvs; never task text) to HUB_REPO, replacing what is there, and writes the
dataset card from CARD. Needs a write token (HF_TOKEN) of the repo owner;
`--private` keeps the repo private, the default makes it public.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from huggingface_hub import HfApi

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:                                  # same default as the other scripts,
    from hash_sft10k_tasks import DEFAULT_CACHE   # but pandas is not needed here
except ImportError:
    DEFAULT_CACHE = Path("/data/cat/ws/frwe188h-otagent/tmp/agenttrove_cache")

HUB_REPO = "FWeindel/teacher-coverage-hash-cache"

#: What the cache dir contributes, relative to `<cache>`. The hashes dir is
#: the expensive part (one parquet per swept repo); the rest is cheap but
#: needed for a report without any network access.
SHARED = ["sft_text.parquet",                 # SFT-10K tasks: id, family, text hash
          "tasktrove_hashes/*.parquet",       # TaskTrove registry: task_path, hash
          "sweep/candidates.csv",             # the worklist (find_candidate_repos.py)
          "sweep/hashes/*.parquet",           # per repo: hash, task, teacher, ... n_traj
          "sweep/sweep_status.csv",           # per repo: read/skipped, tasks matched
          "sweep/instructions_by_teacher.csv",  # merged: hash -> teachers, sources
          "teacher_coverage.csv"]             # SFT-10K task -> teachers, repos
HASHES_ONLY = SHARED[:4]

CARD = """---
license: apache-2.0
pretty_name: teacher-coverage hash cache
---
# teacher-coverage hash cache

The cache behind the teacher-coverage analysis for OpenThoughts-Agent
(code and result tables: https://github.com/franziweindel/otagent-teacher-coverage):
which teacher models have trajectories for which agentic tasks, across the
datagen accounts on the Hub (DCAgent, DCAgent2, mlfoundations-dev, laion,
marin-community, open-thoughts, ...). Tasks are identified by the SHA-1 of
their whitespace-collapsed `instruction.md` text, never by task id (ids are
renumbered and reused across datasets). No task text is included, only
hashes, ids, teacher labels and counts.

| path | one row per | columns |
|---|---|---|
| `sweep/hashes/<repo>.parquet` | (hash, task id, teacher, model, run_id, date, trajectory hash, outcome, reward, trace_source) in that trace repo | `n_traj` rows |
| `sft_text.parquet` | OpenThoughts-Agent-SFT-10K task | `base_id`, `family`, `text` hash source, `run_id` |
| `tasktrove_hashes/<dataset>.parquet` | TaskTrove task | `task_path`, `hash` |
| `sweep/candidates.csv` | Hub dataset considered | name filter outcome, implied teacher |
| `sweep/instructions_by_teacher.csv` | distinct instruction | its teachers, per-teacher `n_traj`, data source |
| `sweep/sweep_status.csv` | repo | read or why skipped, SFT-10K tasks matched |

`task` is the id the trace repo itself gives the row (`superuser-0018`,
`swesmith-01176_copy0001`; a row locator where the repo has no id column).
It names a row inside that repo only. `teacher` is null where the repo has
no per-row model column; the sweep then uses the repo name. `traj_hash` is
the sha1 of the whole conversation (identical copies across repos collapse);
`outcome` is pass / partial / fail / error:<class> / unscored from the
repo's `result` column, `reward` its numeric value. `trace_source` is the
repo's own label (`main`, `summarization-k-summary` / `-answers` for the
agent's segments around its k-th context reset, or a dataset label); the
2-turn `summarization-k-questions` helper calls are not included.

Use: clone the repo above, then `python cache_hub.py download --cache <dir>`;
`python teacher_coverage.py --cache <dir> --cached-only` rebuilds every table
from the cache alone, and `python overlap_members.py <teacher> <teacher>
--cache <dir>` lists the tasks and repos behind one table cell.
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("action", choices=["download", "upload"])
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    ap.add_argument("--repo", default=HUB_REPO)
    ap.add_argument("--only-hashes", action="store_true",
                    help="download: skip the derived csv tables")
    ap.add_argument("--private", action="store_true",
                    help="upload: keep the repo private")
    args = ap.parse_args()
    api = HfApi()

    if args.action == "download":
        patterns = HASHES_ONLY if args.only_hashes else SHARED
        path = api.snapshot_download(args.repo, repo_type="dataset",
                                     local_dir=args.cache,
                                     allow_patterns=patterns)
        n = sum(1 for _ in Path(path).rglob("*.parquet"))
        print(f"cache at {path}: {n} parquet files")
        return

    missing = [p for p in SHARED if not list(args.cache.glob(p))]
    if missing:
        raise SystemExit(f"nothing matches {missing} under {args.cache}")
    api.create_repo(args.repo, repo_type="dataset", exist_ok=True,
                    private=args.private)
    (args.cache / "README.md").write_text(CARD)
    api.upload_folder(repo_id=args.repo, repo_type="dataset",
                      folder_path=args.cache,
                      allow_patterns=[*SHARED, "README.md"],
                      delete_patterns=["sweep/hashes/*", "tasktrove_hashes/*"],
                      commit_message="sweep cache: task ids, copy/src suffix "
                                     "fix, per-repo trajectory counts")
    if not args.private:
        api.update_repo_settings(args.repo, repo_type="dataset", private=False)
    print(f"uploaded to https://huggingface.co/datasets/{args.repo}"
          f" ({'private' if args.private else 'public'})")


if __name__ == "__main__":
    main()
