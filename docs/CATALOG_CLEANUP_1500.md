# Catalog Cleanup — Top 1500 Baseline

**Status:** Active cleanup plan  
**Approved working root:** `D:\MediaServer`  
**Last verified folder counts:** Movies 1497, Series 1285, Anime 1447, Cartoons 114 (2026-09-18)  
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

## Working order

Cleanup is handled one category at a time to reduce cross-category mistakes:

1. Movies
2. Series
3. Anime
4. Cartoons
5. Final cross-category verification
6. Fill verified gaps toward 1500 per category where possible

## Working batch size

All later catalog expansion is performed in **500-title batches**:

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
→ NEXT CATEGORY/BATCH
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

### Verified category repair — 2026-09-16

The first verified category repair corrected 213 misplaced Series entries:

- confirmed Anime entries were moved/deduplicated into Anime
- confirmed Cartoon entries were moved into Cartoons
- verified post-run totals became Movies 1500 / Series 1287 / Anime 1560 / Cartoons 112

Later v6/v7/v8 Top-500 attempts were **preview-only** and intentionally made no filesystem changes after their classification weaknesses were detected.

### Movies cleanup v1 — VERIFIED 2026-09-18

Movies cleanup was handled separately and is now verified.

Before:

- Movies folders: 1500
- all folders empty

Applied safe fixes:

- deleted wrong-year duplicate `Arsenic and Old Lace 1942`; kept `Arsenic and Old Lace 1944`
- deleted wrong-year duplicate `His Girl Friday 1939`; kept `His Girl Friday 1940`
- deleted wrong-year duplicate `Uri_ The Surgical Strike 2018`; kept `Uri_ The Surgical Strike 2019`
- renamed `Apollo 13 PG` → `Apollo 13 1995`

Verification:

- 3 empty wrong-year duplicates deleted
- 1 malformed empty folder renamed
- no blocked actions
- no duplicate folder names introduced
- all remaining Movie folders are empty
- Movies folders after fix: **1497**

Known near-duplicate/remake groups remain intentionally untouched because they are legitimate separate works or require review.

Movies is considered structurally cleaned for this pass. Filling the three verified gaps back toward 1500 is deferred until the existing categories have all been cleaned.

### Series cleanup v2 — VERIFIED 2026-09-18

Series cleanup v2 was applied and verified.

Before:

- Series: 1287
- Cartoons: 112

Applied safe fixes:

- `Dirin Dirin`: Series → Cartoons
- `Sugarland`: Series → Cartoons

Verification:

- 2 folders moved to Cartoons
- 0 blocked actions
- review-only titles such as `The Heroes` were untouched
- Series after: **1285**
- Cartoons after: **114**

The earlier Series v1 preview was intentionally not run because its safe plan contained no actionable changes.

## Next active category

**Anime**

The Anime pass must focus on:

- duplicate Anime folders
- Series/Cartoon titles misplaced in Anime
- malformed Anime names
- franchise/season naming collisions
- keeping Anime Movies and standalone OVAs deferred
- safe empty-folder changes only after preview and review

## Repository rule

This document records the active catalog-cleanup decision and supersedes older block-size/status statements that still describe 1,000-title blocks or the original pre-build state. Those older sections should be harmonized during the documentation cleanup, but this document governs current catalog work in the meantime.


### Anime cleanup v2 — VERIFIED 2026-09-18

Anime cleanup v2 was applied and independently verified against the before/after inventories and the hashed preview plan.

Before:

- Anime: 1560
- all Anime folders empty

Applied safe fix:

- removed 113 empty top-level Anime variants whose names explicitly contained Season / Part / Cour / Final Season markers and whose exact base top-level folder already existed

Verification:

- preview plan rows: 113
- fix result rows: 113
- successful status: `DELETED_EMPTY_TOPLEVEL_VARIANT` = 113
- preview SHA256 matched the reviewed plan
- before inventory: 1560
- after inventory: 1447
- exactly 113 folders removed
- 0 unexpected removals
- 0 unexpected additions
- all base folders preserved
- 0 exact duplicate folder names after the fix
- all remaining Anime folders still empty
- Anime Movies / OVA / Specials were untouched
- base-missing variants were untouched

Anime is not yet considered fully cleaned. A final Anime review must still cover remaining franchise/arc naming variants, unmatched titles, naming anomalies and any legitimate cross-category collisions before the category is locked.
