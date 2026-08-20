# Media Server

Et ryddig, skalerbart og personlig mediebibliotek bygget for Jellyfin.

## 🎯 Hovedmål

Målet er å bygge et profesjonelt mediebibliotek som er enkelt å bruke fra:

- PC
- Mobil
- Nettbrett
- NVIDIA Shield TV Pro
- Andre Jellyfin-klienter

Biblioteket skal også kunne støtte nedlasting for offline-bruk gjennom kompatible Jellyfin-klienter. Dette implementeres senere.

---

## 📚 Bibliotek

Første versjon består kun av:

- 🎬 Movies
- 📺 Series
- 🎨 Cartoons
- 🇯🇵 Anime

Interne arbeidsdata og sikkerhetskopier holdes separat:

- `_Data`
- `_Backups`

Følgende kategorier skal **ikke** bygges inn i første versjon:

- Music
- TV Channels
- Recommendations
- Anime Movies
- OVA

Disse kan eventuelt legges til senere.

---

## 🗂️ Mappestruktur

```text
Media/
├── Movies/
├── Series/
├── Cartoons/
├── Anime/
│
├── _Data/
└── _Backups/
