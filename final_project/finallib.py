"""Detection helpers for ECE 3715 Final Project.

All scores use log(f1/f0): positive scores select H1 for equal priors.
Randomness is supplied by the notebooks, never created in this module.
"""

import numpy as np
from scipy.special import erfc


def _gaussian_inputs(x, mu, S):
    points = np.asarray(x, dtype=float)
    mean = np.asarray(mu, dtype=float)
    covariance = np.asarray(S, dtype=float)
    if mean.ndim != 1 or not mean.size or not np.isfinite(mean).all():
        raise ValueError("mu must be a finite, nonempty vector")
    d = mean.size
    if covariance.shape != (d, d) or not np.isfinite(covariance).all():
        raise ValueError("S must be a finite (d, d) covariance")
    if not np.allclose(covariance, covariance.T, rtol=1e-12, atol=1e-12):
        raise ValueError("S must be symmetric")
    # Reject singular/indefinite covariances rather than silently regularizing.
    factor = np.linalg.cholesky(covariance)
    if points.ndim < 1 or points.shape[-1] != d or not np.isfinite(points).all():
        raise ValueError("x must be finite with shape (..., d)")
    return points, mean, covariance, factor


def log_likelihood_ratio(x, mu0, S0, mu1, S1) -> np.ndarray:
    """Gaussian log(f1/f0), including unequal-covariance quadratic terms.

    x has shape (..., d); the output has shape (...,). Covariances must be
    symmetric positive definite. Cholesky solves avoid explicit inverses.
    """
    points, mean0, _, L0 = _gaussian_inputs(x, mu0, S0)
    _, mean1, _, L1 = _gaussian_inputs(x, mu1, S1)
    if mean0.shape != mean1.shape:
        raise ValueError("class means must have the same dimension")
    shape = points.shape[:-1]
    z0 = np.linalg.solve(L0, (points - mean0).reshape(-1, mean0.size).T)
    z1 = np.linalg.solve(L1, (points - mean1).reshape(-1, mean1.size).T)
    logdet0 = 2 * np.log(np.diag(L0)).sum()
    logdet1 = 2 * np.log(np.diag(L1)).sum()
    result = 0.5 * (np.sum(z0*z0, axis=0) - np.sum(z1*z1, axis=0)
                    + logdet0 - logdet1)
    return np.asarray(result.reshape(shape))


def linear_discriminant(x, mu0, mu1, S) -> np.ndarray:
    """Equal-covariance log(f1/f0) = x @ w - tau.

    w = solve(S, mu1-mu0), tau = (mu0+mu1) @ w / 2. Decide H1
    when the returned centered score is positive, not when it exceeds tau.
    """
    points, mean0, covariance, _ = _gaussian_inputs(x, mu0, S)
    mean1 = np.asarray(mu1, dtype=float)
    if mean1.shape != mean0.shape or not np.isfinite(mean1).all():
        raise ValueError("mu1 must be finite with the same shape as mu0")
    w = np.linalg.solve(covariance, mean1 - mean0)
    return np.asarray((points - (mean0 + mean1) / 2) @ w)


def q_function(x) -> np.ndarray:
    """Gaussian upper tail from erfc, carried over from MP2."""
    return np.asarray(0.5 * erfc(np.asarray(x, dtype=float) / np.sqrt(2)))


def empirical_error_rate(decisions, truth) -> float:
    """Fraction of mismatched binary decisions; shapes must match."""
    decisions, truth = np.asarray(decisions), np.asarray(truth)
    if decisions.shape != truth.shape or not decisions.size:
        raise ValueError("decisions and truth must have matching nonempty shapes")
    if not np.isin(decisions, [0, 1]).all() or not np.isin(truth, [0, 1]).all():
        raise ValueError("decisions and truth must contain binary labels")
    return float(np.mean(decisions != truth))
