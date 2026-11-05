"""Continuous random-variable helpers for ECE 3715 Mini-Project 2.

Randomness is supplied by the notebook through a NumPy Generator.
Helpers for Steps 1-8 and both optional bonus experiments.
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
    """Gaussian upper tail, evaluated without cancellation using erfc."""
    from scipy.special import erfc
    x = np.asarray(x, dtype=float)
    return np.asarray(0.5 * erfc(x / np.sqrt(2.0)))


def empirical_characteristic_function(samples, t, batch_size=16) -> np.ndarray:
    """Estimate E[exp(i*t*X)], batching frequencies to bound memory use."""
    samples = np.asarray(samples, dtype=float)
    t = np.asarray(t, dtype=float)
    if samples.ndim != 1 or not samples.size or not np.all(np.isfinite(samples)):
        raise ValueError("samples must be a nonempty finite one-dimensional array.")
    if not np.all(np.isfinite(t)):
        raise ValueError("frequencies must be finite.")
    if not isinstance(batch_size, (int, np.integer)) or batch_size < 1:
        raise ValueError("batch_size must be a positive integer.")
    flat = t.ravel()
    result = np.empty(flat.size, dtype=complex)
    for start in range(0, flat.size, batch_size):
        frequencies = flat[start:start + batch_size]
        result[start:start + batch_size] = np.exp(1j * frequencies[:, None] * samples).mean(axis=1)
    return result.reshape(t.shape)


def sample_cauchy_ratio(n, rng) -> np.ndarray:
    """Return ratios of independent standard Gaussians; never clip the tail."""
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer)) or n < 0:
        raise ValueError("n must be a nonnegative integer.")
    numerator = rng.standard_normal(n)
    denominator = rng.standard_normal(n)
    # An exact zero has probability zero in the continuous model. Resample the
    # denominator if the finite-precision generator happens to return one.
    zero = denominator == 0
    while np.any(zero):
        denominator[zero] = rng.standard_normal(np.count_nonzero(zero))
        zero = denominator == 0
    return numerator / denominator
