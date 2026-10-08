# CLAUDE.md

Project: Amateur Radio Frequency Germany. React 18 + Vite 7 + Tailwind 3.4 app showing AFuV Anlage 1 for classes A, E, N.

## Commands
- `npm run dev` (port 3000), `npm run build`, `npm run build:standalone`, `npm run lint`

## Rules
- Data lives in `src/data/anlage1.json` and `teilB.json`; never invent values. Verify against gesetze-im-internet.de.
- After any data change update `src/data/meta.js` (`lawVersion`, `checkedOn`).
- The disclaimer ("Angaben ohne Gewähr") must stay visible in the app and README.
- Vite `base` is `/Amateur-Radio-Frequency-Germany/` for Pages, `./` for the standalone build.
- UI language German, code and docs headings English. Dark theme (gray-900), navy table header.
- Lint must pass (CI runs `npm ci`, lint, build).

## Release
- Bump `version` in `package.json` and `appVersion` in `src/data/meta.js`, commit, then `git tag vX.Y.Z && git push origin main --tags`.
- `.github/workflows/release.yml` builds the standalone HTML and creates the GitHub Release with `Amateur-Radio-Frequency-Germany-vX.Y.Z-standalone.html`.
