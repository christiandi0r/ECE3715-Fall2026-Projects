# ECE 3715 Mini-Project 1

## Probability, Bayes, and Discrete Random Variables

This repository contains Mini-Project 1 for **ECE 3715 — Probability and Statistics**.

The project models a wireless communication link that transmits 1000-bit packets over an independent bit-error channel. The notebook develops the model from basic probability and conditional probability through Binomial, Poisson, and geometric random variables, then combines the results to study retransmissions and link goodput.

## Team Members and Contributions

- **Ibrahim Elsousi** — Steps 1 & 4: Sample Space / Binomial; implemented `bsc()` and `packet_errors()`
- **Arun Nambiar** — Steps 2 & 5: Bayes / Poisson; implemented `tv_distance()`
- **Christian Ruelas** — Steps 3, 6 & 7: Independence / Geometric / Convergence; implemented `attempts_until_clean()`
- **Everyone** — Step 8, final notebook integration, README, testing, and cleanup

## Repository Contents

```text
mp1/
├── mp1.ipynb
├── mp1lib.py
└── README.md
```

- **`mp1.ipynb`** — Main Jupyter notebook. Runs the complete project from Step 1 through Step 8.
- **`mp1lib.py`** — Helper functions required by the assignment:
  - `bsc(bits, p, rng)`
  - `packet_errors(n_pkt, n_bits, p, rng)`
  - `attempts_until_clean(n_trials, q, rng)`
  - `tv_distance(pmf1, pmf2)`
- **`README.md`** — Team contributions, repository description, and runtime information.

## Project Steps

1. **Sample Space and Probability Axioms**
   - Enumerates all 16 error patterns for a 4-bit packet.
   - Compares exact probabilities with Monte Carlo estimates.
   - Verifies inclusion-exclusion.

2. **Conditional Probability and Bayes**
   - Derives the posterior probability that a flagged bit is actually in error.
   - Finds and verifies the posterior crossover point.

3. **Independence**
   - Demonstrates pairwise independence without mutual independence.
   - Examines unconditional and conditional dependence between two receiver outputs.

4. **Bernoulli Trials and the Binomial Distribution**
   - Models the number of errors in a 1000-bit packet.
   - Compares simulation results with the exact Binomial distribution.

5. **Poisson Approximation**
   - Measures the quality of the Poisson approximation using total variation distance.
   - Compares the measured distance with the Le Cam bound.

6. **Retransmissions and the Geometric Distribution**
   - Models the number of attempts required to obtain the first clean packet.
   - Verifies the memoryless property.

7. **Expectation, Variance, and Convergence**
   - Studies convergence of sample means over 200 independent experiments.
   - Compares the observed spread with the expected proportionality to `1/sqrt(N)`.

8. **Link Throughput**
   - Computes the clean-packet probability and expected retransmission count.
   - Determines the bit-error-rate requirements for acceptable goodput.
   - Compares packet lengths of 100, 1000, and 10000 bits.

## Key Results

For a 1000-bit packet:

- The link reaches **2 expected transmissions per delivered packet** at approximately `p = 6.9 × 10^-4`.
- Goodput falls to **90%** at approximately `p = 1.05 × 10^-4`.
- Shorter packets tolerate higher bit-error probabilities, while longer packets require a cleaner channel.

## Reproducibility

A single fixed random seed is chosen once near the top of the notebook using NumPy's `Generator` interface:

```python
SEED = 483271
rng = np.random.default_rng(SEED)
```

Each project step receives its own independently spawned random-number generator so that rerunning one section does not shift the random stream used by later sections.

## Runtime

The final notebook was run from a clean kernel in approximately:

**13.35 seconds**

which is well below the required five-minute runtime limit.

## Requirements

The project uses:

- Python 3
- NumPy
- SciPy
- Matplotlib
- Jupyter Notebook

## Submission Checklist

Before submitting:

1. Ensure the final notebook filename is `mp1.ipynb`.
2. Keep `mp1lib.py` in the same `mp1/` directory.
3. Restart the kernel and run all cells from top to bottom.
4. Confirm all cells run without errors.
5. Confirm all figures, tables, and printed outputs are saved in the notebook.
6. Confirm the complete runtime remains under five minutes.
