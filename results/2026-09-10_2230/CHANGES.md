# What changed vs the previous run (2026-09-09_1659)

Full refetch of all 977 candidate repos with a new cache schema (Barnard
jobs 38145010, 38145658, 38147522; tables rebuilt by 38149890 as 2026-09-10_2230). 786 repos
hold trajectories; 191 are skipped for good: 166 have no `conversations` /
`messages` column (task sets with `task_binary`, single-response annotation
dumps, eval outputs), 25 have no parquet. The candidate set itself is the
same as in the previous run.

## Cache schema (`sweep/hashes/<repo>.parquet`)

One row per (instruction hash, task id, teacher, model, run_id, date,
trajectory hash, outcome, reward, trace_source) with a row count `n_traj`.
New columns:

- `task`: the repo's own task id (`task` column, else another id column,
  else `<file>#<rowgroup>:<row>`). Names a row inside that repo only.
- `traj_hash`: sha1 of the whole conversation.
- `outcome` / `reward`: from the repo's `result` column: `pass` /
  `partial` / `fail` for a numeric score, `error:<class>` verbatim,
  `unscored` when null or absent. `error:success` (one GLM-5.x repo
  writes `success`) is aliased to `pass` at read time.
- `trace_source`: kept as the repo wrote it (`main`, a dataset label,
  `summarization-k-summary` / `-answers`); the 2-turn
  `summarization-k-questions` helper rows are dropped at fetch time (they
  start with "You are picking up work from a previous AI agent", not the
  task, and would register as tasks of their own).

The cache is published at
https://huggingface.co/datasets/FWeindel/teacher-coverage-hash-cache
(`cache_hub.py download`).

## Counting

- **Trajectories are deduplicated by conversation hash, then summed** within
  and across repos. Before: the max over cache rows, which undercounted a
  repo holding several runs of one task and could not add independent
  reruns from two repos. Exact-trajectory cells rise accordingly:
  GLM-4.6;GLM-4.7 (OT sources) 56,203 -> 80,359; GLM-4.7;Kimi-2.5
  12,159 -> 25,359. Pairs bounded by a single-run teacher barely move:
  GLM-4.7;GPT-5-nano 29,079 -> 29,116.
- **Summarization segments count as trajectories** of their task (each
  `summarization-k-summary` / `-answers` row is one). `overlap_members.py
  --trace-source main,<none>` counts runs only.
- **Rows without a conversation are not trajectories** and count for
  nothing, teacher coverage included.
- Task-id suffixes `_copy`, `_copyNNNN`, `_srcN` are stripped before the
  source prefix is taken, so the junk sources of the previous run
  (`all_puzzles-0059_copy`, `task_1008_copy`, ...) are gone.
- Exact-task counts and the generation gap are essentially unchanged
  (GLM-4.7;GPT-5-nano exact tasks 20,103 -> 20,111; gap totals identical).

## New files and tools

- `outcomes.md`: every outcome value and every trace_source value in the
  cache with its count, repos and top teachers. The values are what
  `overlap_members.py --outcome` / `--trace-source` accept.
- `overlap_members.py`: one table cell -> the tasks and repos behind it,
  with `task_id`, SFT-10K / TaskTrove ids, per-repo outcome and
  trace_source split, and exact-value filters on both.
- `check_trace_source.py`: finds cached repos that a bug (2026-09-10, kept
  only `main` rows) had truncated; all 323 were refetched before these
  tables were built.
- `cache_hub.py`: upload / download the cache.

## Run notes

Hub rate limit: 1,000 api requests per 300 s per user. Two schema scans run
from the login node during the first sweep made it skip 779 repos with 429;
`fetch_with_retry` now honours the `Retry after` hint. Do not run other
Hub-heavy jobs under the same token while a sweep runs.
