import numpy as np
from scipy.special import erfc


def inv_cdf_exponential(u, lam):
    """
    Inverse CDF of an exponential random variable.
    """
    u = np.asarray(u)

    if lam <= 0:
        raise ValueError("lam must be positive")

    return -np.log1p(-u) / lam


def inv_cdf_rayleigh(u, sigma):
    """
    Inverse CDF of a Rayleigh random variable.
    """
    u = np.asarray(u)

    if sigma <= 0:
        raise ValueError("sigma must be positive")

    return sigma * np.sqrt(-2.0 * np.log1p(-u))


def sample_by_inversion(inv_cdf, n, rng, **kw):
    """
    Generate random samples using inverse-transform sampling.
    """
    u = rng.random(n)
    return inv_cdf(u, **kw)


def ks_statistic(samples, cdf):
    """
    Compute the two-sided Kolmogorov-Smirnov statistic.
    """
    x = np.sort(np.asarray(samples))
    n = len(x)

    if n == 0:
        raise ValueError("samples must not be empty")

    F = np.asarray(cdf(x))

    empirical_upper = np.arange(1, n + 1) / n
    empirical_lower = np.arange(0, n) / n

    d_plus = np.max(empirical_upper - F)
    d_minus = np.max(F - empirical_lower)

    return float(max(d_plus, d_minus))


def q_function(x):
    """
    Gaussian Q-function:
        Q(x) = 0.5 * erfc(x / sqrt(2))
    """
    x = np.asarray(x)
    return 0.5 * erfc(x / np.sqrt(2.0))
