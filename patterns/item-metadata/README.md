# item-metadata

Konfigurationswerte und Alert-Flags als Item-Metadaten statt zusaetzlicher Items. Kein DSL-Beispiel (DSL kann Metadaten nicht lesen/schreiben).

## Dateien in diesem Beispiel

**Items** (`items/`):
- `item-metadata-alerts.items`
- `item-metadata-simple.items`
- `item-metadata-static.items`

**Transformationen** (`transform/`) – benötigt das Add-on „Map Transformation“:
- `admin.map`

**Regeln** – bitte nur EINE der drei Varianten verwenden:

- JavaScript Scripting (`rules-js/`): `item-metadata-alerts.js`
- Python 3 Scripting (`rules-python/`): `item_metadata_alerts.py`

## Installation

Voraussetzung: openHAB läuft bereits und die gewünschte Rule-Engine ist installiert
(siehe Haupt-README im Wurzelverzeichnis dieses Repos für die Add-on-Installation).

1. **Items kopieren:** Inhalt der Datei(en) unter `items/` in eine eigene
   `.items`-Datei unter `$OPENHAB_CONF/items/` einfügen (z. B. anhängen an eine
   bestehende Datei oder als neue Datei ablegen), Item-Namen bei Bedarf an die
   eigene Installation anpassen.

2. **Transformationsdatei(en) kopieren:** Inhalt der Datei(en) unter
   `transform/` nach `$OPENHAB_CONF/transform/` kopieren. Voraussetzung dafür ist
   das Add-on **„Map Transformation“** (`Einstellungen → Add-ons → Transformations`).
   Ohne dieses Add-on bzw. ohne die kopierte(n) Datei(en) meldet openHAB beim
   Anzeigen des Items eine Warnung wie `Transformation service of type 'MAP' is
   not available` – die Automatisierung selbst funktioniert davon unabhängig,
   nur die lesbare Anzeige des Zustands fehlt dann.

3. **EINE Rule-Variante wählen und kopieren:**

   - **JavaScript Scripting:** Datei(en) aus `rules-js/` nach `$OPENHAB_CONF/automation/js/` kopieren.
     Enthält der Ordner eine Unterdatei unter `rules-js/lib/`, diese nach
     `$OPENHAB_CONF/automation/js/lib/` kopieren (wird per `require(...)` eingebunden).
   - **Python 3 Scripting:** Datei(en) aus `rules-python/` nach `$OPENHAB_CONF/automation/python/` kopieren.
     Liegt eine zusätzliche Modul-Datei bei (z. B. ohne `@rule`-Klassen, wie
     `deferred.py` oder `configuration.py`), diese ebenfalls dorthin kopieren –
     sie wird per `import` von der eigentlichen Regel-Datei eingebunden.

   openHAB überwacht diese Verzeichnisse automatisch (File Watcher) und lädt neue
   bzw. geänderte Dateien innerhalb weniger Sekunden selbstständig nach.

4. **Testen:** Über die openHAB-UI (`Einstellungen → Items` bzw. das BasicUI)
   den/die Auslöser des Beispiels manuell schalten und in
   `Einstellungen → System → Log Viewer` bzw. `openhab.log` die Ausgaben der Regel
   verfolgen.

## Hinweis

Item-, Thing- und Kanalnamen in diesem Beispiel sind Platzhalter und müssen an die
eigene Installation angepasst werden. Ausführliche Erklärungen zum Pattern selbst
stehen im zugehörigen Kapitel des Buches „openHAB Design Patterns“.
