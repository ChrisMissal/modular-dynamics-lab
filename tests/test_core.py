import unittest

from modular_dynamics_lab.core import (
    analyze_prime_base,
    distinct_prime_factors,
    fermat_quotient_mod_p,
    harmonic_walk_mod_p,
    is_prime,
    lift_defect_mod_p,
    order_mod_prime,
    orders_over_prime_powers,
    teichmueller_lift_mod_p2,
)


class CoreTests(unittest.TestCase):
    def test_primality_and_factorization(self):
        for p in [7, 1091, 1093, 1097, 3499, 3511, 3517]:
            self.assertTrue(is_prime(p))
        for n in [-1, 0, 1, 4, 9, 1095]:
            self.assertFalse(is_prime(n))
        self.assertEqual(distinct_prime_factors(1092), [2, 3, 7, 13])

    def test_independently_recorded_orders(self):
        expected = {
            7: [3, 21, 147],
            1093: [364, 364, 397852],
            3511: [1755, 1755, 6161805],
        }
        for p, orders in expected.items():
            with self.subTest(p=p):
                self.assertEqual(orders_over_prime_powers(2, p, 3), orders)
                for k, order in enumerate(orders, 1):
                    modulus = p**k
                    self.assertEqual(pow(2, order, modulus), 1)
                    for factor in distinct_prime_factors(order):
                        self.assertNotEqual(pow(2, order // factor, modulus), 1)

    def test_wieferich_and_fixed_point_equivalence(self):
        for p in [7, 1091, 1093, 1097, 3499, 3511, 3517]:
            q = fermat_quotient_mod_p(2, p)
            lift = teichmueller_lift_mod_p2(2, p)
            defect = lift_defect_mod_p(2, p)
            self.assertEqual(defect, (2 * q) % p)
            self.assertEqual(lift == 2, q == 0)
            self.assertEqual(q == 0, p in {1093, 3511})

    def test_harmonic_congruences_and_zero_returns(self):
        for p in [7, 1091, 1093, 1097, 3499, 3511, 3517]:
            walk = harmonic_walk_mod_p(p)
            q = fermat_quotient_mod_p(2, p)
            self.assertEqual(walk[-1], (-2 * q) % p)
            self.assertEqual(walk[p // 4], (-3 * q) % p)
        self.assertEqual([k for k, v in enumerate(harmonic_walk_mod_p(1093)) if k and v == 0],
                         [273, 546])
        self.assertEqual([k for k, v in enumerate(harmonic_walk_mod_p(3511)) if k and v == 0],
                         [877, 1755])

    def test_next_level_coefficients(self):
        self.assertEqual(analyze_prime_base(1093, 2, 3)["higher_order_quotient_mod_p"], 487)
        self.assertEqual(analyze_prime_base(3511, 2, 3)["higher_order_quotient_mod_p"], 51)
        self.assertIsNone(analyze_prime_base(7, 2, 3)["higher_order_quotient_mod_p"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            order_mod_prime(2, 9)
        with self.assertRaises(ValueError):
            order_mod_prime(7, 7)
        with self.assertRaises(ValueError):
            orders_over_prime_powers(2, 1093, 0)
        self.assertEqual(pow(2, 6, 49), 15)


if __name__ == "__main__":
    unittest.main()
