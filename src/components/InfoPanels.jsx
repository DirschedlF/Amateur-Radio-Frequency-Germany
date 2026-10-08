import teilB from '../data/teilB.json'
import { SOURCES } from '../data/meta'

function Panel({ title, children, open = false }) {
  return (
    <details open={open} className="bg-gray-800 rounded-lg p-4 group">
      <summary className="cursor-pointer font-semibold text-white select-none">{title}</summary>
      <div className="mt-3 text-sm text-gray-300 space-y-2">{children}</div>
    </details>
  )
}

export function InfoPanels() {
  return (
    <div className="space-y-3 print:hidden">
      <Panel title="Lesehilfe" open>
        <ul className="list-disc pl-5 space-y-1">
          <li>
            <strong>P / S:</strong> Amateurfunk ist primärer (P) oder sekundärer (S) Funkdienst. Sekundär bedeutet:
            Primärdienste nicht stören und kein Schutz vor Störungen durch sie.
          </li>
          <li>
            <strong>PEP</strong> ist die Spitzenleistung am Senderausgang. <strong>ERP</strong> und <strong>EIRP</strong>{' '}
            sind Strahlungsleistungen, bezogen auf Halbwellendipol bzw. Kugelstrahler (EIRP = ERP × 1,64).
          </li>
          <li>
            Die Sortierung der Leistung folgt dem Zahlenwert in Watt. PEP und ERP/EIRP sind verschiedene Größen und
            nicht direkt vergleichbar.
          </li>
          <li>
            <strong>„–“</strong> in einer Klassenspalte: für diese Klasse in Anlage 1 nicht ausgewiesen.
          </li>
          <li>
            Fernbediente und automatische Stellen dürfen nur auf den in der Rufzeichenzuteilung genannten Frequenzen
            arbeiten, oberhalb 30 MHz mit höchstens 50 W ERP (ausgenommen Remote-Betrieb).
          </li>
        </ul>
      </Panel>

      <Panel title="Satellitenfunk (primär / sekundär)">
        <p>
          Der Vermerk aus Teil B Nr. 13 ist eine Erlaubnis, kein Hinweis auf aktiven Satellitenverkehr. Er sagt, dass
          der Bereich auch für den Amateurfunkdienst über Satelliten genutzt werden darf und mit welchem Status.
        </p>
        <ul className="list-disc pl-5 space-y-1">
          <li>
            <strong>Primär:</strong> Der Satellitendienst kann Schutz vor Störungen durch sekundäre Dienste verlangen.
            Terrestrischer Betrieb muss seinen Vorrang beachten.
          </li>
          <li>
            <strong>Sekundär:</strong> Der Satellitendienst darf Primärdienste nicht stören. In 435–438, 1.260–1.270,
            2.400–2.450 und 5.650–5.670 MHz haben sogar andere sekundäre Dienste Vorrang, und Weltraumfunkstellen
            müssen steuerbar sein.
          </li>
          <li>
            <strong>Nicht geregelt:</strong> Leistung (es gilt die Klassengrenze der Zeile) und konkrete
            Satellitenfrequenzen (siehe Bandpläne).
          </li>
          <li>
            <strong>Praxis:</strong> Auf Kurzwelle ist kaum Satellitenverkehr aktiv, genutzt werden vor allem 2 m,
            70 cm und teils 10 m.
          </li>
        </ul>
      </Panel>

      <Panel title="Zusätzliche Nutzungsbestimmungen (Teil B, Nr. 1–17)">
        <dl className="grid grid-cols-[2.5rem_1fr] gap-x-3 gap-y-2">
          {teilB.map((b) => (
            <div key={b.nr} className="contents">
              <dt className="font-mono text-gray-500">{b.nr}</dt>
              <dd>{b.text}</dd>
            </div>
          ))}
        </dl>
      </Panel>

      <Panel title="Weitere Hinweise außerhalb von Anlage 1">
        <ul className="list-disc pl-5 space-y-1">
          <li>
            <strong>EMF-Anzeige (BEMFV):</strong> Ortsfeste Anlagen mit 10 W EIRP oder mehr müssen vor der
            Inbetriebnahme bei der Bundesnetzagentur angezeigt werden (Selbsterklärung, Sicherheitsabstand).
          </li>
          <li>
            <strong>AFuV § 16:</strong> Betrieb nach den allgemein anerkannten Regeln der Technik, unerwünschte
            Aussendungen minimieren, offene Sprache ohne Verschlüsselung, keine Dauerträger oder rundfunkähnlichen
            Darbietungen.
          </li>
          <li>
            <strong>AFuV § 11:</strong> Rufzeichen zu Beginn und Ende jeder Verbindung und mindestens alle 10 Minuten
            nennen. Ein Rufzeichen darf nicht gleichzeitig von verschiedenen Standorten genutzt werden.
          </li>
          <li>
            <strong>AFuV § 17:</strong> Die Bundesnetzagentur kann bei Störungen Testsendungen verlangen und
            Frequenzen, Leistung oder Betrieb vorübergehend einschränken.
          </li>
          <li>
            <strong>Bandpläne</strong> von IARU und DARC sind keine Gesetze, gehören aber zur guten Betriebspraxis.
          </li>
        </ul>
      </Panel>

      <Panel title="Quellen">
        <ul className="list-disc pl-5 space-y-1">
          {SOURCES.map((s) => (
            <li key={s.url}>
              <a
                className="text-blue-400 hover:underline"
                href={s.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {s.label}
              </a>
            </li>
          ))}
        </ul>
      </Panel>
    </div>
  )
}
