# teacher_coverage

Which teacher models already have trajectories for which tasks. Three questions:

1. **SFT-10K tasks**: which teachers have a trace per task of
   [`open-thoughts/OpenThoughts-Agent-SFT-10K`](https://huggingface.co/datasets/open-thoughts/OpenThoughts-Agent-SFT-10K),
   and how many trajectories a re-SFT with teacher X still needs.
2. **OT-Agent data sources** (`swesmith`, `superuser`, `tezos`, `issue`):
   for a given teacher combination, how many of these sources' tasks do all
   its teachers share, either exactly or by same data source.
3. **All data sources**: for a given teacher combination, how many tasks do
   all its teachers share, either exactly or by same data source.

We use each task's `instruction.md` text (whitespace-collapsed hash) to find
the same task across datasets, not the task id: ids are unreliable, e.g. all
1,588 id-equal `swesmith` pairs between SFT-10K and AgentTrove hold
different texts.

## Result tables, and how to read them

**Generation gap** (question 1): data source x teacher, over the 8,360
SFT-10K tasks. A cell counts the tasks still MISSING a trace from that
teacher, so 0 = fully covered; GLM-4.7 is 0 everywhere because SFT-10K
itself is GLM-4.7 traces.

**Teacher combinations** (questions 2-3): one table per n = 2, 3, ... Every
combination whose teachers share at least one exact task or one data source
gets a row (nothing is cropped), sorted by exact tasks then same-source
tasks, with four counts:

- **exact tasks**: tasks (same `instruction.md` hash) every teacher in the
  combination has a trace for.
- **exact trajectories**: the same tasks counted with duplicates. Per
  shared task, the smallest per-teacher trajectory count, summed: how many
  complete task-aligned trajectory tuples exist. Per-teacher counts are
  over distinct conversation hashes, summed across repos, so a mirror
  (AgentTrove holds copies of the DCAgent dumps) cannot count a trajectory
  twice while an independent rerun does add up. A row without a
  conversation (instruction-only repos: task sets, not trace dumps) is not
  a trajectory and counts for nothing, teacher coverage included.
- **same-source tasks**: tasks a comparison could use if they only need to
  come from the same data source, not be identical. Per source, the
  smallest per-teacher distinct-task count (if GLM-4.6 covers 5,200
  swesmith tasks and GPT-5-nano 5,000, the pair can use 5,000), summed;
  the parenthesis lists the three sources contributing most, the rest
  folded into `+k more`. A task's source label comes from the TaskTrove
  registry where it reaches, else the task-id prefix (`tezos-0561` ->
  `tezos`), else the repo name.
- **same-source trajectories**: the same, counting trajectories instead of
  distinct tasks.

The same tables are printed twice: over all data sources, and constrained to
the OT-Agent sources.

The teacher is extracted per trajectory, in order: the `model` id column,
normalized with `TEACHER_TOKENS` (spelling variants to one name, e.g.
`glm47` to GLM-4.7; full list in `find_candidate_repos.py`); AgentTrove's
hand-typed `original_teacher` column where the id does not resolve; the repo
name, also normalized with `TEACHER_TOKENS`. If no normalization works, the bare model id column is
kept as the label, i.e. `hosted_vllm/glm` (some GLM, version unknown). Two
exceptions pin such bare rows to GLM-4.7: a `run_id` shared with SFT-10K,
and the documented `TEACHER_OVERRIDES`.

The same-source count assumes rerunning the datagen pipeline on a source
yields tasks of similar quality, so same-source trajectories are comparable
training data without being identical. This matters because the exact task
overlap is low (see below).

### Why exact overlap is so low

The paper's teacher ablation (Kimi K2.5, GLM 5, GLM 4.6, GPT-5.3-Codex)
implies multi-teacher traces exist, yet almost none join to SFT-10K. Each
ablation reruns the full pipeline including task generation; what survives a
rerun depends on how a source writes its `instruction.md`:

- **Verbatim sources (superuser, tezos)** copy the StackExchange post body,
  so overlap is set by pool size: two draws of 10K from a pool of N share
  ~10,000^2/N tasks. Tezos has ~997 unique questions and cycles them, so
  runs overlap heavily; superuser draws from a much larger pool and overlaps
  at 5%.
- **LLM-written sources (swesmith, issue)** have a model write the task
  text, so a rerun rewrites it even for the same upstream bug. Their
  cross-teacher coverage comes from repos reusing one task set with another
  teacher, never from independent reruns (checked against a Kimi swesmith
  campaign: 11 id matches, 25 title matches, 0 text matches).


## Skip the hashing: download the cache

The sweep cache is published at
[`FWeindel/teacher-coverage-hash-cache`](https://huggingface.co/datasets/FWeindel/teacher-coverage-hash-cache)
(hashes, ids, teacher labels and counts; no task text). With it, the report
runs without touching any trace repo:

    uv run --no-project --with huggingface_hub python cache_hub.py download --cache <dir>
    uv run --no-project --with pandas --with pyarrow --with huggingface_hub \
      python teacher_coverage.py --cache <dir> --cached-only

`teacher_coverage.py` only fetches repos whose cache file is missing, so a
new candidate repo costs one fetch, not a re-sweep. `cache_hub.py upload`
pushes a refreshed cache back (owner token needed).

## From a table cell to the tasks behind it

`overlap_members.py` takes a row and a column of an `n<k>.md` table and
lists what the number counts: per task its hash, source, SFT-10K id and
TaskTrove id where registered, and per teacher the repos holding a trace.
It recomputes the number from the cache and prints it next to the table's.

    uv run --no-project --with pandas --with pyarrow --with huggingface_hub \
      python overlap_members.py GLM-4.7 GPT-5-nano \
      --column exact-tasks --ot-only --cache <cache>

Teachers as separate arguments or comma-separated, spelled as in the table;
`--column` is one of `exact-tasks`, `exact-trajectories`,
`same-source-tasks`, `same-source-trajectories`; `--ot-only` picks the
`_top-4-datasources` table. Output goes to `results/overlaps/<teachers>__
<column>[__ot].csv`, one row per (task, teacher, repo). For the same-source
columns, `binding=True` marks the rows of the teacher whose count is the
per-source minimum, i.e. the rows that add up to the number. `task_id` is
the id the repo itself gives the task (`task` column, else another id
column, else `file#rowgroup:row`); it names a row inside that dataset only,
the hash is the cross-dataset key. `sft10k_id` / `tasktrove_task` are set
where the task is registered there. Runs in about 90 s on the login node.

`--outcome` takes a comma list of outcome values spelled exactly as the
cache stores them and counts only those trajectories, printing the
filtered number next to the table's. Values: `unscored` (no result
recorded; most of the data, all of AgentTrove), `pass` / `partial` /
`fail` (a numeric result: >=1, between 0 and 1, 0), `error:<class>` for a
run that ended in that exception (`error:AgentTimeoutError`,
`error:DaytonaError`, `error:AgentEnvironmentTimeoutError`, ...). Nothing
is grouped: whether a timed-out or unscored trajectory is useful teacher
data is the user's call. The run's `outcomes.md` lists every value with
its count, repos and teachers.

The sweep cache (`<cache>/sweep/hashes/<repo>.parquet`) holds, per repo, one
row per (instruction hash, task id, teacher, model, run_id, date,
trajectory hash, outcome, reward, trace_source) with a row count `n_traj`. Text is never
cached, only hashes. The trajectory hash is the sha1 of the whole
conversation: trajectories are summed within and across repos, and an
identical conversation hash is the only thing that collapses two rows, so a
mirror's copy (AgentTrove holds the DCAgent dumps) counts once while an
independent rerun adds up. `outcome` comes from the repo's `result`
column: pass / partial / fail from a numeric score, `error:<class>` from an
error name kept verbatim (`error:AgentTimeoutError`), `unscored` where
the column is null or missing. `trace_source` is kept as the repo wrote
it: `main` (or a dataset label, or nothing) for the run itself,
`summarization-k-summary` / `-answers` for the agent's conversation
segments before and after its k-th context reset; each is a row and counts
as a trajectory of the task, `--trace-source main` counts runs only. The
2-turn `summarization-k-questions` helper calls are dropped at fetch time:
they start with "You are picking up work from a previous AI agent", not
the task, and would register as tasks of their own. A repo without a `conversations` or
`messages` column (task sets, single-response annotation dumps, eval
outputs) is skipped, and a row whose conversation is empty is dropped
before it is hashed: no trace, no trajectory. `results/<stamp>/outcomes.md`
lists every outcome value with its count; the combination tables count
every outcome.

## Results

One directory per run, one table per file:

    results/<stamp>/generation_gap.md          question 1
    results/<stamp>/n<k>.md                    k-teacher combinations, all sources
    results/<stamp>/n<k>_top-4-datasources.md  same, OT-Agent sources only
    results/<stamp>/repos.md                   repos read / skipped

`results/candidates.csv` lists every HF dataset found on the datagen
accounts; `results/candidates_swept.csv` is the subset that was actually
swept. Results so far are from public repos only: the
[marin#6191](https://github.com/marin-community/marin/issues/6191) traces are
in the private `open-athena` org, which are not included yet as no access.

## How to run

```bash
cd ~   # not /tmp: a foreign unreadable /tmp/.venv breaks uv's env discovery
set -a; source ~/secrets.env; set +a   # HF_TOKEN (user FWeindel)
RUN="uv run --no-project --with pandas --with pyarrow --with huggingface_hub python"
TC=/data/cat/ws/frwe188h-otagent/OpenThoughts-Agent-trp/scripts/analysis/teacher_coverage

$RUN $TC/hash_sft10k_tasks.py --workers 8          # ~1 min
$RUN $TC/find_candidate_repos.py --all             # ~2 min; --all also keeps
                                                   #   any traces or teacher
                                                   #   name; drop it for
                                                   #   SFT-10K sources only
$RUN $TC/hash_tasktrove.py --workers 100           # ~10 min, one-time
$RUN $TC/teacher_coverage.py --workers 100         # hours; resumable
$RUN $TC/relaxed_coverage.py nl2bash               # instant drill-down
```

`--no-project` skips this repo's torch/vllm install; `--with` names the only
three libraries needed. Every script takes `--cache` (default
`/data/cat/ws/frwe188h-otagent/tmp/agenttrove_cache`, scratch).
`teacher_coverage.py` also takes `--cached-only` (re-report without
fetching), `--refresh`, `--max-repos K`, `--sets-only` (rebuild only the
combination tables).


The whole hash cache is backed up to the private HF dataset
`FWeindel/teacher-coverage-hash-cache`; restore with `hf download
FWeindel/teacher-coverage-hash-cache --repo-type dataset --local-dir <cache>`
instead of re-sweeping.
