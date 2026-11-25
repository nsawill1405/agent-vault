---
title: Local inference
type: memory
updated: "2026-11-25"
tags:
  - memory
  - mlx
  - macos
---

# Local inference

Lessons from running local models on William's M4 Pro with 24 GB. William prefers MLX over `llama.cpp` on Apple Silicon (stated).

- A generic DFlash2 drafter paired with a ternary 2-bit model made decoding slower, from 22.9 to 15.6 tok/s. Ternary QAT drops draft acceptance, and stock 2-bit `quantized_matmul` re-reads the weights per verified row. Use the model's own bundled MTP head instead.
- For `prism-ml/Ternary-Bonsai-2.5-27B-mlx-2bit` on `mlx_vlm.server`, the fast setup was compiled Hadamard rotations, a 2-bit `simdgroup_matrix` verify kernel for 4 to 16 rows, the bundled `mtp/mtp-v2-head.safetensors`, `block_size = 2`, `prefer_requested_block_size = False` and `MLX_VLM_DRAFT_BLOCK_SIZE = 5`. That reached 25 to 35 tok/s in about 8 GiB.
- Tensors loaded on the main thread before `uvicorn.run` crash the first request with `There is no Stream(cpu, 0) in current thread`. Load them and call `mx.eval` inside the model loader on the worker thread.
- Set `APC_ENABLED=1` before importing `mlx_vlm.server.app` to turn on prefix caching across chat turns.

## Related

- [[Memory Index]]
