# What changed vs the previous run (2026-09-08_2132)

Barnard job 38108268, 2h54, 977 repos read (previous run: job 38084300, 717
repos). Same `--all` candidate mode as before; the delta comes from:

- **Any teacher token in the name now qualifies a repo.** `is_candidate` in
  `find_candidate_repos.py` keeps a repo with `--all` if the name has a
  `traces` token OR a teacher token (`teacher_from_text`). Before, only the
  `traces` token counted. All 219 repos new in this run have neither a
  `traces` nor a data-source token in their name: marin-community appears
  for the first time (66 repos, the open-thoughts-4 `*-qwen3-*-annotated`
  sets), plus DCAgent `*-dev-71-tasks`, DCAgent2 `GLM-4.7-*-sandboxes-maxeps`
  / `Kimi-2.5-*`, mlfoundations-dev `*_qwen3` sets, and one public
  open-athena repo.
- **Forced candidates** (ALWAYS_CANDIDATE), the paper's Table 6 teacher
  ablation arms: `DCAgent/b1_top4_seq` (pinned to GLM-4.7 via
  TEACHER_OVERRIDES), `DCAgent/c1_kimi_k2.5_fixed`,
  `DCAgent/c1_gpt53_codex_fixed`. None of the three was in the previous run.
- **New teacher tokens**: Kimi-2.5 also from `kimi-k2.5` / `k2.5`;
  GPT-5.3-Codex, Qwen3-Coder-480B, Qwen3-Coder-30B as distinct teachers.
  Effect: GPT-5.3-Codex and Kimi-2.5 now appear as columns in
  `generation_gap.md` and as rows in the n-tables.
- **Table format**: the combination tables gained the trajectory-count
  columns (exact trajectories, same-source trajectories) next to the
  distinct-task counts.

Not a change: RZ412 (39 repos) and marianna13 (2) were already swept in the
previous run. ORGS also lists open-athena and EtashGuha, both already there.

Headline deltas (OT-Agent sources, n=2): GLM-4.7;GPT-5-nano exact tasks
14,340 -> 20,103; GLM-4.6;GLM-4.7 15,409 -> 19,156; GLM-4.7;Kimi-2.5 is
new at 9,693. Generation gap totals for the old columns are unchanged.

Caveat: `teacher_coverage.py` has uncommitted edits since 2026-08-26 (bare
`hosted_vllm/glm` resolved by run_id, task-id prefix as source, shard
caching); which of those landed between the two runs is not recorded.
