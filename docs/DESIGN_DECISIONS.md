# Design Decisions

- Same stack and look as Amateur Radio DXCC Analyzer Pro (React, Vite, Tailwind, dark UI, GitHub Pages workflow, standalone build).
- No backend; all data is static JSON bundled at build time.
- Power sorts by numeric watt value; PEP and ERP/EIRP are shown with their type because they are not directly comparable.
- Disclaimer shown as banner at the top and in full at the bottom, bilingual DE/EN.
- Print stylesheet: A4 landscape, interactive elements hidden.
- v1.1: The band plan is a separate view (tab) so that law (Anlage 1) and recommendation (IARU plan) are never mixed in one table. The band plan view shows a bar chart per band with Anlage 1 lanes for A/E/N below it.
- Band plan data is generated from a transcription script, not hand-edited JSON, so it can be re-verified against the PDF text.
- The `#bandplan` URL hash opens the band plan view directly.
