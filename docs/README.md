# MediaServer documentation

Dette er dokumentasjonsindeksen for MediaServer.

## Gjeldende dokumenter

### [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md)
Teknisk source of truth for dagens arkitektur, sikkerhetsregler, katalogstruktur og fill/rebuild-prosess.

### [CATALOG_CLEANUP_1500.md](CATALOG_CLEANUP_1500.md)
Detaljert historikk for cleanup av den første katalogen, Global Final Audit, Golden Baseline, housekeeping og Final Prune.

## Verifisert pre-fill baseline — 2026-09-18

- Movies: 1497
- Series: 1285
- Anime: 1378
- Cartoons: 114
- Total: 4274
- Non-empty folders: 0
- Golden inventory SHA256:
  `E9FBE961FFC38E6CE90688B3CB8C8F6E7E379CD35ECAD79AF4ED3B7C36A9D1E9`

Neste operative fase er kontrollert fill til 1500 i alle fire kategorier.

Git-historikken beholder eldre arkitektur og tidligere planer. De skal ikke brukes som gjeldende krav dersom de strider mot PROJECT_SPECIFICATION.md.
