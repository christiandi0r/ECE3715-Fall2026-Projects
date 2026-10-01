"""Helper functions for ECE 3715 Mini-Project 1.

The notebook controls all random-number generation and passes a NumPy
Generator into each simulation function so the project remains reproducible.
"""

import numpy as np


def bsc(bits, p, rng) -> np.ndarray:
    """Flip each input bit independently with probability p."""
    bits = np.asarray(bits)

    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1.")

    if not np.all((bits == 0) | (bits == 1)):
        raise ValueError("bits must contain only 0 and 1.")

    flips = rng.random(bits.shape) < p

    return np.bitwise_xor(
        bits.astype(np.uint8),
        flips.astype(np.uint8)
    )


def packet_errors(n_pkt, n_bits, p, rng) -> np.ndarray:
    """Return the number of bit errors in each simulated packet."""
    if not isinstance(n_pkt, (int, np.integer)) or n_pkt < 0:
        raise ValueError("n_pkt must be a nonnegative integer.")

    if not isinstance(n_bits, (int, np.integer)) or n_bits < 0:
        raise ValueError("n_bits must be a nonnegative integer.")

    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1.")

    return rng.binomial(
        n=n_bits,
        p=p,
        size=n_pkt
    )


def attempts_until_clean(n_trials, q, rng) -> np.ndarray:
    """Return attempts required until the first clean packet.

    The support starts at 1, so a value of 1 means the first attempt was clean.
    q is the per-attempt clean-packet probability.
    """
    if not isinstance(n_trials, (int, np.integer)) or n_trials < 0:
        raise ValueError("n_trials must be a nonnegative integer.")

    if not 0 < q <= 1:
        raise ValueError("q must be greater than 0 and at most 1.")

    return rng.geometric(
        p=q,
        size=n_trials
    )


def tv_distance(pmf1, pmf2) -> float:
    """Compute total variation distance on a common support.

    TV(P,Q) = 0.5 * sum_k |P(k) - Q(k)|.
    """
    pmf1 = np.asarray(pmf1, dtype=float)
    pmf2 = np.asarray(pmf2, dtype=float)

    if pmf1.ndim != 1 or pmf2.ndim != 1:
        raise ValueError("PMFs must be one-dimensional.")

    if pmf1.shape != pmf2.shape:
        raise ValueError("PMFs must have the same shape.")

    if (
        not np.all(np.isfinite(pmf1))
        or not np.all(np.isfinite(pmf2))
        or np.any(pmf1 < 0)
        or np.any(pmf2 < 0)
    ):
        raise ValueError("PMFs must contain finite, nonnegative values.")

    return float(
        0.5 * np.sum(np.abs(pmf1 - pmf2))
    )


def probability_comparison(mask, exact):
    """Compare a Monte Carlo probability estimate with its exact value.

    Returns
    -------
    list
        [estimate, exact, difference, standard_error, difference_over_SE]
    """
    mask = np.asarray(mask)

    if mask.size == 0:
        raise ValueError("mask must contain at least one observation.")

    if not 0 <= exact <= 1:
        raise ValueError("exact must be between 0 and 1.")

    estimate = float(np.mean(mask))
    difference = estimate - exact
    se = float(np.sqrt(exact * (1 - exact) / mask.size))

    if se > 0:
        z = difference / se
    elif difference == 0:
        z = 0.0
    else:
        z = float(np.copysign(np.inf, difference))

    return [estimate, float(exact), difference, se, z]
