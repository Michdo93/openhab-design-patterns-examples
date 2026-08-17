# <pattern-name>

<Kurzbeschreibung: welches Problem löst dieses Pattern, in 1-2 Sätzen.>

## Dateien in diesem Beispiel

**Items** (`items/`):
- `<pattern-name>.items`

**Regeln** – bitte nur EINE der drei Varianten verwenden:

- Rules DSL (`rules-dsl/`): `<pattern-name>.rules`
- JavaScript Scripting (`rules-js/`): `<pattern-name>.js`
- Python 3 Scripting (`rules-python/`): `<pattern_name>.py`

## Installation

Voraussetzung: openHAB läuft bereits und die gewünschte Rule-Engine ist installiert
(siehe Haupt-README im Wurzelverzeichnis dieses Repos für die Add-on-Installation).

1. **Items kopieren:** Inhalt der Datei(en) unter `items/` in eine eigene
   `.items`-Datei unter `$OPENHAB_CONF/items/` einfügen.
2. **EINE Rule-Variante wählen und kopieren:**
   - **Rules DSL:** Datei(en) aus `rules-dsl/` nach `$OPENHAB_CONF/rules/` kopieren.
   - **JavaScript Scripting:** Datei(en) aus `rules-js/` nach `$OPENHAB_CONF/automation/js/` kopieren.
   - **Python 3 Scripting:** Datei(en) aus `rules-python/` nach `$OPENHAB_CONF/automation/python/` kopieren.
3. **Testen:** Auslöser manuell schalten und Log beobachten.

## Hinweis

Item- und Thing-Namen in diesem Beispiel sind Platzhalter und müssen an die
eigene Installation angepasst werden.
