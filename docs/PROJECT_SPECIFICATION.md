# MediaServer — PROJECT SPECIFICATION v2

## 1. Project Definition

This document is the **authoritative technical specification** for the MediaServer project.

The project is a personal, clean, reliable and scalable media library designed primarily for **Jellyfin**.

The implementation must prioritize:

1. Reliability
2. Clean organization
3. Verified information
4. Safe and reversible changes
5. Backups
6. Logging
7. Jellyfin compatibility
8. Simple maintenance
9. Block-by-block development

The project MUST NOT expand its scope without explicit approval.

If an AI, script or developer is uncertain about a requirement, it MUST stop and ask for clarification rather than guessing.

---

# 2. Current Scope

The current media categories are exactly:

* Movies
* Series
* Cartoons
* Anime

The current project also requires internal folders for:

* `_Backups`
* `_Cache`
* `_Data`
* `_Logs`
* `_Manifests`
* `_Docs`

The following are **NOT currently part of the implementation**:

* Music
* TV Channels
* Recommendations
* Anime Movies
* Anime OVAs
* Anime standalone specials
* Advanced duplicate-management systems
* Automatic production migration
* Offline-download implementation

These features may be considered later, but MUST NOT be added automatically.

---

# 3. Development Environment

All initial development MUST take place inside this dedicated Desktop folder:

```text
Desktop/
└── MediaLibrary_Test/
```

`MediaLibrary_Test` is the isolated development and testing environment.

The system MUST NOT modify unrelated files, folders or existing media libraries during development.

The system MUST NOT:

* Delete existing personal files
* Move existing personal media automatically
* Modify Windows system folders
* Modify unrelated Desktop folders
* Write generated project data outside the test environment
* Assume the test folder is the final production location

Production migration is a separate future step.

---

# 4. Required Root Structure

The required structure is:

```text
MediaLibrary_Test/
├── Anime/
├── Cartoons/
├── Movies/
├── Series/
├── _Backups/
├── _Cache/
├── _Data/
├── _Logs/
├── _Manifests/
└── _Docs/
```

These names and spellings MUST remain consistent.

Media folders:

```text
Anime
Cartoons
Movies
Series
```

Internal folders:

```text
_Backups
_Cache
_Data
_Logs
_Manifests
_Docs
```

The system MUST NOT silently rename these folders or create alternative spellings such as:

```text
_Cashe
_Manifest
Backups
Data
Movie
TVShows
```

---

# 5. GitHub Documentation

The GitHub repository contains the authoritative project documentation.

The detailed specification belongs in:

```text
docs/PROJECT_SPECIFICATION.md
```

`README.md` is only a high-level project overview.

Detailed technical requirements MUST NOT depend on README.md.

The local `_Docs/` folder is for local project documentation and MUST NOT replace the GitHub specification.

---

# 6. Block-Based Development

The catalog MUST be generated in fixed blocks of 1,000 titles.

The system MUST NEVER attempt to generate the entire catalog in one operation.

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

The same 1,000-title pattern may continue beyond 10,000 if explicitly required.

## Absolute block rule

Only **ONE block may be processed at a time**.

The system MUST NOT:

* Generate multiple blocks simultaneously
* Automatically continue to the next block
* Skip a failed block
* Start the next block before verification
* Assume that a partially completed block is complete

---

# 7. Block Completion Requirements

A block is considered complete ONLY when all required checks have passed.

For example:

```text
Block 0001–1000
        ↓
Generation
        ↓
Validation
        ↓
Verification
        ↓
Logging
        ↓
Backup
        ↓
100% completion confirmation
        ↓
Only then → Block 1001–2000
```

The next block MUST NOT start until the previous block is:

* Fully generated
* Verified
* Logged
* Backed up
* Confirmed complete

If verification fails, development MUST stop.

No automatic continuation is allowed.

---

# 8. Immediate Development Priority

The immediate priority is:

```text
0001–1000
```

The system MUST complete and verify:

```text
0001–1000
```

before it is allowed to begin:

```text
1001–2000
```

The same rule applies to every later block.

For example:

```text
2001–3000
```

cannot begin until:

```text
1001–2000
```

is completely finished and verified.

---

# 9. Movies

Movies belong exclusively under:

```text
Movies/
```

Movies should use human-readable names.

The project uses a franchise-friendly organization.

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

For a standalone movie:

```text
Movies/
└── Interstellar/
    └── Interstellar (2014).mkv
```

The system MUST NOT use ranking numbers as the primary folder name.

Incorrect:

```text
Movie 0001/
Movie 0002/
Movie 0003/
```

Correct:

```text
Interstellar/
Toy Story/
The Matrix/
```

Ranking information belongs in manifests or metadata.

---

# 10. Series

Normal television and streaming series belong under:

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

Only verified seasons may be created.

The system MUST NEVER invent a season.

If reliable information confirms only Seasons 01–03, the system MUST NOT create Season 04 simply because it expects one.

---

# 11. Cartoons

Cartoons are a separate category from both normal Series and Anime.

Examples include:

* The Simpsons
* Family Guy
* American Dad!
* Futurama
* Other appropriate Western animated television series

Structure:

```text
Cartoons/
└── Family Guy/
    ├── Season 01/
    ├── Season 02/
    └── Season 03/
```

Cartoons MUST NOT automatically be placed under Anime simply because they are animated.

If classification is unclear, the system MUST flag the title for review.

The system MUST NOT guess.

---

# 12. Anime

Anime is a separate top-level category:

```text
Anime/
```

Example:

```text
Anime/
└── Fairy Tail/
    ├── Season 01/
    ├── Season 02/
    └── Season 03/
```

The current Anime scope is **series only**.

The following are explicitly excluded:

* Anime Movies
* OVAs
* Standalone specials

These may be implemented later only after explicit approval.

Anime seasons MUST NOT be guessed.

---

# 13. Season Verification

Season folders must represent real, verified seasons.

The system MUST use reliable metadata or verified source information.

The system MUST NOT create a season folder simply because:

* A show exists
* An episode count exists
* Another source suggests a season might exist
* The AI assumes a standard season structure

When season information cannot be verified, the system MUST:

1. Leave the season structure unchanged
2. Record the issue
3. Flag it for review if necessary
4. Continue only if doing so does not create incomplete or misleading data

---

# 14. Episode Organization and Jellyfin

The final library is intended to work cleanly with Jellyfin.

Episode files should use a recognizable naming structure such as:

```text
Series Name - S01E01.ext
Series Name - S01E02.ext
Series Name - S01E03.ext
```

This allows Jellyfin to identify:

* Series
* Season
* Episode
* Episode number
* Playback order

The project does NOT require manually sorting episodes inside Jellyfin when correct episode numbering is already present in the filenames.

The user may manually add episode files later.

---

# 15. Playback Resume / Continue Watching

The media experience MUST support normal Jellyfin playback-resume behavior.

If a user watches part of a movie or episode and stops, the system should allow Jellyfin to resume from the previous playback position when the user returns.

Example:

A movie is 2 hours long.

The user watches:

```text
1 hour 30 minutes
```

The user exits the movie.

When the user opens the same movie again, Jellyfin should offer continuation from approximately:

```text
1 hour 30 minutes
```

rather than forcing the movie to restart from the beginning.

The project should preserve compatibility with Jellyfin's playback-progress and resume functionality.

Playback state should work correctly across supported Jellyfin clients where Jellyfin provides that functionality.

---

# 16. Supported Clients

The library should work well with:

* PC
* Mobile
* Tablet
* NVIDIA Shield TV
* Other compatible Jellyfin clients

The initial implementation does not need to implement separate applications for each platform.

The goal is to maintain a clean Jellyfin-compatible backend/library structure.

---

# 17. Offline Downloading

Offline downloading is a future requirement.

The system should remain compatible with Jellyfin clients that support downloading where applicable.

However, offline-download functionality MUST NOT be implemented as part of the initial catalog-building system unless explicitly requested.

---

# 18. Metadata

Metadata should be obtained from reliable sources.

Potential sources include:

* IMDb
* Reliable anime metadata providers
* Jellyfin-compatible metadata providers
* Other approved sources

Metadata SHOULD be cached where practical.

The system MUST NOT invent:

* Movie titles
* Series titles
* Anime titles
* Seasons
* Episode numbers
* Release information
* Ratings
* Other factual metadata

If information cannot be reliably verified, the system must flag the problem or stop the affected operation.

---

# 19. Cache

`_Cache/` stores reusable temporary or downloaded information.

Examples:

* API responses
* Metadata responses
* Downloaded pages
* Temporary processing data
* Cached datasets

The system SHOULD reuse valid cache data.

The system MUST NOT unnecessarily download the same large datasets repeatedly.

If cached data is corrupted, the system may safely invalidate and recreate the affected cache.

---

# 20. Data

`_Data/` contains structured project data.

Examples:

```text
_Data/
├── IMDb/
├── Anime/
├── Databases/
└── Processing/
```

The exact internal structure may evolve as implementation progresses.

The `_Data/` folder MUST remain separate from the media folders.

---

# 21. Manifests

`_Manifests/` contains structured catalog information.

Examples:

```text
_Manifests/
├── Movies_0001-1000.json
├── Series_0001-1000.json
├── Cartoons_0001-1000.json
└── Anime_0001-1000.json
```

Manifests may contain:

* Ranking
* Title
* Year
* External ID
* Rating
* Genre
* Category
* Verification status
* Processing status

Ranking information should be stored here rather than forced into user-facing folder names.

---

# 22. Logging

`_Logs/` contains build and processing logs.

Every significant build operation SHOULD produce a log.

Logs should record:

* Start time
* End time
* Block number
* Data sources
* Downloads
* API calls
* Retry attempts
* Successful operations
* Failed operations
* Skipped items
* Warnings
* Final status

A failed operation MUST leave enough information to diagnose the failure.

---

# 23. API Reliability

External APIs can fail, timeout or rate-limit requests.

The system MUST therefore use safe API handling.

Where appropriate, it should support:

* Retries
* Delays between requests
* Timeouts
* Local caching
* Clear error reporting
* Safe failure

A temporary API failure MUST NOT silently produce an incomplete catalog.

If an API cannot provide required information after reasonable retries, the system must stop safely or flag the affected operation according to the block's verification rules.

Previously cached valid information should not be destroyed simply because an API is temporarily unavailable.

---

# 24. Backups

`_Backups/` contains safety copies.

Example:

```text
_Backups/
├── Block_0001-1000/
├── Block_1001-2000/
└── ...
```

A completed block SHOULD have a recoverable backup before the project moves to the next block.

Backups MUST be kept separate from the active media folders.

The backup process MUST NOT delete the only available copy of important project data.

---

# 25. Duplicate Handling

Advanced duplicate management is intentionally postponed.

The current system does not need a sophisticated duplicate-detection engine.

However, the build process MUST avoid obviously creating the exact same folder twice during one operation.

Advanced duplicate detection can be added later.

It MUST NOT become a reason to delay the current 0001–1000 implementation unless an actual data-integrity problem is discovered.

---

# 26. Verification

Every block must be verified before the next block can start.

Verification should check:

* Correct folder structure
* Correct category
* Correct title
* Correct ranking
* Verified metadata
* Verified seasons where applicable
* Expected manifests
* Expected logs
* Backup availability
* No fatal errors
* No incomplete generation

The result must be clearly marked as:

```text
COMPLETE
```

or:

```text
FAILED
```

A block MUST NOT be treated as complete if the result is uncertain.

---

# 27. Failure Handling

If a build fails:

1. Stop the affected operation.
2. Do not start the next block.
3. Preserve the logs.
4. Preserve useful cached data.
5. Identify the cause.
6. Fix the problem.
7. Re-run the affected block safely.
8. Verify the complete block again.
9. Only then proceed.

The system MUST NOT hide failures.

The system MUST NOT report success when the block is incomplete.

---

# 28. AI Development Rules

Any AI working on this repository MUST follow these rules.

### MUST

* Read the existing repository before changing code.
* Read `docs/PROJECT_SPECIFICATION.md`.
* Preserve the existing architecture unless a change is explicitly approved.
* Work one 1,000-title block at a time.
* Use the exact folder structure defined here.
* Use verified information.
* Maintain logs.
* Maintain backups.
* Fail safely.
* Clearly report errors.
* Keep changes reversible where practical.
* Stop when requirements are ambiguous.

### MUST NOT

* Invent seasons.
* Invent metadata.
* Invent titles.
* Change project scope without approval.
* Start multiple blocks simultaneously.
* Skip a failed block.
* Automatically continue after verification failure.
* Delete existing user data.
* Modify unrelated folders.
* Move production media during development.
* Add Music, TV Channels or Recommendations without approval.
* Add Anime Movies or OVAs without approval.
* Rewrite working project components unnecessarily.

---

# 29. Ambiguity Rule

If the specification does not provide enough information to make a safe decision, the AI MUST NOT guess.

The correct action is:

```text
STOP
↓
Explain what is unclear
↓
Ask for clarification
↓
Wait for approval
↓
Continue
```

This rule takes priority over speed.

---

# 30. Change Control

Major architectural changes require explicit approval.

Examples:

* Changing root folder structure
* Adding new media categories
* Changing the block size
* Changing the metadata strategy
* Moving the production library
* Adding new automation systems
* Changing how seasons are represented

An AI must not make these changes silently.

---

# 31. Production Migration

`MediaLibrary_Test` is the development environment.

The project MUST NOT assume that it is the final production location.

Production migration will happen only after the development environment has been fully tested.

The migration must preserve:

* Media structure
* Metadata
* Manifests
* Logs
* Backups
* Jellyfin compatibility

Production migration is a separate future task.

---

# 32. Current Project State

The current project is in the **development and specification phase**.

The immediate target is:

```text
Block 0001–1000
```

No later block should be generated until Block 0001–1000 has been fully completed and verified.

---

# 33. Future Features

Future features may include:

* Offline downloads
* Advanced duplicate detection
* More advanced metadata management
* Automatic episode-file organization
* Additional Jellyfin automation
* Production migration
* Additional media categories

Future features MUST remain outside the current scope until explicitly approved.

---

# 34. Final Development Principle

The project must always follow this sequence:

```text
PLAN
↓
BUILD ONE BLOCK
↓
VALIDATE
↓
VERIFY
↓
LOG
↓
BACKUP
↓
CONFIRM 100% COMPLETE
↓
ONLY THEN START NEXT BLOCK
```

The project is not designed to maximize speed.

It is designed to create a clean, reliable, maintainable and Jellyfin-ready media library that can safely grow from:

```text
0001–1000
```

to:

```text
1001–2000
```

then:

```text
2001–3000
```

and eventually:

```text
9001–10000
```

without sacrificing organization or data integrity.

**No block is considered complete until it has been verified and backed up.**
