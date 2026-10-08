import { AlertTriangle } from 'lucide-react'
import { META } from '../data/meta'

export function DisclaimerBanner() {
  return (
    <div
      role="note"
      className="bg-amber-900/30 border border-amber-600/60 rounded-lg p-4 flex gap-3 text-sm text-amber-100"
    >
      <AlertTriangle className="w-5 h-5 shrink-0 text-amber-400 mt-0.5" aria-hidden="true" />
      <p>
        <strong>Angaben ohne Gewähr.</strong> Inoffizielles Hobbyprojekt, keine Rechtsberatung. Verbindlich ist nur
        die amtliche Fassung der AFuV (Bundesgesetzblatt bzw.{' '}
        <a
          className="underline hover:text-white"
          href={META.officialUrl}
          target="_blank"
          rel="noopener noreferrer"
        >
          gesetze-im-internet.de
        </a>
        ) und die Verfügungen der Bundesnetzagentur. Prüfe vor dem Funkbetrieb immer den aktuellen Stand.
      </p>
    </div>
  )
}

export function DisclaimerFull() {
  return (
    <section className="bg-gray-800 rounded-lg p-5 text-sm text-gray-300 space-y-3" aria-labelledby="disclaimer-h">
      <h2 id="disclaimer-h" className="text-lg font-semibold text-white">
        Haftungsausschluss / Disclaimer
      </h2>
      <p>
        Alle Angaben auf dieser Seite erfolgen <strong>ohne Gewähr</strong> auf Richtigkeit, Vollständigkeit und
        Aktualität. Die Daten wurden mit größter Sorgfalt aus Anlage 1 der Amateurfunkverordnung (AFuV) übernommen
        und gegen den amtlichen Text abgeglichen. Dennoch sind Übertragungsfehler, Auslegungsfehler und veraltete
        Angaben nicht auszuschließen. Spätere Änderungen der AFuV werden nicht automatisch berücksichtigt.
      </p>
      <p>
        Die Seite ist ein privates, nicht kommerzielles Hobbyprojekt. Sie stellt <strong>keine Rechtsberatung</strong>{' '}
        dar und ist weder mit der Bundesnetzagentur noch mit dem DARC verbunden. Maßgeblich sind ausschließlich die
        amtlichen Veröffentlichungen. Für Schäden und Nachteile, die aus der Nutzung der Angaben entstehen, wird keine
        Haftung übernommen.
      </p>
      <p className="text-gray-400">
        <em>English:</em> All information is provided without warranty. This is an unofficial hobby project and not
        legal advice. Only the official text of the German Amateur Radio Ordinance (AFuV) and the notices of the
        Bundesnetzagentur are binding. Always verify against the current official version before operating.
      </p>
    </section>
  )
}
