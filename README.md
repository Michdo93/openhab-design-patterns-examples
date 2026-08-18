# openHAB Design Patterns – Beispiel-Repository

Begleit-Repository zum Buch **„openHAB Design Patterns“** von Michael Christian Dörflinger.

Für jedes im Buch behandelte Design Pattern liegt hier ein eigener, lauffähiger
Beispiel-Ordner unter `patterns/<pattern-name>/` – mit den passenden Items,
Sitemaps/Things (falls nötig) und der Regel-Logik jeweils in **allen drei**
unterstützten Rule-Engines:

- **Rules DSL** (Xtend, die klassische, eingebaute Regelsprache)
- **JavaScript Scripting** (GraalJS, mit der Hilfsbibliothek `openhab-js`)
- **Python 3 Scripting** (GraalPy, Next-Gen-Binding, mit `openhab-python`)

Design Patterns, die ganz ohne Rule-Logik auskommen (reine Items-, Sitemap-
oder Metadaten-Beispiele), enthalten entsprechend nur die passenden
Unterordner. Wo eine Rule-Engine ein Pattern technisch nicht abbilden kann
(z. B. Item-Metadaten in der Rules DSL), fehlt die entsprechende Variante –
das steht dann in der README des jeweiligen Patterns erklärt.

Alle Beispiele sind bewusst **ohne externe Community-Bibliotheken**
umgesetzt, damit sie ohne Zusatzinstallation direkt in eine bestehende
openHAB-Installation übernommen werden können.

---

## Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [openHAB installieren](#openhab-installieren)
3. [Die drei Rule-Engines einrichten](#die-drei-rule-engines-einrichten)
4. [Dieses Repository herunterladen](#dieses-repository-herunterladen)
5. [Ein Beispiel installieren (Kurzfassung)](#ein-beispiel-installieren-kurzfassung)
6. [Struktur eines Pattern-Ordners](#struktur-eines-pattern-ordners)
7. [Alle Design Patterns in diesem Repository](#alle-design-patterns-in-diesem-repository)
8. [Fehlersuche](#fehlersuche)
9. [Neues Pattern hinzufügen](#neues-pattern-hinzufügen)
10. [Lizenz](#lizenz)

---

## Voraussetzungen

- **openHAB 5.x** (die Beispiele nutzen aktuelle APIs; bei älteren Versionen
  können einzelne Trigger/Actions fehlen)
- Ein Rechner/Server, auf dem openHAB läuft (Linux, Windows, macOS, Raspberry
  Pi, Docker – die folgenden Pfadangaben gelten für eine klassische
  Paketinstallation unter Linux)
- Zugriff auf das openHAB-Konfigurationsverzeichnis, im Folgenden
  `$OPENHAB_CONF` genannt:
  - Paketinstallation (Debian/Ubuntu/Raspberry Pi OS): `/etc/openhab`
  - Manuelle Installation: `/opt/openhab/conf`
  - Docker: der Ordner, den man als `/openhab/conf`-Volume gemountet hat
- Grundkenntnisse in Items, Things und Regeln (siehe Buch, Teil I)

## openHAB installieren

Falls noch nicht geschehen, zuerst openHAB selbst installieren. Die
offizielle, aktuelle Anleitung für die eigene Plattform (Linux-Paket,
Windows, Docker, Raspberry Pi Image, …) steht hier:

👉 <https://www.openhab.org/docs/installation/>

Nach der Installation ist openHAB über `http://<IP-oder-Hostname>:8080`
erreichbar (Main UI).

## Die drei Rule-Engines einrichten

Alle drei Engines werden über **Einstellungen → Add-ons → Automation**
in der Main UI installiert (alternativ über die Kommandozeilen-Konsole
`openhab-cli console` mit `bundle:install` bzw. `feature:install`).

### 1. Rules DSL

Ist in jeder openHAB-Installation **bereits vorinstalliert** – kein
zusätzliches Add-on nötig. `.rules`-Dateien werden aus
`$OPENHAB_CONF/rules/` geladen.

### 2. JavaScript Scripting (GraalJS)

1. In der Main UI: **Einstellungen → Add-ons → Automation → „JS Scripting“**
   installieren.
   *Nicht* das alte „Nashorn JavaScript“-Add-on – das ist veraltet und wird
   in diesem Repository nicht verwendet.
2. Skripte werden aus `$OPENHAB_CONF/automation/js/` geladen. Der Ordner wird
   beim ersten Start des Add-ons automatisch angelegt.
3. Optional, aber empfohlen: Für Editor-Unterstützung (Autovervollständigung)
   in VS Code das offizielle `openhab-js`-Typings-Paket gemäß der
   [openhab-js-Dokumentation](https://openhab.github.io/openhab-js/) einrichten.

### 3. Python 3 Scripting (GraalPy, Next-Gen-Binding)

1. In der Main UI: **Einstellungen → Add-ons → Automation** installieren –
   das Add-on heißt **„Python Scripting“ mit dem Zusatz „(Next-Gen)“**
   bzw. intern `pythonscripting`.
   *Nicht* das alte, klassische „Python Scripting“-Add-on ohne Next-Gen-Zusatz
   verwenden – dieses unterstützt keine eigenen, importierbaren Module über
   mehrere Dateien hinweg (siehe Buch, Kapitel „Was ist openHAB Scripted
   Automation?“).
2. Skripte werden aus `$OPENHAB_CONF/automation/python/` geladen.
3. Zusätzliche Python-Pakete (z. B. für eigene Erweiterungen) lassen sich per
   `pip` in die vom Add-on verwaltete virtuelle Umgebung installieren; die
   genauen Befehle stehen in der Add-on-Beschreibung in der Main UI unter
   „Konfigurieren“.
4. Die Bibliothek `openhab-python` (Klassen wie `rule`, `Registry`,
   Trigger-Helfer) ist im Add-on bereits enthalten – kein separates `pip
   install` dafür nötig.

### Alle drei parallel nutzen

Alle drei Engines können **gleichzeitig** installiert sein und parallel
verwendet werden. Für ein einzelnes Beispiel aus diesem Repository sollte
aber immer **nur eine** der drei Rule-Varianten gleichzeitig aktiv sein,
um doppelte Ausführung derselben Logik zu vermeiden.

## Dieses Repository herunterladen

```bash
git clone https://github.com/Michdo93/openhab-design-patterns-examples.git
cd openhab-design-patterns-examples
```

(Passe die URL an, falls du das Repository unter einem anderen Namen oder
Account abgelegt hast.)

Alternativ kann auch einfach das ZIP von GitHub heruntergeladen und entpackt
werden.

## Ein Beispiel installieren (Kurzfassung)

Am Beispiel von `patterns/countdown-timer/` mit der JavaScript-Variante:

```bash
# 1. Items kopieren (oder Inhalt in eine bestehende .items-Datei einfuegen)
cp patterns/countdown-timer/items/*.items $OPENHAB_CONF/items/

# 2. Sitemap kopieren (falls vorhanden)
cp patterns/countdown-timer/sitemaps/*.sitemap $OPENHAB_CONF/sitemaps/ 2>/dev/null

# 3. NUR EINE Rule-Variante waehlen, z. B. JavaScript Scripting:
cp patterns/countdown-timer/rules-js/*.js $OPENHAB_CONF/automation/js/
```

openHAB überwacht `items/`, `sitemaps/` und die Regel-Verzeichnisse per
File-Watcher und lädt neue bzw. geänderte Dateien automatisch innerhalb
weniger Sekunden nach – ein manueller Neustart ist normalerweise nicht nötig.
Für Rules-DSL-Dateien unter `$OPENHAB_CONF/rules/` gilt dasselbe.

Jeder Pattern-Ordner enthält eine eigene `README.md` mit der exakten
Dateiliste und den passenden Zielpfaden für genau dieses Beispiel.

## Struktur eines Pattern-Ordners

```
patterns/<pattern-name>/
├── README.md              Beschreibung + genaue Installationsschritte
├── items/*.items          Item-Definitionen (fuer alle 3 Varianten identisch)
├── things/*.things        Thing-Definitionen (nur wenn benoetigt)
├── sitemaps/*.sitemap     Beispiel-Sitemap fuer das BasicUI (falls sinnvoll)
├── rules-dsl/*.rules      Variante 1: Rules DSL
├── rules-js/*.js          Variante 2: JavaScript Scripting (GraalJS)
│   └── lib/*.js           ggf. wiederverwendbares Modul, per require() eingebunden
└── rules-python/*.py      Variante 3: Python 3 Scripting (GraalPy)
    └── *.py               ggf. wiederverwendbares Modul, per import eingebunden
```

## Alle Design Patterns in diesem Repository

| Pattern | Kurzbeschreibung |
|---|---|
| [`associated-items`](patterns/associated-items/) | Zugehörige Items zur Laufzeit finden: semantisches Modell, Gruppenzugehörigkeit oder Namenskonvention. |
| [`aufgeschobene-automatisierte-aktionen`](patterns/aufgeschobene-automatisierte-aktionen/) | Verzögerte Befehle per Proxy-Item, die durch erneute Interaktion automatisch abgebrochen werden, inkl. wiederverwendbarem Timer-Modul. |
| [`bayes`](patterns/bayes/) | Bayessche Sensor-Aggregation: mehrere unsichere Beobachtungen zu einer Wahrscheinlichkeit kombinieren (Schlaferkennung). |
| [`bewegungssensor-timer`](patterns/bewegungssensor-timer/) | Gerät für X Minuten nach letzter Bewegung eingeschaltet halten, per Expire Binding oder Timer, auch für mehrere Sensoren. |
| [`cancel-activity`](patterns/cancel-activity/) | Abbrechbare lang laufende Schleifen-Aktion (z.B. Dimmen) über ein Cancel-Flag. |
| [`countdown-timer`](patterns/countdown-timer/) | Timer-basierter Countdown auf Basis eines Number-Items mit Expire Binding: Start, Verlängerung, Abbruch und Ablauf über Kommandos steuern. |
| [`cst`](patterns/cst/) | Aktionssequenz nur bei gleichzeitig erfüllten Mehrfachbedingungen auslösen (Conditional Sequence Trigger). |
| [`debounce`](patterns/debounce/) | Rohsignal über ein Proxy-Item entprellen, einzeln und generisch für mehrere Items. |
| [`decoupled-notification-service`](patterns/decoupled-notification-service/) | Benachrichtigungslogik von Automatisierungsregeln entkoppeln über zentrale Notify-Items und eine Sammel-Regel. |
| [`encoding-and-accessing`](patterns/encoding-and-accessing/) | Konstanten/Konfigurationswerte in Regeln speichern: Maps, Item-Namen, Metadaten, Konfigurationsmodule. |
| [`event-debouncer`](patterns/event-debouncer/) | Schnelle Mehrfach-Events per Timer-Sperre entprellen, um Doppelaktionen zu vermeiden. |
| [`expire-binding-based-timer`](patterns/expire-binding-based-timer/) | Timer-Ersatz über das Expire Binding statt klassischer createTimer-Objekte. |
| [`gate-keeper`](patterns/gate-keeper/) | Befehls-Warteschlange mit Mindestabstand für story-sensitive Technologien (433MHz/Insteon). |
| [`generic-is-alive`](patterns/generic-is-alive/) | Geräte-Ausfallerkennung über Expire Binding statt aktiver Abfrage. |
| [`graceful-retry-actions`](patterns/graceful-retry-actions/) | Befehle mit Wiederholung (fest/exponentiell) und optionalem Online-Check erneut senden, konfigurierbar für beliebig viele Geräte über eine Gruppe. |
| [`groups-in-rules`](patterns/groups-in-rules/) | Generische, gruppenbasierte Regel für mehrere Türsensoren statt Code-Duplikation pro Item. |
| [`gruppenbasierte-persistenz`](patterns/gruppenbasierte-persistenz/) | Persistenz-Engine (mapdb/rrd4j/influxdb) über Gruppenzugehörigkeit statt Einzel-Item-Konfiguration steuern. |
| [`human-readable-names`](patterns/human-readable-names/) | Technische Item-Namen per MAP-Transformation in lesbare Namen für Alarme/Logs umwandeln. |
| [`hysteresis`](patterns/hysteresis/) | Pufferzone um einen Schwellwert, um Flattern beim Schalten zu vermeiden. |
| [`item-metadata`](patterns/item-metadata/) | Konfigurationswerte und Alert-Flags als Item-Metadaten statt zusätzlicher Items. Kein DSL-Beispiel (DSL kann Metadaten nicht lesen/schreiben). |
| [`kaskadierende-timer`](patterns/kaskadierende-timer/) | Sequenzielle Mehrzonen-Bewässerung mit zeitversetzten Timern (Kaskade). |
| [`konfigurationsverwaltung`](patterns/konfigurationsverwaltung/) | Systemweite Einstellungen zentral als Map/Dictionary bzw. Konfigurationsmodul statt verstreut im Regelcode. |
| [`lichtsteuerungssystem`](patterns/lichtsteuerungssystem/) | Kombiniertes Lichtsteuerungssystem: zeitgesteuerte Helligkeit, Bewegungsaktivierung, dynamische Tageszeit-Anpassung. |
| [`long-press`](patterns/long-press/) | Kurzen vs. langen Tastendruck unterscheiden über Zeitmessung, inkl. Fallback-Timer. |
| [`looping-timers`](patterns/looping-timers/) | Nicht-blockierende Schleifen-Timer (Deckenventilator-Beispiel) statt while-Schleifen, inkl. Expire-Binding-Alternative. |
| [`manuelle-trigger-erkennung`](patterns/manuelle-trigger-erkennung/) | Manuelle vs. regelgesteuerte Item-Änderungen unterscheiden: Totmannschalter, Zeitstempel, Proxy-Items. |
| [`mqtt-state-supervision`](patterns/mqtt-state-supervision/) | überwachen, ob ein gesendeter MQTT-Befehl innerhalb einer Frist bestätigt wird, sonst Alarm. |
| [`multisensor-aggregation`](patterns/multisensor-aggregation/) | Mehrere unsichere Sensoren zu einer zuverlässigen Entscheidung kombinieren: Weighted-Sum- und Bayes-Variante. |
| [`notifications-in-groups`](patterns/notifications-in-groups/) | Warn-/Alarmschwellen für eine ganze Gruppe gleichartiger Sensoren (z.B. Temperaturen) statt Regel pro Sensor. |
| [`primer-mit-hablladin`](patterns/primer-mit-hablladin/) | Vollständiges Zustandsmaschinen-Beispiel: Garagenlicht mit Timer, Vorwarn-Blinken und manueller überschreibung. |
| [`proxy-item`](patterns/proxy-item/) | Virtuelles Steuer-Item zwischen Sitemap/Benutzer und dem eigentlich gebundenen Gerät-Item, inkl. Garagentor-Beispiel mit Alert. |
| [`rate-limit`](patterns/rate-limit/) | Aktion höchstens einmal pro Zeitfenster ausführen, über den eingebauten Script-Cache. |
| [`rule-deaktivierung`](patterns/rule-deaktivierung/) | Regeln zur Laufzeit aktivieren/deaktivieren (Weihnachtsmodus-Beispiel); DSL nur mit if-return-Workaround. |
| [`rule-manager`](patterns/rule-manager/) | Regeln per Enable/Disable- und Running-Switch zentral steuern und kooperativ abbrechen. |
| [`rule-refresh`](patterns/rule-refresh/) | Dynamisch generierte Rule-Trigger (z.B. aus Metadaten), nur JS/Python möglich. |
| [`rule-strukturierung`](patterns/rule-strukturierung/) | 1-2-3-Regelstruktur (Prüfen/Berechnen/Handeln) statt verschachtelter if-Ketten, plus Gruppen-Variante. |
| [`rule-verriegelung`](patterns/rule-verriegelung/) | Zeitstempel-basierte Entprellung/Latching einer Regel. |
| [`sensor-aggregation`](patterns/sensor-aggregation/) | Mehrere Präsenzsensoren zu einem Gesamtstatus aggregieren, inkl. Anti-Flapping-Timer und Personenerkennung. |
| [`simple-state-machine`](patterns/simple-state-machine/) | Ereignis-zu-Zustand-übergänge, optional mit Ephemeris-Bedingung (Wochentag/Feiertag). |
| [`state-machine-driven-groups`](patterns/state-machine-driven-groups/) | Tageszeit-abhängige Zustände über benannte Gruppen (gLights_ON_MORNING etc.) statt if-else-Ketten. |
| [`switch-dimmer`](patterns/switch-dimmer/) | Kurzer/langer Tastendruck eines Rocker-Switches getrennt über virtuelle Items, inkl. Lichtsteuerung. |
| [`szenenmanagement`](patterns/szenenmanagement/) | Ein Item, eine generische Regel, mehrere Szenen-Funktionen statt Item/Regel pro Szene. |
| [`time-of-day`](patterns/time-of-day/) | Tageszeit-Zustandsautomat (String-Item vTimeOfDay) auf Basis einer Zeitfenster-Tabelle. |
| [`time-of-last-update`](patterns/time-of-last-update/) | Zeitstempel-Item per openHAB-Profil (timestamp-update/-change). Kein Rule-Beispiel nötig. |
| [`timer-management`](patterns/timer-management/) | Zentrale Timer-Verwaltung über eine Map/ein Dictionary für generische, item-übergreifende Regeln. |
| [`toggle-pattern`](patterns/toggle-pattern/) | Zustand eines Geräts per Tastendruck umschalten (Toggle), inkl. UI-Feedback-Variante. |
| [`trennung-von-verhaltensweisen`](patterns/trennung-von-verhaltensweisen/) | Proxy-Item als zentrale Schnittstelle für geteilte Logik (Alarme, Bewölkung). |
| [`unbound-item`](patterns/unbound-item/) | Virtuelles Item ohne Binding/Thing zur Speicherung von regelinternem Zustand. Kein Rule-Beispiel nötig. |
| [`watering-system`](patterns/watering-system/) | Konfigurierbares Mehrzonen-Bewässerungssystem mit entkoppeltem zentralem Service und Timer pro Zone. |

## Fehlersuche

**Regel wird nicht ausgeführt / erscheint nicht im Log**
- Prüfen, ob die Datei im richtigen Verzeichnis liegt (siehe oben) und die
  richtige Dateiendung hat (`.rules`, `.js`, `.py`).
- In der Main UI unter **Einstellungen → Add-ons → Automation** prüfen, ob
  die jeweilige Engine wirklich installiert und aktiv ist.
- Im Log Viewer (`Einstellungen → System → Log Viewer` oder
  `tail -f /var/log/openhab/openhab.log`) nach Fehlermeldungen beim Laden des
  Skripts suchen – Syntaxfehler werden dort mit Datei und Zeile angezeigt.

**„Item xyz existiert nicht“ / NullPointerException**
- Die Items aus `items/` wurden noch nicht angelegt oder falsch benannt.
  Item-Namen im Beispiel ggf. an die eigene Installation anpassen – dann
  aber konsistent in Items- **und** Regel-Datei.

**Python-Regel lädt nicht, „Module not found“**
- Prüfen, ob evtl. mitgelieferte Zusatzmodule (z. B. `deferred.py`,
  `configuration.py`, `supervision.py`) ebenfalls nach
  `$OPENHAB_CONF/automation/python/` kopiert wurden – sie werden von der
  eigentlichen `@rule`-Datei per `import` eingebunden und müssen im selben
  Verzeichnis liegen.

**JavaScript-Regel lädt nicht, „Cannot find module“**
- Analog dazu: Dateien aus einem eventuellen `rules-js/lib/`-Unterordner
  nach `$OPENHAB_CONF/automation/js/lib/` kopieren.

**Mehrere Rule-Varianten gleichzeitig aktiv**
- Wurden versehentlich z. B. sowohl die `.rules`- als auch die `.js`-Datei
  desselben Beispiels kopiert, feuert die Logik doppelt. Nur eine Variante
  pro Pattern aktiv lassen.

## Neues Pattern hinzufügen

Als Vorlage dient `templates/pattern-template/`. Ordner kopieren, umbenennen
und die drei Rule-Varianten sowie ggf. Items/Sitemap/Things befüllen. Die
README des neuen Ordners nach demselben Schema wie die bestehenden Beispiele
ausfüllen (Beschreibung, Dateiliste, Installationsschritte).

## Lizenz

Beispielcode zum Buch „openHAB Design Patterns“ von Michael Christian
Dörflinger. Die Beispiele dürfen frei für eigene openHAB-Installationen
verwendet und angepasst werden.
