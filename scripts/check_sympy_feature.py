"""Independent, reproducible sample of Study 002 order and harmonic results.

Chosen primes span the *entire* prime index range, plus the two focus primes.
The SymPy implementation does not reuse our multiplicative-order algorithm.
"""
from math import gcd

from sympy import n_order

from modular_dynamics_lab.core import orders_over_prime_powers
from modular_dynamics_lab.feature_space import harmonic_zero_stats, primes_below


def main() -> None:
    primes = primes_below(10_000)
    sample = sorted({*primes[::37], primes[-1], 7, 1093, 3511})
    comparisons = 0
    for p in sample:
        stat = harmonic_zero_stats(p)
        cumulative = 0
        zeros = []
        for k in range(1, (p - 1) // 2 + 1):
            cumulative = (cumulative + pow(k, -1, p)) % p
            if cumulative == 0:
                zeros.append(k)
        assert zeros == stat["zero_indices"], (p, "harmonic", zeros)
        for base in (2, 3, 5):
            if gcd(p, base) != 1:
                continue
            expected = [int(n_order(base, p**k)) for k in (1, 2, 3)]
            actual = orders_over_prime_powers(base, p, 3)
            assert expected == actual, (p, base, expected, actual)
            comparisons += 1
    print(f"Independent SymPy check: {len(sample)} sample primes, {comparisons} pairs, "
          f"{3*comparisons} order checks and {len(sample)} harmonic walks.")


if __name__ == "__main__":
    main()
