"""Regression tests for Study 002 population, math, SVG and provenance."""
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree

from modular_dynamics_lab.core import harmonic_walk_mod_p
from modular_dynamics_lab.experiments import verify
from modular_dynamics_lab.feature_coordinates import coordinate_groups
from modular_dynamics_lab.feature_plots import harmonic_intersections_svg, feature_space_svg
from modular_dynamics_lab.feature_space import (
    compute_feature_data,
    harmonic_zero_stats,
    primes_below,
    run_feature_space,
    validate_feature_config,
)

CONFIG_PATH = Path(__file__).resolve().parents[1] / "experiments" / "feature_space_v1.json"


class FeatureSpaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        cls.features, cls.harmonic, cls.summary = compute_feature_data(cls.config)

    def test_prime_population(self):
        self.assertEqual(len(primes_below(10_000)), 1228)
        self.assertEqual(primes_below(13), [3, 5, 7, 11])
        self.assertEqual(self.summary["odd_prime_count"], 1228)
        self.assertEqual(len(self.features), 3682)
        self.assertEqual(len(self.harmonic), 1228)
        self.assertEqual(self.summary["base2_flat_lifts"], [1093, 3511])

    def test_feature_values_and_cross_base_coordinates(self):
        by_pair = {(r["p"], r["base"]): r for r in self.features}
        self.assertEqual(by_pair[(1093, 2)]["orders"], [364, 364, 397852])
        self.assertEqual(by_pair[(3511, 2)]["orders"], [1755, 1755, 6161805])
        self.assertEqual(by_pair[(1093, 3)]["orders"][0], 7)
        self.assertEqual(by_pair[(3511, 3)]["orders"][0], 270)
        for (p, base), record in by_pair.items():
            self.assertEqual(record["order_fraction_numerator"], record["orders"][0])
            self.assertEqual(record["order_fraction_denominator"], p - 1)
            self.assertEqual(p % base == 0, False)

    def test_harmonic_recurrence_matches_independent_inverse(self):
        for p in [3, 5, 7, 11, 1093, 3511, 9973]:
            walk = harmonic_walk_mod_p(p)
            stat = harmonic_zero_stats(p)
            self.assertEqual(stat["zero_indices"], [k for k, v in enumerate(walk) if k and v == 0])
        by_prime = {r["p"]: r for r in self.harmonic}
        self.assertEqual(by_prime[1093]["zero_indices"], [273, 546])
        self.assertEqual(by_prime[3511]["zero_indices"], [877, 1755])
        self.assertEqual(by_prime[1093]["additional_zero_count"], 0)
        self.assertEqual(by_prime[3511]["additional_zero_count"], 0)

    def test_config_contract(self):
        validate_feature_config(self.config)
        bad = dict(self.config)
        bad["prime_limit_exclusive"] = 5
        with self.assertRaises(ValueError):
            validate_feature_config(bad)
        bad = dict(self.config)
        bad["focus_primes"] = [3511, 1093]
        with self.assertRaises(ValueError):
            validate_feature_config(bad)

    def test_exact_coordinate_intersection_aggregation(self):
        groups = coordinate_groups(self.features)
        intersections = self.summary["coordinate_intersections"]
        self.assertEqual(intersections["eligible_primes"], 1227)
        self.assertEqual(intersections["distinct_coordinates"], 204)
        self.assertEqual(intersections["shared_coordinate_groups"], 81)
        self.assertEqual(intersections["primes_at_shared_coordinates"], 1104)
        self.assertEqual(intersections["maximum_multiplicity"], 184)
        self.assertEqual(sum(g["multiplicity"] for g in groups), 1227)
        self.assertEqual(sorted(p for g in groups for p in g["primes"]),
                         [p for p in primes_below(10000) if p != 3])
        group = next(g for g in groups if (g["order2_num"], g["order2_den"],
                                           g["order3_num"], g["order3_den"]) == (1, 1, 1, 1))
        self.assertEqual(group["multiplicity"], 184)
        self.assertTrue(all(g["primes"] == sorted(g["primes"]) for g in groups))
        svg = feature_space_svg(self.features, [1093, 3511])
        root = ElementTree.fromstring(svg)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        marks = root.findall('.//svg:g[@class="intersection"]', ns)
        self.assertEqual(len(marks), 204)
        self.assertEqual(max(int(m.attrib["data-multiplicity"]) for m in marks), 184)

    def test_dynamic_focus_panels_preserve_all_primes(self):
        focus = [7, 1093, 3511]
        svg = harmonic_intersections_svg(self.harmonic, focus, 14)
        root = ElementTree.fromstring(svg)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        panel_groups = root.findall('.//svg:g[@data-focus]', ns)
        self.assertEqual([int(g.attrib["data-focus"]) for g in panel_groups], focus)
        self.assertIn("p=3511", feature_space_svg(self.features, focus))

    def test_maximum_valid_neighbor_setting_keeps_panels_separate(self):
        svg = harmonic_intersections_svg(self.harmonic, [1093, 3511], 30)
        root = ElementTree.fromstring(svg)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        groups = root.findall('.//svg:g[@data-focus]', ns)
        self.assertEqual(len(groups), 2)
        rectangles = [g.find('svg:rect', ns) for g in groups]
        self.assertTrue(all(r is not None for r in rectangles))
        first_end = float(rectangles[0].attrib["y"]) + float(rectangles[0].attrib["height"])
        second_top = float(rectangles[1].attrib["y"])
        self.assertLess(first_end, second_top)
        for group, rect in zip(groups, rectangles):
            panel_end = float(rect.attrib["y"]) + float(rect.attrib["height"])
            max_y = max(float(text.attrib["y"]) for text in group.findall('svg:text', ns))
            self.assertLess(max_y, panel_end)
        self.assertGreater(float(root.attrib["height"]), second_top + float(rectangles[1].attrib["height"]))

    def test_too_many_focus_panels_rejected(self):
        cfg = dict(self.config)
        cfg["focus_primes"] = primes_below(31)[:9]
        with self.assertRaisesRegex(ValueError, "8 panels"):
            validate_feature_config(cfg)

    def test_artifacts_reproducible_and_svg_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a", Path(tmp) / "b"
            run_feature_space(CONFIG_PATH, a)
            run_feature_space(CONFIG_PATH, b)
            a_files = {p.name: p.read_bytes() for p in a.iterdir()}
            b_files = {p.name: p.read_bytes() for p in b.iterdir()}
            self.assertEqual(a_files, b_files)
            verify(a)
            self.assertIn("feature_intersections.jsonl", a_files)
            rows = [json.loads(r) for r in a_files["feature_intersections.jsonl"].decode().splitlines()]
            self.assertEqual(len(rows), 204)
            for name in ("feature_map.svg", "harmonic_intersections.svg"):
                root = ElementTree.fromstring(a_files[name])
                self.assertTrue(root.tag.endswith("svg"))
                self.assertIn(b"1093", a_files[name])
                self.assertIn(b"3511", a_files[name])
            (a / "feature_vectors.jsonl").write_text("altered\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                verify(a)


if __name__ == "__main__":
    unittest.main()
