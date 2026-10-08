import { bandwidthOf, notesOf, powerText } from './notes'
import { bwText, coverage, fmtRange } from './bandplan'

// CSV for German Excel: semicolon separated, UTF-8 BOM, RFC-4180 quoting.
function cell(value) {
  const s = value === null || value === undefined ? '' : String(value)
  return /[";\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
}

export function toCsv(rows) {
  const header = ['Nr.', 'Frequenz', 'Band', 'Status', 'Klasse A', 'Klasse E', 'Klasse N', 'Bandbreite', 'Nutzungsbestimmungen', 'Teil B']
  const lines = [header.map(cell).join(';')]
  rows.forEach((r) => {
    const bw = bandwidthOf(r)
    lines.push(
      [
        r.nr,
        r.freq,
        r.band,
        r.status,
        powerText(r.power.A),
        powerText(r.power.E),
        powerText(r.power.N),
        bw ? bw[1] : '',
        notesOf(r).map((n) => n.text).join(' | '),
        r.refs.join(', '),
      ]
        .map(cell)
        .join(';'),
    )
  })
  return '﻿' + lines.join('\r\n')
}

export function downloadCsv(rows, filename) {
  const blob = new Blob([toCsv(rows)], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export function toBandplanCsv(band, rows) {
  const header = ['Band', 'Frequenz', 'Max. Bandbreite', 'Betriebsart', 'Bevorzugte Nutzung', 'Klasse A', 'Klasse E', 'Klasse N']
  const sym = { full: 'ja', part: 'teilweise', none: 'nein' }
  const lines = [header.map(cell).join(';')]
  rows.forEach((r) => {
    lines.push(
      [
        band.label,
        fmtRange(r, band.unit),
        bwText(r.bw),
        r.mode,
        r.use,
        sym[coverage(r, 'A')],
        sym[coverage(r, 'E')],
        sym[coverage(r, 'N')],
      ]
        .map(cell)
        .join(';'),
    )
  })
  return '\ufeff' + lines.join('\r\n')
}

export function downloadBandplanCsv(band, rows, filename) {
  const blob = new Blob([toBandplanCsv(band, rows)], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
