"""Helper functions for ECE 3715 Mini-Project 2."""

import numpy as np
from scipy.special import erfc


def inv_cdf_exponential(u, lam):
    """Return the exponential inverse CDF evaluated at u."""
    u = np.asarray(u, dtype=float)
    if lam <= 0:
        raise ValueError("lam must be positive")
    return -np.log1p(-u) / lam


def inv_cdf_rayleigh(u, sigma):
    """Return the Rayleigh inverse CDF evaluated at u."""
    u = np.asarray(u, dtype=float)
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    return sigma * np.sqrt(-2.0 * np.log1p(-u))


def sample_by_inversion(inv_cdf, n, rng, **kw):
    """Generate n samples by applying inv_cdf to U(0,1) samples."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    u = rng.random(n)
    return inv_cdf(u, **kw)


def ks_statistic(samples, cdf):
    """Return the two-sided one-sample Kolmogorov-Smirnov statistic."""
    x = np.sort(np.asarray(samples, dtype=float))
    n = x.size
    if n == 0:
        raise ValueError("samples must not be empty")

    F = np.asarray(cdf(x), dtype=float)
    d_plus = np.max(np.arange(1, n + 1) / n - F)
    d_minus = np.max(F - np.arange(0, n) / n)
    return float(max(d_plus, d_minus))


def q_function(x):
    """Return the Gaussian tail probability Q(x) using erfc."""
    x = np.asarray(x, dtype=float)
    return 0.5 * erfc(x / np.sqrt(2.0))
