"""Numerical helpers for ECE 3715 Mini-Project 3."""

import numpy as np


def sample_mean_cov(X) -> tuple[np.ndarray, np.ndarray]:
    """Return the feature mean and unbiased covariance of an (N, d) sample."""
    samples = np.asarray(X, dtype=np.float64)
    if samples.ndim != 2 or samples.shape[0] < 2 or samples.shape[1] == 0:
        raise ValueError("X must be a nonempty (N, d) array with N >= 2")

    mean = samples.mean(axis=0)
    centered = samples - mean
    covariance = (centered.T @ centered) / (samples.shape[0] - 1)
    return mean, covariance


def is_valid_covariance(S, tol=1e-10) -> bool:
    """Check symmetry and positive semidefiniteness to absolute tolerance tol."""
    if not np.isfinite(tol) or tol < 0:
        raise ValueError("tol must be finite and nonnegative")

    matrix = np.asarray(S)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or not matrix.size:
        return False
    if not np.isrealobj(matrix) or not np.isfinite(matrix).all():
        return False

    matrix = matrix.astype(np.float64, copy=False)
    if not np.allclose(matrix, matrix.T, atol=tol, rtol=0):
        return False

    # Average the two triangles when asymmetry is within rounding tolerance.
    symmetric = 0.5 * matrix + 0.5 * matrix.T
    eigenvalues, _ = np.linalg.eigh(symmetric)
    return bool(eigenvalues[0] >= -tol)
