# ECE 3715 Mini-Project 3

## Random Vectors and the Multivariate Gaussian

The notebook contains Steps 1–8 and Bonuses A–B, including mathematical derivations, simulations, numerical comparisons, saved figures, and interpretations.

## Team Contributions

| Team member | Contributions |
| --- | --- |
| Christian Ruelas | Steps 1–3; Monte Carlo comparisons; sample mean and covariance helpers |
| Arun Nambiar | Steps 4, 7, and 8; linear transformations, conditional Gaussians, and linear MMSE sensor fusion |
| Ibrahim Elsousi | Steps 5–6 and Bonuses A–B; Gaussian density validation, whitening, correlated-vector generation, and real-data PCA |

## Package Contents

| File or folder | Description |
| --- | --- |
| `mp3.ipynb` | Complete notebook with saved outputs |
| `mp3lib.py` | Required numerical helper functions |
| `requirements.txt` | Python dependencies |
| `data/wine.csv` | Local dataset for Bonus B |
| `data/SOURCE.md` | Dataset citation and export details |
| `figures/` | Figures 1–10 exported as PNG files |
| `results/` | Numerical comparisons, PCA results, and runtime information |

The setup cell assigns one random stream to each step and an additional stream to Bonus A. The required `lmmse_weights(Sigma_xx, Sigma_sx)` function returns the weight vector; Step 8 computes the MMSE separately. The notebook includes finite-bin corrections in Step 7 and explains the singular covariance endpoints and varying equal-weight baseline in Step 8.

The notebook writes figures and result tables automatically. Bonus B reads the included CSV; it requires neither an online dataset download nor scikit-learn.

## Reproducibility

The fixed seed is `1015518633`, drawn once on November 10, 2026. Setup creates the random streams in this order:

```python
rng = np.random.default_rng(SEED)
rng1, rng2, rng3, rng4, rng5, rng6, rng7, rng8 = rng.spawn(8)
rng_bonus_a = rng.spawn(1)[0]
```

Each simulation uses its assigned generator. Bonus A receives a new stream without changing the original eight streams. Bonus B is deterministic. Rerunning a sampling cell alone advances its stream; restart and run all cells to reproduce the saved results.

## Bonus A — Correlated Vectors from Scratch

- Derives the means and covariances of the Cholesky and eigenvalue constructions.
- Generates independent standard-normal vectors, then applies each matrix factor.
- Verifies both methods for the project's two-dimensional and four-dimensional covariance matrices, using one million observations per method and dimension.
- Reports sample means, covariance entries, signed errors, standard errors, and covariance Frobenius errors.
- Explains why Cholesky is normally cheaper for positive-definite covariance matrices.
- Demonstrates the expected Cholesky failure for a singular covariance and verifies a valid eigenvalue construction for that case.

The numerical tables report the largest standardized discrepancy and factor reconstruction error for each experiment.

## Bonus B — PCA on Real Data

The Wine dataset contains 178 observations and 13 numeric chemical measurements. Cultivar labels color the plots and are excluded from the PCA calculations.

Source: Aeberhard, S. & Forina, M. (1992). *Wine* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5PC7J

The notebook computes the sample covariance, eigenvalues, principal directions, and two-component projections. It repeats the analysis after standardizing each feature to unit sample variance. Figure 10 compares the two projections with equal axis scaling within each panel.

| Analysis | Variance captured by the first two components |
| --- | --- |
| Raw measurements | 99.9827% |
| Standardized measurements | 55.4063% |

Raw PCA is dominated by the numerical scale of proline. Standardization gives each chemical measurement equal starting variance and produces a more balanced view of the feature relationships. The notebook explains why the standardized analysis is preferable for exploring these measurements with different scales. The two explained-variance percentages refer to different total-variance definitions.

The population covariance of the real dataset is unknown. Reconstruction and projection residuals check the numerical calculations rather than measuring error against an unknown population covariance.

Covariance matrices, eigenvalue spectra, principal-component coefficients, feature scales, and projected scores are saved in `results/bonus_b_*.csv`.

## Validation and Runtime

All 18 code cells executed from top to bottom with no execution errors. The complete notebook recorded **12.82 seconds**, below the five-minute project limit. Runtime varies with hardware and software.

The execution environment's Python, NumPy, SciPy, and Matplotlib versions are recorded in `results/runtime.json`.

The final notebook cell updates this section and `results/runtime.json` on every full run.
