# MediaServer

Personal Jellyfin media server project.

The project is designed to build a clean, reliable and scalable personal media library that can be used from PC, mobile, tablet, NVIDIA Shield TV and other compatible Jellyfin clients.

## Current Scope

The initial project contains only:

* Movies
* Series
* Cartoons
* Anime

Internal project folders:

* `_Data` — project data and metadata
* `_Backups` — backups and recovery data
* `_Logs` — build and system logs
* `_Cache` — cached external data and API responses
* `_Manifests` — generated catalog and verification manifests
* `_Docs` — project documentation

## Development Environment

All development and testing must initially take place inside:

```text
Desktop/
└── MediaLibrary_Test/
```

The test environment is isolated from any production media library.

## Development Method

The catalog is built in fixed blocks of 1,000 titles.

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

Only one block may be worked on at a time.

A block must be completed, verified, logged and backed up before the next block can begin.

If a block fails verification, development must stop until the problem has been resolved and the block has been confirmed as complete.

## Project Specification

The complete technical requirements and rules for the project are defined in:

`docs/PROJECT_SPECIFICATION.md`

That document is the primary source of truth for the project's architecture, folder structure, naming rules, verification requirements, backup rules, logging, block-based development and AI development rules.

## Current Status

**Planning and repository review phase.**

No media files are being added yet.

Block `0001–1000` must not begin until the repository, documentation, safety mechanisms, logging, backup system, path-safety rules and development scaffolding have been reviewed and approved.

## Important Rule

Do not make architectural or implementation changes simply because a different approach is preferred.

Read the existing repository and `docs/PROJECT_SPECIFICATION.md` before making conclusions or changes.

When requirements are unclear or contradictory, stop and request clarification rather than guessing.
