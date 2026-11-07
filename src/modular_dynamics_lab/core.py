"""Exact arithmetic only: no floats and no probabilistic primality claims."""
from math import gcd, isqrt


def is_prime(n: int) -> bool:
    """Deterministic trial-division primality test, appropriate for small studies."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for d in range(3, isqrt(n) + 1, 2):
        if n % d == 0:
            return False
    return True


def distinct_prime_factors(n: int) -> list[int]:
    if n < 1:
        raise ValueError("factorization requires a positive integer")
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def validate_prime_base(p: int, base: int) -> None:
    if p <= 2 or not is_prime(p):
        raise ValueError(f"p={p} must be an odd prime")
    if gcd(base, p) != 1:
        raise ValueError(f"base={base} must be coprime to p={p}")


def order_mod_prime(base: int, p: int) -> int:
    """Multiplicative order using p-1 factor reduction and Fermat's theorem."""
    validate_prime_base(p, base)
    order = p - 1
    for q in distinct_prime_factors(order):
        while order % q == 0 and pow(base, order // q, p) == 1:
            order //= q
    return order


def orders_over_prime_powers(base: int, p: int, max_power: int) -> list[int]:
    """Lift order: for odd p, each next order is old order or p*old order."""
    validate_prime_base(p, base)
    if not 1 <= max_power <= 12:
        raise ValueError("max_power must be between 1 and 12")
    period = order_mod_prime(base, p)
    orders = [period]
    for k in range(2, max_power + 1):
        modulus = p**k
        if pow(base, period, modulus) != 1:
            period *= p
        assert pow(base, period, modulus) == 1
        orders.append(period)
    return orders


def fermat_quotient_mod_p(base: int, p: int) -> int:
    """(base^(p-1)-1)/p mod p, computed using small modular powers."""
    validate_prime_base(p, base)
    residue = pow(base, p - 1, p * p)
    return ((residue - 1) // p) % p


def teichmueller_lift_mod_p2(base: int, p: int) -> int:
    validate_prime_base(p, base)
    return pow(base, p, p * p)


def lift_defect_mod_p(base: int, p: int) -> int:
    """(Teichmueller lift - chosen ordinary representative)/p, modulo p."""
    lift = teichmueller_lift_mod_p2(base, p)
    representative = base % (p * p)
    return ((lift - representative) // p) % p


def higher_order_quotient_when_wieferich(base: int, p: int) -> int | None:
    """(base^(p-1)-1)/p² mod p, defined here only when q_p(base)=0."""
    if fermat_quotient_mod_p(base, p) != 0:
        return None
    residue = pow(base, p - 1, p**3)
    return ((residue - 1) // (p * p)) % p


def harmonic_walk_mod_p(p: int) -> list[int]:
    """H_k mod p, k=0..(p-1)/2, using exact modular inverses."""
    validate_prime_base(p, 2)
    values = [0]
    total = 0
    for k in range(1, (p - 1) // 2 + 1):
        total = (total + pow(k, -1, p)) % p
        values.append(total)
    return values


def analyze_prime_base(p: int, base: int, max_power: int) -> dict:
    orders = orders_over_prime_powers(base, p, max_power)
    q = fermat_quotient_mod_p(base, p)
    teich = teichmueller_lift_mod_p2(base, p)
    return {
        "p": p,
        "base": base,
        "orders": orders,
        "growth_ratios": [orders[i] // orders[i - 1] for i in range(1, len(orders))],
        "fermat_quotient_mod_p": q,
        "wieferich_for_base": q == 0,
        "teichmueller_lift_mod_p2": teich,
        "base_is_fixed_point_mod_p2": teich == base % (p * p),
        "lift_defect_mod_p": lift_defect_mod_p(base, p),
        "higher_order_quotient_mod_p": higher_order_quotient_when_wieferich(base, p),
    }
