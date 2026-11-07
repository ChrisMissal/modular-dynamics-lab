"""Command-line interface for deterministic, auditable experiments."""
import argparse
import json
from pathlib import Path

from .experiments import run, verify
from .feature_space import run_feature_space


def main() -> None:
    parser = argparse.ArgumentParser(description="Modular Dynamics Lab")
    sub = parser.add_subparsers(dest="command", required=True)
    run_cmd = sub.add_parser("run", help="Run an experiment and emit reproducible artifacts")
    run_cmd.add_argument("--config", type=Path, default=Path("experiments/baseline.json"))
    run_cmd.add_argument("--output", type=Path, default=Path("out/baseline"))
    verify_cmd = sub.add_parser("verify", help="Check SHA256 hashes of generated artifacts")
    verify_cmd.add_argument("--output", type=Path, default=Path("out/baseline"))
    feature_cmd = sub.add_parser("feature-space", help="Run Study 002 feature and intersection scan")
    feature_cmd.add_argument("--config", type=Path, default=Path("experiments/feature_space_v1.json"))
    feature_cmd.add_argument("--output", type=Path, default=Path("out/feature_space"))
    args = parser.parse_args()
    if args.command == "run":
        summary = run(args.config, args.output)
        print(json.dumps(summary, indent=2))
        print(f"Artifacts: {args.output}")
    elif args.command == "feature-space":
        summary = run_feature_space(args.config, args.output)
        print(json.dumps(summary, indent=2))
        print(f"Artifacts: {args.output}")
    else:
        verify(args.output)
        print(f"Artifact checksums verified: {args.output}")


if __name__ == "__main__":
    main()
