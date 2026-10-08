// Derives readable per-row information from the references into Teil B.

// Maximum occupied bandwidth per Teil B number: [value in Hz, label]
export const BANDWIDTH = {
  1: [800, '800 Hz'],
  3: [2700, '2,7 kHz'],
  4: [7000, '7 kHz (< 29 MHz), 40 kHz (> 29 MHz)'],
  6: [40000, '40 kHz'],
  7: [2e6, '2 MHz (AM-TV 7 MHz)'],
  8: [2e6, '2 MHz (AM/digital-TV 7 MHz, FM-TV 18 MHz)'],
  9: [10e6, '10 MHz (TV 20 MHz)'],
  16: [12000, '12 kHz'],
}

// Short texts for the non-bandwidth Teil B numbers
export const SHORT_NOTES = {
  2: 'Betriebsort der BNetzA anzeigen, Antenne ausreichend entkoppeln, bei Störung von Primärdiensten (auch in Nachbarbereichen) Betrieb einstellen.',
  5: 'Nur horizontale Polarisation und nur ortsfeste Stellen. Keine Störung des Rundfunkempfangs, kein Schutz vor Rundfunk. 50–52 MHz: keine Störung von Windprofilmessradaren, kein Schutz vor diesen. 50-MHz-Bake auf telefonische Anforderung abschaltbar.',
  10: 'Keine fernbedienten Stellen (außer Remote-Betrieb), kein Contestbetrieb.',
  11: '1.247–1.263 MHz: höchstens 3,05 W ERP (≙ 5 W EIRP), keine fernbedienten oder automatisch arbeitenden Stellen.',
  12: 'Automatisch arbeitende Stellen: höchstens 50 W ERP.',
  14: 'Nutzung nach den Bedingungen der Bundesnetzagentur im Amtsblatt, kein Störschutz. Genannt sind u. a. 444–453, 510–546, 711–730, 909–926, 945–951 GHz und oberhalb 956 GHz.',
  15: 'An Wochenenden bis 750 W PEP (A) bzw. 100 W PEP (E), Contestbetrieb am Wochenende erlaubt.',
  17: 'Linkstrecken fernbedienter oder automatischer Stellen in begründeten Fällen bis 1.000 W ERP.',
}

export function bandwidthOf(row) {
  let result = null
  row.refs.forEach((ref) => {
    if (BANDWIDTH[ref]) result = BANDWIDTH[ref]
  })
  return result // [Hz, label] or null
}

export function notesOf(row) {
  const notes = []
  row.refs.forEach((ref) => {
    if (ref === 13 && row.sat) {
      const kind = row.sat.status === 'P' ? 'primär' : 'sekundär'
      notes.push({ sat: true, text: `Satellitenfunk (${kind}): ${row.sat.text}` })
    } else if (SHORT_NOTES[ref]) {
      notes.push({ sat: false, text: SHORT_NOTES[ref] })
    }
  })
  return notes
}

export const nf = new Intl.NumberFormat('de-DE', { maximumFractionDigits: 2 })

export function powerText(p) {
  if (!p) return ''
  return `${nf.format(p.w)} W ${p.type}`
}

export function rangeOf(fromMHz) {
  if (fromMHz < 0.3) return 'LF'
  if (fromMHz < 3) return 'MF'
  if (fromMHz < 30) return 'HF'
  if (fromMHz < 300) return 'VHF'
  if (fromMHz < 3000) return 'UHF'
  if (fromMHz < 30000) return 'SHF'
  return 'EHF'
}
