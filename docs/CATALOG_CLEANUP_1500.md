# Catalog Cleanup — Top 1500 Baseline

**Status:** Active cleanup plan  
**Approved working root:** `D:\MediaServer`  
**Last verified folder counts (2026-09-16):** Movies 1500, Series 1287, Anime 1560, Cartoons 112  
**Media-file state:** The generated media folders are currently empty; cleanup operates on folder structure only.

## Goal

Before expanding the catalog further, clean and reconcile the existing folder structure so it is consistent, correctly categorized, deduplicated and ready for Jellyfin.

Preferred first milestone:

- Movies: 1500
- Series: 1500
- Anime: 1500
- Cartoons: 1500

If a category cannot be safely filled to 1500 using verified titles, correctness wins over count. Do not create filler or guess classifications.

Long-term target:

- Top 10,000 Movies
- Top 10,000 Series
- Top 10,000 Anime
- Top 10,000 Cartoons

## Working batch size

All catalog work is now performed in **500-title batches**:

- 0001–0500
- 0501–1000
- 1001–1500
- 1501–2000
- continuing in 500-title blocks to 10,000

Only one batch is worked on at a time. A batch must be previewed and verified before its fix/run phase.

## Cleanup priorities

1. Remove true duplicate empty folders.
2. Correct Anime folders misplaced under Series.
3. Correct Cartoon folders misplaced under Series.
4. Detect Series misplaced under Anime or Cartoons.
5. Correct clear malformed folder names.
6. Preserve legitimate remakes, alternate-year films and different works sharing a title.
7. Keep Anime Movies and standalone OVAs deferred until a later project phase.
8. Recount and verify all four categories after each approved cleanup run.

## Safety workflow

The required workflow is:

```text
SNAPSHOT
→ AUDIT
→ PREVIEW
→ REVIEW
→ FIX
→ NEW INVENTORY
→ VERIFY
→ APPROVE
→ NEXT BATCH
```

Preview and Fix commands should be distributed together in one package when practical, but Fix must remain blocked while unresolved BLOCK/REVIEW items exist.

## Category rules

### Movies

Movies only. Year remains significant when it distinguishes remakes or separate releases.

### Series

Non-anime, non-cartoon television/streaming series only.

### Anime

Anime series only for the current milestone. Anime Movies and standalone OVAs remain deferred.

### Cartoons

Non-anime animated television/streaming series. Generic "Animation" metadata is not sufficient by itself to classify a title as Cartoon.

## Classification rule

Do not guess.

A title collision across categories must be reviewed rather than automatically moved solely because normalized names match.

## Current cleanup history

The first verified category repair corrected 213 misplaced Series entries:

- confirmed Anime entries were moved/deduplicated into Anime
- confirmed Cartoon entries were moved into Cartoons
- the verified post-run totals became Movies 1500 / Series 1287 / Anime 1560 / Cartoons 112

Later v6/v7/v8 Top-500 attempts were **preview-only** and intentionally made no filesystem changes after their classification weaknesses were detected.

## Repository rule

This document records the active catalog-cleanup decision and supersedes older block-size/status statements that still describe 1,000-title blocks or the original pre-build state. Those older sections should be harmonized during the documentation cleanup, but this document governs current catalog work in the meantime.
