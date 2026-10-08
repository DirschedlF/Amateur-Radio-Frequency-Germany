import anlage from '../data/anlage1.json'

const EPS = 1e-9

// Merged allowed frequency intervals (MHz) per licence class, from Anlage 1.
function buildAllowed(cls) {
  const list = anlage
    .filter((r) => r.power[cls])
    .map((r) => [r.fromMHz, r.toMHz])
    .sort((a, b) => a[0] - b[0])
  const merged = []
  list.forEach(([a, b]) => {
    const last = merged[merged.length - 1]
    if (last && a <= last[1] + EPS) last[1] = Math.max(last[1], b)
    else merged.push([a, b])
  })
  return merged
}

export const ALLOWED = { A: buildAllowed('A'), E: buildAllowed('E'), N: buildAllowed('N') }

// 'full' | 'part' | 'none': how much of a band plan segment lies inside the
// ranges that Anlage 1 grants to the class.
export function coverage(seg, cls) {
  const ranges = ALLOWED[cls]
  if (seg.f === seg.t) {
    return ranges.some(([a, b]) => seg.f >= a - EPS && seg.f <= b + EPS) ? 'full' : 'none'
  }
  let covered = 0
  ranges.forEach(([a, b]) => {
    const lo = Math.max(a, seg.f)
    const hi = Math.min(b, seg.t)
    if (hi > lo) covered += hi - lo
  })
  const width = seg.t - seg.f
  if (covered <= EPS) return 'none'
  return covered >= width - EPS ? 'full' : 'part'
}

export function clip(ranges, lo, hi) {
  return ranges
    .map(([a, b]) => [Math.max(a, lo), Math.min(b, hi)])
    .filter(([a, b]) => b > a - EPS && b >= lo && a <= hi)
}

const nfKhz = new Intl.NumberFormat('de-DE', { maximumFractionDigits: 1 })
const nfMhz = new Intl.NumberFormat('de-DE', { minimumFractionDigits: 3, maximumFractionDigits: 4 })

// Values are stored in MHz. HF bands are shown in kHz like the source plan.
export function fmtFreq(mhz, unit) {
  return unit === 'kHz' ? nfKhz.format(Math.round(mhz * 1e7) / 1e4) : nfMhz.format(mhz)
}

export function fmtRange(seg, unit) {
  const a = fmtFreq(seg.f, unit)
  return seg.f === seg.t ? `${a} ${unit}` : `${a} – ${fmtFreq(seg.t, unit)} ${unit}`
}

export function bwText(bw) {
  if (bw === '' || bw === null || bw === undefined) return ''
  if (typeof bw === 'number') return `${bw.toLocaleString('de-DE')} Hz`
  const map = { none: 'keine Angabe', unrestricted: 'unbegrenzt', '*': '* (national)' }
  return map[bw] || bw
}

export const CATEGORIES = {
  cw: { label: 'CW', bar: 'bg-sky-600', chip: 'bg-sky-900/60 text-sky-200' },
  narrow: { label: 'Schmalband / Digimodes', bar: 'bg-teal-600', chip: 'bg-teal-900/60 text-teal-200' },
  all: { label: 'Alle Betriebsarten / SSB', bar: 'bg-emerald-600', chip: 'bg-emerald-900/60 text-emerald-200' },
  beacon: { label: 'Baken', bar: 'bg-rose-600', chip: 'bg-rose-900/60 text-rose-200' },
  fm: { label: 'FM / Relais / Kanäle', bar: 'bg-amber-600', chip: 'bg-amber-900/60 text-amber-200' },
  sat: { label: 'Satellit / Weltraum', bar: 'bg-violet-600', chip: 'bg-violet-900/60 text-violet-200' },
  other: { label: 'Sonstiges / ATV / reserviert', bar: 'bg-gray-500', chip: 'bg-gray-700 text-gray-200' },
}
