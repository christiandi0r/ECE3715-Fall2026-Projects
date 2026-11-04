"""Continuous random-variable helpers for ECE 3715 Mini-Project 2.

Randomness is supplied by the notebook through a NumPy Generator.
Steps 1 and 2 helpers are preserved; q_function implements the Step 6 tail.
"""
import numpy as np


def _positive(value, name):
    if np.ndim(value) != 0 or not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive scalar.")


def _uniform_input(u):
    u = np.asarray(u, dtype=float)
    if np.any(~np.isfinite(u)) or np.any((u < 0) | (u > 1)):
        raise ValueError("u must contain finite values in [0, 1].")
    return u


def inv_cdf_exponential(u, lam) -> np.ndarray:
    """Exponential quantiles: 0 maps to 0; 1 maps to positive infinity."""
    _positive(lam, "lam")
    u = _uniform_input(u)
    with np.errstate(divide="ignore"):
        return np.asarray(-np.log1p(-u) / lam)


def inv_cdf_rayleigh(u, sigma) -> np.ndarray:
    """Rayleigh quantiles; sigma is the scale, not the standard deviation."""
    _positive(sigma, "sigma")
    u = _uniform_input(u)
    with np.errstate(divide="ignore"):
        return np.asarray(sigma * np.sqrt(-2 * np.log1p(-u)))


def sample_by_inversion(inv_cdf, n, rng, **kw) -> np.ndarray:
    """Transform n uniforms. rng.random is the only source of randomness."""
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer)) or n < 0:
        raise ValueError("n must be a nonnegative integer.")
    return np.asarray(inv_cdf(rng.random(n), **kw))


def ks_statistic(samples, cdf) -> float:
    """Two-sided one-sample KS distance, including both sides of each jump.

    The CDF callable must accept and return arrays of the sample shape.
    The continuous-null 1.36/sqrt(n) cutoff is applied by the notebook.
    """
    x = np.asarray(samples, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("samples must be a nonempty finite one-dimensional array.")
    x = np.sort(x)
    f = np.asarray(cdf(x), dtype=float)
    if f.shape != x.shape or np.any(~np.isfinite(f)) or np.any((f < 0) | (f > 1)):
        raise ValueError("cdf must return finite probabilities of the sample shape.")
    if np.any(np.diff(f) < 0):
        raise ValueError("cdf must be nondecreasing.")
    i = np.arange(1, x.size + 1)
    d_plus = np.max(i / x.size - f)
    d_minus = np.max(f - (i - 1) / x.size)
    return float(max(d_plus, d_minus))


def q_function(x) -> np.ndarray:
    """Gaussian upper-tail Q(x) = erfc(x / sqrt(2)) / 2.

    Accept scalars or arrays and return an ndarray of the same shape.
    erfc avoids the cancellation in 1 - Phi(x) for a small upper tail.
    Infinities have their limiting values; NaNs propagate.
    No numerical quadrature or normal survival function is used here.
    """
    from scipy.special import erfc

    x = np.asarray(x, dtype=float)
    return np.asarray(0.5 * erfc(x / np.sqrt(2.0)))
