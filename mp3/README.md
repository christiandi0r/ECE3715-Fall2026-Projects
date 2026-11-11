# ECE 3715 Mini-Project 3

## Random Vectors and the Multivariate Gaussian

This notebook contains Steps 1–3 of the team project. It studies joint and conditional densities, the difference between zero correlation and independence, and the sample size needed to estimate a covariance matrix.

## Team contributions

- **Christian Ruelas** — Steps 1–3, including Figures 1–3, the Monte Carlo comparisons, `sample_mean_cov`, and `is_valid_covariance`.
- **Arun Nambiar** — Assigned Steps 4, 7, and 8 (linear transformations, conditional Gaussians, and sensor fusion).
- **Ibrahim Elsousi** — Assigned Steps 5–6 (multivariate Gaussian densities and whitening) and the bonus work.

## Repository contents

| Path | Contents |
| --- | --- |
| `mp3.ipynb` | Derivations, experiments, results, and figure interpretations for Steps 1–3 |
| `mp3lib.py` | The sample mean and covariance estimator and covariance validation |
| `README.md` | Team contributions, setup, and reproducibility notes |
| `requirements.txt` | Python dependencies for running the notebook |
| `figures/` | Figures 1–3 exported as PNGs |
| `results/` | Ten CSVs with numerical checks for Steps 1–3 and `runtime.json` with timing and environment details |

## Project steps

1. **Two variables at once.** Derive the marginals, conditional density, and moments of the unit-square joint density. Check them by quadrature and use one million rejection samples to compare sample statistics with theory.
2. **Uncorrelated does not mean independent.** Simulate ten million points on the parabola and compare the observed correlation with zero. Compare narrow-bin variances with finite-bin theory and the exact point-conditional limit. Check factorization for a jointly Gaussian pair using joint and product histogram probabilities.
3. **The covariance matrix and how well you can estimate it.** Validate the given covariance, estimate it at five sample sizes, and fit the convergence rate using the required independent repetitions. Use relative Frobenius accuracy to extrapolate the sample requirement for an isotropic 100-element array.

## Key results

- **Step 1.** The rejection sampler accepted **50.0135%** of proposals. All seven Monte Carlo statistics were within **1.16 standard errors** of their analytic values.
- **Step 2.** The parabola gave a sample correlation of **−0.000262** with a standard error of **0.000396**. The Gaussian joint histogram and the product of its marginals differed by **0.00338** in binned total variation.
- **Step 3.** The covariance determinant was **55**. The replicated log-log slope was **−0.50931** with a regression standard error of **0.00855**. The scaled mean errors ranged from **14.08 to 16.68**.

## Reproducibility

The seed was drawn once on November 10, 2026 and fixed near the top of the notebook.

```python
SEED = 1015518633  # drawn 2026-11-10, do not change
rng = np.random.default_rng(SEED)
rng1, rng2, rng3, rng4, rng5, rng6, rng7, rng8 = rng.spawn(8)
```

Install the dependencies in your Python environment.

```sh
python -m pip install -r requirements.txt
```

Open `mp3.ipynb` from the folder containing `mp3lib.py`, then restart the kernel and run all cells. The notebook contains the saved outputs and generates PNGs in `figures/` and numerical CSVs in `results/` locally. Rerunning a sampling cell by itself advances its random stream.

## Runtime

Steps 1–3 ran from a fresh Jupyter kernel in **4.72 seconds**. The notebook saves timing and environment versions in `results/runtime.json`.

## Team integration

Arun can use `rng4`, `rng7`, and `rng8` and add `lmmse_weights` to `mp3lib.py`. Ibrahim can use `rng5` and `rng6` and add `gaussian_pdf` and `whitening_matrix`. Step 6 can reuse `SIGMA_4D` from Step 3. Spawn any bonus streams after the eight existing step streams in the setup cell.

Insert Steps 4–8 in order, followed by the bonus work, before the runtime cell. After merging, rerun from a clean kernel, verify the full runtime is below five minutes, and update the README with completed contributions and runtime.
