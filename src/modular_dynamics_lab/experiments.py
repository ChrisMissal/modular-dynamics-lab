"""Deterministic experiment runner and artifact checksums."""
import hashlib
from math import gcd
import json
from pathlib import Path
from typing import Any

from . import __version__
from .core import analyze_prime_base, harmonic_walk_mod_p, is_prime
from .plots import growth_svg, harmonic_svg


def json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def jsonl_bytes(rows: list[dict]) -> bytes:
    return ("".join(json.dumps(r, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False) + "\n" for r in rows)).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_config(config: dict) -> None:
    if config.get("schema_version") != 1:
        raise ValueError("Expected schema_version: 1")
    if not isinstance(config.get("study"), str) or not config["study"]:
        raise ValueError("Study name is required")
    for name in ("primes", "bases"):
        values = config.get(name)
        if not isinstance(values, list) or not values or any(type(v) is not int for v in values):
            raise ValueError(f"{name} must be a nonempty integer list")
        if values != sorted(set(values)):
            raise ValueError(f"{name} must be sorted and unique")
    if not 1 <= config.get("max_power", 0) <= 12:
        raise ValueError("max_power must be between 1 and 12")
    if any(p <= 2 or not is_prime(p) for p in config["primes"]):
        raise ValueError("All primes must be odd primes")
    if any(b < 2 for b in config["bases"]):
        raise ValueError("All bases must be >= 2")
    if not isinstance(config.get("harmonic_walk"), bool):
        raise ValueError("harmonic_walk must be a boolean")
    if not isinstance(config.get("visualized_primes"), list):
        raise ValueError("visualized_primes must be a list")
    if any(p not in config["primes"] for p in config["visualized_primes"]):
        raise ValueError("visualized_primes must be in primes")
    if config.get("seed", None) is not None:
        raise ValueError("This deterministic experiment has no RNG: seed must be null")


def run(config_path: Path, output_dir: Path) -> dict:
    config_raw = config_path.read_bytes()
    config = json.loads(config_raw)
    validate_config(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, bytes] = {}
    # Skip non-unit bases; multiplication by a non-unit has no multiplicative order.
    pairs = [analyze_prime_base(p, b, config["max_power"])
             for p in config["primes"] for b in config["bases"] if gcd(p, b) == 1]
    outputs["cycles.jsonl"] = jsonl_bytes(pairs)
    harmonic_rows: list[dict] = []
    walks: dict[int, list[int]] = {}
    if config["harmonic_walk"]:
        for p in config["primes"]:
            walk = harmonic_walk_mod_p(p)
            walks[p] = walk
            harmonic_rows.append({
                "p": p,
                "zero_return_indices": [k for k, v in enumerate(walk) if k and v == 0],
                "half_harmonic_mod_p": walk[-1],
                "quarter_harmonic_mod_p": walk[p // 4],
                "length": len(walk) - 1,
            })
    outputs["harmonic.jsonl"] = jsonl_bytes(harmonic_rows)
    if pairs:
        svg = growth_svg(pairs, config["visualized_primes"])
        if svg:
            outputs["cycle_growth.svg"] = svg.encode("utf-8")
    if walks:
        svg = harmonic_svg(walks, config["visualized_primes"])
        if svg:
            outputs["harmonic_walks.svg"] = svg.encode("utf-8")
    summary = {
        "schema_version": 1,
        "study": config["study"],
        "primes_tested": len(config["primes"]),
        "base_prime_pairs_tested": len(pairs),
        "wieferich_pairs": [{"p": r["p"], "base": r["base"]}
                            for r in pairs if r["wieferich_for_base"]],
        "note": "Equivalent conditions are consistency checks, not independent discoveries.",
    }
    outputs["summary.json"] = json_bytes(summary)
    manifest = {
        "schema_version": 1,
        "experiment_version": __version__,
        "input_config_sha256": sha256(config_raw),
        "input_config": config,
        "files_sha256": {name: sha256(data) for name, data in sorted(outputs.items())},
        "notes": "No RNG, wall clock, or host-specific paths in generated results.",
    }
    for name, data in outputs.items():
        (output_dir / name).write_bytes(data)
    (output_dir / "manifest.json").write_bytes(json_bytes(manifest))
    return summary


def verify(output_dir: Path) -> None:
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files_sha256"].items():
        actual = sha256((output_dir / name).read_bytes())
        if expected != actual:
            raise ValueError(f"SHA256 mismatch: {name}")
