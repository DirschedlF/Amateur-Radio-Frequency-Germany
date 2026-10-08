# 📡 Amateur Radio Frequency Germany

Sortierbare Übersicht aller deutschen Amateurfunk-Frequenzbereiche (Langwelle bis 275 GHz und darüber) für die Klassen **A, E und N** nach Anlage 1 der Amateurfunkverordnung (AFuV), ergänzt um den **IARU-Region-1-Bandplan** für HF, VHF und UHF.

![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4-06B6D4?logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> ⚠️ **Angaben ohne Gewähr.** Inoffizielles Hobbyprojekt, keine Rechtsberatung. Verbindlich ist ausschließlich die amtliche Fassung der AFuV. See [Disclaimer](#disclaimer--haftungsausschluss).

## 🌐 Live Demo

**https://dirschedlf.github.io/Amateur-Radio-Frequency-Germany/**

## ✨ Features

- All 45 rows of Anlage 1 AFuV (3. AFuV-Änderung, BGBl. 2024 I Nr. 175, class N included)
- Compare maximum power (PEP / ERP / EIRP) for classes A, E and N side by side
- Status primary / secondary, bandwidth and usage rules (Teil B, Nr. 1–17) per row
- Satellite service notes (primary / secondary) per band
- Sort by any column, full-text search (`/` shortcut), filters for class, status and frequency range
- CSV export (semicolon, UTF-8 BOM, Excel-ready) and print layout (A4 landscape)
- Info panels: reading guide, satellite explanation, Teil B, further rules (BEMFV, AFuV §§ 11/16/17), sources
- **New in 1.1:** IARU Region 1 band plan view (HF 2200 m–10 m, VHF 6 m/4 m/2 m, UHF 70 cm/23 cm/13 cm): segment bar chart, max. bandwidth, mode and usage per segment, and for each segment whether Anlage 1 grants it to class A, E or N
- Band plan is a recommendation, not law: clearly labelled in the app, with the source version shown
- Prominent disclaimer banner ("Angaben ohne Gewähr")
- Standalone single-file HTML build that works offline

## 🚀 Quick Start

```bash
git clone https://github.com/DirschedlF/Amateur-Radio-Frequency-Germany.git
cd Amateur-Radio-Frequency-Germany
npm install
npm run dev            # http://localhost:3000
```

```bash
npm run build              # GitHub Pages build -> dist/
npm run build:standalone   # single HTML file -> dist-standalone/
npm run lint
```

## 💾 Offline / Standalone Version

A **single self-contained HTML file** is available as a release asset:

**[⬇ Download Standalone HTML](https://github.com/DirschedlF/Amateur-Radio-Frequency-Germany/releases/latest)**

Download `Amateur-Radio-Frequency-Germany-vX.X.X-standalone.html` and open it in your browser. No server, no installation, no internet required.

## 🧭 Usage

1. Search or filter by class (A/E/N), status (P/S) or frequency range.
2. Click a column header to sort. Power sorts by numeric watt value.
3. Export the current view as CSV or print it.
4. Open the info panels for Teil B rules, satellite notes and sources.
5. Switch to **Bandplan IARU Region 1** (also reachable via `#bandplan`), pick a band and optionally filter by class.

## 🛠️ Tech Stack

React 18 · Vite 7 · Tailwind CSS 3.4 · lucide-react · vite-plugin-singlefile · ESLint · GitHub Actions + Pages

## 📁 Project Structure

```
src/
  components/   FrequencyOverview, BandplanView, InfoPanels, DisclaimerBanner
  data/         anlage1.json, teilB.json, bandplan.json, meta.js
  utils/        notes.js, bandplan.js, exportCsv.js
scripts/        gen_bandplan.py (generates src/data/bandplan.json)
docs/           DESIGN_DECISIONS.md, DATA_SOURCES.md
.github/workflows/deploy.yml
```

## 🔄 Updating the Data

See [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md). In short: compare the official text on gesetze-im-internet.de with `src/data/anlage1.json` and `teilB.json`, then update `src/data/meta.js` (`lawVersion`, `checkedOn`).

## 🗺️ Roadmap

- [x] Anlage 1 table with sort, filter, CSV and print (v1.0)
- [x] Disclaimer in app and README
- [ ] PWA / offline install
- [ ] GitHub Action to monitor changes of Anlage 1
- [ ] English UI toggle
- [x] Band plan layer (IARU Region 1 HF/VHF/UHF, v1.1)
- [ ] Update band plans to the latest IARU versions, add DARC 2 m plan and SHF/microwave

## Disclaimer / Haftungsausschluss

**DE:** Alle Angaben erfolgen ohne Gewähr auf Richtigkeit, Vollständigkeit und Aktualität. Dies ist ein privates, nicht kommerzielles Hobbyprojekt, keine Rechtsberatung und weder mit der Bundesnetzagentur noch mit dem DARC verbunden. Maßgeblich sind allein die amtlichen Veröffentlichungen (Bundesgesetzblatt, gesetze-im-internet.de, Verfügungen der Bundesnetzagentur). Für Schäden aus der Nutzung wird keine Haftung übernommen.

Der **Bandplan** (IARU Region 1, Stand der Quellen: HF 16.10.2020, VHF und UHF Dezember 2020) ist eine Empfehlung und kein Gesetz. Neuere Fassungen können abweichen.

**EN:** All information is provided without warranty. This is an unofficial hobby project and not legal advice. Only the official text of the German Amateur Radio Ordinance (AFuV) and the notices of the Bundesnetzagentur are binding. Always verify against the current official version before operating.

## License

MIT, see [LICENSE](LICENSE). The legal texts themselves are official works (amtliche Werke, § 5 UrhG) and not subject to copyright.

**73 de DK9RC**
