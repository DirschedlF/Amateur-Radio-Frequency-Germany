# Data Sources and Update Process

## Source
- Official: https://www.gesetze-im-internet.de/afuv_2005/anlage_1.html (Anlage 1 AFuV)
- Version in app: 3. AFuV-Änderung, BGBl. 2024 I Nr. 175 (class N since 24.06.2024)
- Verified against an official printout dated 14.09.2024.

## Known detail
Row 29 (5830-5850 MHz) does not reference Teil B Nr. 13 in the official table, although Nr. 13 lists the range. The app follows the table (no satellite flag on that row).

## Update process
1. Compare the official table with `src/data/anlage1.json` (45 rows) and `teilB.json` (17 entries).
2. Power values: `w` in watt, `type` PEP/ERP/EIRP, `eirp` optional equivalent (EIRP = ERP x 1.64).
3. Update `src/data/meta.js`: `lawVersion`, `checkedOn`.
4. `npm run lint && npm run build`, check in the browser, commit.
