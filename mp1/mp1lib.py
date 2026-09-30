"""Probability models and comparison helpers for ECE 3715 MP1."""

import numpy as np


def bsc(bits, p, rng) -> np.ndarray:
    """Flip each input bit independently with probability p."""
    bits = np.asarray(bits)
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1.")
    if not np.all((bits == 0) | (bits == 1)):
        raise ValueError("bits must contain only 0 and 1.")
    flips = rng.random(bits.shape) < p
    return np.bitwise_xor(bits.astype(np.uint8), flips)

def packet_errors(n_pkt, n_bits, p, rng) -> np.ndarray:
    """Return the number of independent bit errors in each packet."""
    
    if not isinstance(n_pkt, (int, np.integer)) or n_pkt < 0:
        raise ValueError("n_pkt must be a nonnegative integer.")
        
    if not isinstance(n_bits, (int, np.integer)) or n_bits < 0:
        raise ValueError("n_bits must be a nonnegative integer.")
        
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1.")
        
    return rng.binomial(n_bits, p, size=n_pkt)

def attempts_until_clean(n_trials, q, rng) -> np.ndarray:
    """Return attempts through the first clean packet, starting at 1.
    q is the clean-packet probability for each independent attempt. """
    if not isinstance(n_trials, (int, np.integer)) or n_trials < 0:
        raise ValueError("n_trials must be a nonnegative integer.")
        
    if not 0 < q <= 1:
        raise ValueError("q must be greater than 0 and at most 1.")
        
    return rng.geometric(q, size=n_trials)

def tv_distance(pmf1, pmf2) -> float:
    """Return half the sum of absolute PMF differences.
    Both arrays must represent the same support. Truncated PMFs are
    allowed and are not renormalized."""
    pmf1 = np.asarray(pmf1, dtype=float)
    pmf2 = np.asarray(pmf2, dtype=float)
    
    if pmf1.ndim != 1 or pmf1.shape != pmf2.shape:
        raise ValueError(
            "PMFs must be one-dimensional arrays with identical shape."
        )
        
    if (
        not np.all(np.isfinite(pmf1))
        or not np.all(np.isfinite(pmf2))
        or np.any(pmf1 < 0)
        or np.any(pmf2 < 0)
    ):
        raise ValueError("PMFs must contain finite, nonnegative values.")

    return float(0.5 * np.abs(pmf1 - pmf2).sum())

def probability_comparison(mask, exact):
    """Compare an empirical event probability with its exact value.
    Return estimate, exact probability, signed difference,
    theoretical standard error, and difference divided by SE."""
    estimate = float(np.mean(mask))
    se = float(np.sqrt(exact * (1 - exact) / np.size(mask)))
    difference = estimate - exact

    if se > 0:
        z = difference / se
    elif difference == 0:
        z = 0.0
    else:
        z = float(np.copysign(np.inf, difference))

    return [estimate, exact, difference, se, z]
