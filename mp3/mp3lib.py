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


def _positive_definite_matrix(Sigma):
    """Validate a real, finite, symmetric positive-definite covariance."""
    raw = np.asarray(Sigma)
    if not np.isrealobj(raw):
        raise ValueError("Sigma must be real")
    matrix = np.asarray(raw, dtype=float)
    if (matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]
            or not matrix.size or not np.isfinite(matrix).all()):
        raise ValueError("Sigma must be a finite, nonempty square matrix")
    if not np.allclose(matrix, matrix.T, atol=1e-12, rtol=1e-12):
        raise ValueError("Sigma must be symmetric")
    matrix = (matrix + matrix.T) / 2
    values, vectors = np.linalg.eigh(matrix)
    if values[0] <= 0:
        raise ValueError("Sigma must be positive definite, not singular")
    return matrix, values, vectors


def gaussian_pdf(x, mu, Sigma) -> np.ndarray:
    """Evaluate a nonsingular Gaussian density; x has shape (..., d).

    The output has shape x.shape[:-1] (a zero-dimensional array for one point).
    Singular covariances have no full-dimensional density and are rejected.
    """
    matrix, _, _ = _positive_definite_matrix(Sigma)
    mean = np.asarray(mu, dtype=float)
    points = np.asarray(x, dtype=float)
    d = matrix.shape[0]
    if mean.shape != (d,) or not np.isfinite(mean).all():
        raise ValueError("mu must be a finite vector with shape (d,)")
    if points.ndim < 1 or points.shape[-1] != d or not np.isfinite(points).all():
        raise ValueError("x must be finite with shape (..., d)")
    delta = points - mean
    flat = delta.reshape(-1, d)
    # A linear solve avoids explicitly forming an inverse and is more stable.
    solved = np.linalg.solve(matrix, flat.T).T
    distance_sq = np.sum(flat * solved, axis=1).reshape(delta.shape[:-1])
    # slogdet evaluates the determinant in log form to avoid overflow/underflow.
    _, logdet = np.linalg.slogdet(matrix)
    return np.asarray(np.exp(-0.5 * (d * np.log(2 * np.pi) + logdet + distance_sq)))


def whitening_matrix(Sigma) -> np.ndarray:
    """Return PCA whitening W = diag(lambda**(-1/2)) @ V.T.

    Requires a positive-definite covariance. For row samples, apply
    (X - mu) @ W.T. Singular covariance cannot be whitened to a full identity.
    """
    _, values, vectors = _positive_definite_matrix(Sigma)
    return vectors.T / np.sqrt(values)[:, None]
