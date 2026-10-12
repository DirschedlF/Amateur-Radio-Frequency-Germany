import { useMemo, useState } from 'react'
import { Info } from 'lucide-react'
import plan from '../data/bandplan.json'
import hotspots from '../data/hotspots.json'
import { HOTSPOTS_META } from '../data/meta'
import { coverage, fmtFreq } from '../utils/bandplan'

const CLASSES = ['A', 'E', 'N']
const TYPE_CHIP = {
  cw: 'bg-sky-900/60 text-sky-200',
  qrp: 'bg-lime-900/60 text-lime-200',
  digital: 'bg-teal-900/60 text-teal-200',
  image: 'bg-fuchsia-900/60 text-fuchsia-200',
  dv: 'bg-indigo-900/60 text-indigo-200',
  ssb: 'bg-emerald-900/60 text-emerald-200',
  fm: 'bg-amber-900/60 text-amber-200',
  dx: 'bg-orange-900/60 text-orange-200',
  emergency: 'bg-red-900/60 text-red-200',
  aprs: 'bg-cyan-900/60 text-cyan-200',
  weak: 'bg-violet-900/60 text-violet-200',
}
const BAND_BY_ID = Object.fromEntries(plan.bands.map((b) => [b.id, b]))
const BAND_ORDER = plan.bands.map((b) => b.id).filter((id) => hotspots.entries.some((e) => e.band === id))

function CoverChip({ state, cls }) {
  const map = {
    full: ['✓', 'bg-green-900/60 text-green-300', `Für Klasse ${cls} in Anlage 1 zugewiesen`],
    part: ['◐', 'bg-amber-900/60 text-amber-300', `Für Klasse ${cls} nur teilweise zugewiesen`],
    none: ['–', 'text-gray-600', `Für Klasse ${cls} nicht zugewiesen`],
  }
  const [sym, cls2, title] = map[state]
  return (
    <span className={`inline-block min-w-[1.6rem] text-center font-mono text-xs rounded px-1.5 py-0.5 ${cls2}`} title={title}>
      <span aria-hidden="true">{sym}</span>
      <span className="sr-only">{title}</span>
    </span>
  )
}

export default function HotspotsView() {
  const [type, setType] = useState('all')
  const [bandId, setBandId] = useState('all')
  const [cls, setCls] = useState('all')

  const rows = useMemo(
    () =>
      hotspots.entries.filter(
        (e) =>
          (type === 'all' || e.type === type) &&
          (bandId === 'all' || e.band === bandId) &&
          (cls === 'all' || coverage({ f: e.f, t: e.f }, cls) !== 'none'),
      ),
    [type, bandId, cls],
  )
  const bands = BAND_ORDER.filter((id) => rows.some((r) => r.band === id))

  const segBtn = (active) =>
    `px-3 py-1.5 text-sm transition ${active ? 'bg-blue-600 text-white' : 'bg-gray-700 hover:bg-gray-600 text-gray-200'}`
  const chipBtn = (active) =>
    `px-3 py-1 rounded-lg text-sm border transition ${
      active ? 'bg-blue-600 border-blue-500 text-white' : 'bg-gray-700 border-gray-600 hover:bg-gray-600 text-gray-200'
    }`

  return (
    <div className="space-y-5" id="hotspots">
      <div role="note" className="bg-blue-900/20 border border-blue-700/50 rounded-lg p-4 flex gap-3 text-sm text-blue-100">
        <Info className="w-5 h-5 shrink-0 text-blue-300 mt-0.5" aria-hidden="true" />
        <div className="space-y-2">
          <p>
            <strong>Aktivitätszentren sind Empfehlungen, kein Gesetz.</strong> Rechtlich verbindlich sind nur Anlage 1 AFuV und
            die Verfügungen der Bundesnetzagentur. Die Spalten A, E, N zeigen, ob die Frequenz in Anlage 1 für die Klasse
            zugewiesen ist (Leistungsgrenzen und Teil B nicht geprüft). <strong>Angaben ohne Gewähr.</strong>
          </p>
          <p>
            Die WSJT-X-Modi (FT8, FT4, FT2, WSPR, Q65, JT65 …) sind Dial-Frequenzen (USB), die Standardwerte der WSJT-X-Frequenztabelle für Region 1. Gesendet
            wird je nach Tonhöhe rund 1 bis 3 kHz darüber. Prüfe, dass das Signal im Band bleibt. Stand der Daten:{' '}
            {HOTSPOTS_META.checkedOn}.
          </p>
        </div>
      </div>

      <section className="space-y-3 print:hidden" aria-label="Filter">
        <div className="flex flex-wrap items-center gap-2">
          <span className="w-32 text-xs uppercase tracking-wide text-gray-400">Betriebsart</span>
          {['all', ...Object.keys(hotspots.types)].map((t) => (
            <button key={t} type="button" onClick={() => setType(t)} aria-pressed={type === t} className={chipBtn(type === t)}>
              {t === 'all' ? 'Alle' : hotspots.types[t]}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <span className="w-32 text-xs uppercase tracking-wide text-gray-400">Band</span>
          {['all', ...BAND_ORDER].map((id) => (
            <button key={id} type="button" onClick={() => setBandId(id)} aria-pressed={bandId === id} className={chipBtn(bandId === id)}>
              {id === 'all' ? 'Alle' : BAND_BY_ID[id].label}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex flex-col gap-1">
            <span className="text-xs uppercase tracking-wide text-gray-400">Nur Frequenzen für Klasse</span>
            <div className="inline-flex rounded-lg overflow-hidden border border-gray-600" role="group" aria-label="Klasse">
              {['all', ...CLASSES].map((c) => (
                <button key={c} type="button" onClick={() => setCls(c)} className={segBtn(cls === c)} aria-pressed={cls === c}>
                  {c === 'all' ? 'Alle' : c}
                </button>
              ))}
            </div>
          </div>
          <div className="ml-auto text-sm text-gray-400" role="status" aria-live="polite">
            {rows.length} von {hotspots.entries.length} Einträgen
          </div>
        </div>
      </section>

      <div className="scroll-box relative bg-gray-800 rounded-lg overflow-auto max-h-[70vh] border border-gray-700" tabIndex={0} aria-label="Aktivitätsfrequenzen">
        <table className="w-full min-w-[760px] text-sm border-separate border-spacing-0">
          <thead>
            <tr>
              {['Band', 'Frequenz', 'Betriebsart', 'Beschreibung', 'A', 'E', 'N', 'Quelle'].map((h) => (
                <th key={h} scope="col" className="sticky top-0 z-10 bg-[#1F3864] text-left font-semibold whitespace-nowrap px-3 py-2.5">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {bands.flatMap((id) =>
              rows
                .filter((r) => r.band === id)
                .map((r, i) => {
                  const b = BAND_BY_ID[id]
                  return (
                    <tr key={`${id}-${r.f}-${r.type}-${i}`} className={`${i % 2 ? 'bg-gray-800' : 'bg-gray-900/40'} hover:bg-gray-700/60`}>
                      <td className="px-3 py-2 align-top whitespace-nowrap font-semibold">{i === 0 ? b.label : ''}</td>
                      <td className="px-3 py-2 align-top whitespace-nowrap font-mono font-medium">
                        {fmtFreq(r.f, b.unit)} {b.unit}
                      </td>
                      <td className="px-3 py-2 align-top">
                        <span className={`inline-block rounded px-2 py-0.5 text-xs ${TYPE_CHIP[r.type]}`}>{hotspots.types[r.type]}</span>
                      </td>
                      <td className="px-3 py-2 align-top min-w-[14rem]">{r.text}</td>
                      {CLASSES.map((c) => (
                        <td key={c} className="px-3 py-2 align-top">
                          <CoverChip state={coverage({ f: r.f, t: r.f }, c)} cls={c} />
                        </td>
                      ))}
                      <td
                        className={`px-3 py-2 align-top text-xs whitespace-nowrap ${
                          hotspots.sources[r.src].level === 'Sekundärquelle' ? 'text-amber-300' : 'text-gray-400'
                        }`}
                        title={`${hotspots.sources[r.src].level}: ${hotspots.sources[r.src].text}`}
                      >
                        {hotspots.sources[r.src].short}
                        {hotspots.sources[r.src].level === 'Sekundärquelle' && <span className="block">Sekundärquelle</span>}
                      </td>
                    </tr>
                  )
                }),
            )}
          </tbody>
        </table>
        {rows.length === 0 && <div className="p-8 text-center text-gray-400">Keine Einträge für diese Auswahl.</div>}
      </div>

      <details className="bg-gray-800 rounded-lg p-4 text-sm text-gray-300 print:hidden">
        <summary className="cursor-pointer font-semibold text-white select-none">Quellen und Hinweise</summary>
        <ul className="list-disc pl-5 space-y-1 mt-3">
          {Object.entries(hotspots.sources).map(([k, v]) => (
            <li key={k}>
              <strong>{v.short}</strong> ({v.level}): {v.text}
            </li>
          ))}
          <li>Centre of Activity (CoA) und Calling-Frequenzen sind Empfehlungen zum Treffen, keine Vorschrift und keine Leistungsgrenze.</li>
        </ul>
      </details>
    </div>
  )
}
