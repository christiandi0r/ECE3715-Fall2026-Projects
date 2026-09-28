"""Step 1 functions; append other steps here."""
import numpy as np

def bsc(bits, p, rng):
    """Return binary input with independent flips of probability p; preserve shape."""
    bits = np.asarray(bits)
    if not 0 <= p <= 1 or not np.all((bits == 0) | (bits == 1)):
        raise ValueError("Require binary bits and 0 <= p <= 1.")
    return np.bitwise_xor(bits.astype(np.uint8), rng.random(bits.shape) < p)

def probability_comparison(mask, exact):
    """Return estimate, exact value, signed difference, null SE and z score."""
    estimate = np.mean(mask)
    se = np.sqrt(exact * (1 - exact) / np.size(mask))
    return [estimate, exact, estimate-exact, se, (estimate-exact)/se if se else 0.0]
