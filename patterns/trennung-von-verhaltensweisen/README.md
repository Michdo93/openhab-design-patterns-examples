# trennung-von-verhaltensweisen

Proxy-Item als zentrale Schnittstelle fuer geteilte Logik (Alarme, Bewoelkung).

## Dateien in diesem Beispiel

**Items** (`items/`):
- `trennung-von-verhaltensweisen-alarm.items`
- `trennung-von-verhaltensweisen-cloudy.items`

**Regeln** – bitte nur EINE der drei Varianten verwenden:

- Rules DSL (`rules-dsl/`): `trennung-von-verhaltensweisen-alarm.rules`, `trennung-von-verhaltensweisen-cloudy.rules`
- JavaScript Scripting (`rules-js/`): `trennung-von-verhaltensweisen-alarm.js`, `trennung-von-verhaltensweisen-cloudy.js`
- Python 3 Scripting (`rules-python/`): `trennung_von_verhaltensweisen_alarm.py`, `trennung_von_verhaltensweisen_cloudy.py`

## Installation

Voraussetzung: openHAB läuft bereits und die gewünschte Rule-Engine ist installiert
(siehe Haupt-README im Wurzelverzeichnis dieses Repos für die Add-on-Installation).

1. **Items kopieren:** Inhalt der Datei(en) unter `items/` in eine eigene
   `.items`-Datei unter `$OPENHAB_CONF/items/` einfügen (z. B. anhängen an eine
   bestehende Datei oder als neue Datei ablegen), Item-Namen bei Bedarf an die
   eigene Installation anpassen.

2. **EINE Rule-Variante wählen und kopieren:**

   - **Rules DSL:** Datei(en) aus `rules-dsl/` nach `$OPENHAB_CONF/rules/` kopieren.
   - **JavaScript Scripting:** Datei(en) aus `rules-js/` nach `$OPENHAB_CONF/automation/js/` kopieren.
     Enthält der Ordner eine Unterdatei unter `rules-js/lib/`, diese nach
     `$OPENHAB_CONF/automation/js/lib/` kopieren (wird per `require(...)` eingebunden).
   - **Python 3 Scripting:** Datei(en) aus `rules-python/` nach `$OPENHAB_CONF/automation/python/` kopieren.
     Liegt eine zusätzliche Modul-Datei bei (z. B. ohne `@rule`-Klassen, wie
     `deferred.py` oder `configuration.py`), diese ebenfalls dorthin kopieren –
     sie wird per `import` von der eigentlichen Regel-Datei eingebunden.

   openHAB überwacht diese Verzeichnisse automatisch (File Watcher) und lädt neue
   bzw. geänderte Dateien innerhalb weniger Sekunden selbstständig nach.

3. **Testen:** Über die openHAB-UI (`Einstellungen → Items` bzw. das BasicUI)
   den/die Auslöser des Beispiels manuell schalten und in
   `Einstellungen → System → Log Viewer` bzw. `openhab.log` die Ausgaben der Regel
   verfolgen.

## Hinweis

Item-, Thing- und Kanalnamen in diesem Beispiel sind Platzhalter und müssen an die
eigene Installation angepasst werden. Ausführliche Erklärungen zum Pattern selbst
stehen im zugehörigen Kapitel des Buches „openHAB Design Patterns“.
