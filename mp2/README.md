# ECE 3715 Mini-Project 2

## Continuous Random Variables

This repository contains Mini-Project 2 for **ECE 3715 — Probability and Statistics**.

The project studies continuous random variables through densities, cumulative distribution functions, inverse-transform sampling, moments, and the central limit theorem, then applies these ideas to signal detection in noise. The notebook currently covers Steps 1–4.

## Team Members and Contributions

- **Christian Ruelas** — Steps 1, 2 & 4: From CDF to Density / Inverse-Transform Sampling / Expectation and Moments; implemented `inv_cdf_exponential()`, `inv_cdf_rayleigh()`, `sample_by_inversion()`, and `ks_statistic()`
- **Arun Nambiar** — Steps 3 & 5: A Function of a Random Variable / The Central Limit Theorem; derives and simulates transformed distributions and measures convergence of standardized sums to the Gaussian.
- **Ibrahim Elsousi** — Steps 6, 7 & 8: Gaussian Threshold Detection / Envelope Detection and Noise Mismatch / Choosing the Operating Point; implements `q_function()` and analyzes detection thresholds, ROC curves, noise uncertainty, and operating-point tradeoffs.
- **Everyone** — Planned extra-credit work: Bonus A (Characteristic Functions) and Bonus B (A Distribution with No Mean); final notebook integration, README, testing, and cleanup

## Repository Contents

```text
mp2/
├── mp2.ipynb
├── mp2lib.py
├── README.md
├── requirements.txt
├── figures/
└── ECE3715_MP2.pdf
```

- **`mp2.ipynb`** — Main Jupyter notebook. Currently runs Steps 1–4 with saved figures, tables, and interpretations.
- **`mp2lib.py`** — Helper functions implemented so far: `inv_cdf_exponential(u, lam)`, `inv_cdf_rayleigh(u, sigma)`, `sample_by_inversion(inv_cdf, n, rng, **kw)`, and `ks_statistic(samples, cdf)`.
- **`README.md`** — Team contributions, repository description, and runtime information.
- **`requirements.txt`** — Python dependencies.
- **`figures/`** — Figures exported by the notebook.
- **`ECE3715_MP2.pdf`** — Project assignment.

## Project Steps

1. **From CDF to Density**
   - States the CDF, density, and support of uniform, exponential, Gaussian, and Rayleigh distributions.
   - Generates 100,000 samples of each distribution and compares empirical CDFs and normalized histograms with analytic formulas.
   - Reports KS statistics and compares exponential and Rayleigh means, medians, and variances with closed forms.

2. **Build Your Own Generator by Inversion**
   - Proves the inversion result and derives the exponential and Rayleigh inverse CDFs.
   - Generates 100,000 samples of each using uniform random samples and the inverse functions.
   - Verifies both generators against analytic CDFs and independent library samples, including numerical endpoint handling.

3. **A Function of a Random Variable**
   - Derives the CDF and density of a squared standard Gaussian.
   - Checks the density numerically and shows its behavior near zero on linear and log-log axes.

4. **Expectation and Moments**
   - Compares the first four Rayleigh raw moments with theory in units of standard error.
   - Derives the Pareto mean and shows why the variance is infinite.
   - Plots running means and variances at four sample sizes for both distributions.

## Key Results

For Steps 1 and 2, using 100,000 samples per distribution:

- All four Step 1 KS statistics fall below the 95 percent critical value of **0.0043007**.
- Exponential inversion gives a KS statistic of **0.0038259**; Rayleigh inversion gives **0.0020791**, both below the same critical value.
- Inversion and library samples give two-sample KS statistics of **0.0042500** and **0.0041700**, below the two-sample critical value of **0.0060821**.
- The exponential sample mean and median are **1.000320** and **0.692804**, compared with theoretical values of **1** and **0.693147**.
- The Rayleigh sample mean, median, and variance are **1.252540**, **1.175111**, and **0.428195**, compared with theoretical values of **1.253314**, **1.177410**, and **0.429204**.

- The squared Gaussian density integrates to **1** and has a log-log slope of **−0.5** near zero.
- All four Rayleigh raw moments are within **0.70 standard errors** of theory. At one million draws the Pareto sample mean is **3.0405**, close to its theoretical mean of **3**, while the sample variance is **3,225.94**.

## Reproducibility

A random seed was drawn once on November 2, 2026 and fixed near the top of the notebook using NumPy's `Generator` interface:

```python
SEED = 1274601137  # drawn 2026-11-02, do not change
rng = np.random.default_rng(SEED)
```

Each project step receives its own independently spawned random-number generator so that rerunning one section does not shift the random stream used by later sections. Restarting the kernel and running all cells reproduces the saved results.

## Runtime

The code cells for Steps 1–4 ran in order in a fresh Python process in approximately:

**33.15 seconds**

which is below the required five-minute runtime limit. The complete project runtime will be updated as the remaining steps are added.

## Requirements

The project uses:

- Python 3.10+
- NumPy 1.25+
- SciPy
- Matplotlib
- Jupyter Notebook

Install the dependencies with `python -m pip install -r requirements.txt`.

## Submission Checklist

Before submitting:

1. Complete all eight project steps and required helper functions.
2. Ensure the final notebook filename is `mp2.ipynb`.
3. Keep `mp2lib.py` in the same `mp2/` directory.
4. Restart the kernel and run all cells from top to bottom.
5. Confirm all cells run without errors.
6. Confirm all figures, tables, and printed outputs are saved in the notebook.
7. Confirm the complete runtime remains under five minutes.
