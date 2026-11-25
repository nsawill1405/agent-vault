---
title: MLX speculative decoding for Ternary Bonsai 2.5 27B
type: memory
outcome: worked
updated: "2026-11-25"
tags:
  - memory
  - mlx
  - macos
---

# MLX speculative decoding for Ternary Bonsai 2.5 27B

Run `prism-ml/Ternary-Bonsai-2.5-27B-mlx-2bit` on Apple Silicon through `mlx_vlm.server` with compiled Hadamard rotations, a 2-bit `simdgroup_matrix` Metal verify kernel for 4 to 16 rows, OrcaRouter's 129-site runtime refusal projection, and the bundled v2 MTP drafter on adaptive block sizes 2 to 5.

## Scenario

Serving OrcaRouter Ternary Bonsai 2.5 27B Uncensored locally on an Apple M4 Pro with 24 GB unified memory at maximum throughput for Atomic Chat.

## What failed

1. Pairing `incoai/Qwen3.8-27B-DFlash2` with the ternary Bonsai 2.5 pack dropped generation speed from 22.9 tok/s to 15.6 tok/s on chat and 20.8 tok/s on code. Bonsai 2.5's post-training and ternary QAT lowered DFlash2 acceptance to 1.9 to 3.2 tokens, while stock MLX 2-bit `quantized_matmul` re-read the 7 GB weights per verified row.
2. Loading the refusal direction tensor on the main Python thread before `uvicorn.run` crashed the first `mlx_vlm.server` request with `RuntimeError: There is no Stream(cpu, 0) in current thread` inside `mx.async_eval`. Lazy `mx.load` and `reshape` graphs captured the main thread's CPU stream, which does not exist on `ResponseGenerator`'s worker thread.

## What worked

1. Compiling the signed Walsh-Hadamard transform and fusing the FP32 refusal projection `y - alpha * (y . r) * r` into the 129 residual writers lifted plain MLX decode from 15.9 tok/s to 22.6 tok/s.
2. Adding a 2-bit `simdgroup_matrix` Metal kernel for batch widths 4 to 16 cut verify matmul latency by 1.7x to 2.1x on the 27B linear shapes and `lm_head`.
3. Using PrismML's bundled `mtp/mtp-v2-head.safetensors` with its 3 residual writers also runtime-ablated, `block_size = 2`, `prefer_requested_block_size = False`, and `MLX_VLM_DRAFT_BLOCK_SIZE = 5` gave 24.9 tok/s on chat, 30.0 tok/s on code, and 35.4 tok/s on math in 8.21 GiB active GPU memory.
4. Initializing `mx.default_stream(mx.cpu)` and calling `mx.eval` on the direction and Hadamard sign tensors inside `load_model_resources` on the worker thread eliminated the cross-thread stream error. Setting `APC_ENABLED=1` before importing `mlx_vlm.server.app` turned on automatic prefix caching across multi-turn chats.

## Related

- [[Memory Index]]
- [[Workflow Preferences]]
- [[Coding Principles]]
