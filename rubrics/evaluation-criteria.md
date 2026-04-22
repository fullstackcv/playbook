# Evaluation Criteria

A resource should not be Recommended only because it is popular, or because it has a strong benchmark number. "Recommended" in this playbook means *a senior CV engineer shipping a product would pick it first*. This page makes that judgment explicit.

## Primary criteria (heavy weight)

These matter most. A pick without strong marks here doesn't go in the top tier.

1. **Practical adoption in 2026 production systems.** Is this actually running in real products, or is it a research codebase with a strong paper?
2. **Maintenance status.** Has the project shipped a release in the last 6 months? Are open issues being triaged? Abandoned projects graveyard, however good they were once.
3. **Deployment ease.** Clear `pip install` / one-line Docker / clear ONNX export path. If getting it working is a two-week odyssey, it's not a recommended pick.
4. **Documentation quality.** Real tutorials and examples, not just a README with a PyPI badge.
5. **Ecosystem strength.** Integrations, community support, how many other tools assume its existence.

## Secondary criteria (tie-break weight)

These break ties between otherwise comparable picks.

6. **License clarity.** MIT / Apache 2 preferred. Restricted licenses (non-commercial, SSPL, custom) noted explicitly. Some picks might still be listed but with a license warning.
7. **Hardware friendliness.** Does it run on CPU + GPU + edge? Or GPU-only?
8. **Export paths.** ONNX, TensorRT, CoreML, TFLite availability.
9. **Training support.** Can the user fine-tune this easily if they need to?
10. **Benchmark relevance.** Strong on *realistic* benchmarks, not just on a single saturated academic one.
11. **Reproducibility.** If the paper claims X accuracy, does the public code reproduce X?

## Recommendation tiers

### Recommended (top 3 per section)

A pick that most senior engineers should reach for first given the tier's constraint. Each Recommended entry must include:
- A *why* — 1-3 sentences.
- A *when to avoid* — at least one concrete failure mode or unfit scenario.
- An install / try command or link.

### Alternatives (the Dump)

Everything else that's worth knowing. The Dump isn't curated — contributions welcome. Each entry has a one-line honest verdict. No marketing blurbs.

### Graveyard

Historically important, retired. Format:
- Name (year retired).
- Why it was the pick before.
- Why it's retired.

## Anti-criteria — things that should NOT influence tiering

- **Hype / social media visibility.** A project with 30K stars that shipped last in 2022 is still dead.
- **Single-benchmark wins.** A model that beats COCO by 0.5 AP at 3× the latency is research, not a production pick.
- **Author authority alone.** Even a famous lab's code gets unmaintained. Check the commits.
- **"It's what we used before."** Sunk cost is not a vote.

## How to disagree

If you think the rubric produced the wrong pick:
1. Open an issue with your counter-argument.
2. Name which criterion you think was misjudged.
3. Provide evidence.

Disagreements are welcome. Hand-wavy "I think X is better" is not.

## Last reviewed

2026-04-22.
