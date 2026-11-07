"""Independent SymPy cross-check not used by production code."""
from math import gcd

from sympy import n_order
from modular_dynamics_lab.core import orders_over_prime_powers

primes = [7, 1091, 1093, 1097, 3499, 3511, 3517]
bases = [2, 3, 5]
checked = 0
for p in primes:
    for base in bases:
        if gcd(p, base) != 1:
            continue
        ours = orders_over_prime_powers(base, p, 3)
        independent = [int(n_order(base, p**k)) for k in range(1, 4)]
        assert ours == independent, (p, base, ours, independent)
        checked += 1
print(f"SymPy checked {checked} prime/base combinations (3 powers each).")
