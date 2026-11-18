# ECE 3715 Mini-Project 3

## Random Vectors and the Multivariate Gaussian

The notebook contains Steps 1–6. Steps 1–4 were retained from the uploaded notebook; Steps 5–6 have been added with derivations, numerical verification, and Figures 5–7. Steps 7–8 and bonus work are pending.

## Team contributions

- **Christian Ruelas** — Steps 1–3, Figures 1–3, Monte Carlo comparisons, `sample_mean_cov`, and `is_valid_covariance`.
- **Arun Nambiar** — Step 4 and Figure 4; assigned Steps 7–8 (pending).
- **Ibrahim Elsousi** — Steps 5–6, Figures 5–7, `gaussian_pdf`, and `whitening_matrix`; assigned bonus work (pending).

## Files

| Path | Contents |
| --- | --- |
| `mp3.ipynb` | Steps 1–6 with derivations and saved execution outputs |
| `mp3lib.py` | Sample mean/covariance, covariance validation, Gaussian PDF, and whitening |
| `requirements.txt` | Dependencies for running in Jupyter |
| `figures/` | Figures 1–7 as PNGs |
| `results/` | Numerical CSVs and runtime/environment information |
| `HANDOFF.md` | Integration notes for the remaining steps |

## Running the notebook

Extract the package, open a terminal in the `mp3` folder, and install dependencies:

```sh
python -m pip install -r requirements.txt
python -m jupyterlab mp3.ipynb
```

Keep `mp3.ipynb` and `mp3lib.py` in the same folder. In Jupyter, choose **Restart Kernel and Run All Cells**. All figures and results are generated automatically. Rerunning a sampling cell alone advances that step's stream; restart and run all for the recorded result.

## Reproducibility

The original seed and stream allocation are unchanged:

```python
SEED = 1015518633  # drawn 2026-11-10, do not change
rng = np.random.default_rng(SEED)
rng1, rng2, rng3, rng4, rng5, rng6, rng7, rng8 = rng.spawn(8)
```

Step 5 uses `rng5`. Step 6 reuses the Step 5 samples for geometric comparisons and uses `rng6` for its independent four-dimensional check. `rng7` and `rng8` are unused and ready for the remaining steps. Do not reseed below setup.

## Steps 5–6

- **Step 5:** Gaussian density formula, a determinant/linear-solve implementation, checks against SciPy at five points, normalization over an eight-standard-deviation rectangle, 50%/90%/99% contour counts with standard errors, ellipse axis lengths/directions, and a four-panel correlation sweep.
- **Step 6:** Symmetric eigendecomposition, scaled eigenvector arrows, decorrelation, whitening, entrywise covariance errors and standard errors, a rotated whitening transform, and a four-dimensional verification using one million samples.

The covariance used for whitening is the known population covariance, not the covariance estimated from the same sample. Thus agreement with identity is a meaningful simulation check. The functions reject non-positive-definite covariances because a full-dimensional PDF and full-dimensional identity whitening require positive eigenvalues.

## Validation and runtime

All code cells executed in order in a fresh Python/IPython process, without errors. Saved notebook runtime for Steps 1–6 was **8.05 seconds**, below the 300-second limit. Standard Jupyter kernel startup was blocked by socket restrictions in the validation environment, so final **Restart Kernel and Run All** validation should also be performed locally before submission.

The helper functions passed independent checks against SciPy in 1, 2, 4, and 7 dimensions, checks of arbitrary leading sample dimensions, and rejection checks for asymmetric, indefinite, and singular covariances. Figures 5–7 were inspected for labels, legends, and equal aspect ratios.

Recorded environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8. Runtime depends on hardware and numerical-library thread settings; validation used one BLAS thread.

## Team integration

Continue with Steps 7–8 before the final Runtime section. Add `lmmse_weights` to `mp3lib.py`; it is intentionally pending. Update the notebook introduction, this README, and runtime after the final merge. The project is not yet a complete Steps 1–8 submission.
