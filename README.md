🎬 Media Server

Et ryddig, skalerbart og personlig mediebibliotek bygget rundt Jellyfin.

Målet er å bygge et stabilt, brukervennlig og gjenopprettbart personlig hjemmemediesenter med kontrollert organisering, metadata, sikker utvikling, logging, backup og trinnvis automatisering.

🎯 Hovedmål

MediaServer skal være:

Ryddig

Stabilt

Skalerbart

Sikkert

Enkelt å bruke

Enkelt å vedlikeholde

Enkelt å sikkerhetskopiere

Enkelt å gjenopprette

Optimalisert for Jellyfin

Tilgjengelig fra PC, mobil, nettbrett og NVIDIA Shield TV Pro

Jellyfin skal brukes til å håndtere:

Filmer

TV-serier

Cartoons

Anime

Metadata

Posters

Bakgrunnsbilder

Genres

Ratings

Sesonger

Episoder

Søking

Fortsett å se

Sehistorikk

Streaming på kompatible klienter

Offline-nedlasting og fjernaksess er fremtidige funksjoner og skal ikke prioriteres før grunnsystemet er stabilt.

📚 Første bibliotekversjon

Første versjon består av fire hovedbiblioteker:

🎬 Movies

📺 Series

🎨 Cartoons

🇯🇵 Anime

Følgende skal ikke bygges som egne biblioteker i første versjon:

Music

TV Channels

Recommendations

Anime Movies

OVA

Disse kan vurderes senere etter at grunnsystemet er stabilt.

🏗️ Utviklingsprinsipp

Prosjektet skal bygges trinnvis og kontrollert.

Hovedprinsippet er:

Test → verifiser → dokumenter → backup → godkjenn → fortsett

Testmiljøet skal alltid komme før produksjonsmiljøet.

Ingen større funksjoner skal implementeres direkte i produksjon før de er testet og verifisert.

📁 Utviklings- og testmiljø

All første utvikling og testing skal foregå isolert i:

Desktop\MediaLibrary_Test

Dette er prosjektets dedikerte testmiljø.

Testmiljøet skal holdes adskilt fra eventuell produksjonsbasert mediesamling.

Ingen utviklings- eller katalogbyggingsoperasjon skal skrive til produksjonsbiblioteket eller andre uautoriserte områder.

🗂️ Godkjent mappestruktur

Testmiljøet skal bruke følgende struktur:

MediaLibrary_Test/
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

Mediemapper

Movies/ — filmer.

Series/ — vanlige TV-serier.

Cartoons/ — tegnefilmer og animert TV-innhold som ikke skal klassifiseres som Anime.

Anime/ — anime.

Interne mapper

_Data/ — intern prosjektdata og metadata.

_Backups/ — sikkerhetskopier og gjenopprettingsdata.

_Logs/ — logger og feilsøkingsinformasjon.

_Cache/ — midlertidige og gjenbrukbare cachedata.

_Manifests/ — manifests, kataloginformasjon og kontrollinformasjon.

_Docs/ — dokumentasjon som tilhører det lokale testmiljøet.

Mapper som begynner med _ er interne system-/administrasjonsmapper og skal ikke opprettes som vanlige Jellyfin-mediebiblioteker.

📦 Blokkbasert katalogbygging

Mediekatalogen skal bygges kontrollert i blokker på 1 000 titler.

Første blokk er:

0001–1000

Deretter:

1001–2000
2001–3000
3001–4000
4001–5000
5001–6000
6001–7000
7001–8000
8001–9000
9001–10000

Samme mønster kan fortsette dersom prosjektet senere utvides.

Blokkregel

Bare én blokk skal behandles om gangen.

Neste blokk skal ikke starte før den forrige blokken er:

Ferdig bygget

Logget

Verifisert

Sikkerhetskopiert

Godkjent

Systemet skal aldri automatisk hoppe videre til neste blokk etter en feil.

⛔ Block 0001–1000

Block 0001–1000 skal ikke starte før den nødvendige infrastrukturen er ferdig testet og godkjent.

Før første blokk kan starte må følgende være på plass:

Minimal scaffolding

Path-safety

Logging

Backup-mekanisme

Block-state håndtering

Feilhåndtering

Verifisering

Repository-dokumentasjon

.gitignore

QA-gjennomgang

Block 0001–1000 skal ikke startes før disse kravene er oppfylt og eksplisitt godkjent.

🧪 Teststrategi

Før massebygging skal systemet testes med små og kontrollerte eksempler.

Minimum:

Én film

Én serie

Én cartoon

Én anime

Metadata

Jellyfin-identifikasjon

Avspilling

Fortsett å se

Klienttesting

Backup

Restore

Feilhåndtering

Path-safety

Et stort bibliotek skal ikke bygges før den grunnleggende testflyten fungerer.

🎬 Movies

Movies skal organiseres med menneskelesbare titler.

Eksempel:

Movies/
└── Interstellar/
    └── Interstellar (2014).mkv

Franchiser kan organiseres i egne undermapper dersom det gir bedre struktur.

Rangeringstall skal ikke brukes som hovednavn på synlige mediemapper.

Rangering og intern kataloginformasjon skal lagres i data/manifests.

📺 Series

Series skal organiseres separat fra Movies, Cartoons og Anime.

Eksempel:

Series/
└── Breaking Bad/
    ├── Season 01/
    ├── Season 02/
    ├── Season 03/
    ├── Season 04/
    └── Season 05/

Sesonger skal baseres på verifisert informasjon.

Systemet skal aldri gjette sesongnummer.

🎨 Cartoons

Cartoons er en egen hovedkategori.

Eksempler kan være:

The Simpsons

Family Guy

Futurama

American Dad!

Animasjon alene betyr ikke at innholdet skal klassifiseres som Anime.

Ved usikker klassifisering skal elementet markeres for gjennomgang i stedet for å gjette.

🇯🇵 Anime

Anime er en egen hovedkategori:

Anime/

Anime skal ikke automatisk plasseres i Series eller Cartoons.

Anime Movies og OVA er utenfor første versjon og skal ikke automatisk opprette egne biblioteker eller undermapper.

Anime-sesonger skal kun opprettes når sesongforholdet er verifisert.

Et API-resultat eller en rangert anime-entry skal ikke automatisk tolkes som en ny franchise-sesong.

🎞️ Episode- og sesongstruktur

Når episodefiler senere implementeres, skal strukturen være kompatibel med Jellyfin.

Eksempel:

Series Name/
└── Season 01/
    ├── Series Name - S01E01.mkv
    ├── Series Name - S01E02.mkv
    └── Series Name - S01E03.mkv

Systemet skal ikke finne på episode- eller sesonginformasjon.

▶️ Playback og Resume

Jellyfin skal beholde ansvaret for brukerens playback-status.

Hvis en bruker stopper en film eller episode midt i avspillingen, skal Jellyfin kunne fortsette fra tidligere avspillingsposisjon.

Eksempel:

Film: 2:00:00
Stoppet ved: 1:30:00

Jellyfin skal kunne fortsette rundt:

1:30:00

Katalogbyggingen skal ikke slette, nullstille eller overskrive Jellyfins playback-status.

🛡️ Sikkerhet og Path Safety

Sikkerhet og datakorrekthet har prioritet over hastighet.

Systemet skal:

aldri skrive utenfor det godkjente testmiljøet

beskytte mot .. path traversal

beskytte mot feilaktige absolutte stier

forhindre utilsiktede writes til andre disker

forhindre utilsiktede writes til systemmapper

forhindre utilsiktede writes til produksjonsbibliotek

begrense destruktive operasjoner til eksplisitt genererte testdata

Før en fil skrives, flyttes eller slettes skal den endelige oppløste stien kunne verifiseres som tillatt.

Hvis dette ikke kan verifiseres sikkert:

STOP.
DO NOT PERFORM THE OPERATION.
LOG THE FAILURE.

📝 Logging

Alle viktige bygge- og systemoperasjoner skal logges.

Logger lagres i:

_Logs/

Logger skal minst kunne dokumentere:

Starttid

Sluttid

Varighet

Block-ID

Operasjon

API-kall

Nedlastinger

Retries

Warnings

Errors

Antall behandlede elementer

Antall hoppede elementer

Sluttstatus

Verifiseringsstatus

En feil skal aldri rapporteres som vellykket.

💾 Backup

Backup er en kritisk del av prosjektet.

Backup-relaterte data lagres i:

_Backups/

Backup skal på sikt kunne dekke:

Jellyfin-konfigurasjon

Systemdata

Metadata

Manifests

Dokumentasjon

Viktige konfigurasjonsfiler

Automatiseringskonfigurasjon

Backup regnes ikke som ferdig før restore faktisk er testet.

Systemet skal ikke automatisk slette den eneste kjente fungerende backupen.

⚡ Cache

Midlertidige og gjenbrukbare eksterne data lagres i:

_Cache/

Dette kan blant annet omfatte:

API-svar

Nedlastede datasett

Metadata

Page-baserte API-responser

Andre trygge midlertidige data

Gyldig cache skal ikke slettes bare fordi én API-forespørsel feiler.

📋 Manifests

Genererte katalog- og kontrollopplysninger lagres i:

_Manifests/

Manifests kan inneholde:

Rangering

Tittel

Kategori

Source ID

År

Rating

Antall stemmer

Metadata-status

Verifiseringsstatus

Sesonginformasjon

Block-ID

Manifestdata skal holdes separat fra selve mediefilene.

🌐 API og eksterne datakilder

Eksterne API-er kan feile, time out eller rate-limite.

Systemet skal derfor støtte:

Timeouts

Retries

Backoff

Rate-limit-håndtering

Caching

Tydelig logging

Sikker feilhåndtering

Systemet skal aldri oppfinne metadata dersom nødvendig informasjon ikke er tilgjengelig.

⚠️ API Partial Failure

Hvis én API-side eller forespørsel feiler, skal allerede gyldig cache ikke ødelegges.

Eksempel:

_Cache/
├── page_001.json
├── page_002.json
└── page_003.json

Hvis page_003.json feiler, skal ikke gyldige data fra page_001.json og page_002.json slettes.

Systemet skal forsøke å hente den manglende informasjonen på nytt når dette er trygt.

🚫 Ingen gjetting

Systemet skal aldri gjette:

Filnavn

Metadata

Kategorier

Sesonger

Episoder

Rangering

Filstier

API-resultater

Prosjektkrav

Hvis informasjonen er uklar, skal den markeres for gjennomgang.

Hvis usikkerheten kan føre til feil eller datatap:

STOP.
DO NOT GUESS.

🔄 Feilhåndtering

Operasjoner skal ha tydelige statuser:

SUCCESS

WARNING

FAILED

SKIPPED

DEFERRED

En feil skal ikke skjules.

En blokk skal ikke merkes som ferdig dersom kritiske operasjoner har feilet.

🧠 Metadata

Målet er at mediebiblioteket skal kunne få konsistent metadata som:

Tittel

Originaltittel

Poster

Bakgrunn

Genre

Utgivelsesår

Rating

Beskrivelse

Skuespillere

Regissør

Sesonger

Episoder

Episodebeskrivelser

Undertekster der tilgjengelig

Metadata skal ikke oppfinnes dersom datakilden ikke kan bekrefte informasjonen.

📺 Jellyfin

Jellyfin er hovedplattformen for mediebiblioteket.

Første bibliotekoppsett er:

Movies   → Filmer
Series   → TV-serier
Cartoons → Cartoons
Anime    → Anime

Jellyfin skal håndtere:

Metadata

Posters

Bakgrunnsbilder

Genres

Ratings

Sesonger

Episoder

Søking

Fortsett å se

Sehistorikk

Bibliotekvisning

Streaming

Direct Play

Direct Stream

Transcoding ved behov

Undertekster

Klienttilgang

📱 Klienter

Prosjektet skal testes på:

PC

Mobil

Nettbrett

NVIDIA Shield TV Pro

Andre kompatible Jellyfin-klienter

Det skal etter hvert testes:

1080p

4K

HDR der tilgjengelig

Direct Play

Direct Stream

Transcoding

Undertekster

Lyd

Store filer

Høy bitrate

🌐 Fjernaksess

Fjernaksess kommer etter at lokal streaming fungerer stabilt.

Målet er sikker tilgang fra:

Mobil

PC

Nettbrett

Andre kompatible Jellyfin-klienter

Fjernaksess skal ikke åpnes før:

Lokal Jellyfin fungerer

Backup er etablert

Sikkerhetsoppsett er gjennomgått

Lokal avspilling er stabil

Sikkerhet skal prioriteres foran enkel konfigurering.

🎮 Gaming-PC

MediaServer skal kunne eksistere ved siden av gaming uten unødvendig påvirkning av gaming-oppsettet.

Regler:

Ikke gjør unødvendige Windows-endringer

Ikke fjern gaming-optimaliseringer

Ikke kjør unødvendige bakgrunnsprosesser

Ikke bruk mer systemressurser enn nødvendig

Ikke endre BIOS uten konkret behov

Ikke prioriter mediaserver over gaming uten grunn

🤖 Automatisering

Automatisering skal introduseres etter at grunnsystemet fungerer.

Planlagte funksjoner inkluderer:

Automatisk metadata

Automatisk organisering

Automatisk import

Automatisk filnavngiving

Logging

Manifestoppdatering

Bibliotekkontroll

Feildeteksjon

Backup

Automatisering skal ikke gjøre irreversible endringer uten at systemet først er testet.

🧪 Produksjonskrav

Før systemet kan regnes som produksjonsklart skal følgende være oppfylt:

Jellyfin fungerer stabilt

Alle fire hovedbibliotek fungerer

Metadata fungerer

Filmer fungerer

Serier fungerer

Anime fungerer

Cartoons fungerer

PC fungerer

Mobil fungerer

Nettbrett fungerer

NVIDIA Shield TV Pro fungerer

Direct Play fungerer der det skal

Transcoding fungerer der det er nødvendig

Backup fungerer

Restore er testet

Filstruktur er dokumentert

Viktige konfigurasjoner er dokumentert

Ingen kritiske feil er kjent

🗺️ Roadmap

Fase 1 — Grunnstruktur

GitHub-repository

Root README

Dokumentasjonsstruktur

Prosjektspesifikasjon

.gitignore

Testmiljø

Godkjent mappestruktur

Fase 2 — Sikker scaffolding

Path-safety

Logging

Backup

Block-state

Feilhåndtering

Verifisering

Test av sikkerhetsmekanismer

Fase 3 — Jellyfin

Installere Jellyfin

Grunnkonfigurere Jellyfin

Koble Movies

Koble Series

Koble Cartoons

Koble Anime

Teste metadata

Teste avspilling

Teste resume

Fase 4 — Klienttesting

PC

Mobil

Nettbrett

NVIDIA Shield TV Pro

Direct Play

Direct Stream

Transcoding

1080p

4K

HDR

Undertekster

Lyd

Fase 5 — Organisering

Filmstruktur

Seriestruktur

Anime-struktur

Cartoon-struktur

Metadata

Navnestandard

Verifisering

Fase 6 — Første katalogblokk

Block 0001–1000

Bygging

Logging

Manifest

Verifisering

Backup

Godkjenning

Fase 7 — Videre blokker

1001–2000

2001–3000

3001–4000

4001–5000

5001–6000

6001–7000

7001–8000

8001–9000

9001–10000

Hver blokk behandles separat og må godkjennes før neste blokk.

Fase 8 — Backup og restore

Endelig backupstrategi

Backup av Jellyfin-konfigurasjon

Backup av metadata

Backup av systemdata

Backup av manifests

Restore-test

Dokumentere restore

Fase 9 — Fjernaksess

Velge sikker metode

Sette opp sikker tilgang

Teste mobil

Teste PC

Teste ekstern streaming

Kontrollere sikkerhet

Fase 10 — Produksjon

Godkjenne testmiljø

Fullføre backup

Fullføre Jellyfin-testing

Fullføre klienttesting

Opprette produksjonsstruktur

Full produksjonstest

Restore-test

Offisiell produksjonssetting

🚫 Funksjoner som kommer senere

Følgende skal ikke prioriteres før grunnsystemet er stabilt:

Music

TV Channels

Recommendations

Separat Anime Movies-bibliotek

OVA-bibliotek

Offline-system

Avansert automatisering

Fjernaksess

Kompleks backupautomatisering

Flere servere

Avansert brukeradministrasjon

Eventuell fremtidig utvidelse til andre medietyper

🔒 Viktige prosjektregler

Regel 1 — Test først

Alt skal testes før produksjon.

Regel 2 — Én ting om gangen

Ved feilsøking skal vi unngå å endre mange ting samtidig.

Regel 3 — Dokumenter viktige endringer

Viktige arkitekturvalg og endringer skal dokumenteres.

Regel 4 — Ikke bland media og systemdata

Systemmapper skal holdes utenfor Jellyfin-mediebibliotekene.

Regel 5 — Backup før større endringer

Viktige konfigurasjoner skal kunne gjenopprettes før større endringer.

Regel 6 — Ikke bygg for mye for tidlig

Første versjon skal være enkel og stabil.

Regel 7 — Gaming skal beskyttes

MediaServer skal ikke unødvendig påvirke gaming.

Regel 8 — Produksjon kommer sist

Testmiljøet skal godkjennes før produksjon.

Regel 9 — Ikke gjett

Manglende informasjon skal ikke erstattes med antakelser.

Regel 10 — Ikke hopp over verifisering

Neste blokk skal aldri starte før forrige blokk er verifisert og godkjent.

📖 Dokumentasjon

Den detaljerte tekniske prosjektspesifikasjonen finnes i:

docs/PROJECT_SPECIFICATION.md

Dokumentasjonsoversikten finnes i:

docs/README.md

PROJECT_SPECIFICATION.md er prosjektets tekniske source of truth.

Root README.md er den overordnede introduksjonen, statusen og roadmap-en for prosjektet.

docs/README.md er oversikten over prosjektets dokumentasjon.

Disse dokumentene skal ikke inneholde motstridende krav.

📌 Nåværende prosjektstatus

Prosjektet er i forberedelses- og scaffoldingfasen.

Følgende er definert:

Prosjektmål

Første bibliotekversjon

Testmiljø

Godkjent mappestruktur

Blokkbasert utvikling

Sikkerhetskrav

Logging

Backup

Cache

Manifests

API-feilhåndtering

Jellyfin-struktur

Roadmap

Selve massebyggingen av katalogen er ikke startet.

Block 0001–1000 er ikke startet.

Ingen senere blokk skal startes før tidligere blokk er ferdig bygget, verifisert, sikkerhetskopiert og godkjent.

🏁 Sluttmål

Det ferdige systemet skal være et komplett personlig hjemmemediesenter.

Brukeren skal kunne:

Åpne Jellyfin.

Se alle mediebibliotekene samlet.

Søke etter filmer og serier.

Se metadata og bilder.

Starte avspilling.

Fortsette der man slapp.

Bruke NVIDIA Shield TV Pro på TV.

Bruke PC.

Bruke mobil.

Bruke nettbrett.

Få automatisk metadata.

Få automatisk organisering.

Ha sikkerhetskopi.

Gjenopprette systemet ved behov.

Få sikker fjernaksess når dette er ferdig implementert.

📌 Prosjektfilosofi

MediaServer skal ikke bygges raskest mulig.

Det skal bygges riktig.

Prioriteringen er:

Stabilitet → Struktur → Testing → Verifisering → Backup → Automatisering → Sikkerhet → Produksjon

En enkel og stabil løsning er bedre enn en komplisert løsning som er vanskelig å feilsøke.

Korrekthet kommer før hastighet.

Sikkerhet kommer før automatisering.

Verifisering kommer før neste blokk.

Produksjon kommer sist.
