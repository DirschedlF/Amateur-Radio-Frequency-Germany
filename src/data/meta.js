// Metadata for the data set shown in the app. Update this file together with
// anlage1.json / teilB.json whenever Anlage 1 AFuV changes.
export const META = {
  appVersion: '1.1.1',
  law: 'Anlage 1 AFuV (Amateurfunkverordnung)',
  lawVersion: '3. AFuV-Änderung, BGBl. 2024 I Nr. 175 (Klasse N seit 24.06.2024)',
  checkedOn: '08.10.2026',
  officialPrintDate: '14.09.2024',
  officialUrl: 'https://www.gesetze-im-internet.de/afuv_2005/anlage_1.html',
  repoUrl: 'https://github.com/DirschedlF/Amateur-Radio-Frequency-Germany',
}

export const SOURCES = [
  {
    label: 'IARU Region 1: Bandpläne (HF, VHF, UHF, SHF, µWave) und VHF Handbook',
    url: 'https://www.iaru-r1.org/on-the-air/band-plans/',
  },
  {
    label: 'Anlage 1 AFuV (gesetze-im-internet.de)',
    url: 'https://www.gesetze-im-internet.de/afuv_2005/anlage_1.html',
  },
  {
    label: 'AFuV Volltext (gesetze-im-internet.de)',
    url: 'https://www.gesetze-im-internet.de/afuv_2005/BJNR024200005.html',
  },
  {
    label: 'Bundesnetzagentur: Anzeige Amateurfunk (BEMFV)',
    url: 'https://www.bundesnetzagentur.de/DE/Fachthemen/Telekommunikation/Technik/EMF/AnzeigeAmateurfunk/anzeig_amateurfunk_node.html',
  },
  {
    label: 'Dritte Verordnung zur Änderung der AFuV (Überblick)',
    url: 'https://hamradio.bzsax.de/2024/06/25/dritte-verordnung-zur-aenderung-der-amateurfunkverordnung/',
  },
]

// Band plan data (IARU Region 1), shown in the "Bandplan" view.
export const BANDPLAN_META = {
  hfStand: 'HF 16.10.2020',
  vhfStand: 'VHF Dezember 2020',
  uhfStand: 'UHF Dezember 2020',
  shfStand: 'SHF/µWave Dezember 2020',
  handbook: 'V10.03 (Februar 2026)',
  checkedOn: '08.10.2026',
  url: 'https://www.iaru-r1.org/on-the-air/band-plans/',
}
