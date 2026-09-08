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

**Teacher combinations** (questions 2-3): one table per n = 2, 3, ... Each
row is a combination of n teachers, largest overlap first, with two counts:

- **exact task overlap**: tasks (same `instruction.md` hash) every teacher
  in the combination has a trace for.
- **same-source overlap**: tasks a comparison could use if they only need
  to come from the same data source, not be identical. Per source, the
  usable count is the smallest per-teacher count (if GLM-4.6 covers 5,200
  swesmith tasks and GPT-5-nano 5,000, the pair can use 5,000); the cell
  sums this over sources; the parenthesis lists the three sources
  contributing most, the rest folded into `+k more`, e.g.
  `8,400 (swesmith 5,000; nl2bash 2,400; tezos 700; +2 more)`. A task's source label
  comes from the TaskTrove registry where it reaches, else the task-id
  prefix (`tezos-0561` -> `tezos`), else the repo name.

The same tables are printed twice: over all data sources, and constrained to
the OT-Agent sources.

The teacher of a trajectory is read, in order, from: AgentTrove's per-row
`original_teacher` column; the `model` column (the model id the pipeline
recorded, e.g. `gpt-5-nano-2025-08-07`); for version-less `hosted_vllm/glm`
rows, a generation `run_id` shared with SFT-10K (proves GLM-4.7); the repo
name; documented `TEACHER_OVERRIDES`; else the raw model string is kept as
the label (`hosted_vllm/glm` still says "some GLM", just not which). Only
traces with no model value at all become `<unknown>`, which the tables
exclude.

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
$RUN $TC/find_candidate_repos.py --all             # ~2 min; drop --all for
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
