# 3-teacher combinations, OT-Agent data sources only

| teachers | exact task overlap | same-source overlap |
|---|---|---|
| GLM-4.6;GLM-4.7;GPT-5-nano | 13,021 | 14,266 (swesmith 10,005; superuser 4,018; tezos 243) |
| GLM-4.6;GPT-5-nano;Kimi K2.0 Thinking | 2,981 | 3,019 (swesmith 3,019) |
| GLM-4.7;GPT-5-nano;Kimi K2.0 Thinking | 2,750 | 3,019 (swesmith 3,019) |
| GLM-4.6;GLM-4.7;Kimi K2.0 Thinking | 2,715 | 3,019 (swesmith 3,019) |
| GLM-4.6;GLM-4.7;hosted_vllm/glm | 2,244 | 3,530 (tezos 1,529; superuser 987; issue 562; +1 more) |
| GLM-4.7;Kimi-2.5;Kimi-2.6 | 1,956 | 3,304 (swesmith 3,304) |
| GLM-4.7;GPT-5-nano;hosted_vllm/glm | 1,229 | 1,682 (superuser 987; swesmith 452; tezos 243) |
| GLM-4.6;GPT-5-nano;hosted_vllm/glm | 1,229 | 1,682 (superuser 987; swesmith 452; tezos 243) |
| GLM-4.7;GPT-5-nano;Kimi-2.5 | 792 | 10,248 (swesmith 10,005; tezos 243) |
| GLM-4.6;GLM-4.7;Kimi-2.5 | 772 | 12,239 (swesmith 10,187; tezos 2,052) |
| GLM-4.6;GPT-5-nano;Kimi-2.5 | 772 | 10,248 (swesmith 10,005; tezos 243) |
| GLM-4.6;GLM-4.7;GLM-5.x | 502 | 15,125 (swesmith 10,187; superuser 3,340; issue 1,598) |
| GLM-4.7;GPT-5-nano;Kimi-2.6 | 481 | 3,304 (swesmith 3,304) |
| GPT-5-nano;Kimi-2.5;Kimi-2.6 | 478 | 3,304 (swesmith 3,304) |
| GLM-4.6;GPT-5-nano;Kimi-2.6 | 463 | 3,304 (swesmith 3,304) |
| GLM-4.6;GLM-4.7;Kimi-2.6 | 463 | 3,304 (swesmith 3,304) |
| GLM-4.6;Kimi-2.5;Kimi-2.6 | 460 | 3,304 (swesmith 3,304) |
| GLM-4.7;GLM-5.x;hosted_vllm/glm | 452 | 2,001 (superuser 987; issue 562; swesmith 452) |
| GLM-4.6;GLM-5.x;hosted_vllm/glm | 452 | 2,001 (superuser 987; issue 562; swesmith 452) |
| GLM-4.7;Kimi K2.0 Thinking;Kimi-2.5 | 239 | 3,019 (swesmith 3,019) |
| GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.5 | 239 | 3,019 (swesmith 3,019) |
| GLM-4.6;Kimi K2.0 Thinking;Kimi-2.5 | 237 | 3,019 (swesmith 3,019) |
| Kimi K2.0 Thinking;Kimi-2.5;Kimi-2.6 | 144 | 3,019 (swesmith 3,019) |
| GPT-5-nano;Kimi K2.0 Thinking;Kimi-2.6 | 144 | 3,019 (swesmith 3,019) |
| GLM-4.7;Kimi K2.0 Thinking;Kimi-2.6 | 144 | 3,019 (swesmith 3,019) |
| GLM-4.6;Kimi K2.0 Thinking;Kimi-2.6 | 142 | 3,019 (swesmith 3,019) |
| GLM-4.7;GLM-5.1;GPT-5-nano | 10 | 10 (tezos 10) |
| GLM-4.6;GLM-5.1;GPT-5-nano | 10 | 10 (tezos 10) |
| GLM-5.1;GPT-5-nano;hosted_vllm/glm | 10 | 10 (tezos 10) |
| GLM-4.6;GLM-4.7;GLM-5.1 | 10 | 10 (tezos 10) |
| GLM-4.6;GLM-5.1;hosted_vllm/glm | 10 | 10 (tezos 10) |
| GLM-4.7;GLM-5.1;hosted_vllm/glm | 10 | 10 (tezos 10) |
| GLM-4.7;GLM-5.x;GPT-5-nano | 1 | 13,345 (swesmith 10,005; superuser 3,340) |
| GLM-4.6;GLM-5.x;GPT-5-nano | 0 | 13,345 (swesmith 10,005; superuser 3,340) |
| GLM-4.7;GLM-5.x;Kimi-2.5 | 0 | 10,827 (swesmith 10,827) |
| GLM-4.6;GLM-5.x;Kimi-2.5 | 0 | 10,187 (swesmith 10,187) |
| GLM-5.x;GPT-5-nano;Kimi-2.5 | 0 | 10,005 (swesmith 10,005) |
| GLM-5.0;GLM-5.x;Kimi-2.5 | 0 | 8,011 (swesmith 8,011) |
| GLM-4.6;GLM-4.7;GLM-5.0 | 0 | 8,011 (swesmith 8,011) |
| GLM-5.0;GLM-5.x;GPT-5-nano | 0 | 8,011 (swesmith 8,011) |
| GLM-4.7;GLM-5.0;Kimi-2.5 | 0 | 8,011 (swesmith 8,011) |
| GLM-4.6;GLM-5.0;GPT-5-nano | 0 | 8,011 (swesmith 8,011) |
| GLM-4.6;GLM-5.0;Kimi-2.5 | 0 | 8,011 (swesmith 8,011) |
| GLM-4.7;GLM-5.0;GPT-5-nano | 0 | 8,011 (swesmith 8,011) |
| GLM-4.6;GLM-5.0;GLM-5.x | 0 | 8,011 (swesmith 8,011) |
| GLM-4.7;GLM-5.0;GLM-5.x | 0 | 8,011 (swesmith 8,011) |
| GLM-5.0;GPT-5-nano;Kimi-2.5 | 0 | 8,011 (swesmith 8,011) |
| GLM-5.x;GPT-5-nano;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-5.0;GLM-5.x;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-5.x;Kimi-2.5;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-4.6;GLM-5.0;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-4.7;GLM-5.0;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-4.6;GLM-5.x;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-5.0;Kimi-2.5;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-5.0;GPT-5-nano;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-4.7;GLM-5.x;Kimi-2.6 | 0 | 3,304 (swesmith 3,304) |
| GLM-5.0;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 3,019 (swesmith 3,019) |
| GLM-4.6;GLM-5.0;Kimi K2.0 Thinking | 0 | 3,019 (swesmith 3,019) |
| GLM-5.0;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 3,019 (swesmith 3,019) |
| GLM-5.x;Kimi K2.0 Thinking;Kimi-2.6 | 0 | 3,019 (swesmith 3,019) |
| GLM-5.0;GPT-5-nano;Kimi K2.0 Thinking | 0 | 3,019 (swesmith 3,019) |
| GLM-4.7;GLM-5.x;Kimi K2.0 Thinking | 0 | 3,019 (swesmith 3,019) |
| GLM-5.x;Kimi K2.0 Thinking;Kimi-2.5 | 0 | 3,019 (swesmith 3,019) |
| GLM-5.0;GLM-5.x;Kimi K2.0 Thinking | 0 | 3,019 (swesmith 3,019) |
| GLM-4.6;GLM-5.x;Kimi K2.0 Thinking | 0 | 3,019 (swesmith 3,019) |
| GLM-5.x;GPT-5-nano;Kimi K2.0 Thinking | 0 | 3,019 (swesmith 3,019) |
| GLM-4.7;GLM-5.0;Kimi K2.0 Thinking | 0 | 3,019 (swesmith 3,019) |
| GLM-4.6;Kimi-2.5;hosted_vllm/glm | 0 | 1,981 (tezos 1,529; swesmith 452) |
| GLM-4.7;Kimi-2.5;hosted_vllm/glm | 0 | 1,981 (tezos 1,529; swesmith 452) |
| GLM-5.x;GPT-5-nano;hosted_vllm/glm | 0 | 1,439 (superuser 987; swesmith 452) |
| GPT-5-nano;Kimi-2.5;hosted_vllm/glm | 0 | 695 (swesmith 452; tezos 243) |
| GLM-4.6;Kimi-2.5;Qwen3 | 0 | 571 (tezos 571) |
| GLM-4.6;Qwen3;hosted_vllm/glm | 0 | 571 (tezos 571) |
| GLM-4.7;Qwen3;hosted_vllm/glm | 0 | 571 (tezos 571) |
| GLM-4.6;GLM-4.7;Qwen3 | 0 | 571 (tezos 571) |
| Kimi-2.5;Qwen3;hosted_vllm/glm | 0 | 571 (tezos 571) |
| GLM-4.7;Kimi-2.5;Qwen3 | 0 | 571 (tezos 571) |
| GLM-5.0;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| Kimi K2.0 Thinking;Kimi-2.5;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-4.7;GLM-5.0;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-5.x;Kimi-2.5;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-4.6;GLM-5.0;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| Kimi-2.5;Kimi-2.6;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-4.6;Kimi-2.6;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| Kimi K2.0 Thinking;Kimi-2.6;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-5.x;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GPT-5-nano;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-4.7;Kimi-2.6;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-5.0;GPT-5-nano;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-5.0;Kimi-2.6;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-5.x;Kimi-2.6;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GPT-5-nano;Kimi-2.6;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-4.6;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-5.0;GLM-5.x;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-5.0;Kimi-2.5;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GLM-4.7;Kimi K2.0 Thinking;hosted_vllm/glm | 0 | 452 (swesmith 452) |
| GPT-5-nano;Qwen3;hosted_vllm/glm | 0 | 243 (tezos 243) |
| GPT-5-nano;Kimi-2.5;Qwen3 | 0 | 243 (tezos 243) |
| GLM-4.7;GPT-5-nano;Qwen3 | 0 | 243 (tezos 243) |
| GLM-4.6;GPT-5-nano;Qwen3 | 0 | 243 (tezos 243) |
| GLM-4.6;GLM-5.1;Qwen3 | 0 | 10 (tezos 10) |
| GLM-4.7;GLM-5.1;Kimi-2.5 | 0 | 10 (tezos 10) |
| GLM-4.7;GLM-5.1;Qwen3 | 0 | 10 (tezos 10) |
| GLM-5.1;GPT-5-nano;Kimi-2.5 | 0 | 10 (tezos 10) |
| GLM-5.1;Qwen3;hosted_vllm/glm | 0 | 10 (tezos 10) |
| GLM-5.1;GPT-5-nano;Qwen3 | 0 | 10 (tezos 10) |
| GLM-5.1;Kimi-2.5;hosted_vllm/glm | 0 | 10 (tezos 10) |
| GLM-5.1;Kimi-2.5;Qwen3 | 0 | 10 (tezos 10) |
| GLM-4.6;GLM-5.1;Kimi-2.5 | 0 | 10 (tezos 10) |
