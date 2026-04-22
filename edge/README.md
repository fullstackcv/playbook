# Edge Deployment

> Running CV models on devices that aren't in a data center. Four broad tiers: accelerated embedded (Jetson), general embedded (Pi), dedicated TPU (Coral), and mobile (phones).

> [!WARNING]
> **Hardware landscape changes quickly.** The specific board recommendations below reflect *today's practical defaults* (as of April 2026), not universal truths. New SKUs ship every quarter; prices and availability shift. Power budgets and model-class fit are more stable guidance than specific product picks. Verify current pricing and availability before committing to a BOM.

Edge deployment is where most CV products actually live. The constraints are different from server-side — you care about power, thermals, cost, and the specific accelerator more than raw FLOPs.

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Premium embedded (GPU-ish) | **Jetson Orin Nano Super** (2024, $249) | Strong ML performance in a 15W envelope |
| Budget embedded | **Raspberry Pi 5** (8GB) | General-purpose, larger ecosystem, OK CV performance |
| Dedicated TPU | **Google Coral USB/Dev Board** | Efficient INT8 inference; but check current availability |
| Mobile flagship | **iPhone + CoreML** | Best-in-class on-device ML in the consumer device category |

## Jetson — the embedded default

NVIDIA's embedded GPU line. The Orin Nano Super (launched Dec 2024) is the current sweet-spot board: 67 TOPS INT8, 8 GB RAM, 15W, $249. Runs TensorRT natively. Can execute most modern CV models including smaller VLMs.

Options in the Jetson family (roughly increasing power):
- **Jetson Nano** (original, 2019) — 472 GFLOPS FP16, 4 GB RAM. End-of-life; avoid for new work.
- **Jetson Orin Nano** (2023) — 40 TOPS INT8, 8 GB. Decent.
- **Jetson Orin Nano Super** (2024) — 67 TOPS INT8 via firmware boost, 8 GB, $249. **The current default for consumer / maker edge.**
- **Jetson Orin NX** — 100 TOPS, 8 or 16 GB. More expensive.
- **Jetson AGX Orin** — 275 TOPS, 32/64 GB. Premium.
- **Jetson Thor** (2025–2026) — ~2,070 FP4 TFLOPS (petaFLOP-class at the edge), ~7.5× Orin generation. Targeted at robotics / autonomous / industrial; expensive; overkill for most CV products. Verify current availability and pricing before committing.

Pick Jetson when:
- You're training or evaluating on an NVIDIA cluster and want the same model to run at the edge with TensorRT optimization.
- You need to run models larger than classical CV (small LLM, SAM, depth estimation) on the edge.
- Power budget is 10–25W.

## Raspberry Pi — the budget default

Not accelerated, just a decent ARM CPU. Pi 5 (8GB) is good enough for classical CV (Haar, HOG), small CNNs (YOLOv8n INT8 at ~10 FPS), and anything where the pipeline doesn't saturate the CPU.

Pick Pi when:
- Cost is critical ($80).
- Power is critical (~5W).
- The CV model is light or legacy.
- You don't need hardware ML acceleration.

Add a **Hailo M.2 accelerator** to turn a Pi 5 into a credible edge AI platform. Two variants sold as Pi 5 kits:
- **Hailo-8L** (standard AI Kit) — 13 TOPS, cheaper.
- **Hailo-8** (AI+ Kit) — 26 TOPS, premium.

Pi 5 + Hailo-8 is competitive with Jetson Orin Nano at similar cost; Pi 5 + Hailo-8L is cheaper but noticeably slower.

## Google Coral — the dedicated TPU

Coral USB Accelerator ($60) + Coral Dev Board. 4 TOPS INT8 on a tiny module. Runs TFLite-quantized models only.

Status: **uncertain in 2026.** Google announced no new Coral hardware since 2022, though the current products still ship. Treat Coral as a "mature, possibly slowly fading" option — fine for existing deployments, shaky for new commitments.

## Mobile — CoreML (iOS) and NNAPI / QNN (Android)

Phones are the highest-shipping-volume edge devices. Deploy CV models as part of an app:

- **iOS** → export to CoreML. Apple Neural Engine runs INT8/INT16 quantized models at very high efficiency.
- **Android** → export to TFLite or ONNX. TFLite runs on NNAPI (vendor-specific) or GPU delegate. Qualcomm QNN for Snapdragon-specific performance.

iPhone's Neural Engine is the strongest single-device mobile ML platform in 2026. If your product ships on iOS, CoreML is not optional.

## When to pick something else

- **Multi-camera office/retail** → an Intel NUC + small dGPU outperforms any embedded board at ~4× the price and 10× the compute. Different form factor.
- **Industrial / outdoor** → look at ruggedized boards (NVIDIA IGX Orin, specific industrial PC vendors). Jetson in an enclosure works but isn't ruggedized.
- **Low-power, always-on** → sub-watt vision SoC (e.g., Sony IMX500 sensor with in-sensor ML, Himax WE-I Plus). Specialized, not plug-and-play.
- **Existing browser-based product** → you're not really edge; you're web. Different section.

## The three questions to narrow

1. **Power budget?** < 5W → Pi. 5–15W → Jetson Orin Nano Super. 15W+ → Orin NX / AGX.
2. **Model family?** Classical CV / small CNN → Pi. Modern CNN / small transformer → Jetson Orin Nano Super. Large (SAM, VLM) → Orin NX / AGX or NUC+GPU.
3. **Ship volume?** Low (< 100 devices) → developer-friendly (Jetson, Pi). High (> 10K devices) → custom board design with specific SoC.

## The Dump

### Embedded boards
- **NVIDIA Jetson family** — Nano / Orin Nano / Orin Nano Super / Orin NX / AGX Orin.
- **Raspberry Pi 4 / 5** — general-purpose ARM. Pi 5 8GB is the usable baseline.
- **Orange Pi / Rock Pi / Banana Pi** — Rockchip-based Pi alternatives. Some (RK3588) have decent NPUs.
- **ASUS Tinker Board** — Rockchip-based. Less community.
- **BeagleBone AI-64** — TI-based. Niche.
- **NVIDIA IGX Orin** — industrial/medical hardened Jetson variant.
- **NVIDIA Thor (announced)** — next-gen auto/robotics.

### Accelerators
- **Hailo-8 / Hailo-10 M.2** — the winning Pi accelerator story. 26 / 40 TOPS.
- **Google Coral (USB + board)** — dedicated TPU. Aging.
- **Intel Neural Compute Stick 2** — USB accelerator. Discontinued; Intel shifted focus to iGPU.
- **Kneron KL720 / KL630** — dedicated SoC.
- **Gyrfalcon Lightspeeur** — niche.
- **Axelera Metis** — newer dedicated ML accelerator, interesting.

### Mobile / consumer
- **iPhone + CoreML / Neural Engine** — top of the consumer mobile class.
- **Android flagships + QNN (Qualcomm NPU)** — strong in Snapdragon 8 Gen 3+.
- **Google Pixel + Tensor chip** — Google's own mobile chip with TPU.

### Industrial / automotive
- **NVIDIA DRIVE Orin / Thor** — automotive.
- **Qualcomm Ride / Flex** — automotive.
- **Ambarella CV-family** — dashcam / auto / robotics vision SoCs.
- **Intel IGX Orin / NVIDIA IGX Orin** — medical-grade.

### Cameras with built-in compute
- **Luxonis OAK-D / OAK-1** — Intel Myriad X inside. Depth + detection in one device.
- **ReoLink / Reolink Duo smart cameras** — consumer CV cameras with basic on-device ML.
- **Sony IMX500** — sensor with ML inside. Niche but interesting.

### Software stacks
- **NVIDIA JetPack** — Jetson's SDK (CUDA, TensorRT, DeepStream, etc.).
- **NVIDIA DeepStream** — video pipeline + model serving for Jetson/servers.
- **Picamera2** — Raspberry Pi camera API.
- **libcamera** — cross-embedded camera library.
- **GStreamer** — media pipelines; the glue on most Linux embedded CV stacks.

## Graveyard

- **Jetson Nano (original 2019)** — end-of-life by NVIDIA. Avoid for new projects.
- **Movidius NCS / NCS2** — discontinued.
- **Intel Neural Compute Stick 2** — discontinued.
- **Coral TPU as a clearly-growing platform** — uncertain status.
- **Qualcomm Robotics RB3** — superseded by RB5, and attention moved to mobile SoCs.

## Last reviewed

2026-04-22.
