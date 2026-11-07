# Mathematical contract

Only odd primes `p` and integer bases `a` coprime to `p` are analyzed; integer arithmetic is exact.

## Multiplicative order

The order `ord_(p^k)(a)` is the least positive `d` satisfying `a^d ≡ 1 (mod p^k)`. For odd `p`, each step from `p^k` to `p^(k+1)` retains the order or multiplies it by `p`.

For base 2, 1093 has order sequence 364 → 364 → 397852, while 3511 has 1755 → 1755 → 6161805. As an ordinary-prime control, 7 has 3 → 21 → 147.

## Fermat quotient and Wieferich condition

`q_p(a) = (a^(p-1) - 1)/p mod p`. The condition `q_p(a) = 0` is equivalent to `a^(p-1) ≡ 1 (mod p²)`. For base 2 this defines a Wieferich prime. Equality of multiplicative orders at `p` and `p²` is another equivalent characterization.

## Teichmüller lift

`w = a^p mod p²` is the unique unit congruent to `a` modulo `p` with `w^(p-1) ≡ 1 (mod p²)`. The integer representative `a` is its own lift precisely when `q_p(a) = 0`. The lift defect `delta = (w-a)/p mod p` satisfies `delta ≡ a*q_p(a) (mod p)`.

## Harmonic congruences (base 2)

Define `H_k = sum_{j=1}^k inv(j) (mod p)` and `H_0 = 0`.

- `H_((p-1)/2) ≡ -2*q_p(2) (mod p)`.
- `H_floor(p/4) ≡ -3*q_p(2) (mod p)`.

At 1093, the harmonic walk has positive zero returns at 273 and 546. At 3511, the zero returns are 877 and 1755. Both are consequences of known congruences; these are **not independent discoveries**.

## Higher-order coefficient

For `q_p(a) = 0`, define `c = (a^(p-1) - 1)/p² mod p`. For base 2, `c_1093 = 487` and `c_3511 = 51`, both nonzero. Thus the cycle grows again at `p³`.

None of these statements establishes literal physical dimensions, secrecy, or a novel cryptographic scheme.
