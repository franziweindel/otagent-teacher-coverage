# 6-teacher combinations, OT-Agent data sources only

| teachers | exact tasks | exact trajectories | same-source tasks | same-source trajectories |
|---|---|---|---|---|
| GLM-4.6;GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 699 | 2,952 | 3,176 (superuser 1,855; swesmith 1,074; tezos 247) | 8,911 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 255 | 290 | 4,262 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 8,374 |
| GLM-4.6;GLM-4.7;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 142 | 142 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.1;GPT-5-nano;Kimi-2.5;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1;GPT-5-nano;GPT-5.3-Codex;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5 | 1 | 1 | 5,116 (superuser 2,497; swesmith 2,372; tezos 247) | 10,574 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;Kimi-2.5;hosted_vllm/glm | 1 | 1 | 3,926 (superuser 1,855; swesmith 1,074; tezos 997) | 6,400 |
| GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 1 | 1 | 3,176 (superuser 1,855; swesmith 1,074; tezos 247) | 6,400 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;hosted_vllm/glm | 1 | 1 | 3,176 (superuser 1,855; swesmith 1,074; tezos 247) | 6,400 |
| GLM-4.6;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 1 | 1 | 3,176 (superuser 1,855; swesmith 1,074; tezos 247) | 6,400 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-4.6;GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-4.6;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-4.6;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GLM-4.7;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.x;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.7;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;GPT-5-nano;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GLM-5.x;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GPT-5-nano;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GLM-5.x;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GLM-5.x;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;GPT-5.3-Codex;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.x;GPT-5-nano;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GPT-5-nano;GPT-5.3-Codex;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-4.7;GLM-5.1;GLM-5.x;GPT-5.3-Codex;Kimi-2.5 | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GLM-5.x;GPT-5-nano;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1;GLM-5.x;GPT-5-nano;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5 | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1;GLM-5.x;GPT-5-nano;Kimi-2.5 | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GLM-5.x;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1;GLM-5.x;GPT-5-nano;GPT-5.3-Codex | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GLM-5.x;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GLM-5.x;GPT-5-nano;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5 | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1;GLM-5.x;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1;GLM-5.x;GPT-5.3-Codex;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;GPT-5-nano;GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
