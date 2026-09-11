# Trajectory outcomes (deduplicated trajectories)

Every outcome value in the cache. These are the values
`overlap_members.py --outcome` accepts, spelled exactly so.

| outcome | trajectories | repos | teachers |
|---|---|---|---|
| unscored | 10,376,739 | 584 | Qwen3 7,034,340; GLM-4.7 1,571,713; GPT-5-nano 629,114; hosted_vllm/glm 395,832; +24 more |
| error:AgentTimeoutError | 1,299,228 | 426 | GLM-4.7 1,097,381; hosted_vllm/glm 148,977; GLM-4.6 17,972; Kimi-2.5 8,375; +20 more |
| error:AgentEnvironmentTimeoutError | 93,742 | 146 | GLM-4.7 89,652; hosted_vllm/glm 2,023; GPT-5-nano 1,964; hosted_vllm/76c033d3f8b95796a21444f4340a3eeeb4e17142 51; +7 more |
| pass | 75,762 | 81 | hosted_vllm/9a1fb08510d7b18e8a32d5b6abcdb75f2fcabc24 20,138; Kimi-2.5 17,498; GLM-4.7 17,021; GLM-5.x 6,930; +13 more |
| fail | 54,578 | 82 | GLM-4.7 19,591; Kimi-2.5 18,164; Qwen3 4,857; hosted_vllm/9a1fb08510d7b18e8a32d5b6abcdb75f2fcabc24 3,688; +12 more |
| error:DaytonaError | 46,524 | 317 | GLM-4.7 35,913; GLM-4.6 5,331; hosted_vllm/glm 2,491; Kimi-2.5 2,120; +10 more |
| error:DaytonaNotFoundError | 40,533 | 205 | hosted_vllm/glm 23,153; GLM-4.7 17,189; GLM-4.6 134; Kimi-2.5 23; +6 more |
| error:ContextLengthExceededError | 27,222 | 109 | GLM-4.7 10,446; Qwen3 8,221; hosted_vllm/76c033d3f8b95796a21444f4340a3eeeb4e17142 5,014; Kimi-2.5 2,798; +3 more |
| error:RewardFileNotFoundError | 25,011 | 4 | hosted_vllm/76c033d3f8b95796a21444f4340a3eeeb4e17142 13,183; Qwen3 11,822; Kimi-2.5 3; GLM-4.7 3 |
| error:CancelledError | 4,607 | 47 | GLM-4.7 3,978; GLM-4.6 169; hosted_vllm/glm 136; hosted_vllm/9a1fb08510d7b18e8a32d5b6abcdb75f2fcabc24 112; +3 more |
| error:VerifierTimeoutError | 3,222 | 28 | hosted_vllm/76c033d3f8b95796a21444f4340a3eeeb4e17142 1,414; Qwen3 1,032; Kimi-2.5 514; GLM-4.7 203; +3 more |
| error:TypeError | 1,858 | 3 | GLM-4.7 1,858 |
| error:DaytonaAuthenticationError | 1,771 | 27 | GLM-4.7 1,747; Qwen3.5-122B 17; hosted_vllm/9a1fb08510d7b18e8a32d5b6abcdb75f2fcabc24 7 |
| error:InternalServerError | 1,467 | 21 | GLM-5.x 903; GLM-4.7 350; GLM-4.6 151; hosted_vllm/9a1fb08510d7b18e8a32d5b6abcdb75f2fcabc24 61; +1 more |
| error:FileNotFoundError | 1,338 | 5 | GLM-4.7 1,323; GLM-5.x 15 |
| error:timeout | 1,073 | 1 | GLM-5.x 1,073 |
| error:RuntimeError | 780 | 90 | GLM-4.7 709; Kimi-2.5 34; GLM-4.6 22; hosted_vllm/glm 6; +2 more |
| error:VerifierRuntimeError | 529 | 19 | GLM-4.7 274; hosted_vllm/grug-agentic-s3-step1903 95; Kimi-2.5 87; Qwen3 64; +2 more |
| error:DaytonaValidationError | 353 | 17 | GLM-4.7 353 |
| error:BadRequestError | 333 | 4 | Kimi-2.5 278; GLM-4.7 55 |
| error:ModelNotFoundError | 154 | 3 | GLM-5.x 154 |
| error:SummarizationTimeoutError | 112 | 7 | Kimi-2.5 101; GLM-4.6 7; Kimi-2.6 2; hosted_vllm/glm 2 |
| error:VerificationNotCompletedError | 95 | 4 | GLM-4.7 73; MiniMax-M2.7 22 |
| error:ServiceUnavailableError | 60 | 3 | GLM-5.x 43; GLM-4.6 17 |
| partial | 36 | 4 | Qwen3 16; GLM-4.7 11; Qwen3-Coder-30B 6; GLM-4.6 3 |
| error:OutputLengthExceededError | 34 | 7 | Kimi-2.5 28; Kimi-2.6 5; GLM-4.7 1 |
| error:AgentKilledBySignalError | 24 | 2 | hosted_vllm/grug-agentic-s3-step1903 24 |
| error:ContextManagementInfrastructureError | 6 | 1 | Qwen3 6 |
| error:NonZeroAgentExitCodeError | 5 | 1 | hosted_vllm/grug-agentic-s3-step1903 5 |
| error:AddTestsDirError | 3 | 3 | GLM-5.x 3 |
| error:IndexError | 2 | 2 | GLM-4.7 1; hosted_vllm/glm 1 |
| error:APITimeoutError | 1 | 1 | Qwen3 1 |
| error:OSError | 1 | 1 | Kimi K2.0 Thinking 1 |
| error:RateLimitError | 1 | 1 | GLM-4.6 1 |

# Trace sources

What each row is: `main` (or a dataset label, or none) is the
run itself; `summarization-k-summary` / `-answers` are the
agent's conversation segments before and after its k-th context
reset, counted as trajectories of the task. The 2-turn
`summarization-k-questions` helper calls are not cached. These
are the values `overlap_members.py --trace-source` accepts.

| trace_source | trajectories | repos | teachers |
|---|---|---|---|
| \<none\> | 9,571,525 | 473 | Qwen3 7,068,022; GLM-4.7 1,063,901; GPT-5-nano 615,981; GLM-4.6 237,428; +30 more |
| main | 2,154,174 | 250 | GLM-4.7 1,594,103; hosted_vllm/glm 447,541; GLM-4.6 65,050; Kimi-2.5 24,028; +3 more |
| summarization-1-summary | 116,136 | 245 | GLM-4.7 79,604; hosted_vllm/glm 29,777; Kimi-2.5 4,273; GLM-4.6 1,808; +3 more |
| summarization-1-answers | 82,605 | 239 | GLM-4.7 57,375; hosted_vllm/glm 19,228; Kimi-2.5 3,981; GLM-4.6 1,376; +3 more |
| summarization-2-summary | 38,841 | 195 | GLM-4.7 29,978; Kimi-2.5 3,796; hosted_vllm/glm 3,325; GLM-4.6 1,125; +3 more |
| summarization-2-answers | 32,103 | 183 | GLM-4.7 24,784; Kimi-2.5 3,775; hosted_vllm/glm 1,830; GLM-4.6 1,097; +3 more |
| summarization-3-summary | 8,005 | 152 | GLM-4.7 6,073; Kimi-2.5 930; hosted_vllm/glm 641; GLM-4.6 231; +3 more |
| summarization-3-answers | 6,614 | 149 | GLM-4.7 4,936; Kimi-2.5 873; hosted_vllm/glm 481; GLM-4.6 202; +3 more |
| summarization-4-summary | 5,248 | 143 | GLM-4.7 3,817; Kimi-2.5 829; hosted_vllm/glm 341; GLM-4.6 152; +3 more |
| summarization-4-answers | 4,241 | 137 | GLM-4.7 2,997; Kimi-2.5 811; hosted_vllm/glm 202; GLM-4.6 129; +3 more |
| exp_rpt_issue_10k | 3,994 | 1 | GLM-5.x 3,994 |
| stackex_tezos | 2,487 | 1 | GLM-5.x 2,487 |
| stackexchange_daytona | 1,649 | 1 | GLM-5.x 1,649 |
| stackexchange | 887 | 1 | GLM-5.x 887 |
| summarization-5-summary | 867 | 78 | GLM-4.7 624; Kimi-2.5 184; hosted_vllm/glm 42; GLM-4.6 14; +2 more |
| summarization-5-answers | 659 | 70 | GLM-4.7 462; Kimi-2.5 165; hosted_vllm/glm 18; GLM-4.6 12; +1 more |
| summarization-6-summary | 545 | 65 | GLM-4.7 368; Kimi-2.5 152; hosted_vllm/glm 14; GLM-4.6 9; +2 more |
| summarization-6-answers | 475 | 58 | GLM-4.7 309; Kimi-2.5 147; hosted_vllm/glm 10; GLM-4.6 8; +1 more |
| summarization-7-summary | 154 | 27 | GLM-4.7 119; Kimi-2.5 27; hosted_vllm/glm 6; GLM-4.6 1; +1 more |
| summarization-7-answers | 132 | 26 | GLM-4.7 98; Kimi-2.5 26; hosted_vllm/glm 6; GLM-4.6 1; +1 more |
| summarization-8-summary | 108 | 22 | GLM-4.7 80; Kimi-2.5 24; hosted_vllm/glm 3; hosted_vllm/qwen 1 |
| summarization-8-answers | 84 | 20 | GLM-4.7 58; Kimi-2.5 22; hosted_vllm/glm 3; hosted_vllm/qwen 1 |
| stackexchange_kube | 76 | 1 | GLM-5.x 76 |
| stackex_kube_verify2 | 70 | 1 | GLM-5.x 70 |
| summarization-9-summary | 33 | 9 | GLM-4.7 28; hosted_vllm/glm 3; Kimi-2.5 1; hosted_vllm/qwen 1 |
| summarization-9-answers | 29 | 9 | GLM-4.7 24; hosted_vllm/glm 3; Kimi-2.5 1; hosted_vllm/qwen 1 |
| summarization-10-summary | 26 | 8 | GLM-4.7 22; hosted_vllm/glm 2; Kimi-2.5 1; hosted_vllm/qwen 1 |
| stackexchange_bridge | 25 | 1 | GLM-5.x 25 |
| summarization-10-answers | 22 | 6 | GLM-4.7 18; hosted_vllm/glm 2; Kimi-2.5 1; hosted_vllm/qwen 1 |
| summarization-11-summary | 16 | 4 | GLM-4.7 14; hosted_vllm/glm 1; hosted_vllm/qwen 1 |
| summarization-11-answers | 15 | 4 | GLM-4.7 13; hosted_vllm/glm 1; hosted_vllm/qwen 1 |
| summarization-12-summary | 11 | 2 | GLM-4.7 10; hosted_vllm/glm 1 |
| summarization-12-answers | 9 | 2 | GLM-4.7 8; hosted_vllm/glm 1 |
| summarization-13-summary | 7 | 2 | GLM-4.7 6; hosted_vllm/glm 1 |
| stackex_kube_verify | 6 | 1 | GLM-5.x 6 |
| summarization-13-answers | 6 | 2 | GLM-4.7 5; hosted_vllm/glm 1 |
| stackex_kube_test | 4 | 1 | GLM-5.x 4 |
| summarization-14-summary | 4 | 2 | GLM-4.7 3; hosted_vllm/glm 1 |
| summarization-14-answers | 3 | 1 | GLM-4.7 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00194__f2kWNGa | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00216__Wx7gxED | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00333__jQkLmT5 | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00368__hKtdn6w | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00472__t9STVyA | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00578__VH8Bw7x | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00592__ZX625bU | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00602__cZoxLxj | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00619__ryeQZBn | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00756__aMnL5Ta | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00917__Hz2CYqD | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-00986__BFvpymn | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01156__Rc9GqM6 | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01233__BEjdBp4 | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01235__hTdRwWJ | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01422__rGiKtGs | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01465__KcWTjkF | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01492__5QBtuuS | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01614__UCyq294 | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01726__5Ba5bxw | 3 | 3 | GLM-5.x 3 |
| swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/swesmith-01830__fodNtKd | 3 | 3 | GLM-5.x 3 |
| \<10,748 more values, each below 3\> | 25,246 |  | values are in the cache; e.g. swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/s; swesmith/chunk_0/jobs/swesmith_chunk0_1775738964/s |
