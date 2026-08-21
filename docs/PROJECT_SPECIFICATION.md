# MediaServer — Project Specification

**Document status:** Active project specification
**Version:** 1.0
**Primary purpose:** Define exactly how the MediaServer project must be designed, developed, tested, organized and expanded.

---

# 1. PROJECT PURPOSE

The goal of this project is to create a clean, reliable and scalable personal media library designed for **Jellyfin**.

The finished library must work well with:

* PC
* Mobile
* Tablet
* NVIDIA Shield TV
* Other compatible Jellyfin clients

The system must be designed so the library can grow safely over time without requiring the entire project to be rebuilt from scratch.

The project must prioritize:

1. Reliability
2. Clean organization
3. Correct metadata
4. Jellyfin compatibility
5. Safe backups
6. Clear logging
7. Recoverability
8. Simple maintenance
9. Controlled block-by-block expansion

Speed must never be prioritized over data correctness and project safety.

---

# 2. IMPORTANT AI INSTRUCTION

Any AI working on this repository, including Grok or another coding agent, MUST read this document before modifying the project.

The AI MUST treat this document as the current project specification.

The AI MUST NOT:

* invent requirements
* silently change the project scope
* remove existing requirements
* invent metadata
* invent seasons
* skip failed verification
* start a later block before the previous block is completely verified
* rewrite working components without a clear reason
* place generated data in arbitrary locations
* modify existing media outside the designated test environment

If the AI is uncertain about an important decision, it MUST stop and ask for clarification.

**When in doubt: STOP. Do not guess.**

---

# 3. CURRENT PROJECT SCOPE

The initial MediaServer scope contains exactly these media categories:

```text
Movies
Series
Cartoons
Anime
```

The project also requires internal support folders for:

```text
_Data
_Backups
```

The following are explicitly OUTSIDE the current scope:

* Music
* TV channels
* Recommendations
* Anime movies
* Anime OVAs
* Advanced duplicate-management systems
* Offline-download implementation
* Other media categories not explicitly approved

These features may be added later, but they MUST NOT be added automatically.

---

# 4. DEVELOPMENT ENVIRONMENT

All development and testing MUST initially happen inside a dedicated test folder on the user's Windows Desktop.

Preferred name:

```text
Desktop\MediaLibrary_Test
```

or:

```text
Desktop\MediaServer_Test
```

The exact name may be selected by the user.

The important rule is:

**The project MUST use a dedicated test directory on the Desktop before anything is considered production-ready.**

The AI MUST NOT:

* modify unrelated system directories
* overwrite existing media libraries
* modify the user's production media collection
* delete existing user data
* assume a production path
* silently move the project to another location

The test environment must be isolated and recoverable.

---

# 5. REQUIRED MEDIA STRUCTURE

The intended media structure is:

```text
Media/
├── Movies/
├── Series/
├── Cartoons/
├── Anime/
├── _Data/
└── _Backups/
```

No additional top-level media categories should be created unless explicitly requested.

---

# 6. MOVIES

Movies belong under:

```text
Media/Movies/
```

The movie organization must be clean and human-readable.

A movie folder must use the movie's real title.

Example:

```text
Media/
└── Movies/
    └── Interstellar/
        └── Interstellar (2014).mkv
```

For a movie franchise, the franchise can have its own parent folder.

Example:

```text
Media/
└── Movies/
    └── Toy Story/
        ├── Toy Story 1/
        │   └── Toy Story 1.mkv
        ├── Toy Story 2/
        │   └── Toy Story 2.mkv
        └── Toy Story 3/
            └── Toy Story 3.mkv
```

The important requirement is that the actual movie title is clearly represented.

Do NOT create generic names such as:

```text
Movie 0001
Movie 0002
Movie 0003
```

Ranking numbers MUST NOT replace the movie title.

Ranking information belongs in project metadata/manifests.

---

# 7. SERIES

Normal television series belong under:

```text
Media/Series/
```

Example:

```text
Media/
└── Series/
    └── Breaking Bad/
        ├── Season 01/
        ├── Season 02/
        ├── Season 03/
        ├── Season 04/
        └── Season 05/
```

A series folder must use the real series title.

The system MUST NOT invent seasons.

A season folder may only be created when the season can be verified from reliable information.

The system MUST NOT assume that every series has Season 01 simply because it is a series.

---

# 8. CARTOONS

Cartoons are a separate category from both normal Series and Anime.

Cartoons include Western/non-anime animated television shows such as:

* The Simpsons
* Family Guy
* American Dad!
* Futurama
* Similar animated television series

Cartoons belong under:

```text
Media/Cartoons/
```

Example:

```text
Media/
└── Cartoons/
    └── Family Guy/
        ├── Season 01/
        ├── Season 02/
        └── Season 03/
```

Animated does NOT automatically mean Anime.

If a title cannot be classified confidently as Anime or Cartoon, the AI MUST flag it for review rather than guessing.

---

# 9. ANIME

Anime is a completely separate top-level category.

Anime belongs under:

```text
Media/Anime/
```

Example:

```text
Media/
└── Anime/
    └── Fairy Tail/
        ├── Season 01/
        ├── Season 02/
        └── Season 03/
```

Only anime television/series content is included in the current scope.

The current project MUST NOT include:

* Anime movies
* OVAs
* standalone anime specials

These can be addressed later.

The AI MUST NOT invent Anime seasons.

If season information cannot be verified, it must be flagged for later review.

---

# 10. EPISODES

When actual episode files are eventually added, they should use a Jellyfin-friendly naming convention.

Example:

```text
Fairy Tail - S01E01.ext
Fairy Tail - S01E02.ext
Fairy Tail - S01E03.ext
```

The purpose is to allow Jellyfin to identify:

* series
* season
* episode
* episode number

The project should rely on correct file naming and metadata so Jellyfin can display episodes in the correct order.

Manual rearrangement of episodes inside Jellyfin should not normally be necessary when the files are correctly named.

---

# 11. WATCH PROGRESS / RESUME PLAYBACK

The Jellyfin experience must preserve playback progress.

If the user starts a movie and stops watching partway through, Jellyfin should retain the playback position.

Example:

A movie is 2 hours long.

The user stops watching at:

```text
01:30:00
```

When the user returns to the same movie, the system should allow playback to continue from approximately:

```text
01:30:00
```

rather than automatically restarting from the beginning.

The same principle applies to television episodes.

The MediaServer project must remain compatible with Jellyfin's normal watch-progress and resume functionality.

Playback progress should work across supported Jellyfin clients where Jellyfin provides that functionality.

The project must not intentionally reset playback progress when media is reorganized.

---

# 12. RANKING SYSTEM

The library will eventually contain large ranked collections.

The project must be built in blocks of exactly 1,000 titles.

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

The same pattern may continue beyond 10,000 if the user later requests it.

The ranking applies independently to:

* Movies
* Series
* Cartoons
* Anime

Ranking numbers are catalog information.

They must not replace human-readable media names.

---

# 13. ABSOLUTE BLOCK RULE

Only ONE 1,000-title block may be processed at a time.

The system MUST NOT attempt to generate:

* 10,000 titles in one operation
* 100,000 titles in one operation
* multiple 1,000-title blocks simultaneously

The first block is:

```text
0001–1000
```

The next block is:

```text
1001–2000
```

and so on.

The next block MUST NOT begin until the previous block is completely finished and verified.

---

# 14. BLOCK COMPLETION REQUIREMENTS

A block is NOT considered complete merely because the script stopped without an error.

A block is considered complete only when ALL required checks have passed.

For example, Block 0001–1000 must be:

1. Generated
2. Checked
3. Verified
4. Logged
5. Backed up
6. Checked for structural errors
7. Checked for failed data operations
8. Confirmed ready for the next block

Only then may Block 1001–2000 begin.

The AI MUST NOT automatically continue to the next block.

---

# 15. FAILURE RULE

If any important verification fails:

**STOP.**

Do not automatically continue.

Examples of reasons to stop include:

* API failure that prevents verification
* corrupted metadata
* missing required data
* incorrect folder structure
* invalid season information
* unexpected category classification
* incomplete block
* failed backup
* failed manifest generation
* unexpected script error

The AI must report:

* what failed
* where it failed
* what data was affected
* whether anything was written
* whether recovery is possible

The AI must not hide or silently ignore failures.

---

# 16. DATA SOURCES

The project may use reliable metadata sources such as:

* IMDb
* reliable anime metadata APIs
* Jellyfin-compatible metadata providers
* other sources explicitly approved by the user

The AI must distinguish between:

**verified information**

and

**assumed information**.

Assumptions must not be silently converted into project data.

If information cannot be verified, the item should be flagged for review.

---

# 17. API HANDLING

External APIs may temporarily fail, timeout or rate-limit requests.

The project should therefore support:

* retries
* delays between requests
* timeouts
* local caching
* safe failure
* clear logging

A temporary API failure must not corrupt an already completed block.

Downloaded API data should be cached whenever practical so that a failed second attempt does not require downloading everything again.

If repeated retries fail and required information cannot be verified, the current operation must stop safely.

---

# 18. CACHE

Large external datasets should not unnecessarily be downloaded again.

The project should use:

```text
_Data/
```

for:

* downloaded datasets
* API caches
* manifests
* logs
* temporary project metadata

Cached data must be clearly separated from the actual media folders.

---

# 19. BACKUPS

Backups are mandatory.

The project must maintain:

```text
_Backups/
```

separately from the active media library.

A successful block should have a recoverable backup before the next block begins.

Example:

```text
_Backups/
├── Block_0001-1000/
├── Block_1001-2000/
├── Block_2001-3000/
└── ...
```

The exact backup implementation may change later, but the principle must remain:

**A completed block must be recoverable.**

The AI MUST NOT delete old verified backups unless the user explicitly requests it.

---

# 20. LOGGING

Every build operation must produce a log.

Logs should contain, where applicable:

* start time
* end time
* block number
* source datasets
* API requests
* retry attempts
* successful operations
* failed operations
* skipped items
* generated manifests
* backup status
* final result

Logs should be stored under:

```text
_Data/Logs/
```

A failed build must leave enough information to understand what happened.

---

# 21. MANIFESTS

Each completed block should produce a manifest.

The manifest should make it possible to determine:

* ranking
* title
* category
* source ID
* metadata status
* verification status
* relevant season information

Manifests should be stored under:

```text
_Data/Manifests/
```

The manifest is the authoritative catalog record for the build process.

---

# 22. DUPLICATES

Advanced duplicate detection is intentionally postponed.

The current project does NOT require a complex duplicate-management system.

However, the build process should avoid obviously creating the exact same folder twice during the same operation.

A complete duplicate-management system may be designed later.

The AI MUST NOT spend significant development effort on advanced duplicate handling unless explicitly requested.

---

# 23. CATEGORY RULES

The four media categories are:

```text
Movies
Series
Cartoons
Anime
```

Rules:

### Movies

Feature films and movie content within the current approved scope.

### Series

Normal non-anime television series.

### Cartoons

Western/non-anime animated television series.

### Anime

Anime television/series content.

If classification is uncertain:

**DO NOT GUESS.**

Flag it for review.

---

# 24. NO UNAUTHORIZED SCOPE EXPANSION

The AI must not decide on its own to add:

* Music
* TV Channels
* Recommendations
* Anime movies
* OVAs
* Specials
* Advanced duplicate systems
* Other categories

The user must explicitly approve scope expansion.

---

# 25. JELLYFIN COMPATIBILITY

The project must be designed for Jellyfin.

The structure should make it easy for Jellyfin to identify:

* movies
* series
* seasons
* episodes
* titles
* metadata

The project should avoid unnecessary custom behavior that conflicts with normal Jellyfin library organization.

The goal is:

**Correct filesystem structure + correct metadata + Jellyfin handles presentation.**

---

# 26. CLIENT COMPATIBILITY

The finished system should work well through supported Jellyfin clients on:

* PC
* mobile
* tablet
* NVIDIA Shield TV
* other Jellyfin-compatible devices

Offline downloading is a future feature and must not be treated as a required part of the current build.

---

# 27. DEVELOPMENT SAFETY

All development should initially occur in:

```text
Desktop\MediaLibrary_Test
```

or the explicitly approved equivalent.

The AI must never assume that a folder is safe to delete.

Before destructive operations, the AI must identify exactly what will be affected.

The AI must not delete user media without explicit approval.

---

# 28. GITHUB REPOSITORY RULES

The GitHub repository is the source of truth for the project's code and documentation.

The AI must:

1. Read the repository before changing code.
2. Read `README.md`.
3. Read this specification.
4. Inspect existing scripts and structure.
5. Reuse working components where possible.
6. Avoid unnecessary rewrites.
7. Keep changes understandable.
8. Explain important changes.
9. Preserve existing functionality unless a change is explicitly required.

Documentation should be kept synchronized with important project decisions.

---

# 29. CHANGE CONTROL

If an implementation decision conflicts with this specification, the AI must stop and identify the conflict.

It must not silently choose one interpretation.

The AI should state:

```text
CONFLICT DETECTED
Current specification:
...
Requested implementation:
...
Action required:
Clarification/approval
```

The user makes the final decision.

---

# 30. REQUIRED BUILD WORKFLOW

Every block should follow this general process:

```text
1. Read project specification
2. Read existing repository
3. Check current block status
4. Check existing cache
5. Check previous backup
6. Collect required metadata
7. Verify metadata
8. Generate folders/manifests
9. Generate logs
10. Run validation
11. Create backup
12. Report results
13. STOP
```

The process must NOT automatically begin the next block.

---

# 31. FIRST BLOCK

The immediate target is:

```text
Block 0001–1000
```

The first block must be completed independently.

The AI must not start:

```text
1001–2000
```

until Block 0001–1000 has been explicitly confirmed as:

**100% complete, verified and backed up.**

---

# 32. NEXT BLOCK RULE

After Block 0001–1000 is complete, the next permitted block is:

```text
1001–2000
```

After Block 1001–2000 is complete:

```text
2001–3000
```

Then:

```text
3001–4000
4001–5000
5001–6000
6001–7000
7001–8000
8001–9000
9001–10000
```

No block may be skipped.

No blocks may be merged.

No blocks may be processed in parallel.

---

# 33. VERIFICATION CHECKLIST

Before declaring a block complete, verify:

* [ ] Correct block range
* [ ] Correct number of intended entries
* [ ] Correct categories
* [ ] Human-readable titles
* [ ] No invented seasons
* [ ] No unapproved media types
* [ ] Required metadata available
* [ ] Required manifests generated
* [ ] Logs generated
* [ ] No critical errors
* [ ] Backup completed
* [ ] Test folder remains intact
* [ ] Jellyfin-compatible structure maintained

If any critical item fails, the block is NOT complete.

---

# 34. COMPLETION STATUS

A block may only be marked:

```text
COMPLETE
```

when all required verification and backup requirements have passed.

Possible statuses are:

```text
NOT_STARTED
IN_PROGRESS
WAITING_FOR_REVIEW
FAILED
VERIFIED
BACKED_UP
COMPLETE
```

The AI must not mark an incomplete block as COMPLETE.

---

# 35. USER APPROVAL GATE

The user has final authority over moving from one block to the next.

Even if the AI believes a block is complete, it must not automatically start the next block.

The correct sequence is:

```text
Block finished
        ↓
Validation
        ↓
Backup
        ↓
Report
        ↓
STOP
        ↓
User approval
        ↓
Next block
```

---

# 36. FUTURE FEATURES

Potential future features include:

* Offline downloads
* Advanced duplicate detection
* More sophisticated metadata handling
* Automatic media-file importing
* Automatic episode renaming
* Additional Jellyfin automation
* Additional media categories
* Larger catalog sizes

These features are intentionally postponed.

They must not be implemented automatically.

---

# 37. CORE PRINCIPLE

The project follows this principle:

```text
CLEAN STRUCTURE
      ↓
VERIFIED DATA
      ↓
SAFE BUILD
      ↓
LOGGING
      ↓
BACKUP
      ↓
VERIFICATION
      ↓
USER APPROVAL
      ↓
NEXT 1000-TITLE BLOCK
```

The project is not simply trying to generate thousands of folders.

The objective is to create a **clean, reliable, maintainable and Jellyfin-ready personal media library** that can grow safely from:

```text
0001–1000
```

to:

```text
10000+
```

without sacrificing organization, correctness or recoverability.

---

# 38. FINAL AI RULE

If there is any uncertainty about:

* title
* category
* season
* metadata
* folder structure
* block status
* backup status
* scope
* destructive action

the AI must **STOP and ask**.

It must never invent an answer simply to keep the build moving.

**Correctness is more important than speed.**

**Safety is more important than automation.**

**Verification is required before progression.**

**One block at a time.**
