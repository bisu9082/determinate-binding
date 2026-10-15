# Reproducibility: what each gate covers, and what it does not

Referenced from the Data availability statement and from Appendix B of the manuscript.

It exists because a pass count is not evidence of coverage. Three times in this project a gate
was repaired into a state in which it could not fail and went on reporting full passes. For each
gate below we state what breaks it, what does not, and the measured size of the gap where we
have measured it.

The suite in this archive is **not** the suite the first version of this paper described. That one,
523 checks in eleven or twelve gates depending on which paragraph you read, was lost with the
working tree and is not recovered. What runs here was rebuilt to close the defect classes this
project actually produced. The rebuild is smaller and we report its real size.

## Run it

```
pip install -r requirements.txt
sha256sum -c MANIFEST.sha256
python3 -I verify/fig_measures.py
python3 -I fig2026/fig_concept.py && python3 -I fig2026/fig_method.py
python3 -I fig2026/fig_results.py && python3 -I fig2026/fig_scope.py
cd tex && pdflatex main_v23 && bibtex main_v23 && pdflatex main_v23 && pdflatex main_v23 && cd ..
python3 -I verify/gate.py
```

Exit code 0 only if every check passes. There is no partial-pass report.

141 checks in eleven gates. Run from inside this archive, the 30 archive checks are skipped
and reported as skipped; the other 111 run.

## Four design rules

1. **No check takes its expected value from the thing it checks.** Expected values come from the
   measurement (`labels/tpset.json`, `graph/`) or from the freeze record, never from what the
   build writes. This rule exists because a figure-freshness check once compared against hashes
   that the build script had written moments earlier, inside the same run, and so could not fail.
2. **Every negative check is paired with a positive one.** "The superseded number is absent"
   passes as soon as it is gone. It passed while the manuscript carried a corrected numerator and
   the uncorrected p-value computed from the old one.
3. **Where a file has two copies, both are compared.** The back matter existed in three places
   and only one was typeset. Two of them were corrected and the printed page did not change.
4. **The typeset PDF is read directly.** Three defects reached the manuscript that no check on
   the source files could see.

## The gates

### GATE 1 — Integrity (8 checks)
The label set, the audit records, the classification and `verify/fig_measures.json` all describe
the same 41 provisions and the same 1,014 authorising provisions.
**Breaks it:** editing `labels/tpset.json` without re-running `verify/fig_measures.py`; a
classification record for a provision that is not a binding.
**Does not break it:** a wrong label. This gate checks that the artefacts agree, not that they
are right. Nothing in this suite can check that a label is right.

### GATE 2 — Table arithmetic (11 checks)
Every integer column with a Total row must sum to it, and Table 1's authorising column must
equal the count the graph produces for each instrument.
**Breaks it:** a table edited by hand; a per-instrument count that drifts from the graph.
**Measured gap:** this gate found that Table 1's authorising column summed to 1,019 against its
own Total row of 1,014, and located the difference in two instruments (US107 35→33, US89 20→17)
where a paragraph-node repair had reduced the denominator and the table was never updated.
**Documented exception:** Table 4's corrected authorising counts are not additive. The gate
exempts that column only because the caption says so *and* names both numbers (508 and 501); an
undocumented mismatch fails.

### GATE 3 — Negative: superseded numbers are absent (12 checks)
Twelve superseded values must not appear in the manuscript.
**Breaks it:** a reverted edit.
**Does not break it:** a superseded value this list does not name. The list was hand-written and
leaked four times. It is kept because it is cheap, not because it is sufficient; GATE 4 is what
makes the pair informative.
**Registered history:** three sites legitimately print a superseded number (the before column of
the ten-changes table, a per-change delta, and the paragraph that discloses the re-adjudication).
Each is registered with a reason. The registry is printed on every run.

### GATE 4 — Positive: current measured values are present (16 checks)
Sixteen quantities recomputed from the label set must appear in the manuscript, including the
English cardinals that carry the classification counts.
**Breaks it:** changing a count and leaving a statistic computed from it; changing a count and
leaving the word ("Thirty-five of the 41").
**Does not break it:** a current value that appears somewhere other than where it belongs.

### GATE 5 — Typeset duplication (20 checks)
Reads the PDF text layer. No table may be printed twice, each back-matter section exactly once,
and no superseded figure's text layer may appear as prose.
**Measured gap:** this gate found 71 paragraphs of table echo, 91 paragraphs of superseded figure
text set as body prose, and a back matter printed twice. Together, 28 per cent of the recovered
paragraph stream was typesetting noise.

### GATE 6 — Copy divergence (3 checks)
Where the same text exists in more than one file, exactly one must be the one that is typeset,
and the others must not carry a divergent copy.
**Does not break it:** two copies that agree. The gate catches divergence, not duplication of
content; GATE 5 catches duplication in the output.

### GATE 7 — Figure provenance (12 checks)
No figure script may contain a measured value as a literal, each must read
`verify/fig_measures.json`, and none may read the label set directly.
**Does not break it:** a layout constant that happens to equal a measured value. Lines that call
axis and style helpers are excluded from the scan, so a measured value smuggled into a tick list
would not be seen.

### GATE 8 — Build (10 checks)
Zero LaTeX errors, zero undefined citations or references, zero missing figures, zero em-dashes,
no placeholder box in the output, four figures typeset, no unregistered placeholder in the source.
**Measured gap:** "zero missing figures" passed for several builds while all four figures were
empty placeholder boxes, because the assembler drew a box instead of requesting a file. The
check that catches it reads the PDF for the box's text.

### GATE 9 — Disclosure obligations (11 checks)
The AI-use declaration must name all four uses; the data availability statement must name all
three label passes; the disclaimer must name exactly the institutions that appear as author
affiliations, in both directions; the re-adjudication and the labelling instability must be
stated in the body.
**Measured gap:** the disclaimer named an institution no author belonged to, and then, after it
was corrected, stopped naming one that an author did belong to. The gate now derives the required
set from the `\address` labels rather than from a fixed list.

### GATE 10 — Self-description (8 checks)
The manuscript's statements about its own apparatus must match the apparatus: the number of
checks, the number of gates, the vocabulary-saturation figures, the repository URL, and the
absence of a deposit promise this archive does not keep.
**Measured gap:** the data availability statement promised 523 checks in twelve gates while
Appendix B, in the same manuscript, said eleven. Neither matched anything that existed.

### GATE 11 — The archive (30 checks)
Every directory and metadata file the data availability statement promises must be present, the
manifest must cover every file, the compiled PDF must *not* be present, `CITATION.cff` must name
all five authors, `CITATION.cff` must carry the commit pin the data availability statement
promises, and `REPRODUCIBILITY.md` must carry the vocabulary-saturation figures that
`verify/vocab_saturation.json` produces.
**Skipped, not failed, when the suite is run from inside the archive**, where there is no
`release/` directory. The checks are still counted, so the total the manuscript states is the
size of the apparatus and not the size of one run.

## The provenance gate's own weakness, measured

The check that every measured quantity in the manuscript appears in a released output compares
**values, not provenance**. `verify/vocab_saturation.py` measures how low that bar is by building
the vocabulary the way the check does — every number in every released output, rounded to one,
two and three decimals, with proportions converted to percentages — and counting how many of the
possible decimals between 0 and 1 it already holds.

| precision | possible | already in the vocabulary |
|---|---|---|
| one decimal | 10 | **10** |
| two decimals | 100 | **54** |
| three decimals | 1,000 | **75** |

**At one decimal place the vocabulary is saturated and the check cannot fail.** At two places a
value has to clear a bar that about half the possible values do not clear. At three places the
bar is real.

These counts are a re-measurement. The script that produced the figures an earlier version
printed (9, 63 and 128) was lost, and this reimplementation, written from the manuscript's own
description, does not reproduce them. The counts above are the ones the paper now stands on, and
GATE 10 fails if the paper and `verify/vocab_saturation.json` disagree. The direction of the
correction is against us at one decimal place, where the earlier figure implied a bar that does
not exist.

## What no gate here tests

That a label is right. That the corpus is the right corpus. That the predicate is the right
predicate. That the sixteen instruments are the sixteen that matter. Section 4.6 of the paper is
about those, and no apparatus in this archive speaks to them.
