# ECE 3715 Final Project: Detection, Decision and Estimation

## Current status

Part I Steps 1 and 2 are implemented in `part1.ipynb`, with derivations,
Figure 1, analytic checks, and Monte Carlo verification using 1,000,000
samples per class. Steps 3-5, Part II, and the final report remain pending.

**Part II selection: Track A5 - Medical screening.** Planned scope: a synthetic
continuous biomarker model, ROC, positive predictive value versus disease
prevalence, and the 99% sensitivity / 99% specificity base-rate example.
These are illustrative probability models, with no clinical dataset selected.

## Team and contributions

Assignments are listed below; assigned work is not necessarily completed.

| Member | Current final-project responsibility |
| --- | --- |
| Christian Ruelas | Part I Steps 1, 2, and 4; initial detector helpers and Part I integration. Steps 1-2 completed; Step 4 pending. |
| Arun Nambiar | Part I Steps 3 and 5: ROC/AUC, `roc_curve_from_scores`, parameter-estimation experiments, figures, and interpretations. Pending. |
| Ibrahim Elsousi | Part II, Track A5: medical screening; `part2.ipynb`, model, derivation, simulations, figures, and limitations. Pending. |
| Everyone | Write report sections for their own work; review the report and validate the integrated submission. |

Christian retains Step 4 from the original proposed split. Arun should add his
sections to `part1.ipynb` and coordinate edits to `finallib.py` with Christian.
Ibrahim should build `part2.ipynb` and reuse the shared helpers where useful.
Coordinate notebook changes before merging; avoid simultaneous edits to the
same notebook. Each owner supplies their derivations, outputs, interpretations,
and report-ready figures with captions.

## Files and running

- `part1.ipynb`: current Part I notebook; restart kernel and run all cells.
- `finallib.py`: Gaussian likelihood ratio, centered linear discriminant,
  Q function, and empirical error rate. ROC helper will be added in Step 3.
- `figures/`: generated figures.
- `results/`: generated numerical tables and runtime record.
- `requirements.txt`: notebook dependencies.

From this folder, install with `python -m pip install -r requirements.txt`,
then open `part1.ipynb` with Jupyter or VS Code. No earlier project folder is
needed to run it. Tables and figures are refreshed by running the notebook.

## Reproducibility

Seed: **791607502**, drawn once in a scratch process on November 27, 2026
using `np.random.default_rng().integers(0, 2**31)` and then hard coded.
Do not draw a replacement seed.

Both parts initialize the same root generator in their setup cell. Part I
uses the first spawned child:

```python
rng = np.random.default_rng(SEED)
rng_part1 = rng.spawn(1)[0]
```

Ibrahim should use this setup in `part2.ipynb` so Part II uses the second
child and is independent of Part I:

```python
SEED = 791607502
rng = np.random.default_rng(SEED)
rng.spawn(1)  # reserve the child used by Part I; do not use it here
rng_part2 = rng.spawn(1)[0]
```

Part I uses its one child for all steps, with no reseeding below setup.
Rerunning an individual sampling cell advances that stream; restart and run
all cells to reproduce submitted outputs. Step 2 shares its observations
between detectors for a paired comparison. The standard error of each
equal-prior error estimate accounts for the separate fixed-size class samples.

## Remaining submission work

- Christian: Part I Step 4.
- Arun: Part I Steps 3 and 5 and `roc_curve_from_scores`.
- Ibrahim: Part II notebook with explicit model, derivation, simulation verification,
  trial counts, standard errors, and specific limitations.
- A separate 4-6 page `report.pdf`, including Track A5 in its abstract.
- Everyone: finish contribution records, clean-kernel execution, and complete runtimes
  (Part I under 5 minutes; Part II under 15 minutes or cache as specified).

Runtime for the implemented subset is recorded in `results/part1_runtime.json`;
it does not establish the runtime of the future complete Part I notebook.

## Validation of Steps 1-2

All four code cells executed in a fresh Jupyter kernel with saved outputs and
no execution errors. Recorded subset runtime: **14.09 seconds**. Figure 1 was
visually inspected. The general log-likelihood ratio agrees with SciPy log
densities to within 1.8e-15 on the deterministic equal/unequal-covariance checks.

| Detector | Analytic error | Monte Carlo error | Standard error |
| --- | --- | --- | --- |
| Optimal | 0.158655254 | 0.1584765 | 0.000258226 |
| Naive | 0.172352111 | 0.1720965 | 0.000266907 |

Each estimate uses 1,000,000 trials per class. Both are within one standard
error of theory. The naive rule makes 8.63% more errors than optimal;
equivalently, 7.95% of its errors are avoidable (different denominators).
Full numerical differences, class-conditional errors, intervals, and the
paired comparison are saved in `results/step2_*.csv`.
