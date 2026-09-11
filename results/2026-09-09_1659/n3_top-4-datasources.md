# 3-teacher combinations, OT-Agent data sources only

| teachers | exact tasks | exact trajectories | same-source tasks | same-source trajectories |
|---|---|---|---|---|
| GLM-4.6;GLM-4.7;GPT-5-nano | 15,837 | 24,813 | 17,280 (swesmith 10,007; superuser 6,279; tezos 994) | 26,781 |
| GLM-4.7;GPT-5.3-Codex;Kimi-2.5 | 5,639 | 7,639 | 6,314 (superuser 2,497; swesmith 2,372; issue 1,199; +1 more) | 8,392 |
| GLM-4.6;GLM-4.7;hosted_vllm/glm | 4,989 | 9,318 | 6,907 (tezos 2,122; superuser 2,042; swesmith 1,479; +1 more) | 13,175 |
| GLM-4.6;GLM-4.7;GPT-5.3-Codex | 4,190 | 6,193 | 7,208 (superuser 2,500; swesmith 2,372; issue 2,090; +1 more) | 9,228 |
| GLM-4.7;GPT-5-nano;Kimi-2.5 | 3,529 | 5,545 | 13,498 (swesmith 10,007; superuser 2,497; tezos 994) | 15,783 |
| GLM-4.6;GLM-4.7;Kimi-2.5 | 3,443 | 5,646 | 16,121 (swesmith 11,324; superuser 2,497; issue 1,199; +1 more) | 23,137 |
| GLM-4.6;GPT-5-nano;Kimi K2.0 Thinking | 2,981 | 2,981 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.6;GPT-5-nano;hosted_vllm/glm | 2,848 | 6,434 | 4,515 (superuser 2,042; swesmith 1,479; tezos 994) | 11,255 |
| GLM-4.7;GPT-5-nano;hosted_vllm/glm | 2,847 | 6,433 | 4,515 (superuser 2,042; swesmith 1,479; tezos 994) | 11,255 |
| GLM-4.7;GPT-5-nano;Kimi K2.0 Thinking | 2,750 | 2,750 | 3,019 (swesmith 3,019) | 3,019 |
| GPT-5-nano;GPT-5.3-Codex;Kimi-2.5 | 2,740 | 4,736 | 5,115 (superuser 2,497; swesmith 2,372; tezos 246) | 7,113 |
| GLM-4.7;GPT-5-nano;GPT-5.3-Codex | 2,739 | 4,736 | 5,118 (superuser 2,500; swesmith 2,372; tezos 246) | 7,116 |
| GLM-4.6;GLM-4.7;Kimi K2.0 Thinking | 2,715 | 2,715 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.6;GPT-5.3-Codex;Kimi-2.5 | 2,651 | 4,648 | 6,314 (superuser 2,497; swesmith 2,372; issue 1,199; +1 more) | 8,392 |
| GLM-4.6;GPT-5-nano;Kimi-2.5 | 2,609 | 4,625 | 13,498 (swesmith 10,007; superuser 2,497; tezos 994) | 15,783 |
| GLM-4.7;GLM-5.x;Kimi-2.5 | 2,233 | 2,234 | 18,098 (swesmith 13,301; superuser 2,497; issue 1,199; +1 more) | 22,588 |
| GLM-4.7;GLM-5.x;GPT-5.3-Codex | 2,138 | 2,139 | 7,077 (superuser 2,500; swesmith 2,372; issue 1,959; +1 more) | 8,813 |
| GLM-5.x;GPT-5.3-Codex;Kimi-2.5 | 2,135 | 2,136 | 6,314 (superuser 2,497; swesmith 2,372; issue 1,199; +1 more) | 8,130 |
| GLM-4.6;GPT-5.3-Codex;hosted_vllm/glm | 2,009 | 2,856 | 5,031 (superuser 2,042; swesmith 1,479; issue 1,264; +1 more) | 8,428 |
| GLM-4.7;GPT-5.3-Codex;hosted_vllm/glm | 2,008 | 2,854 | 5,031 (superuser 2,042; swesmith 1,479; issue 1,264; +1 more) | 8,428 |
| GLM-4.7;Kimi-2.5;Kimi-2.6 | 1,956 | 2,065 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-4.6;GPT-5-nano;GPT-5.3-Codex | 1,839 | 3,836 | 5,118 (superuser 2,500; swesmith 2,372; tezos 246) | 7,116 |
| GLM-4.7;Kimi-2.5;hosted_vllm/glm | 1,243 | 2,093 | 5,821 (superuser 2,042; swesmith 1,479; issue 1,199; +1 more) | 8,823 |
| GLM-4.6;Kimi-2.5;hosted_vllm/glm | 1,243 | 2,094 | 5,821 (superuser 2,042; swesmith 1,479; issue 1,199; +1 more) | 8,823 |
| GPT-5.3-Codex;Kimi-2.5;hosted_vllm/glm | 1,226 | 2,069 | 4,966 (superuser 2,042; swesmith 1,479; issue 1,199; +1 more) | 7,787 |
| GLM-4.6;GLM-4.7;GLM-5.x | 1,209 | 1,209 | 18,604 (swesmith 11,324; superuser 3,340; tezos 1,981; +1 more) | 23,363 |
| GLM-4.7;GLM-5.x;hosted_vllm/glm | 1,073 | 1,073 | 6,766 (superuser 2,042; tezos 1,981; swesmith 1,479; +1 more) | 8,166 |
| GLM-4.6;GLM-5.x;hosted_vllm/glm | 1,073 | 1,073 | 6,766 (superuser 2,042; tezos 1,981; swesmith 1,479; +1 more) | 8,166 |
| GPT-5-nano;Kimi-2.5;hosted_vllm/glm | 698 | 1,541 | 4,515 (superuser 2,042; swesmith 1,479; tezos 994) | 7,544 |
| GPT-5-nano;GPT-5.3-Codex;hosted_vllm/glm | 698 | 1,541 | 3,767 (superuser 2,042; swesmith 1,479; tezos 246) | 6,508 |
| GLM-4.7;GPT-5-nano;Kimi-2.6 | 481 | 481 | 3,304 (swesmith 3,304) | 6,002 |
| GPT-5-nano;Kimi-2.5;Kimi-2.6 | 478 | 478 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-4.6;GLM-4.7;Kimi-2.6 | 463 | 467 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-4.6;GPT-5-nano;Kimi-2.6 | 463 | 463 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-4.6;Kimi-2.5;Kimi-2.6 | 460 | 493 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-4.6;GLM-5.x;Kimi-2.5 | 297 | 297 | 16,121 (swesmith 11,324; superuser 2,497; issue 1,199; +1 more) | 21,839 |
| GLM-4.6;GLM-5.x;GPT-5.3-Codex | 284 | 284 | 7,077 (superuser 2,500; swesmith 2,372; issue 1,959; +1 more) | 8,813 |
| GLM-5.x;Kimi-2.5;hosted_vllm/glm | 268 | 268 | 5,821 (superuser 2,042; swesmith 1,479; issue 1,199; +1 more) | 7,525 |
| GLM-5.x;GPT-5.3-Codex;hosted_vllm/glm | 255 | 255 | 5,031 (superuser 2,042; swesmith 1,479; issue 1,264; +1 more) | 8,166 |
| GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5 | 239 | 239 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.7;Kimi K2.0 Thinking;Kimi-2.5 | 239 | 239 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.6;Kimi K2.0 Thinking;Kimi-2.5 | 237 | 237 | 3,019 (swesmith 3,019) | 3,019 |
| GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.6 | 144 | 144 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.7;Kimi K2.0 Thinking;Kimi-2.6 | 144 | 144 | 3,019 (swesmith 3,019) | 3,019 |
| Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 144 | 144 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.6;Kimi K2.0 Thinking;Kimi-2.6 | 142 | 142 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.6;GLM-5.1;GPT-5-nano | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-4.7;GLM-5.1 | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;hosted_vllm/glm | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;hosted_vllm/glm | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5-nano;hosted_vllm/glm | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GPT-5-nano | 35 | 35 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5-nano;GPT-5.3-Codex | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5-nano;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;GPT-5.3-Codex | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GPT-5.3-Codex | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;Kimi-2.5;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.1;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5.3-Codex;Kimi-2.5 | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-5.1;GPT-5.3-Codex;hosted_vllm/glm | 11 | 11 | 35 (tezos 35) | 35 |
| GLM-4.7;GLM-5.x;GPT-5-nano | 2 | 2 | 14,341 (swesmith 10,007; superuser 3,340; tezos 994) | 15,329 |
| GLM-5.x;GPT-5-nano;Kimi-2.5 | 2 | 2 | 13,498 (swesmith 10,007; superuser 2,497; tezos 994) | 14,485 |
| GLM-5.x;GPT-5-nano;GPT-5.3-Codex | 2 | 2 | 5,118 (superuser 2,500; swesmith 2,372; tezos 246) | 6,854 |
| GLM-4.6;GLM-5.x;GPT-5-nano | 1 | 1 | 14,341 (swesmith 10,007; superuser 3,340; tezos 994) | 15,329 |
| GLM-5.x;GPT-5-nano;hosted_vllm/glm | 1 | 1 | 4,515 (superuser 2,042; swesmith 1,479; tezos 994) | 6,246 |
| GLM-4.7;GLM-5.x;Kimi-2.6 | 0 | 0 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-4.6;GLM-5.x;Kimi-2.6 | 0 | 0 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-5.x;GPT-5-nano;Kimi-2.6 | 0 | 0 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-5.x;Kimi-2.5;Kimi-2.6 | 0 | 0 | 3,304 (swesmith 3,304) | 6,002 |
| GLM-4.6;GLM-5.x;Kimi K2.0 Thinking | 0 | 0 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-4.7;GLM-5.x;Kimi K2.0 Thinking | 0 | 0 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-5.x;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking | 0 | 0 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-5.x;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 3,019 (swesmith 3,019) | 3,019 |
| GLM-5.x;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GLM-4.7;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GLM-4.7;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GLM-4.6;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GLM-5.x;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GPT-5-nano;GPT-5.3-Codex;Kimi-2.6 | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GPT-5.3-Codex;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GPT-5-nano;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GLM-4.6;GPT-5.3-Codex;Kimi K2.0 Thinking | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| GPT-5.3-Codex;Kimi-2.5;Kimi-2.6 | 0 | 0 | 2,372 (swesmith 2,372) | 2,373 |
| Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GPT-5-nano;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GLM-4.6;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GPT-5-nano;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GLM-5.x;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GPT-5.3-Codex;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GPT-5.3-Codex;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GLM-4.7;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GLM-4.7;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GLM-4.6;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GLM-5.x;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 0 | 1,479 (swesmith 1,479) | 2,026 |
| GLM-4.7;GLM-5.1;GLM-5.x | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-4.6;GLM-5.1;GLM-5.x | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;GPT-5.3-Codex | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;GPT-5-nano | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;Kimi-2.5 | 0 | 0 | 35 (tezos 35) | 35 |
| GLM-5.1;GLM-5.x;hosted_vllm/glm | 0 | 0 | 35 (tezos 35) | 35 |
