# Inference Runtimes

> How you actually execute a model in production. PyTorch is for training; runtimes are for serving.

A runtime is the software that loads your model, moves data in, runs the math, moves results out. You almost never ship PyTorch as your production inference path — it's too heavy, too loose with threads, too full of Python. You export to a runtime that's compiled, fast, and embeddable.

## Recommended picks

| Target | Pick | When to use |
|--------|------|-------------|
| **Default (cross-platform)** | **ONNX Runtime** | Anything not NVIDIA-specific or Apple-specific. CPU + GPU + mobile, all one runtime. |
| NVIDIA max performance | **TensorRT** | Squeeze last 30–50% out of NVIDIA GPUs. Worth it for high-volume production. |
| Apple ecosystem | **CoreML** | iOS / macOS / Vision Pro. Uses the Neural Engine automatically. |
| Intel CPU / iGPU | **OpenVINO** | Intel laptop/workstation targets. |
| Browser / JS | **ONNX Runtime Web** or **TensorFlow.js** | Client-side inference. |
| Mobile (non-Apple) | **TensorFlow Lite** / **LiteRT** | Android, embedded. |

## Why ONNX Runtime is the default

Microsoft's cross-platform inference runtime. Takes an `.onnx` model and runs it on CPU, NVIDIA GPU (via CUDA or TensorRT execution provider), AMD GPU (ROCm), Intel CPU/iGPU (OpenVINO EP), Apple (CoreML EP), ARM (NNAPI / XNNPack).

Pick it because:
- **One model format** (ONNX) across deploy targets.
- **Consistent API** across platforms.
- **Execution providers** let you target specific hardware without rewriting code.
- **Mature export** — PyTorch, TensorFlow, and most ML libraries have solid ONNX exporters.

Install: `pip install onnxruntime` (CPU) or `pip install onnxruntime-gpu` (with CUDA).

Recent additions (2026):
- **TensorRT RTX execution provider** — new EP targeting NVIDIA RTX-class GPUs.
- **OpenVINO EP memory optimization** — patch to reuse weight files across shared contexts, lowering resident memory.
- Hybrid strategy recommended: ONNX Runtime as the primary API, TensorRT EP for GPU paths, OpenVINO EP or default CPU EP for CPU-only nodes.

## When to pick something else

- **Max NVIDIA performance with static shapes** → TensorRT directly. ~30–50% faster than ONNX Runtime's TensorRT EP in practice because you can tune more aggressively.
- **Shipping an iOS app** → CoreML. The Neural Engine is *fast* and ONNX Runtime's CoreML EP doesn't always use it optimally.
- **Intel-only deploy, CPU-focused** → OpenVINO directly. Slightly better than ONNX Runtime's OpenVINO EP.
- **Browser-side inference** → ONNX Runtime Web works but payload sizes are chunky. TensorFlow.js has smaller models for basic tasks.
- **Embedded / microcontroller** → TensorFlow Lite Micro, or NXP/STM32 SDK-native. ONNX Runtime is too big.
- **Coral TPU** → TFLite only (Coral runs quantized TFLite specifically).

## The three questions to narrow

1. **What hardware?** NVIDIA → TensorRT or ONNX. Apple → CoreML. Intel → OpenVINO or ONNX. Browser → ONNX Web / TFJS. Mobile → TFLite / CoreML.
2. **How performance-sensitive?** Very → hardware-native runtime. Moderate → ONNX Runtime.
3. **How many deploy targets?** Many → ONNX Runtime (one format). Few → native runtime for each.

## Quantization — free performance

Once the runtime is picked, quantization is the next lever:

- **INT8** — post-training quantization. 4× memory reduction, typically 2–3× inference speedup. Minor accuracy loss (0.5–2 pp on typical CV tasks).
- **FP16** — half-precision. 2× memory, 1.5–2× speedup on GPUs with FP16 units. Almost no accuracy loss.
- **INT4 / INT2** — aggressive, emerging. Larger accuracy hits. Use for edge where you can tolerate it.

All the runtimes above support quantized models; the export tooling varies.

## The Dump

### Runtimes
- **ONNX Runtime (Microsoft)** — cross-platform. Default.
- **TensorRT (NVIDIA)** — NVIDIA-only, max performance. FP32/FP16/INT8/INT4.
- **CoreML (Apple)** — Apple Neural Engine + GPU + CPU.
- **OpenVINO (Intel)** — Intel CPU/iGPU/VPU.
- **TensorFlow Lite / LiteRT (Google)** — mobile, edge.
- **TensorFlow.js** — browser JS.
- **PyTorch Mobile / ExecuTorch** — PyTorch's mobile runtime. Smaller footprint for PyTorch-native models.
- **TorchScript / torch.compile** — in-process PyTorch compilation. Not a separate runtime; still PyTorch under the hood.
- **vLLM** — LLM-specific serving, not general CV.
- **Triton Inference Server (NVIDIA)** — multi-model serving on top of TensorRT / ONNX / PyTorch.
- **BentoML** — Python-first model serving framework.
- **NVIDIA DeepStream** — video pipeline + inference stack for NVIDIA devices.
- **Apple Vision framework** — higher-level Apple API on top of CoreML for common tasks.
- **Android NNAPI** — Android's neural network API.
- **Qualcomm QNN / SNPE** — Qualcomm mobile SoC runtimes.
- **MediaTek NeuroPilot** — MediaTek SoC runtime.
- **Rockchip RKNN** — Rockchip embedded SoC (Orange Pi, etc.).
- **Hexagon NPU** — Qualcomm DSP.
- **TVM / MLIR / IREE** — compile-your-own runtime stacks. Research-heavy, production-sparse.
- **GGML / llama.cpp** — originally LLM-only, increasingly covers multimodal. Runs on almost anything.

### Serving frameworks (wrappers around runtimes)
- **FastAPI + uvicorn** — bring your own model, your own routes. What most CV APIs look like.
- **Triton Inference Server** — production-grade multi-model serving.
- **BentoML** — Python-first, batteries included.
- **TorchServe** — PyTorch's official serving. Widely used.
- **KServe (Kubernetes)** — scales model serving on K8s.
- **Ray Serve** — for complex multi-model / multi-step pipelines.
- **vLLM** — LLM-specific.
- **SGLang** — LLM-specific serving.

### Export tools
- **torch.onnx.export** — PyTorch → ONNX.
- **onnxruntime-tools / Olive (Microsoft)** — optimization, quantization.
- **coremltools** — PyTorch/TensorFlow → CoreML.
- **tensorflow.lite.TFLiteConverter** — TF → TFLite.
- **openvino.tools.mo** — ONNX → OpenVINO IR.
- **TensorRT trtexec / polygraphy** — ONNX → TensorRT engine.

## Graveyard

- **Caffe / Caffe2** — retired.
- **MXNet** — AWS abandoned 2023.
- **Theano** — retired 2017.
- **Keras (standalone)** — subsumed into TensorFlow.
- **TensorFlow Serving as a default** — still around, but TorchServe / Triton / BentoML cover more ground.
- **PyTorch JIT / TorchScript as the primary production path** — mostly replaced by ONNX export + runtime, or PyTorch 2.x `torch.compile` + ExecuTorch.

## Last reviewed

2026-04-22.
