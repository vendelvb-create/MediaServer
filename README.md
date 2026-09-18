# MediaServer

Et ryddig, skalerbart og gjenopprettbart personlig mediebibliotek bygget rundt Jellyfin.

## Nåværende status

Cleanup- og housekeeping-fasen for første katalogmilepæl er ferdig og verifisert.

Golden baseline før fill:

| Kategori | Mapper |
|---|---:|
| Movies | 1497 |
| Series | 1285 |
| Anime | 1378 |
| Cartoons | 114 |
| **Totalt** | **4274** |

Alle katalogmappene i baseline er tomme. Golden inventory er verifisert med SHA256:

`E9FBE961FFC38E6CE90688B3CB8C8F6E7E379CD35ECAD79AF4ED3B7C36A9D1E9`

Detaljert cleanup-historikk finnes i [docs/CATALOG_CLEANUP_1500.md](docs/CATALOG_CLEANUP_1500.md).

## Aktiv lokal struktur

Den aktive arbeidsroten er:

`D:\MediaServer`

Godkjente hovedmapper:

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

Movies, Series, Anime og Cartoons er mediekategoriene. De øvrige mappene er administrasjons-/runtime-data og skal ikke bli Jellyfin-biblioteker.

## Neste milepæl: Top 1500

Første fill-fase er:

- Movies: 1497 → 1500 (+3)
- Series: 1285 → 1500 (+215)
- Anime: 1378 → 1500 (+122)
- Cartoons: 114 → 1500 (+1386)

Korrekt innhold har prioritet over å treffe et tall. Ingen filler-titler skal legges inn bare for å nå 1500.

Arbeidsflyt:

```text
PREVIEW
→ REVIEW
→ APPLY/BUILD
→ INVENTORY
→ VERIFY
→ BACKUP
→ APPROVE
→ NEXT BATCH
```

Når Top 1500 er verifisert, fortsetter katalogen i kontrollerte 500-title batches mot 10 000 per kategori.

## Kategoriregler

- **Movies**: filmer.
- **Series**: vanlige TV-serier, ikke Anime og ikke Cartoons.
- **Anime**: anime-serier. Anime Movies/standalone OVA behandles senere.
- **Cartoons**: ikke-anime animert TV-innhold, f.eks. Futurama, Archer og Bob's Burgers.

Ved usikker klassifisering: stopp eller send til review. Ikke gjett.

## Mediafiler

GitHub-repositoryet skal inneholde kode, dokumentasjon og små gjenopprettings-/baselinefiler — **aldri selve filmene, episodene eller store runtime-datasett**.

Faktiske mediafiler kan legges inn i de verifiserte katalogmappene etter at Top-1500-strukturen er låst.

## Jellyfin

Jellyfin er hovedplattformen og skal håndtere metadata, posters, sesonger/episoder, playback, resume, Direct Play/Direct Stream og transcoding ved behov.

Målklienter inkluderer PC, mobil, nettbrett og NVIDIA Shield TV Pro.

## Sikkerhetsprinsipper

1. Ingen gjetting av tittel, kategori, sesong eller filsti.
2. Ingen destruktiv handling uten preview/review når det er praktisk mulig.
3. Backup før større strukturelle endringer.
4. Ingen skriving utenfor godkjent MediaServer-root.
5. En feil skal ikke rapporteres som suksess.
6. Neste batch starter først når forrige er verifisert og godkjent.
7. GitHub lagrer ikke media, secrets eller store lokale runtime-datasett.

## Repository

- `src/` — eksisterende Python-moduler og tester.
- `docs/PROJECT_SPECIFICATION.md` — gjeldende teknisk source of truth.
- `docs/CATALOG_CLEANUP_1500.md` — historikk og verifikasjon for cleanup/baseline.
- `.gitignore` — beskytter media og lokale runtime-data mot commits.

## Langsiktig mål

Bygge et stabilt Jellyfin-bibliotek med opptil:

- 10 000 Movies
- 10 000 Series
- 10 000 Anime
- 10 000 Cartoons

utvidet i kontrollerte, verifiserte batches.
