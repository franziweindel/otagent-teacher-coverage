# 3-teacher combinations, OT-Agent data sources only

| teachers | exact tasks | exact trajectories | same-source tasks | same-source trajectories |
|---|---|---|---|---|
| GLM-4.6;GLM-4.7;GPT-5-nano | 15,840 | 24,843 | 17,022 (swesmith 10,010; superuser 6,015; tezos 997) | 28,466 |
| GLM-4.7;GPT-5.3-Codex;Kimi-2.5 | 5,641 | 15,186 | 6,326 (superuser 2,497; swesmith 2,372; issue 1,210; +1 more) | 19,730 |
| GLM-4.6;GLM-4.7;hosted_vllm/glm | 5,010 | 60,663 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 70,955 |
| GLM-4.6;GLM-4.7;GPT-5.3-Codex | 4,212 | 10,307 | 7,230 (superuser 2,500; swesmith 2,372; issue 2,111; +1 more) | 18,962 |
| GLM-4.7;GPT-5-nano;Kimi-2.5 | 3,530 | 5,784 | 13,504 (swesmith 10,010; superuser 2,497; tezos 997) | 25,004 |
| GLM-4.6;GLM-4.7;Kimi-2.5 | 3,445 | 9,509 | 23,468 (swesmith 10,895; tezos 8,866; superuser 2,497; +1 more) | 40,183 |
| GLM-4.6;GPT-5-nano;Kimi K2.0 Thinking | 2,981 | 2,981 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-4.6;GPT-5-nano;hosted_vllm/glm | 2,851 | 11,854 | 3,926 (superuser 1,855; swesmith 1,074; tezos 997) | 13,913 |
| GLM-4.7;GPT-5-nano;hosted_vllm/glm | 2,850 | 11,853 | 3,926 (superuser 1,855; swesmith 1,074; tezos 997) | 13,913 |
| GLM-4.7;GPT-5-nano;Kimi K2.0 Thinking | 2,750 | 2,750 | 3,019 (swesmith 3,019) | 3,385 |
| GPT-5-nano;GPT-5.3-Codex;Kimi-2.5 | 2,741 | 4,995 | 5,116 (superuser 2,497; swesmith 2,372; tezos 247) | 14,738 |
| GLM-4.7;GPT-5-nano;GPT-5.3-Codex | 2,740 | 4,994 | 5,119 (superuser 2,500; swesmith 2,372; tezos 247) | 14,744 |
| GLM-4.6;GLM-4.7;Kimi K2.0 Thinking | 2,715 | 2,862 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-4.6;GPT-5.3-Codex;Kimi-2.5 | 2,653 | 8,233 | 6,326 (superuser 2,497; swesmith 2,372; issue 1,210; +1 more) | 18,956 |
| GLM-4.6;GPT-5-nano;Kimi-2.5 | 2,610 | 4,863 | 13,504 (swesmith 10,010; superuser 2,497; tezos 997) | 25,004 |
| GLM-4.7;GLM-5.x;Kimi-2.5 | 2,233 | 4,324 | 17,187 (swesmith 10,993; superuser 2,497; tezos 2,487; +1 more) | 27,923 |
| GLM-4.7;GLM-5.x;GPT-5.3-Codex | 2,138 | 4,140 | 7,230 (superuser 2,500; swesmith 2,372; issue 2,111; +1 more) | 14,568 |
| GLM-5.x;GPT-5.3-Codex;Kimi-2.5 | 2,135 | 4,159 | 6,326 (superuser 2,497; swesmith 2,372; issue 1,210; +1 more) | 14,568 |
| GLM-4.6;GPT-5.3-Codex;hosted_vllm/glm | 2,028 | 7,218 | 4,262 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 10,885 |
| GLM-4.7;GPT-5.3-Codex;hosted_vllm/glm | 2,027 | 7,214 | 4,262 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 10,885 |
| GLM-4.7;Kimi-2.5;Kimi-2.6 | 1,956 | 2,937 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GPT-5-nano;GPT-5.3-Codex | 1,840 | 4,093 | 5,119 (superuser 2,500; swesmith 2,372; tezos 247) | 14,744 |
| GLM-4.6;Kimi-2.5;hosted_vllm/glm | 1,245 | 6,609 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 19,904 |
| GLM-4.7;Kimi-2.5;hosted_vllm/glm | 1,245 | 6,607 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 19,904 |
| GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 1,228 | 6,112 | 4,262 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 10,885 |
| GLM-4.6;GLM-4.7;GLM-5.x | 1,209 | 1,382 | 18,844 (swesmith 10,895; superuser 3,340; tezos 2,487; +1 more) | 26,776 |
| GLM-4.7;GLM-5.x;hosted_vllm/glm | 1,073 | 1,243 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 8,374 |
| GLM-4.6;GLM-5.x;hosted_vllm/glm | 1,073 | 1,244 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 8,374 |
| GPT-5-nano;Kimi-2.5;hosted_vllm/glm | 699 | 2,952 | 3,926 (superuser 1,855; swesmith 1,074; tezos 997) | 13,913 |
| GPT-5-nano;GPT-5.3-Codex;hosted_vllm/glm | 699 | 2,952 | 3,176 (superuser 1,855; swesmith 1,074; tezos 247) | 8,911 |
| GLM-4.7;GPT-5-nano;Kimi-2.6 | 481 | 481 | 1,974 (swesmith 1,974) | 4,661 |
| GPT-5-nano;Kimi-2.5;Kimi-2.6 | 478 | 478 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GLM-4.7;Kimi-2.6 | 463 | 529 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GPT-5-nano;Kimi-2.6 | 463 | 463 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;Kimi-2.5;Kimi-2.6 | 460 | 504 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GLM-5.x;Kimi-2.5 | 297 | 335 | 17,089 (swesmith 10,895; superuser 2,497; tezos 2,487; +1 more) | 26,776 |
| GLM-4.6;GLM-5.x;GPT-5.3-Codex | 284 | 319 | 7,230 (superuser 2,500; swesmith 2,372; issue 2,111; +1 more) | 14,568 |
| GLM-5.x;Kimi-2.5;hosted_vllm/glm | 268 | 306 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 8,374 |
| GLM-5.x;GPT-5.3-Codex;hosted_vllm/glm | 255 | 290 | 4,262 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 8,374 |
| GLM-4.7;Kimi K2.0 Thinking;Kimi-2.5 | 239 | 246 | 3,019 (swesmith 3,019) | 3,385 |
| GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5 | 239 | 239 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-4.6;Kimi K2.0 Thinking;Kimi-2.5 | 237 | 244 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-4.7;Kimi K2.0 Thinking;Kimi-2.6 | 144 | 147 | 1,974 (swesmith 1,974) | 3,385 |
| Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 144 | 146 | 1,974 (swesmith 1,974) | 3,385 |
| GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.6 | 144 | 144 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;Kimi K2.0 Thinking;Kimi-2.6 | 142 | 144 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-4.6;GLM-4.7;GLM-5.1 | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;hosted_vllm/glm | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GPT-5-nano | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5-nano;hosted_vllm/glm | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;hosted_vllm/glm | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GPT-5-nano | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5.3-Codex;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GPT-5.3-Codex | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5-nano;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GPT-5.3-Codex | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5.3-Codex;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5-nano;GPT-5.3-Codex | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;Kimi-2.5;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.x;GPT-5-nano | 3 | 3 | 14,347 (swesmith 10,010; superuser 3,340; tezos 997) | 15,838 |
| GLM-5.x;GPT-5-nano;Kimi-2.5 | 2 | 2 | 13,504 (swesmith 10,010; superuser 2,497; tezos 997) | 15,838 |
| GLM-5.x;GPT-5-nano;GPT-5.3-Codex | 2 | 2 | 5,119 (superuser 2,500; swesmith 2,372; tezos 247) | 10,574 |
| GLM-4.6;GLM-5.x;GPT-5-nano | 1 | 1 | 14,347 (swesmith 10,010; superuser 3,340; tezos 997) | 15,838 |
| GLM-5.x;GPT-5-nano;hosted_vllm/glm | 1 | 1 | 3,926 (superuser 1,855; swesmith 1,074; tezos 997) | 6,400 |
| GLM-4.7;GLM-5.x;Kimi K2.0 Thinking | 0 | 0 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-5.x;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-4.6;GLM-5.x;Kimi K2.0 Thinking | 0 | 0 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking | 0 | 0 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-4.6;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-4.7;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-4.6;GLM-5.x;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.7;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-5.x;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-5.x;GPT-5-nano;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.7;GLM-5.x;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-5.x;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GPT-5.3-Codex;Kimi-2.5;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GPT-5-nano;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-5.x;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GPT-5.3-Codex;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-5.x;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GPT-5.3-Codex;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GPT-5-nano;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GPT-5-nano;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.7;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-5.x;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-4.6;GLM-5.1;GLM-5.x | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;GPT-5.3-Codex | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;GPT-5-nano | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;Kimi-2.5 | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GLM-5.x | 0 | 0 | 35 (tezos 35) | 35 |
