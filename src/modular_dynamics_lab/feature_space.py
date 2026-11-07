"""Study 002: exact prime feature vectors and harmonic zero-intersection statistics.

Generated artifacts are sorted, deterministic, and independent of wall clock or host.
"""
from collections import Counter
from math import gcd, isqrt
import json
from pathlib import Path

from . import __version__
from .core import analyze_prime_base, distinct_prime_factors, fermat_quotient_mod_p
from .experiments import json_bytes, jsonl_bytes, sha256
from .feature_plots import feature_space_svg, harmonic_intersections_svg


def primes_below(limit: int) -> list[int]:
    """Odd primes strictly below limit, using an exact sieve of Eratosthenes."""
    if limit <= 3:
        return []
    sieve = bytearray(b"\x01") * limit
    sieve[0:2] = b"\x00\x00"
    for candidate in range(2, isqrt(limit - 1) + 1):
        if sieve[candidate]:
            for multiple in range(candidate * candidate, limit, candidate):
                sieve[multiple] = 0
    return [p for p in range(3, limit, 2) if sieve[p]]


def harmonic_zero_stats(p: int) -> dict:
    """Zero intersections of H_k mod p for 1 <= k <= (p-1)/2.

    Uses inv[k] = -(p//k)*inv[p%k] mod p; cross-check separately against pow(k,-1,p).
    These values are discrete modular residues, not continuous curves.
    """
    half = (p - 1) // 2
    inverse = [0] * (half + 1)
    inverse[1] = 1
    total = 0
    returns: list[int] = []
    for k in range(1, half + 1):
        if k > 1:
            inverse[k] = (-(p // k) * inverse[p % k]) % p
        total = (total + inverse[k]) % p
        if total == 0:
            returns.append(k)
    q = fermat_quotient_mod_p(2, p)
    quarter = p // 4
    forced = sorted(set([quarter, half])) if q == 0 else []
    extra = [k for k in returns if k not in forced]
    # In the study all selected primes are odd. The identities are exact.
    assert total == (-2 * q) % p
    if q == 0:
        assert all(k in returns for k in forced if k >= 1)
    return {
        "p": p,
        "half_length": half,
        "quarter_index": quarter,
        "zero_indices": returns,
        "zero_return_count": len(returns),
        "forced_zero_indices": [k for k in forced if k >= 1],
        "additional_zero_indices": extra,
        "additional_zero_count": len(extra),
        "is_base2_wieferich": q == 0,
    }


def validate_feature_config(config: dict) -> None:
    if config.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if not isinstance(config.get("study"), str) or not config["study"]:
        raise ValueError("study name required")
    limit = config.get("prime_limit_exclusive")
    if type(limit) is not int or not 10 <= limit <= 100_000:
        raise ValueError("prime_limit_exclusive must be 10..100000")
    bases = config.get("bases")
    if not isinstance(bases, list) or not bases or any(type(x) is not int for x in bases):
        raise ValueError("bases must be a nonempty list of integers")
    if bases != sorted(set(bases)) or any(b < 2 for b in bases) or 2 not in bases or 3 not in bases:
        raise ValueError("bases must be unique sorted integers including 2 and 3")
    if config.get("max_power") != 3:
        raise ValueError("Study 002 currently requires max_power=3")
    if config.get("seed") is not None:
        raise ValueError("no randomness used: seed must be null")
    focus = config.get("focus_primes")
    if not isinstance(focus, list) or not focus or any(type(x) is not int for x in focus):
        raise ValueError("focus_primes must be a nonempty integer list")
    primes = set(primes_below(limit))
    if focus != sorted(set(focus)) or any(p not in primes for p in focus):
        raise ValueError("focus_primes must be sorted distinct primes under the limit")
    radius = config.get("comparison_neighbor_count")
    if type(radius) is not int or not 1 <= radius <= 30:
        raise ValueError("comparison_neighbor_count must be 1..30")


def compute_feature_data(config: dict) -> tuple[list[dict], list[dict], dict]:
    validate_feature_config(config)
    primes = primes_below(config["prime_limit_exclusive"])
    features: list[dict] = []
    harmonics: list[dict] = []
    for p in primes:
        h = harmonic_zero_stats(p)
        harmonics.append(h)
        factors = distinct_prime_factors(p - 1)
        for base in config["bases"]:
            if gcd(base, p) != 1:
                continue
            r = analyze_prime_base(p, base, 3)
            r["order_fraction_numerator"] = r["orders"][0]
            r["order_fraction_denominator"] = p - 1
            r["p_minus_1_distinct_prime_factors"] = factors
            r["is_primitive_root_mod_p"] = r["orders"][0] == p - 1
            features.append(r)
    base2 = [r for r in features if r["base"] == 2]
    summary = {
        "schema_version": 1,
        "study": config["study"],
        "odd_prime_count": len(primes),
        "prime_base_vector_count": len(features),
        "harmonic_walk_count": len(harmonics),
        "prime_limit_exclusive": config["prime_limit_exclusive"],
        "base2_flat_lifts": [r["p"] for r in base2 if r["growth_ratios"][0] == 1],
        "base2_harmonic_return_histogram": {str(k): v for k, v in
                sorted(Counter(h["zero_return_count"] for h in harmonics).items())},
        "focus_profiles": [
            {"p": h["p"], "zero_indices": h["zero_indices"],
             "additional_zero_indices": h["additional_zero_indices"]}
            for h in harmonics if h["p"] in config["focus_primes"]
        ],
        "caveat": "Zero-return coincidences at p/4 and (p-1)/2 for a base-2 Wieferich prime are guaranteed by known congruences; exploratory visual clustering is not proof of new structure.",
    }
    return features, harmonics, summary


def run_feature_space(config_path: Path, output_dir: Path) -> dict:
    raw = config_path.read_bytes()
    config = json.loads(raw)
    features, harmonic, summary = compute_feature_data(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "feature_vectors.jsonl": jsonl_bytes(features),
        "harmonic_stats.jsonl": jsonl_bytes(harmonic),
        "intersection_summary.json": json_bytes(summary),
        "feature_map.svg": feature_space_svg(features, config["focus_primes"]).encode("utf-8"),
        "harmonic_intersections.svg": harmonic_intersections_svg(
            harmonic, config["focus_primes"], config["comparison_neighbor_count"]
        ).encode("utf-8"),
    }
    manifest = {
        "schema_version": 1,
        "engine_version": __version__,
        "configuration_sha256": sha256(raw),
        "configuration": config,
        "files_sha256": {name: sha256(contents) for name, contents in sorted(outputs.items())},
        "notes": "Deterministic exact arithmetic; SVG positions are derived display coordinates, not mathematical measurements.",
    }
    for name, content in outputs.items():
        (output_dir / name).write_bytes(content)
    (output_dir / "manifest.json").write_bytes(json_bytes(manifest))
    return summary
