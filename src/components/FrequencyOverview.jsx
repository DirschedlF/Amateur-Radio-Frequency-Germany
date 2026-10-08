import { useEffect, useMemo, useRef, useState } from 'react'
import {
  AlertTriangle,
  ArrowDown,
  ArrowUp,
  ChevronsUpDown,
  Download,
  Printer,
  RotateCcw,
  Search,
} from 'lucide-react'
import rows from '../data/anlage1.json'
import { META } from '../data/meta'
import { bandwidthOf, notesOf, nf, powerText, rangeOf } from '../utils/notes'
import { downloadCsv } from '../utils/exportCsv'
import { DisclaimerBanner, DisclaimerFull } from './DisclaimerBanner'
import { InfoPanels } from './InfoPanels'
import BandplanView from './BandplanView'

const CLASSES = ['A', 'E', 'N']

const RANGES = [
  ['all', 'Alle Bereiche'],
  ['LF', 'LF (< 300 kHz)'],
  ['MF', 'MF (300 kHz – 3 MHz)'],
  ['HF', 'HF / Kurzwelle (3 – 30 MHz)'],
  ['VHF', 'VHF (30 – 300 MHz)'],
  ['UHF', 'UHF (300 MHz – 3 GHz)'],
  ['SHF', 'SHF (3 – 30 GHz)'],
  ['EHF', 'EHF (> 30 GHz)'],
]

const CLASS_TEXT = {
  A: 'Alle ausgewiesenen Bereiche, bis 750 W PEP auf Kurzwelle, VHF, UHF und 23 cm, bis 75 W PEP auf den Mikrowellen. Als einzige Klasse mit Remote-Betrieb.',
  E: '160 m (oberhalb 1.850 kHz sekundär mit 75 W bzw. 10 W PEP), 80 m, 15 m und 10 m mit 100 W PEP. Ab 144 MHz aufwärts mit 75 W PEP bis 23 cm und 5 W PEP auf den Mikrowellen.',
  N: 'Nur 10 m mit 10 W ERP sowie 2 m und 70 cm mit 6,1 W ERP (≙ 10 W EIRP).',
}

const CLASS_COLOR = { A: 'border-blue-500', E: 'border-green-500', N: 'border-amber-500' }

const COLUMNS = [
  { key: 'nr', label: 'Nr.' },
  { key: 'freq', label: 'Frequenz' },
  { key: 'band', label: 'Band' },
  { key: 'status', label: 'Status' },
  { key: 'A', label: 'Klasse A' },
  { key: 'E', label: 'Klasse E' },
  { key: 'N', label: 'Klasse N' },
  { key: 'bw', label: 'Bandbreite' },
  { key: 'notes', label: 'Zusätzliche Nutzungsbestimmungen', sortable: false },
  { key: 'refs', label: 'Teil B', sortable: false },
]

function sortValue(row, key) {
  switch (key) {
    case 'nr':
      return row.nr
    case 'freq':
    case 'band':
      return row.fromMHz
    case 'status':
      return row.status === 'P' ? 0 : row.status === 'S' ? 1 : 2
    case 'A':
    case 'E':
    case 'N':
      return row.power[key] ? row.power[key].w : null
    case 'bw': {
      const bw = bandwidthOf(row)
      return bw ? bw[0] : null
    }
    default:
      return null
  }
}

function haystack(row) {
  return [
    row.freq,
    row.band,
    row.status === 'P' ? 'primär' : row.status === 'S' ? 'sekundär' : '',
    (bandwidthOf(row) || [0, ''])[1],
    notesOf(row).map((n) => n.text).join(' '),
    `nr ${row.refs.join(' nr ')}`,
    ...CLASSES.map((c) => powerText(row.power[c])),
  ]
    .join(' ')
    .toLowerCase()
}

function PowerCell({ power, highlight }) {
  const base = `px-3 py-2 align-top whitespace-nowrap font-mono ${highlight ? 'bg-blue-900/30' : ''}`
  if (!power) {
    return (
      <td className={`${base} text-gray-600 text-center`} title="Für diese Klasse nicht ausgewiesen">
        –
      </td>
    )
  }
  return (
    <td className={base}>
      <span className="font-semibold">{nf.format(power.w)}</span>
      <span className="text-gray-400 text-xs ml-1">W {power.type}</span>
      {power.eirp && <span className="block text-xs text-gray-400">≙ {power.eirp}</span>}
    </td>
  )
}

function StatusChip({ status }) {
  if (status === 'P' || status === 'S') {
    const cls = status === 'P' ? 'bg-green-900/60 text-green-300' : 'bg-amber-900/60 text-amber-300'
    const title = status === 'P' ? 'primärer Funkdienst' : 'sekundärer Funkdienst'
    return (
      <span className={`inline-block min-w-[1.6rem] text-center font-mono font-bold text-xs rounded px-2 py-0.5 ${cls}`} title={title}>
        {status}
      </span>
    )
  }
  return <span className="text-gray-500">–</span>
}

export default function FrequencyOverview() {
  const [search, setSearch] = useState('')
  const [cls, setCls] = useState('all')
  const [status, setStatus] = useState('all')
  const [range, setRange] = useState('all')
  const [sort, setSort] = useState({ key: 'nr', dir: 1 })
  const [view, setView] = useState(() => (window.location.hash === '#bandplan' ? 'bandplan' : 'anlage'))
  const searchRef = useRef(null)

  const counts = useMemo(
    () =>
      Object.fromEntries(
        CLASSES.map((c) => [
          c,
          {
            total: rows.filter((r) => r.power[c]).length,
            primary: rows.filter((r) => r.power[c] && r.status === 'P').length,
          },
        ]),
      ),
    [],
  )

  const visible = useMemo(() => {
    const q = search.trim().toLowerCase()
    const list = rows.filter((r) => {
      if (cls !== 'all' && !r.power[cls]) return false
      if (status !== 'all' && r.status !== status) return false
      if (range !== 'all' && rangeOf(r.fromMHz) !== range) return false
      if (q) {
        const h = haystack(r)
        if (!h.includes(q) && !h.replace(/\./g, '').includes(q.replace(/\./g, ''))) return false
      }
      return true
    })
    return list.sort((a, b) => {
      const va = sortValue(a, sort.key)
      const vb = sortValue(b, sort.key)
      const na = va === null || va === undefined
      const nb = vb === null || vb === undefined
      if (na && nb) return a.nr - b.nr
      if (na) return 1
      if (nb) return -1
      return va === vb ? a.nr - b.nr : (va - vb) * sort.dir
    })
  }, [search, cls, status, range, sort])

  useEffect(() => {
    const onKey = (e) => {
      const tag = (e.target.tagName || '').toLowerCase()
      if (e.key === '/' && tag !== 'input' && tag !== 'select') {
        e.preventDefault()
        searchRef.current?.focus()
      } else if (e.key === 'Escape' && e.target === searchRef.current) {
        setSearch('')
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  const toggleSort = (key) => {
    setSort((s) =>
      s.key === key
        ? { key, dir: -s.dir }
        : { key, dir: key === 'A' || key === 'E' || key === 'N' ? -1 : 1 },
    )
  }

  const switchView = (k) => {
    setView(k)
    try {
      window.history.replaceState(null, '', k === 'bandplan' ? '#bandplan' : window.location.pathname + window.location.search)
    } catch {
      /* ignore */
    }
  }

  const reset = () => {
    setSearch('')
    setCls('all')
    setStatus('all')
    setRange('all')
    setSort({ key: 'nr', dir: 1 })
  }

  const SortIcon = ({ column }) => {
    if (sort.key !== column) return <ChevronsUpDown className="w-3.5 h-3.5 opacity-50" aria-hidden="true" />
    return sort.dir === 1 ? (
      <ArrowUp className="w-3.5 h-3.5" aria-hidden="true" />
    ) : (
      <ArrowDown className="w-3.5 h-3.5" aria-hidden="true" />
    )
  }

  const segBtn = (active) =>
    `px-3 py-1.5 text-sm transition ${active ? 'bg-blue-600 text-white' : 'bg-gray-700 hover:bg-gray-600 text-gray-200'}`

  return (
    <div className="max-w-7xl mx-auto p-4 sm:p-6 space-y-6">
      <header>
        <h1 className="text-4xl font-bold mb-2 text-center">Amateur Radio Frequency Germany</h1>
        <p className="text-gray-400 text-center">
          Frequenzbereiche nach Anlage 1 AFuV für die Klassen A, E und N, mit IARU-Bandplan · v{META.appVersion}
        </p>
        <p className="text-gray-500 text-center text-sm mt-1">
          Fassung: {META.lawVersion} · geprüft am {META.checkedOn}
        </p>
        <div className="hidden print-show text-center mt-2 text-sm">
          Angaben ohne Gewähr. Verbindlich ist nur die amtliche Fassung der AFuV.
        </div>
      </header>

      <DisclaimerBanner />

      <nav className="flex gap-2 print:hidden" aria-label="Ansicht">
        {[
          ['anlage', 'Anlage 1 AFuV (gesetzlich)'],
          ['bandplan', 'Bandplan IARU Region 1 (Empfehlung)'],
        ].map(([k, label]) => (
          <button
            key={k}
            type="button"
            onClick={() => switchView(k)}
            aria-pressed={view === k}
            className={`px-4 py-2 rounded-lg text-sm font-medium border transition ${
              view === k
                ? 'bg-blue-600 border-blue-500 text-white'
                : 'bg-gray-800 border-gray-700 hover:bg-gray-700 text-gray-200'
            }`}
          >
            {label}
          </button>
        ))}
      </nav>

      {view === 'bandplan' ? (
        <BandplanView />
      ) : (
        <>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4" aria-label="Klassen im Überblick">
        {CLASSES.map((c) => (
          <div key={c} className={`bg-gray-800 rounded-lg p-4 border-t-4 ${CLASS_COLOR[c]}`}>
            <div className="flex items-baseline justify-between mb-1">
              <span className="text-lg font-bold">Klasse {c}</span>
              <span className="text-xs font-mono text-gray-400">
                {counts[c].total} Teilbereiche, {counts[c].primary} primär
              </span>
            </div>
            <p className="text-sm text-gray-400">{CLASS_TEXT[c]}</p>
          </div>
        ))}
      </section>

      <section className="flex flex-wrap items-end gap-4 print:hidden" aria-label="Filter">
        <div className="flex flex-col gap-1">
          <label htmlFor="search" className="text-xs uppercase tracking-wide text-gray-400">
            Suche
          </label>
          <div className="relative">
            <Search className="w-4 h-4 absolute left-2.5 top-2.5 text-gray-500" aria-hidden="true" />
            <input
              id="search"
              ref={searchRef}
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="z. B. 40 m, Contest, Satellit  ( / )"
              className="bg-gray-700 border border-gray-600 rounded-lg pl-8 pr-3 py-1.5 text-sm w-64 max-w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <span className="text-xs uppercase tracking-wide text-gray-400">Klasse</span>
          <div className="inline-flex rounded-lg overflow-hidden border border-gray-600" role="group" aria-label="Klasse">
            {['all', ...CLASSES].map((c) => (
              <button key={c} type="button" onClick={() => setCls(c)} className={segBtn(cls === c)} aria-pressed={cls === c}>
                {c === 'all' ? 'Alle' : c}
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <span className="text-xs uppercase tracking-wide text-gray-400">Status</span>
          <div className="inline-flex rounded-lg overflow-hidden border border-gray-600" role="group" aria-label="Status">
            {['all', 'P', 'S'].map((s) => (
              <button key={s} type="button" onClick={() => setStatus(s)} className={segBtn(status === s)} aria-pressed={status === s}>
                {s === 'all' ? 'Alle' : s}
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <label htmlFor="range" className="text-xs uppercase tracking-wide text-gray-400">
            Frequenzbereich
          </label>
          <select
            id="range"
            value={range}
            onChange={(e) => setRange(e.target.value)}
            className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {RANGES.map(([v, l]) => (
              <option key={v} value={v}>
                {l}
              </option>
            ))}
          </select>
        </div>

        <div className="flex gap-2">
          <button type="button" onClick={reset} className="inline-flex items-center gap-1 px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition">
            <RotateCcw className="w-4 h-4" aria-hidden="true" /> Zurücksetzen
          </button>
          <button
            type="button"
            onClick={() => downloadCsv(visible, 'afuv-anlage1-frequenzen.csv')}
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
          {visible.length} von {rows.length} Teilbereichen
        </div>
      </section>

      <div className="scroll-box bg-gray-800 rounded-lg overflow-auto max-h-[75vh] border border-gray-700" tabIndex={0} aria-label="Frequenztabelle">
        <table className="w-full min-w-[1080px] text-sm border-separate border-spacing-0">
          <thead>
            <tr>
              {COLUMNS.map((col) => {
                const active = sort.key === col.key
                const ariaSort = active ? (sort.dir === 1 ? 'ascending' : 'descending') : 'none'
                return (
                  <th
                    key={col.key}
                    scope="col"
                    aria-sort={col.sortable === false ? undefined : ariaSort}
                    className="sticky top-0 z-10 bg-[#1F3864] text-left font-semibold whitespace-nowrap p-0"
                  >
                    {col.sortable === false ? (
                      <span className="block px-3 py-2.5">{col.label}</span>
                    ) : (
                      <button
                        type="button"
                        onClick={() => toggleSort(col.key)}
                        className="flex items-center gap-1.5 w-full px-3 py-2.5 hover:bg-white/10 focus:outline-none focus-visible:ring-2 focus-visible:ring-white"
                      >
                        {col.label}
                        <SortIcon column={col.key} />
                      </button>
                    )}
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody>
            {visible.map((row, i) => {
              const bw = bandwidthOf(row)
              const notes = notesOf(row)
              return (
                <tr key={row.nr} className={`${i % 2 ? 'bg-gray-800' : 'bg-gray-900/40'} hover:bg-gray-700/60`}>
                  <td className="px-3 py-2 align-top font-mono text-gray-500">{row.nr}</td>
                  <td className="px-3 py-2 align-top whitespace-nowrap font-mono font-medium">{row.freq}</td>
                  <td className="px-3 py-2 align-top whitespace-nowrap">{row.band}</td>
                  <td className="px-3 py-2 align-top">
                    <StatusChip status={row.status} />
                  </td>
                  {CLASSES.map((c) => (
                    <PowerCell key={c} power={row.power[c]} highlight={cls === c} />
                  ))}
                  <td className="px-3 py-2 align-top max-w-[12rem]">{bw ? bw[1] : <span className="text-gray-600">–</span>}</td>
                  <td className="px-3 py-2 align-top min-w-[18rem] max-w-md">
                    {notes.length ? (
                      <ul className="list-disc pl-4 space-y-0.5">
                        {notes.map((n, k) => (
                          <li key={k} className={n.sat ? 'text-blue-300' : ''}>
                            {n.text}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <span className="text-gray-600">–</span>
                    )}
                  </td>
                  <td className="px-3 py-2 align-top whitespace-nowrap font-mono text-xs text-gray-500">{row.refs.join(', ')}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
        {visible.length === 0 && (
          <div className="p-8 text-center text-gray-400 flex items-center justify-center gap-2">
            <AlertTriangle className="w-4 h-4" aria-hidden="true" /> Keine Teilbereiche für diese Auswahl.
          </div>
        )}
      </div>
        </>
      )}

      <InfoPanels />
      <DisclaimerFull />

      <footer className="text-center text-sm text-gray-500 pb-6 space-y-1">
        <p>
          Daten: {META.law}, {META.lawVersion}. Abgeglichen mit dem amtlichen Ausdruck vom {META.officialPrintDate}.
        </p>
        <p>
          <a className="hover:underline text-blue-400" href={META.repoUrl} target="_blank" rel="noopener noreferrer">
            Quellcode auf GitHub
          </a>{' '}
          · MIT-Lizenz · Angaben ohne Gewähr
        </p>
        <p>Developed by Fritz (DK9RC) · 73</p>
      </footer>
    </div>
  )
}
