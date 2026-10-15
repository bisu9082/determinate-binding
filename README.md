# determinate-binding

Measurement archive for

> **A police robot proves where it is, not what it senses: an audited measurement of 1,014 authorising provisions**
> Janghyeon Cha, Myeongsik Shin, Boyeon Park, Inae Han, Ku Kang\*

Everything the paper reports is produced from the files here. Nothing is withheld.

## The question

Where does law make an authorisation depend on a **demonstrated property of the machine**?

A provision is called **determinately bound** when a determinate operator conditions it, unhedged,
on a named evaluation reached through the law's own cross-references within four hops.

## What the measurement says

| | |
|---|---|
| Instruments | 16 official machine-readable sources |
| Provision graph | 5,758 nodes · 8,834 edges |
| Authorising provisions | 1,014 |
| Returned by the predicate | 91 |
| Surviving the audit | **41** (precision 0.451 [0.352, 0.553]) |
| Aviation / ground binding rate | 10.8% / 2.5% |
| Surviving the police carve-out | **1** — 14 CFR §89.110(b), which binds *reported position*, not sensing |

## Layout

```
corpus/      16 instruments, each pinned by SHA-256 with its retrieval date
graph/       extractor, provision graph (nodes3/edges3), path predicate
probe/       lexicons: determinate operators, evaluation terms, hedges, penalties
frozen/      the frozen ruleset and its hash chain
stpa/        control structures and constraint registers
labels/      tpset.json — the 41 bindings. This is the canonical label set
audit/       the binding audit: all three label passes, the rubric, the records
classify/    permission-type classification: rubric, both blind passes, adjudication
verify/      measurement scripts and the consistency suite (gate.py)
fig2026/     figure scripts. They hold no numbers; they read verify/fig_measures.json
tex/         manuscript source
```

## Reproduce

```bash
pip install -r requirements.txt
sha256sum -c MANIFEST.sha256          # every file is pinned
python3 -I verify/fig_measures.py     # measurement -> verify/fig_measures.json
python3 -I fig2026/fig_concept.py     # figures, from the measurement only
python3 -I fig2026/fig_method.py
python3 -I fig2026/fig_results.py
python3 -I fig2026/fig_scope.py
cd tex && pdflatex main_v23 && bibtex main_v23 && pdflatex main_v23 && pdflatex main_v23
cd .. && python3 -I verify/gate.py    # the consistency suite
```

`verify/gate.py` exits 0 only if the manuscript, the tables, the figures and the typeset
output all agree with the measurement.

## On the three label sets

The audit was labelled three times. The counts on the binding value are **43, 26 and 41**.
The adopted set is the third pass, not an average. The first release of this work reported
**34**; the records published with it omitted the text of the provision a path arrived at, so the
adjudication could not be reproduced from them. The records here carry that text, and all three
label sets are in `audit/`.

**The labelling is not stable to the procedure that produces it.** The paper says so, and this
archive is where you check it.

## On the consistency suite

`verify/gate.py` was rebuilt after the original suite was lost, and it was built to close the
defect classes this project actually produced, not to restore a pass count. Its four design rules:

1. **No check takes its expected value from the thing it checks.** A figure-freshness check once
   compared against hashes the build script had just written, and could not fail.
2. **Every negative check is paired with a positive one.** "The superseded number is absent"
   passes the moment it is gone; it does not mean the replacement is right.
3. **Where a file has two copies, both are compared.** The back matter lived in three places and
   only one of them was typeset.
4. **The typeset PDF is read directly.** Three defects reached the manuscript that no check on
   the source files could see: every table printed twice, four superseded figures' text layer set
   as body prose, and the figures replaced by empty boxes on every build.

`REPRODUCIBILITY.md` states, gate by gate, what breaks it and what does not, and measures how low
the bar of one of them is. Appendix B of the paper carries the same measurement.

## Licence

Data and documentation CC BY 4.0; code additionally MIT. The instruments in `corpus/` are
official legal texts and are not covered by either — see `LICENSE` and `corpus/MANIFEST.json`.
