# MediaServer — Project Specification v3

**Status:** Active  
**Updated:** 2026-09-18  
**Source of truth:** This file

## 1. Objective

MediaServer skal bygge og vedlikeholde et ryddig, verifiserbart og gjenopprettbart Jellyfin-bibliotek med fire hovedkategorier:

- Movies
- Series
- Anime
- Cartoons

Langsiktig mål er opptil 10 000 mapper/titler per kategori, bygget kontrollert i batches.

## 2. Active root

Aktiv lokal root:

`D:\MediaServer`

Godkjent struktur:

```text
D:\MediaServer\
├── Movies\
├── Series\
├── Anime\
├── Cartoons\
├── Data\
│   └── RankingCache\
├── Backups\
├── Logs\
├── CACHE\
├── Manifests\
└── Docs\
```

Legacy-navn som `_Data`, `_Cache`, `_Backups`, `_Logs`, `_Manifests` og `MediaLibrary_Test` er ikke den aktive lokale strukturen.

## 3. Verified pre-fill baseline

Per 2026-09-18:

| Category | Count |
|---|---:|
| Movies | 1497 |
| Series | 1285 |
| Anime | 1378 |
| Cartoons | 114 |
| Total | 4274 |

Alle disse katalogmappene er tomme.

Canonical Golden inventory SHA256:

`E9FBE961FFC38E6CE90688B3CB8C8F6E7E379CD35ECAD79AF4ED3B7C36A9D1E9`

Cleanup og lokal housekeeping er ferdig. Detaljer finnes i `CATALOG_CLEANUP_1500.md`.

## 4. Top-1500 fill

Neste mål:

- Movies +3
- Series +215
- Anime +122
- Cartoons +1386

Målet er ikke å tvinge hver kategori til 1500 med dårlige kandidater. Dersom 1500 korrekte, verifiserbare titler ikke kan fastslås sikkert, skal kategorien stoppe under 1500 og avviket dokumenteres.

## 5. Batch strategy

Arbeid utføres i maksimalt 500-title batches der det er praktisk.

Standardsekvens etter Top 1500:

```text
1501–2000
2001–2500
2501–3000
...
9501–10000
```

Én batch behandles om gangen.

Required flow:

```text
PREVIEW
→ REVIEW
→ APPLY / BUILD
→ INVENTORY
→ VERIFY
→ BACKUP
→ APPROVE
→ NEXT BATCH
```

Ingen automatisk overgang til neste batch ved feil.

## 6. Classification

### Movies
Kun filmer.

### Series
Ikke-anime, ikke-cartoon TV-serier.

### Anime
Anime-serier. Anime Movies, standalone OVAs og tilsvarende spesialscope er deferred til en senere fase.

### Cartoons
Ikke-anime animert TV-innhold. Eksempler: Futurama, Archer, Bob's Burgers, Family Guy, The Simpsons.

Når klassifisering er uklar: `REVIEW`. Ikke gjett.

## 7. Naming

Mapper skal bruke menneskelesbare, kanoniske navn.

År kan legges til der det trengs for disambiguering, f.eks. `DuckTales (2017)`.

Unngå rankingnummer i synlige mappenavn.

Windows-ugyldige tegn må håndteres deterministisk. Sanitized navn skal ikke skape normaliserte duplikater.

## 8. Duplicates and collisions

Før nye mapper opprettes skal systemet kontrollere:

- exact duplicate i samme kategori
- normalized duplicate i samme kategori
- cross-category exact/normalized collision
- allerede eksisterende canonical title

Cross-category treff er ikke automatisk feil. Film/serie/anime-adaptasjoner kan legitimt dele navn og skal reviewes.

## 9. No guessing

Systemet skal aldri gjette:

- tittel
- kategori
- år
- sesongforhold
- episodeforhold
- filsti
- ranking/source-resultat

Usikkerhet som kan gi feil struktur skal føre til review/defer/stop.

## 10. Data sources

`Data\RankingCache` er den lokale gjenbrukbare source-cache som skal beholdes gjennom fill-fasen.

Store source-/rankingdatasett skal ikke committes til GitHub.

Kildebruk skal være deterministisk og dokumenterbar. Source-kandidater kan kombineres, men endelig katalogisering må følge kategorireglene.

## 11. Safety

Før destruktive eller strukturelle handlinger:

- verifiser root/path
- preview når mulig
- review plan
- backup dersom handlingen er vanskelig å reversere
- verifiser etterpå

Ingen operasjon skal skrive utenfor `D:\MediaServer` uten eksplisitt godkjenning.

Ingen cleanup-rutine skal endre faktiske mediafiler automatisk.

## 12. Logging and manifests

Runtime-data:

- `Logs\` — kortvarige kjørelogger
- `Manifests\` — inventories, preview/fix plans, verification
- `CACHE\` — midlertidig cache
- `Data\` — vedvarende kilde-/prosjektdata
- `Backups\` — lokale recoverable snapshots/archives

Gamle runtime-artifacts kan arkiveres/prunes etter at milepælen er verifisert.

## 13. Golden baseline and restore

Før større fill-faser skal en verifisert Golden Baseline beholdes.

Golden Baseline består minst av:

- canonical inventory
- SHA256
- counts/metadata
- restore-script eller tilsvarende gjenopprettingsmetode

Restore må verifisere inventory-hash før den oppretter manglende mapper.

## 14. GitHub policy

GitHub skal inneholde:

- kildekode
- tester
- dokumentasjon
- små baseline-/restore-artifacts som trengs for gjenoppbygging

GitHub skal ikke inneholde:

- filmer/episoder
- secrets
- lokale logger
- CACHE
- store RankingCache-datasett
- backup-ZIP-er
- genererte runtime-manifests som ikke er eksplisitt valgt som baseline

## 15. Media ingestion

Faktiske filmer/episoder kan legges inn etter at Top-1500-strukturen er verifisert og Golden Baseline for Top-1500 er tatt.

Scripts skal ikke slette, flytte eller overskrive eksisterende mediefiler uten en egen eksplisitt og reviewet media-migration-plan.

## 16. Jellyfin

Jellyfin skal være ansvarlig for:

- metadata
- posters/backgrounds
- season/episode display
- playback
- resume/progress
- Direct Play / Direct Stream
- transcoding ved behov

Katalogbygging skal ikke nullstille Jellyfin playback-state.

## 17. Repository code

Eksisterende Python-moduler i `src/` representerer sikkerhets-/workflow-scaffolding. Endringer i kode skal testes før bruk mot `D:\MediaServer`.

Gamle antakelser om `MediaLibrary_Test`, underscore-runtime-folders eller 1000-title blocks skal ikke tas som gjeldende krav dersom de strider mot denne spesifikasjonen.

## 18. Acceptance for next batch

En batch er ferdig først når:

- plan/build fullført
- kritiske feil = 0
- riktig kategori verifisert
- duplikat/collision review ferdig
- inventory generert
- forventede counts forstått
- backup/baseline oppdatert når nødvendig
- bruker har godkjent overgang

## 19. Immediate next steps

1. Back up pre-fill Golden Baseline artifacts to GitHub.
2. Verify repository documentation and ignore rules.
3. Fill Movies 1497 → 1500.
4. Verify Movies.
5. Fill Series 1285 → 1500.
6. Verify Series.
7. Fill Anime 1378 → 1500.
8. Verify Anime.
9. Build Cartoons toward 1500 using strict cartoon classification.
10. Create a new Top-1500 Golden Baseline before media ingestion.

## 20. Core principle

```text
READ
→ PLAN
→ PREVIEW
→ REVIEW
→ APPLY
→ VERIFY
→ BACK UP
→ APPROVE
→ CONTINUE
```

Correctness and recoverability are more important than speed or hitting a target count.
