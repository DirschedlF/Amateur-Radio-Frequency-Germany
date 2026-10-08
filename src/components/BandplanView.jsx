import { useMemo, useState } from 'react'
import { Download, Info, Printer } from 'lucide-react'
import plan from '../data/bandplan.json'
import { BANDPLAN_META } from '../data/meta'
import { ALLOWED, CATEGORIES, bwText, clip, coverage, fmtRange } from '../utils/bandplan'
import { downloadBandplanCsv } from '../utils/exportCsv'

const CLASSES = ['A', 'E', 'N']
const CLASS_BAR = { A: 'bg-blue-500', E: 'bg-green-500', N: 'bg-amber-500' }
const GROUPS = [
  ['hf', 'Kurzwelle (HF)'],
  ['vhf', 'VHF'],
  ['uhf', 'UHF'],
  ['shf', 'SHF (3–24 GHz)'],
  ['uwave', 'Mikrowelle (47–250 GHz)'],
]

function CoverChip({ state, cls }) {
  const map = {
    full: ['✓', 'bg-green-900/60 text-green-300', `Für Klasse ${cls} in Anlage 1 vollständig zugewiesen`],
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

function BandBar({ band, lo, hi }) {
  const span = hi - lo
  const pct = (v) => ((v - lo) / span) * 100
  let overlapCount = 0
  const segs = band.rows
    .filter((r) => !r.umbrella)
    .map((r) => {
      let lane = null
      if (r.overlap) {
        lane = overlapCount % 2
        overlapCount += 1
      }
      return { ...r, lane }
    })
  return (
    <div
      role="img"
      aria-label={`Bandplan ${band.label} als Balkendiagramm, darunter die in Anlage 1 zugewiesenen Bereiche je Klasse`}
      className="grid grid-cols-[3rem_1fr] items-center gap-x-2 gap-y-1"
    >
      <span className="text-xs font-mono text-gray-400">Plan</span>
      <div className="relative h-10 bg-gray-900 rounded overflow-hidden border border-gray-700">
        {segs.map((r, i) => {
          const left = pct(r.f)
          const width = Math.max(pct(r.t) - left, 0.25)
          const top = r.lane === null ? 0 : r.lane === 0 ? 0 : 50
          const height = r.lane === null ? 100 : 50
          return (
            <div
              key={i}
              className={`absolute ${CATEGORIES[r.cat].bar} border-r border-gray-900/70 opacity-90`}
              style={{ left: `${left}%`, width: `${width}%`, top: `${top}%`, height: `${height}%` }}
              title={`${fmtRange(r, band.unit)} · ${r.mode}`}
            />
          )
        })}
      </div>
      {CLASSES.map((c) => (
        <div key={c} className="contents">
          <span className="text-xs font-mono text-gray-400">Kl. {c}</span>
          <div className="relative h-2.5 bg-gray-900 rounded overflow-hidden border border-gray-700">
            {clip(ALLOWED[c], lo, hi).map(([a, b], i) => (
              <div
                key={i}
                className={`absolute inset-y-0 ${CLASS_BAR[c]}`}
                style={{ left: `${pct(a)}%`, width: `${Math.max(pct(b) - pct(a), 0.25)}%` }}
                title={`Klasse ${c}: ${a}–${b} MHz laut Anlage 1`}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

export default function BandplanView() {
  const [bandId, setBandId] = useState('20m')
  const [cls, setCls] = useState('all')
  const band = plan.bands.find((b) => b.id === bandId)
  const src = plan.sources[band.src]

  const bounds = useMemo(() => {
    const rows = band.rows.filter((r) => !r.umbrella)
    return [Math.min(...rows.map((r) => r.f)), Math.max(...rows.map((r) => r.t))]
  }, [band])

  const rows = useMemo(
    () => (cls === 'all' ? band.rows : band.rows.filter((r) => coverage(r, cls) !== 'none')),
    [band, cls],
  )

  const segBtn = (active) =>
    `px-3 py-1.5 text-sm transition ${active ? 'bg-blue-600 text-white' : 'bg-gray-700 hover:bg-gray-600 text-gray-200'}`

  return (
    <div className="space-y-5" id="bandplan">
      <div role="note" className="bg-blue-900/20 border border-blue-700/50 rounded-lg p-4 flex gap-3 text-sm text-blue-100">
        <Info className="w-5 h-5 shrink-0 text-blue-300 mt-0.5" aria-hidden="true" />
        <p>
          <strong>Der Bandplan ist eine Empfehlung, kein Gesetz.</strong> Rechtlich verbindlich sind nur die Frequenzzuteilung
          in Anlage 1 AFuV und die Verfügungen der Bundesnetzagentur. Die Pläne stammen von der IARU Region 1 (Stand der
          Quellen: {BANDPLAN_META.hfStand}, {BANDPLAN_META.vhfStand}, {BANDPLAN_META.uhfStand}, {BANDPLAN_META.shfStand}; ergänzende Hinweise aus dem VHF Handbook {BANDPLAN_META.handbook}). Neuere Fassungen können
          abweichen. Die Spalten A, E, N zeigen, ob ein Segment in Anlage 1 für die Klasse zugewiesen ist.
          <strong> Angaben ohne Gewähr.</strong>
        </p>
      </div>

      <section className="space-y-3 print:hidden" aria-label="Bandauswahl">
        {GROUPS.map(([g, label]) => (
          <div key={g} className="flex flex-wrap items-center gap-2">
            <span className="w-32 text-xs uppercase tracking-wide text-gray-400">{label}</span>
            {plan.bands
              .filter((b) => b.src === g)
              .map((b) => (
                <button
                  key={b.id}
                  type="button"
                  onClick={() => setBandId(b.id)}
                  aria-pressed={bandId === b.id}
                  className={`px-3 py-1 rounded-lg text-sm border transition ${
                    bandId === b.id
                      ? 'bg-blue-600 border-blue-500 text-white'
                      : 'bg-gray-700 border-gray-600 hover:bg-gray-600 text-gray-200'
                  }`}
                >
                  {b.label}
                </button>
              ))}
          </div>
        ))}
      </section>

      <section className="bg-gray-800 rounded-lg p-4 space-y-4" aria-label={`Bandplan ${band.label}`}>
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 className="text-2xl font-bold">
            {band.label} <span className="text-base font-normal text-gray-400 font-mono">{band.title}</span>
          </h2>
          <p className="text-xs text-gray-400">
            Quelle: {src.title}, gültig {src.effective}, bearbeitet von {src.editor}
          </p>
        </div>

        <BandBar band={band} lo={bounds[0]} hi={bounds[1]} />

        <ul className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-300" aria-label="Legende">
          {Object.entries(CATEGORIES).map(([k, v]) => (
            <li key={k} className="flex items-center gap-1.5">
              <span className={`inline-block w-3 h-3 rounded-sm ${v.bar}`} aria-hidden="true" /> {v.label}
            </li>
          ))}
        </ul>
        <p className="text-xs text-gray-500">
          Die Farbzuordnung ist eine Einordnung dieser App zur besseren Übersicht. Maßgeblich ist der Text der Spalte
          „Betriebsart“. Untere Balken: Zuweisung laut Anlage 1 (blau A, grün E, gelb N).
        </p>
      </section>

      <section className="flex flex-wrap items-end gap-4 print:hidden" aria-label="Filter">
        <div className="flex flex-col gap-1">
          <span className="text-xs uppercase tracking-wide text-gray-400">Nur Segmente für Klasse</span>
          <div className="inline-flex rounded-lg overflow-hidden border border-gray-600" role="group" aria-label="Klasse">
            {['all', ...CLASSES].map((c) => (
              <button key={c} type="button" onClick={() => setCls(c)} className={segBtn(cls === c)} aria-pressed={cls === c}>
                {c === 'all' ? 'Alle' : c}
              </button>
            ))}
          </div>
        </div>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => downloadBandplanCsv(band, rows, `bandplan-${band.id}.csv`)}
            className="inline-flex items-center gap-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition"
          >
            <Download className="w-4 h-4" aria-hidden="true" /> CSV
          </button>
          <button
            type="button"
            onClick={() => window.print()}
            className="inline-flex items-center gap-1 px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition"
          >
            <Printer className="w-4 h-4" aria-hidden="true" /> Drucken
          </button>
        </div>
        <div className="ml-auto text-sm text-gray-400" role="status" aria-live="polite">
          {rows.length} von {band.rows.length} Segmenten
        </div>
      </section>

      <div className="scroll-box relative bg-gray-800 rounded-lg overflow-auto max-h-[70vh] border border-gray-700" tabIndex={0} aria-label={`Bandplan-Tabelle ${band.label}`}>
        <table className="w-full min-w-[920px] text-sm border-separate border-spacing-0">
          <thead>
            <tr>
              {['Frequenz', 'Max. Bandbreite', 'Betriebsart', 'Bevorzugte Nutzung', 'A', 'E', 'N'].map((h) => (
                <th key={h} scope="col" className="sticky top-0 z-10 bg-[#1F3864] text-left font-semibold whitespace-nowrap px-3 py-2.5">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} className={`${i % 2 ? 'bg-gray-800' : 'bg-gray-900/40'} hover:bg-gray-700/60 ${r.umbrella ? 'italic text-gray-400' : ''}`}>
                <td className="px-3 py-2 align-top whitespace-nowrap font-mono font-medium">{fmtRange(r, band.unit)}</td>
                <td className="px-3 py-2 align-top whitespace-nowrap">{bwText(r.bw) || <span className="text-gray-600">–</span>}</td>
                <td className="px-3 py-2 align-top">
                  <span className={`inline-block rounded px-2 py-0.5 text-xs ${CATEGORIES[r.cat].chip}`}>{r.mode}</span>
                  {r.umbrella && <span className="block text-xs mt-1">übergeordnete Angabe, Unterbereiche folgen</span>}
                  {r.overlap && <span className="block text-xs text-gray-400 mt-1">überlappt mit einem weiteren Segment (so in der Quelle)</span>}
                  {r.quirk && <span className="block text-xs text-amber-300 mt-1">{r.quirk}</span>}
                </td>
                <td className="px-3 py-2 align-top min-w-[18rem] max-w-xl">{r.use || <span className="text-gray-600">–</span>}</td>
                {CLASSES.map((c) => (
                  <td key={c} className="px-3 py-2 align-top">
                    <CoverChip state={coverage(r, c)} cls={c} />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length === 0 && <div className="p-8 text-center text-gray-400">Keine Segmente für diese Auswahl.</div>}
      </div>

      {(band.notes.length > 0 || band.src === 'hf') && (
        <section className="bg-gray-800 rounded-lg p-4 text-sm text-gray-300 space-y-2" aria-label="Hinweise">
          <h3 className="font-semibold text-white">Hinweise zu {band.label}</h3>
          {band.notes.length > 0 && (
            <ul className="list-disc pl-5 space-y-1">
              {band.notes.map((n, i) => (
                <li key={i}>{n}</li>
              ))}
            </ul>
          )}
          {band.src === 'hf' && (
            <details className="mt-2">
              <summary className="cursor-pointer text-gray-200">Allgemeine Hinweise des HF-Bandplans (sinngemäß)</summary>
              <ul className="list-disc pl-5 space-y-1 mt-2">
                {plan.hfNotes.map((n, i) => (
                  <li key={i}>{n}</li>
                ))}
              </ul>
            </details>
          )}
        </section>
      )}

      <details className="bg-gray-800 rounded-lg p-4 text-sm text-gray-300 print:hidden">
        <summary className="cursor-pointer font-semibold text-white select-none">Begriffe des IARU-Bandplans</summary>
        <dl className="mt-3 grid grid-cols-[10rem_1fr] gap-x-3 gap-y-2">
          {plan.definitions.map((d) => (
            <div key={d.term} className="contents">
              <dt className="font-mono text-gray-400">{d.term}</dt>
              <dd>{d.text}</dd>
            </div>
          ))}
          <div className="contents">
            <dt className="font-mono text-gray-400">MGM</dt>
            <dd>Mixed-Mode-Betriebsarten (Begriff der VHF/UHF-Pläne). CoA = Centre of Activity (Aktivitätszentrum).</dd>
          </div>
        </dl>
      </details>
    </div>
  )
}
