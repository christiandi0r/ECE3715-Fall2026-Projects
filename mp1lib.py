def bsc(bits, p, rng) -> ndarray # flip each bit independently w.p. p
def packet_errors(n_pkt, n_bits, p, rng) -> ndarray # number of errors in each packet
def attempts_until_clean(n_trials, q, rng)-> ndarray # attempts until the first clean packet,
# q = per-attempt clean probability
def tv_distance(pmf1, pmf2) -> float # total variation distance,
# both arrays over the same support
