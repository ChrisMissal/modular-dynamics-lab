import json
import tempfile
import unittest
from pathlib import Path

from modular_dynamics_lab.experiments import run, validate_config, verify


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "experiments" / "baseline.json"


class PipelineTests(unittest.TestCase):
    def test_deterministic_artifacts_and_verification(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "run1", Path(d) / "run2"
            summary = run(CONFIG, a)
            run(CONFIG, b)
            self.assertEqual(summary["base_prime_pairs_tested"], 21)
            self.assertEqual(summary["wieferich_pairs"],
                             [{"p": 1093, "base": 2}, {"p": 3511, "base": 2}])
            self.assertEqual({f.name: f.read_bytes() for f in a.iterdir()},
                             {f.name: f.read_bytes() for f in b.iterdir()})
            verify(a)
            self.assertTrue((a / "harmonic_walks.svg").read_text().startswith("<svg"))
            (a / "cycles.jsonl").write_text("tampered", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                verify(a)

    def test_invalid_config_fails_closed(self):
        config = json.loads(CONFIG.read_text())
        config["primes"] = [1093, 9]
        with self.assertRaises(ValueError):
            validate_config(config)
        config["primes"] = [1093]
        config["seed"] = 7
        with self.assertRaises(ValueError):
            validate_config(config)


if __name__ == "__main__":
    unittest.main()
