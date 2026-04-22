# The LLM-refresh idea (sketch, not implemented)

The long-term plan for this playbook: keep the **Dump** as the ground truth, and regenerate the **Recommended picks** periodically by running the Dump through an LLM with a curation prompt.

This page describes the approach. No code yet — contributions welcome.

## The shape

Each section's README has two parts:
1. **Recommended picks** — a short table with 3 picks + when-to-pick + when-to-avoid.
2. **The Dump** — the exhaustive list.

The Dump is human-maintained. Anyone can add an entry via PR. No curation gate on the Dump.

The Recommended picks are currently also human-maintained. That's the part we want to automate (partially).

## The pipeline

```
for each section:
    dump = read Dump markdown
    criteria = read rubrics/evaluation-criteria.md
    previous_picks = read Recommended markdown
    last_reviewed_date = extracted from frontmatter
    
    prompt = f"""
        Given:
        - the evaluation criteria (primary: adoption, maintenance, deployment; 
          secondary: license, docs, ecosystem)
        - the full dump of options for this subtask
        - the previous picks (so you can note if they rotate)
        - the previous review date
        
        Produce:
        - 3 picks (default, edge/low-end, max-accuracy, OR an axis that makes sense for this subtask)
        - Each with a why / when-to-pick / when-to-avoid / install command
        - A Graveyard section for anything that was a pick before but isn't now
        - A last-reviewed date (today)
    """
    
    new_picks_markdown = llm(prompt)
    write_to_file(section, new_picks_markdown)
    open PR with the diff
```

## Why a PR and not direct commit

The LLM's picks need human review. It will occasionally:
- Pick something that's marketed well but not actually deployed.
- Miss a nuance that a maintainer knows (licensing trap, model-weights availability).
- Rotate a pick out that should have stayed.

The PR gives the maintainer a chance to veto or refine before merge.

## Cadence

- **Slow-moving sections** (face detection, face alignment, face recognition): every 6 months.
- **Medium sections** (object detection, segmentation, OCR): every 3 months.
- **Fast-moving sections** (VLM, generation): every month.

## The prompt (draft)

```
You are curating the Recommended picks for the {section} page of a CV playbook.
The audience is senior CV engineers shipping products, not researchers.

Criteria, in order of weight:
1. Practical deployment evidence in 2026 production systems.
2. Maintenance status — actively developed in the last 6 months.
3. Ecosystem — easy installation, good docs, lots of examples.
4. License clarity — prefer permissive (MIT/Apache) over restricted.
5. Accuracy/speed tradeoff on realistic hardware.

Axes for the 3 picks (pick the axis that fits the subtask):
- For general models: default / edge or low-end / max accuracy.
- For face-specific pipelines: clean input / surveillance / edge.
- For models with a commercial/open split: commercial flagship / open default / edge.

Each pick must include:
- Name with link.
- Why this pick.
- When to avoid (at least one concrete failure mode).
- One-line install/try command.

If the previous picks are still correct, note that and move on.
If a previous pick rotates out, add it to the Graveyard with a brief "retired for X" note.

Output in exactly the markdown template at templates/section-template.md.

Dump follows below:
---
{dump_markdown}
---
```

## Open problems

- **LLM hallucination about package status** — the LLM might confidently say a pick is "the 2026 default" when it hasn't shipped a release in a year. Mitigation: cross-check with PyPI / GitHub release dates programmatically.
- **Benchmark quoting** — the LLM will sometimes invent numbers. Mitigation: either suppress numeric claims or require a citation.
- **License drift** — licenses change. Mitigation: re-check license on each refresh.
- **Cost** — running 14 sections through a flagship VLM / LLM every quarter is a few dollars. Not a blocker, but noted.

## When this ships

No timeline. The hand-curated v1 is the priority; automation is a nice-to-have for when the repo has enough contributions in the Dump to make curation bandwidth the bottleneck.

---

*Sketch by Vikas Gupta. If you want to implement this, open an issue first — the template and criteria will likely evolve.*
