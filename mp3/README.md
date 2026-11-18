# ECE 3715 Mini-Project 3

## Random Vectors and the Multivariate Gaussian

This project explores joint and conditional densities, correlation and independence, covariance estimation, linear transformations, multivariate Gaussian densities, decorrelation, and whitening. The notebook includes mathematical derivations, simulations, numerical comparisons, and figure interpretations for Steps 1–6.

## Team Contributions

| Team member | Contributions |
| --- | --- |
| Christian Ruelas | Steps 1–3; Monte Carlo comparisons; `sample_mean_cov` and `is_valid_covariance` |
| Arun Nambiar | Step 4; Figure 4; linear transformations and rank-deficient covariance analysis |
| Ibrahim Elsousi | Steps 5–6; `gaussian_pdf` and `whitening_matrix`; Gaussian density validation, probability contours, decorrelation, and whitening |

## Repository Contents

| File or folder | Description |
| --- | --- |
| `mp3.ipynb` | Derivations, code, saved outputs, and figure interpretations |
| `mp3lib.py` | Reusable numerical functions |
| `requirements.txt` | Python dependencies |
| `figures/` | Figures exported as PNG files |
| `results/` | Numerical checks saved as CSV files and runtime information |
| `README.md` | Contributions, setup instructions, reproducibility details, and runtime |

## Setup and Execution

Keep `mp3.ipynb`, `mp3lib.py`, and `requirements.txt` in the same folder. Open a terminal in that folder.

On Windows with Python 3.12 installed:

```bat
py -3.12 -m pip install -r requirements.txt
py -3.12 -m jupyterlab mp3.ipynb
```

On a system where Python is available through the `python` command:

```sh
python -m pip install -r requirements.txt
python -m jupyterlab mp3.ipynb
```

In Jupyter, select **Kernel → Restart Kernel and Run All Cells**. Wait for execution to finish, then save the notebook. Keep the terminal running while using Jupyter. The notebook creates the `figures/` and `results/` folders and writes its outputs automatically.

## Reproducibility

The seed was drawn once on November 10, 2026 and is fixed in the notebook:

```python
SEED = 1015518633  # drawn 2026-11-10, do not change
rng = np.random.default_rng(SEED)
rng1, rng2, rng3, rng4, rng5, rng6, rng7, rng8 = rng.spawn(8)
```

Each step has its own random generator, created in the setup cell. Step 5 uses `rng5`. Step 6 reuses the Step 5 observations for the geometric comparisons and uses `rng6` for the independent four-dimensional experiment.

Rerunning a sampling cell alone advances its random stream. Restart the kernel and run all cells to reproduce the saved results. Do not reseed partway through the notebook.

## Numerical Functions

| Function | Purpose |
| --- | --- |
| `sample_mean_cov(X)` | Computes the sample mean and unbiased sample covariance for observations stored as rows |
| `is_valid_covariance(S, tol=1e-10)` | Checks symmetry and positive semidefiniteness within the specified tolerance |
| `gaussian_pdf(x, mu, Sigma)` | Evaluates the multivariate Gaussian density using a linear solve and the log determinant |
| `whitening_matrix(Sigma)` | Constructs a whitening matrix using symmetric eigendecomposition |

The private helper `_positive_definite_matrix` validates covariance inputs for the density and whitening functions. Both functions require positive-definite covariance matrices. For observations stored as rows, apply whitening as `(X - mu) @ W.T`.

## Steps 5–6

**Step 5 — The multivariate Gaussian**

- Derives and implements the multivariate Gaussian density.
- Compares the implementation with SciPy at five scattered points.
- Checks normalization over a region extending eight marginal standard deviations in each direction.
- Plots 50%, 90%, and 99% probability contours over 10,000 samples and reports empirical coverage with standard errors.
- Reports ellipse axis lengths and directions.
- Compares correlations of 0, 0.5, 0.9, and 0.99 while holding both variances at 4.

**Step 6 — Eigendecomposition, decorrelation, and whitening**

- Reports eigenvalues and eigenvectors and displays the scaled eigenvector axes.
- Applies decorrelation and compares the estimated covariance with the diagonal eigenvalue matrix.
- Applies whitening and compares the estimated covariance with the identity matrix.
- Verifies whitening after an orthogonal rotation.
- Verifies the same whitening implementation in four dimensions using 1,000,000 samples.
- Reports entrywise covariance differences, standard errors, and Frobenius errors.

Whitening uses the known population covariance. The estimated covariance is therefore free to differ from identity by sampling error, which is quantified in the output tables.

## Results and Runtime

| Check | Recorded result |
| --- | --- |
| Largest relative PDF difference from SciPy | 9.509 × 10⁻¹⁶ |
| Numerical density integral | 0.999999999999998 |
| Empirical coverage of the 50% contour | 49.60% |
| Empirical coverage of the 90% contour | 89.63% |
| Empirical coverage of the 99% contour | 99.00% |
| Two-dimensional covariance eigenvalues | 2 and 6 |
| Two-dimensional whitening Frobenius error | 0.02791427 |
| Four-dimensional whitening Frobenius error | 0.003090821 |
| Notebook runtime for Steps 1–6 | 8.06 seconds |

All 13 code cells executed in sequence with no execution errors. The recorded runtime is below the five-minute project limit. Runtime varies with hardware and software configuration.

Recorded execution environment:

- Python 3.12.10
- NumPy 2.5.5
- SciPy 1.18.1
- Matplotlib 3.11.2
