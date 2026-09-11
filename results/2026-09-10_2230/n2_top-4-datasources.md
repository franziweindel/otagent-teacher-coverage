# 2-teacher combinations, OT-Agent data sources only

| teachers | exact tasks | exact trajectories | same-source tasks | same-source trajectories |
|---|---|---|---|---|
| GLM-4.7;GPT-5-nano | 20,111 | 29,116 | 20,990 (swesmith 10,010; superuser 9,983; tezos 997) | 29,995 |
| GLM-4.6;GLM-4.7 | 19,180 | 80,359 | 30,029 (tezos 10,997; swesmith 10,895; superuser 6,015; +1 more) | 94,696 |
| GLM-4.6;GPT-5-nano | 16,688 | 25,691 | 17,022 (swesmith 10,010; superuser 6,015; tezos 997) | 28,466 |
| GLM-4.7;Kimi-2.5 | 9,705 | 25,359 | 23,566 (swesmith 10,993; tezos 8,866; superuser 2,497; +1 more) | 42,108 |
| GLM-4.7;GLM-5.x | 9,076 | 17,116 | 26,925 (swesmith 17,104; issue 3,994; superuser 3,340; +1 more) | 35,126 |
| GLM-4.7;GPT-5.3-Codex | 7,223 | 18,935 | 7,230 (superuser 2,500; swesmith 2,372; issue 2,111; +1 more) | 19,736 |
| GPT-5.3-Codex;Kimi-2.5 | 5,646 | 15,978 | 6,326 (superuser 2,497; swesmith 2,372; issue 1,210; +1 more) | 19,730 |
| GLM-4.6;hosted_vllm/glm | 5,012 | 60,950 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 70,955 |
| GLM-4.7;hosted_vllm/glm | 5,010 | 521,887 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 547,625 |
| GLM-4.6;GPT-5.3-Codex | 4,216 | 10,483 | 7,230 (superuser 2,500; swesmith 2,372; issue 2,111; +1 more) | 18,962 |
| GPT-5-nano;Kimi-2.5 | 3,533 | 5,787 | 13,504 (swesmith 10,010; superuser 2,497; tezos 997) | 25,004 |
| GLM-4.6;Kimi-2.5 | 3,447 | 9,685 | 23,468 (swesmith 10,895; tezos 8,866; superuser 2,497; +1 more) | 40,183 |
| GPT-5-nano;Kimi K2.0 Thinking | 3,019 | 3,019 | 3,019 (swesmith 3,019) | 3,385 |
| GLM-4.6;Kimi K2.0 Thinking | 2,981 | 3,244 | 3,019 (swesmith 3,019) | 3,385 |
| GPT-5-nano;hosted_vllm/glm | 2,851 | 11,854 | 3,926 (superuser 1,855; swesmith 1,074; tezos 997) | 13,913 |
| GLM-4.7;Kimi K2.0 Thinking | 2,750 | 2,952 | 3,019 (swesmith 3,019) | 3,385 |
| GPT-5-nano;GPT-5.3-Codex | 2,744 | 4,998 | 5,119 (superuser 2,500; swesmith 2,372; tezos 247) | 14,744 |
| GLM-5.x;Kimi-2.5 | 2,235 | 4,354 | 17,187 (swesmith 10,993; superuser 2,497; tezos 2,487; +1 more) | 27,923 |
| GLM-5.x;GPT-5.3-Codex | 2,140 | 4,169 | 7,230 (superuser 2,500; swesmith 2,372; issue 2,111; +1 more) | 14,568 |
| GPT-5.3-Codex;hosted_vllm/glm | 2,028 | 7,218 | 4,262 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 10,885 |
| GLM-4.7;Kimi-2.6 | 1,974 | 3,402 | 1,974 (swesmith 1,974) | 4,661 |
| Kimi-2.5;Kimi-2.6 | 1,956 | 3,669 | 1,974 (swesmith 1,974) | 4,661 |
| Kimi-2.5;hosted_vllm/glm | 1,245 | 6,609 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 19,904 |
| GLM-4.6;GLM-5.x | 1,209 | 1,383 | 18,844 (swesmith 10,895; superuser 3,340; tezos 2,487; +1 more) | 26,776 |
| GLM-5.x;hosted_vllm/glm | 1,073 | 1,244 | 5,012 (superuser 1,855; issue 1,086; swesmith 1,074; +1 more) | 8,374 |
| GPT-5-nano;Kimi-2.6 | 481 | 481 | 1,974 (swesmith 1,974) | 4,661 |
| GLM-4.6;Kimi-2.6 | 463 | 531 | 1,974 (swesmith 1,974) | 4,661 |
| Kimi K2.0 Thinking;Kimi-2.5 | 239 | 246 | 3,019 (swesmith 3,019) | 3,385 |
| Kimi K2.0 Thinking;Kimi-2.6 | 144 | 147 | 1,974 (swesmith 1,974) | 3,385 |
| GLM-5.1;GPT-5-nano | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1 | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1 | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-5.1;hosted_vllm/glm | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-5.1;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5.3-Codex | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.x;GPT-5-nano | 3 | 3 | 14,347 (swesmith 10,010; superuser 3,340; tezos 997) | 15,838 |
| GLM-5.x;Kimi K2.0 Thinking | 0 | 0 | 3,019 (swesmith 3,019) | 3,385 |
| GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 3,385 |
| GLM-5.x;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 1,974 (swesmith 1,974) | 4,661 |
| Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,074 (swesmith 1,074) | 1,772 |
| GLM-5.1;GLM-5.x | 0 | 0 | 35 (tezos 35) | 35 |
