# Pre-fill Golden Baseline — 2026-09-18

This directory records the verified MediaServer state immediately before the controlled Top-1500 fill.

## Verified counts

- Movies: 1497
- Series: 1285
- Anime: 1378
- Cartoons: 114
- Total folders: 4274
- Non-empty folders: 0

Canonical `GOLDEN_inventory.csv` SHA256:

`E9FBE961FFC38E6CE90688B3CB8C8F6E7E379CD35ECAD79AF4ED3B7C36A9D1E9`

The exact local package `GoldenBaselineV1.zip` supplied for this baseline has SHA256:

`63E008AFA269E333342C9A046CFB9F1FB9ADAA325A059B8689E1E7974D13D2D1`

The package contains the canonical inventory, hash, counts, metadata, summary, zero-nonempty report and restore script.

Note: the baseline summary is an immutable snapshot captured before later housekeeping/final-prune work. Historical references in that summary (such as an older cleanup archive or an empty housekeeping directory) describe the capture-time state and do not override the later verified cleanup status in `docs/CATALOG_CLEANUP_1500.md`.

The full inventory CSV remains the authoritative folder list. Do not run restore unless its SHA256 matches the value above.
