#!/usr/bin/env bash
# Rebuild the whole database from the mod rules, then run the sanity checks.
set -euo pipefail
cd "$(dirname "$0")"
MOD="${1:-../../mods/rv}"
python3 extract.py "$MOD"
python3 ai_profile.py "$MOD"
python3 catalog.py
python3 calc.py matrix --up none          > data/matrix_allies_vs_soviets_rookie.csv
python3 calc.py matrix --up all           > data/matrix_allies_vs_soviets_upgraded.csv
python3 calc.py matrix --up all --rank 3  > data/matrix_allies_vs_soviets_elite_upgraded.csv
python3 validate.py
