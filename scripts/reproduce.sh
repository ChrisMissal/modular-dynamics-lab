#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e .
python -m unittest discover -s tests -v
python -m modular_dynamics_lab run --config experiments/baseline.json --output out/baseline
python -m modular_dynamics_lab verify --output out/baseline
