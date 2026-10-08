# Design Decisions

- Same stack and look as Amateur Radio DXCC Analyzer Pro (React, Vite, Tailwind, dark UI, GitHub Pages workflow, standalone build).
- No backend; all data is static JSON bundled at build time.
- Power sorts by numeric watt value; PEP and ERP/EIRP are shown with their type because they are not directly comparable.
- Disclaimer shown as banner at the top and in full at the bottom, bilingual DE/EN.
- Print stylesheet: A4 landscape, interactive elements hidden.
