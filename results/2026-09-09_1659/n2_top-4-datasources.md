# 2-teacher combinations, OT-Agent data sources only

| teachers | exact tasks | exact trajectories | same-source tasks | same-source trajectories |
|---|---|---|---|---|
| GLM-4.7;GPT-5-nano | 20,103 | 29,079 | 20,982 (swesmith 10,007; superuser 9,981; tezos 994) | 29,958 |
| GLM-4.6;GLM-4.7 | 19,156 | 56,203 | 22,248 (swesmith 11,324; superuser 6,279; issue 2,523; +1 more) | 64,528 |
| GLM-4.6;GPT-5-nano | 16,685 | 25,661 | 17,280 (swesmith 10,007; superuser 6,279; tezos 994) | 26,781 |
| GLM-4.7;Kimi-2.5 | 9,693 | 12,159 | 18,098 (swesmith 13,301; superuser 2,497; issue 1,199; +1 more) | 24,995 |
| GLM-4.7;GLM-5.x | 8,801 | 8,803 | 24,109 (swesmith 16,829; superuser 3,340; tezos 1,981; +1 more) | 24,112 |
| GLM-4.7;GPT-5.3-Codex | 7,201 | 9,219 | 7,208 (superuser 2,500; swesmith 2,372; issue 2,090; +1 more) | 9,228 |
| GLM-4.7;hosted_vllm/glm | 6,261 | 10,590 | 8,168 (tezos 3,383; superuser 2,042; swesmith 1,479; +1 more) | 13,175 |
| GLM-4.6;hosted_vllm/glm | 5,830 | 10,833 | 6,907 (tezos 2,122; superuser 2,042; swesmith 1,479; +1 more) | 13,175 |
| GPT-5.3-Codex;Kimi-2.5 | 5,644 | 7,645 | 6,314 (superuser 2,497; swesmith 2,372; issue 1,199; +1 more) | 8,392 |
| GLM-4.6;GPT-5.3-Codex | 4,194 | 6,198 | 7,208 (superuser 2,500; swesmith 2,372; issue 2,090; +1 more) | 9,228 |
| GPT-5-nano;Kimi-2.5 | 3,532 | 5,548 | 13,498 (swesmith 10,007; superuser 2,497; tezos 994) | 15,783 |
| GLM-4.6;Kimi-2.5 | 3,445 | 5,721 | 16,121 (swesmith 11,324; superuser 2,497; issue 1,199; +1 more) | 23,137 |
| GPT-5-nano;Kimi K2.0 Thinking | 3,019 | 3,019 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.6;Kimi K2.0 Thinking | 2,981 | 2,981 | 3,019 (swesmith 3,019) | 3,019 |
| GPT-5-nano;hosted_vllm/glm | 2,848 | 6,434 | 4,515 (superuser 2,042; swesmith 1,479; tezos 994) | 11,255 |
| GLM-4.7;Kimi K2.0 Thinking | 2,750 | 2,750 | 3,019 (swesmith 3,019) | 3,019 |
| GPT-5-nano;GPT-5.3-Codex | 2,743 | 4,740 | 5,118 (superuser 2,500; swesmith 2,372; tezos 246) | 7,116 |
| GLM-5.x;Kimi-2.5 | 2,235 | 2,236 | 18,098 (swesmith 13,301; superuser 2,497; issue 1,199; +1 more) | 22,588 |
| GLM-5.x;GPT-5.3-Codex | 2,140 | 2,141 | 7,077 (superuser 2,500; swesmith 2,372; issue 1,959; +1 more) | 8,813 |
| GPT-5.3-Codex;hosted_vllm/glm | 2,009 | 2,856 | 5,031 (superuser 2,042; swesmith 1,479; issue 1,264; +1 more) | 8,428 |
| GLM-4.7;Kimi-2.6 | 1,974 | 2,101 | 3,304 (swesmith 3,304) | 6,002 |
| Kimi-2.5;Kimi-2.6 | 1,956 | 3,669 | 3,304 (swesmith 3,304) | 6,002 |
| Kimi-2.5;hosted_vllm/glm | 1,243 | 2,094 | 5,821 (superuser 2,042; swesmith 1,479; issue 1,199; +1 more) | 8,823 |
| GLM-4.6;GLM-5.x | 1,209 | 1,209 | 18,604 (swesmith 11,324; superuser 3,340; tezos 1,981; +1 more) | 23,363 |
| GLM-5.x;hosted_vllm/glm | 1,073 | 1,073 | 6,766 (superuser 2,042; tezos 1,981; swesmith 1,479; +1 more) | 8,166 |
| GPT-5-nano;Kimi-2.6 | 481 | 481 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-4.6;Kimi-2.6 | 463 | 513 | 3,304 (swesmith 3,304) | 6,002 |
| Kimi K2.0 Thinking;Kimi-2.5 | 239 | 239 | 3,019 (swesmith 3,019) | 3,019 |
| Kimi K2.0 Thinking;Kimi-2.6 | 144 | 144 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-5.1;hosted_vllm/glm | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1 | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1 | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5-nano | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-5.1;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5.3-Codex | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.x;GPT-5-nano | 2 | 2 | 14,341 (swesmith 10,007; superuser 3,340; tezos 994) | 15,329 |
| GLM-5.x;Kimi-2.6 | 0 | 0 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-5.x;Kimi K2.0 Thinking | 0 | 0 | 3,019 (swesmith 3,019) | 3,019 |
| GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GLM-5.1;GLM-5.x | 0 | 0 | 35 (tezos 35) | 35 |
