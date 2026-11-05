# ECE 3715 Mini-Project 2

## Continuous Random Variables

This repository contains Mini-Project 2 for **ECE 3715 — Probability and Statistics**.

The project studies continuous random variables through densities, cumulative distribution functions, inverse-transform sampling, moments, and the central limit theorem. It then applies these ideas to signal detection in noise, noise-power uncertainty, and operating-point selection. The notebook includes **Steps 1–8 and both extra-credit sections**.

## Team Members and Contributions

- **Christian Ruelas** — Steps 1, 2 & 4: From CDF to Density / Inverse-Transform Sampling / Expectation and Moments; implemented `inv_cdf_exponential()`, `inv_cdf_rayleigh()`, `sample_by_inversion()`, and `ks_statistic()`.
- **Arun Nambiar** — Steps 3 & 5: A Function of a Random Variable / The Central Limit Theorem; derived and simulated transformed distributions and measured convergence of standardized sums to the Gaussian.
- **Ibrahim Elsousi** — Steps 6, 7 & 8: Gaussian Threshold Detection / Envelope Detection and Noise Mismatch / Choosing the Operating Point; implemented `q_function()` and analyzed detection thresholds, ROC curves, noise uncertainty, and operating-point tradeoffs.
- **Everyone** — Bonus A (Characteristic Functions), Bonus B (A Distribution with No Mean), final notebook integration, README, testing, and cleanup.

## Repository Contents

```text
mp2/
├── mp2.ipynb
├── mp2lib.py
├── README.md
├── requirements.txt
├── figures/
├── results/
└── ECE3715_MP2.pdf
```

- **`mp2.ipynb`** — Main Jupyter notebook. Runs all eight steps and both bonus sections with saved figures, tables, and interpretations.
- **`mp2lib.py`** — Required helper functions: `inv_cdf_exponential(u, lam)`, `inv_cdf_rayleigh(u, sigma)`, `sample_by_inversion(inv_cdf, n, rng, **kw)`, `ks_statistic(samples, cdf)`, and `q_function(x)`. Additional helpers compute an empirical characteristic function and sample Cauchy variables from Gaussian ratios.
- **`README.md`** — Team contributions, project description, results, and runtime information.
- **`requirements.txt`** — Python dependencies.
- **`figures/`** — Eleven figures exported by the notebook.
- **`results/`** — Numerical CSV tables for the detector and bonus experiments, plus runtime information in `runtime.json`.
- **`ECE3715_MP2.pdf`** — Project assignment.

## Project Steps

1. **From CDF to Density**
   - Compares CDFs and normalized histograms for uniform, exponential, Gaussian, and Rayleigh distributions using 100,000 samples each.
   - Reports KS statistics and exponential/Rayleigh means, medians, and variances against closed forms.

2. **Build Your Own Generator by Inversion**
   - Proves the inversion result and derives exponential and Rayleigh inverse CDFs.
   - Verifies both generators against analytic CDFs and independent library samples, including endpoint handling.

3. **A Function of a Random Variable**
   - Derives the CDF and density of a squared standard Gaussian.
   - Shows the integrable density divergence near zero on linear and log-log axes using one million samples.

4. **Expectation and Moments**
   - Compares the first four Rayleigh raw moments against theory in units of standard error.
   - Derives the Pareto mean and shows why its variance is infinite, then compares running estimates.

5. **The Central Limit Theorem, and Where It Fails**
   - Measures convergence of standardized uniform sums to a Gaussian with KS statistics.
   - Contrasts this behavior with infinite-variance Pareto summands and discusses stable-law behavior.

6. **A Threshold Detector in Gaussian Noise**
   - Derives false-alarm and detection probabilities using the Q function.
   - Verifies thresholds by Monte Carlo and plots ROC curves for multiple signal amplitudes.

7. **The Envelope Detector and Noise Mismatch**
   - Derives and verifies the Rayleigh threshold relation.
   - Quantifies the false-alarm increase when actual noise power differs from its assumed value.

8. **Choosing the Operating Point**
   - Derives required SNR for specified false-alarm and detection probabilities.
   - Recommends conditional smoke-alarm and radar operating points and evaluates a margin for noise uncertainty.

## Extra Credit

**Bonus A — Characteristic Functions**

- Computes Gaussian and uniform characteristic functions numerically and verifies the product rule for an independent sum.
- Recovers the sum density by inverse transform and compares it against direct numerical convolution, an analytic density, and simulated samples.
- Reports density errors, a KS statistic, and timing measurements for both numerical routes.

**Bonus B — A Distribution with No Mean**

- Derives the standard Cauchy density from the ratio of two independent standard Gaussians.
- Compares sample means and medians at 1,000, 10,000, 100,000, and one million observations.
- Uses characteristic functions to show that a Cauchy sample mean has the same distribution at every sample size, and verifies this with independent block averages.
- Recommends the sample median for location estimation with Cauchy measurement noise.

## Key Results

- All four Step 1 KS statistics fall below **0.0043007**, the approximate 95% cutoff at 100,000 samples. Exponential and Rayleigh inversion give **0.0038259** and **0.0020791**.
- The squared Gaussian density has a near-zero log-log slope of **−0.5**, despite integrating to **1**.
- All four Rayleigh raw moments are within **0.70 standard errors** of theory. The Pareto mean exists and equals **3**, but its variance is infinite.
- A **+3 dB** noise-power mismatch increases the envelope detector's false-alarm rate from **0.001** to approximately **0.03136**, a factor of **31.36**.
- At 90% detection, the Gaussian detector needs `A/sigma = 4.3718` for `P_FA = 10^-3` and **6.0350** for `10^-6` (**12.81 dB** and **15.61 dB**). The notebook explains the sign error in the assignment's supplied Step 8 check values.
- Bonus A recovers the sum density with maximum analytic error **1.23e-06** and L1 error **3.62e-06**. Its sample KS statistic is **0.002312** against cutoff **0.004301**.
- At one million Gaussian ratios, Bonus B gives sample mean **1.41999** and median **0.000994**. The Cauchy population mean is undefined; averaging cannot concentrate its distribution, while the median estimates the location.

## Reproducibility

A seed was drawn once on November 2, 2026 and fixed near the top of the notebook:

```python
SEED = 1274601137  # drawn 2026-11-02, do not change
rng = np.random.default_rng(SEED)
```

Each project step uses its own independently spawned generator. Bonus streams `rngA` and `rngB` are spawned after the original eight streams, preserving the previous results. Restart the kernel and run all cells to reproduce the experiments. Rerunning a sampling cell alone advances its stream.

## Runtime

All code cells for Steps 1–8 and both bonuses ran in order in a fresh Python process in approximately:

**187.29 seconds**

This is below the five-minute limit. The notebook records runtime and environment versions in `results/runtime.json`. Numerical timings vary by machine; the Bonus A table reports measured transform and direct-convolution costs separately.

## Requirements

The project uses:

- Python 3.10+
- NumPy 1.25+
- SciPy
- Matplotlib
- Jupyter Notebook

Install dependencies with `python -m pip install -r requirements.txt`, then open `mp2.ipynb` in a Python notebook environment. Keep `mp2lib.py` beside the notebook. The notebook creates `figures/` and `results/` automatically.

## Submission Checklist

Before submitting:

1. Ensure the final notebook filename is `mp2.ipynb`.
2. Keep `mp2lib.py` in the same directory.
3. Restart the kernel and run all cells from top to bottom.
4. Confirm all cells run without errors and all figures, tables, derivations, and interpretations are saved.
5. Keep the seed fixed and confirm the complete runtime remains under five minutes.
6. Submit once per team following the assignment instructions.
