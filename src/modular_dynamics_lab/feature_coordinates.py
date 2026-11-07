"""Canonical exact-rational intersection groups for cross-base order fractions."""
from collections import defaultdict
from fractions import Fraction


def coordinate_groups(rows: list[dict]) -> list[dict]:
    """Group primes by EXACT (ord_p(2)/(p-1), ord_p(3)/(p-1)).

    Float display positions must never determine whether coordinates coincide.
    Primes for which base 3 is not a unit (p=3) are omitted.
    """
    orders: dict[int, dict[int, int]] = defaultdict(dict)
    for record in rows:
        if record["base"] in (2, 3):
            orders[record["p"]][record["base"]] = record["orders"][0]
    grouped: dict[tuple[Fraction, Fraction], list[int]] = defaultdict(list)
    for p, bases in sorted(orders.items()):
        if 2 in bases and 3 in bases:
            key = (Fraction(bases[2], p - 1), Fraction(bases[3], p - 1))
            grouped[key].append(p)
    return [
        {
            "order2_num": x.numerator,
            "order2_den": x.denominator,
            "order3_num": y.numerator,
            "order3_den": y.denominator,
            "multiplicity": len(primes),
            "primes": primes,
        }
        for (x, y), primes in sorted(grouped.items())
    ]
