# MediaServer — Project Specification

**Document status:** Authoritative project specification
**Project phase:** Pre-implementation / controlled scaffolding
**Current implementation status:** No production media-library build has started
**Current catalog block:** 0001–1000 — NOT STARTED
**Primary platform:** Jellyfin
**Development environment:** Windows
**Development test root:** `Desktop\MediaLibrary_Test`

---

# 1. Purpose

MediaServer is a personal media-library project designed to provide a clean, reliable and scalable library for Jellyfin.

The project must eventually support:

* Movies
* Series
* Cartoons
* Anime

The system must be usable through compatible Jellyfin clients, including:

* PC
* Mobile
* Tablet
* NVIDIA Shield TV
* Other Jellyfin-compatible clients

The project must prioritize:

1. Reliability
2. Data correctness
3. Safe filesystem operations
4. Recoverability
5. Clear organization
6. Jellyfin compatibility
7. Maintainability
8. Controlled scalability

The system must not prioritize speed at the expense of correctness or safety.

---

# 2. Authoritative Specification

This document is the authoritative technical specification for the MediaServer project.

All implementation decisions must follow this document unless a newer, explicitly approved project decision replaces a requirement.

AI tools working on the repository must read this document before making implementation decisions.

The AI must not assume that an older script, prototype or previous build file represents the current specification.

Older scripts may contain obsolete architecture, obsolete categories or obsolete rules.

If an older script conflicts with this document, this document takes priority.

---

# 3. Repository Documentation

The repository contains documentation in:

```text
docs/
```

The primary specification is:

```text
docs/PROJECT_SPECIFICATION.md
```

The documentation overview is:

```text
docs/README.md
```

The repository root contains:

```text
README.md
```

The root README is the project introduction.

The documentation README is the documentation index.

The PROJECT_SPECIFICATION is the detailed technical source of truth.

These documents must not contain contradictory requirements.

---

# 4. Current Project Status

The project is currently in the preparation and controlled-scaffolding phase.

The following must be considered complete or established before media generation begins:

* Project requirements defined
* Media categories defined
* Folder structure defined
* Block-based development strategy defined
* Backup requirements defined
* Logging requirements defined
* Path-safety requirements defined
* `.gitignore` established
* Documentation structure established
* Test environment established
* Repository reviewed by AI/QA

The following has NOT yet started:

```text
Block 0001–1000
```

No media catalog block may start until the required scaffolding and safety mechanisms have been implemented and verified.

---

# 5. Development Philosophy

The project must be developed conservatively.

The system must:

* Build one controlled block at a time
* Verify every block before proceeding
* Preserve logs
* Preserve manifests
* Create recoverable backups
* Avoid destructive operations
* Avoid guessed metadata
* Avoid guessed seasons
* Avoid writing outside the approved test root
* Stop safely when a required operation fails

The system must never continue silently after a critical failure.

---

# 6. Development Test Environment

All initial development must take place inside:

```text
Desktop\MediaLibrary_Test
```

This directory is the isolated development and testing environment.

The implementation must not automatically modify:

* Windows system directories
* Existing personal media directories
* Other drives
* Existing Jellyfin production libraries
* Other repositories
* Arbitrary user directories

The project must remain isolated until explicitly approved for production use.

---

# 7. Final Test-Root Structure

The initial test environment must use this structure:

```text
MediaLibrary_Test/
│
├── Movies/
├── Series/
├── Cartoons/
├── Anime/
│
├── _Data/
├── _Backups/
├── _Logs/
├── _Cache/
├── _Manifests/
└── _Docs/
```

This is the approved root structure.

Do not add the following categories:

```text
Music/
TV Channels/
Recommendations/
Anime Movies/
OVAs/
```

unless explicitly approved in a future project change.

---

# 8. Folder Naming Rules

Media folders use normal human-readable names.

Internal/system folders use a leading underscore.

Approved media folders:

```text
Movies
Series
Cartoons
Anime
```

Approved internal folders:

```text
_Data
_Backups
_Logs
_Cache
_Manifests
_Docs
```

Do not create variations such as:

```text
_Cashe
_Manifest
Data
Backups
logs
```

Use the exact approved spelling and capitalization.

The implementation must not silently rename these folders.

---

# 9. Movies

Movies are stored under:

```text
Movies/
```

Movies must use readable title-based folders.

Example:

```text
Movies/
└── Interstellar/
    └── Interstellar (2014).mkv
```

For movie franchises, a franchise/container folder may be used.

Example:

```text
Movies/
└── Toy Story/
    ├── Toy Story 1/
    │   └── Toy Story 1.mkv
    ├── Toy Story 2/
    │   └── Toy Story 2.mkv
    └── Toy Story 3/
        └── Toy Story 3.mkv
```

The system must not use generic names such as:

```text
Movie 0001
Movie 0002
Movie 0003
```

Catalog ranking must be stored in manifests/data rather than being the primary human-facing folder name.

---

# 10. Movie Titles and Filenames

Titles must be based on reliable metadata.

Where useful for Jellyfin identification, the year may be included in the filename.

Example:

```text
Interstellar (2014).mkv
```

The system must not invent titles.

If a title cannot be reliably identified, it must be flagged for review rather than guessed.

---

# 11. Series

Series are stored under:

```text
Series/
```

Example:

```text
Series/
└── Breaking Bad/
    ├── Season 01/
    ├── Season 02/
    ├── Season 03/
    ├── Season 04/
    └── Season 05/
```

Series are separate from Cartoons and Anime.

The system must not place animated content into Series merely because it is a television series.

---

# 12. Series Seasons

Season folders must be based on verified information.

The system must never invent seasons.

If verified information says a series has:

```text
Season 01
Season 02
Season 03
```

those seasons may be created.

If season information is unavailable or ambiguous, the system must not guess.

Instead:

* leave the season structure unresolved
* record the issue
* add it to a review manifest
* continue only if doing so is safe and does not create false information

---

# 13. Episode Organization

When actual episode files are eventually added, the preferred naming pattern is:

```text
Series Name - S01E01.ext
Series Name - S01E02.ext
Series Name - S01E03.ext
```

Example:

```text
Fairy Tail/
└── Season 01/
    ├── Fairy Tail - S01E01.mkv
    ├── Fairy Tail - S01E02.mkv
    └── Fairy Tail - S01E03.mkv
```

Correct episode naming allows Jellyfin to identify and order episodes correctly.

The project does not require manually sorting every episode inside the Jellyfin interface.

---

# 14. Playback Progress / Resume Position

Jellyfin must be allowed to preserve playback progress.

If a user watches part of a movie or episode and stops, the system must support resuming from the previous playback position when the user returns.

Example:

A movie is 2 hours long.

The user stops at:

```text
1:30:00
```

When the user returns to the same item, Jellyfin should offer or resume playback from approximately:

```text
1:30:00
```

rather than restarting from the beginning.

Playback-progress storage must not be manually overwritten by the catalog-building scripts.

The media-library builder must not delete or reset Jellyfin playback state.

Cross-client resume behavior is expected where supported by Jellyfin and its clients.

---

# 15. Cartoons

Cartoons are a separate top-level category.

Examples include:

* The Simpsons
* Family Guy
* American Dad!
* Futurama
* Other Western animated television series

Example:

```text
Cartoons/
└── Family Guy/
    ├── Season 01/
    ├── Season 02/
    └── Season 03/
```

Cartoons must not automatically be classified as Anime.

Animation alone does not mean Anime.

If classification is uncertain, the system must flag the item for review rather than guessing.

---

# 16. Anime

Anime is a separate top-level category:

```text
Anime/
```

Example:

```text
Anime/
└── Fairy Tail/
```

Anime series must not be mixed into:

```text
Series/
```

or:

```text
Cartoons/
```

Anime movies and standalone OVAs are explicitly excluded from the initial implementation.

They must not be automatically placed into separate Anime Movie or OVA directories.

These features may be considered in a later version.

---

# 17. Anime Seasons

Anime season mapping must be treated carefully.

Ranking/API entries must not automatically be interpreted as franchise seasons.

For example, the existence of:

```text
Fairy Tail
Fairy Tail: Final Series
```

does not automatically authorize the system to create:

```text
Season 01
Season 02
```

unless reliable metadata confirms the relationship.

The system must not invent anime season numbers.

Uncertain season relationships must be recorded for later review.

---

# 18. Media Categories Must Remain Separate

The four media categories have distinct purposes:

```text
Movies
Series
Cartoons
Anime
```

Rules:

* Movies are movies.
* Series are non-anime, non-cartoon television series.
* Cartoons are non-anime animated television series.
* Anime is anime television/series content.

If classification is uncertain:

```text
DO NOT GUESS.
```

Record the item for review.

---

# 19. Block-Based Development

Catalog generation is performed in blocks of exactly 1,000 ranking positions.

The intended sequence is:

```text
0001–1000
1001–2000
2001–3000
3001–4000
4001–5000
5001–6000
6001–7000
7001–8000
8001–9000
9001–10000
```

The same pattern may continue beyond 10,000 if explicitly required.

Only one block may be active at a time.

---

# 20. Block 0001–1000

The immediate first catalog block is:

```text
0001–1000
```

This block has NOT started yet.

No script may begin generating Block 0001–1000 until the required safety/scaffolding implementation has been reviewed and approved.

The system must not automatically jump to:

```text
1001–2000
```

or any later block.

---

# 21. Block Completion Requirements

A block is not considered complete merely because a script finishes without crashing.

A block is considered complete only after all required checks pass.

Required checks include:

* Build completed
* No critical errors
* Required data sources processed
* Required manifests generated
* Logs generated
* Backup completed
* Path-safety checks passed
* Folder structure verified
* Category classification reviewed
* Season information handled according to the rules
* No unexpected output directories created
* Build summary generated

Only then can the block be marked:

```text
VERIFIED
```

---

# 22. Block Progression Rule

The next block MUST NOT begin automatically.

For example:

```text
0001–1000
```

must be:

```text
COMPLETED
VERIFIED
BACKED UP
APPROVED
```

before:

```text
1001–2000
```

can begin.

If any required verification fails, development stops.

There must be no automatic progression after a failure.

---

# 23. Block State and Safety

The implementation should maintain an explicit block state.

Recommended states:

```text
NOT_STARTED
RUNNING
FAILED
COMPLETED
VERIFYING
VERIFIED
BACKED_UP
APPROVED
```

A block must never be considered verified merely because the process exited with code 0.

Verification must be explicit.

The system should prevent accidental execution of a later block when the previous block is not approved.

---

# 24. Logging

All build operations must generate logs.

Logs belong under:

```text
_Logs/
```

A log should record at minimum:

* Timestamp
* Build/block identifier
* Start time
* End time
* Operation performed
* Data sources used
* Downloads
* Cache usage
* API requests
* Retry attempts
* Errors
* Warnings
* Number of items processed
* Number of items skipped
* Final result
* Verification result

Logs must be human-readable.

Critical failures must be clearly identifiable.

---

# 25. Start Time and End Time

Every build operation must record:

```text
StartTime
EndTime
Duration
```

This allows the user to determine how long each block required.

If a process fails before an end time can be recorded normally, the failure log must still contain the last known timestamp and failure information.

---

# 26. Cache

Temporary and reusable downloaded data belongs under:

```text
_Cache/
```

Cache data must not be confused with the actual media library.

The cache should allow safe reuse of data where possible.

For example:

* downloaded API responses
* temporary metadata
* downloaded datasets
* page-level API responses

A temporary API failure should not unnecessarily destroy valid cached data.

Invalid cache entries may be discarded and re-fetched when safe.

---

# 27. Manifests

Generated catalog information belongs under:

```text
_Manifests/
```

Manifests should record information such as:

* Ranking
* Title
* Category
* Source ID
* Year
* Rating
* Vote count
* Metadata source
* Verification status
* Season information where verified
* Build/block identifier

The manifest is an internal catalog record.

The ranking should not be forced into the visible media folder name.

---

# 28. Data

Persistent project data belongs under:

```text
_Data/
```

Examples include:

```text
_Data/
├── IMDb/
├── Anime/
└── other approved project data/
```

The exact internal layout may evolve.

However, generated data must remain separate from the actual media directories.

---

# 29. Backups

Backups are mandatory.

Backups belong under:

```text
_Backups/
```

Before significant destructive or structural operations, a recoverable backup must be created where appropriate.

After a successful block, the important state of that block must be preserved.

A backup should allow recovery from:

* failed builds
* accidental modifications
* corrupted manifests
* incorrect generated structure
* failed migrations

The system must never delete the only known good backup automatically.

---

# 30. Path Safety

Path safety is a critical requirement.

All generated paths must resolve inside the approved test root:

```text
Desktop\MediaLibrary_Test
```

The implementation must prevent:

* `..` path traversal
* absolute-path escape
* accidental writes to system directories
* accidental writes to unrelated drives
* accidental writes outside the test root
* destructive operations against unrelated directories

Before writing, deleting or moving a path, the system should verify that the resolved absolute path remains inside the approved project root.

If the path cannot be safely verified:

```text
STOP.
DO NOT PERFORM THE OPERATION.
LOG THE FAILURE.
```

---

# 31. Destructive Operations

The system must be conservative with deletion.

The implementation must not automatically delete:

* existing user media
* production Jellyfin libraries
* unrelated folders
* unknown files
* backups
* files outside the test root

If cleanup is required, it must operate only on explicitly generated project output inside the test environment.

Destructive cleanup should require a clear and auditable operation.

---

# 32. API Reliability

External APIs can fail, timeout or rate-limit requests.

The implementation must support:

* Timeouts
* Retries
* Backoff
* Reasonable request pacing
* Cache reuse
* Clear error logging
* Safe failure

If an API repeatedly fails, the system must not silently fabricate missing information.

The system may retry according to an approved retry policy.

If required data remains unavailable after retries:

```text
STOP OR SAFELY DEFER THE AFFECTED OPERATION.
```

The system must clearly report what failed.

---

# 33. API Partial-Failure Rule

One failed API request must not corrupt an otherwise valid cache.

For page-based APIs, each successfully retrieved page should be cached independently where practical.

For example:

```text
_Cache/
└── Anime/
    ├── page_001.json
    ├── page_002.json
    ├── page_003.json
    └── ...
```

If page 003 fails, the system must not delete pages 001 and 002.

The system should retry page 003 rather than restarting all downloads unnecessarily.

If the required information cannot be retrieved safely, the build must stop or defer according to the block rules.

---

# 34. Final AI Development Rules and Acceptance Criteria

Any AI working on this repository must follow these rules.

## 34.1 Read First

The AI MUST read the repository before reaching conclusions.

The AI must inspect:

* Repository structure
* README.md
* docs/README.md
* PROJECT_SPECIFICATION.md
* `.gitignore`
* Existing scripts
* Existing configuration
* Existing test environment
* Relevant generated data

The AI must not reach conclusions based on one file alone.

---

## 34.2 Do Not Guess

The AI must not guess:

* Metadata
* Titles
* Categories
* Seasons
* Episode relationships
* Filesystem locations
* Project requirements

If information is unclear, the AI must identify the uncertainty.

If the uncertainty affects correctness or safety:

```text
STOP AND ASK FOR CLARIFICATION.
```

---

## 34.3 Do Not Change Architecture Just Because You Prefer Another Architecture

The AI must not rewrite or replace the architecture simply because it prefers a different design.

Existing design decisions must be respected.

Changes should only be recommended when there is a genuine technical reason.

Each recommended change should explain:

* What is wrong
* Why it matters
* Consequences
* Proposed fix
* Whether the fix is required or optional

---

## 34.4 Review Before Changing

The required order is:

```text
READ
↓
ANALYZE
↓
REPORT
↓
PROPOSE
↓
WAIT FOR APPROVAL
↓
CHANGE
↓
VERIFY
```

The AI must not silently modify the repository while performing a review.

---

## 34.5 No Premature Implementation

The AI must not begin generating:

```text
Block 0001–1000
```

until:

* Safety mechanisms exist
* Logging exists
* Backup handling exists
* Path safety exists
* Block state handling exists
* Repository scaffolding has been reviewed
* Required documentation is consistent
* The user explicitly approves implementation

---

## 34.6 Existing Repository Must Be Respected

Older prototype scripts may contain obsolete functionality.

Examples of obsolete or currently excluded categories include:

```text
TV Channels
Recommendations
Anime Movies
OVA folders
```

The AI must not reintroduce these merely because an older script contains them.

Older scripts are historical/prototype material unless explicitly approved for reuse.

---

## 34.7 Verification Before Progression

After implementation of each block:

```text
BUILD
↓
LOG
↓
VERIFY
↓
BACKUP
↓
USER APPROVAL
↓
NEXT BLOCK
```

Never:

```text
BUILD
↓
AUTOMATICALLY NEXT BLOCK
```

---

## 34.8 Jellyfin Compatibility

The resulting library must be designed for Jellyfin.

The structure should allow Jellyfin to identify:

* Movies
* Series
* Cartoons
* Anime
* Seasons
* Episodes
* Metadata

The project must not interfere with Jellyfin playback state.

Playback resume information belongs to Jellyfin/application state and must not be destroyed by catalog-generation scripts.

---

## 34.9 Client Compatibility

The project should remain compatible with Jellyfin clients on:

* PC
* Mobile
* Tablet
* NVIDIA Shield TV
* Other supported clients

Offline downloading is a future capability.

It is not part of the initial catalog-builder implementation.

---

## 34.10 Duplicate Handling

Advanced duplicate management is intentionally postponed.

The current system may perform basic safety checks against accidentally creating the same generated path twice during one operation.

A complete duplicate-detection system is a future feature.

The AI must not introduce a large duplicate-management subsystem unless explicitly requested.

---

## 34.11 `.gitignore`

The repository must maintain a `.gitignore`.

The `.gitignore` must prevent inappropriate generated or temporary files from being committed.

At minimum, project-generated temporary data should be reviewed for exclusion, including appropriate:

```text
logs
cache
temporary files
generated build artifacts
local environment files
```

The exact `.gitignore` contents must remain consistent with the repository's actual structure.

The AI must not commit secrets, credentials, tokens or private environment data.

---

## 34.12 Secrets

Secrets must never be hard-coded into source code.

This includes:

* API keys
* Tokens
* Passwords
* Authentication credentials
* Private access credentials

Secrets must use an approved secure configuration mechanism.

If a required secret mechanism is not defined, the AI must stop and ask before implementing one.

---

## 34.13 Error Handling

Errors must be explicit.

A failed operation must not be presented as successful.

The system must distinguish between:

```text
SUCCESS
WARNING
FAILED
SKIPPED
DEFERRED
```

Critical errors must stop the affected operation.

---

## 34.14 Acceptance Criteria

The project is ready to begin Block 0001–1000 only when all of the following are true:

* Repository structure is correct
* Documentation is consistent
* README is consistent
* docs/README is present and correct
* `.gitignore` is present
* `MediaLibrary_Test` exists
* Approved root folders exist
* Path-safety mechanism is implemented
* Logging mechanism is implemented
* Backup mechanism is implemented
* Block-state mechanism is implemented
* Failure handling is implemented
* No production media directory is being modified
* AI/QA review is complete
* Critical findings are resolved
* User explicitly approves starting Block 0001–1000

Until then:

```text
DO NOT BUILD THE MEDIA CATALOG.
```

---

## 34.15 Final Development Principle

The entire project follows this rule:

```text
READ
→ PLAN
→ REVIEW
→ IMPLEMENT SAFELY
→ LOG
→ VERIFY
→ BACK UP
→ GET APPROVAL
→ CONTINUE
```

Never sacrifice correctness for speed.

Never guess when reliable information is unavailable.

Never silently change project scope.

Never automatically proceed to the next 1,000-title block.

Never write outside the approved test environment.

The objective is not simply to generate thousands of folders.

The objective is to build a clean, reliable, recoverable and Jellyfin-ready personal media library that can safely grow from:

```text
0001–1000
```

to:

```text
1001–2000
2001–3000
3001–4000
4001–5000
5001–6000
6001–7000
7001–8000
8001–9000
9001–10000
```

one verified block at a time.
