# Tests.md – Testprotokoll openHAB Design Patterns

Diese Datei dokumentiert die Testabläufe für alle Design Patterns über die Karaf-Konsole (`openhab:send`/`openhab:update`). Die Befehle sind sprachunabhängig – es spielt keine Rolle, ob die zugrunde liegende Regel als Python, JavaScript oder Rules DSL vorliegt.

---

## associated-items

### Variante: group

```
openhab:update Sensor1 ON
```
Erwartung: Log zeigt `status1=Sensor1_Status status2=...` – reine Logausgabe, kein Item ändert sich (die Regel ist rein lesend). `status1` (Namenskonvention) ist immer eindeutig `Sensor1_Status`. `status2` (nur nach Tag „Status" gesucht) kann je nach interner Reihenfolge auch `Sensor2_Status` sein – erwartetes Verhalten, kein Fehler.

### Variante: naming

```
openhab:update Sensor1 ON
```
Erwartung: `Sensor1_Status` wird auf `ON` gesetzt.

```
openhab:update Sensor1 OFF
```
Erwartung: `Sensor1_Status` wird auf `OFF` gesetzt.

Schutzabfrage testen:
```
openhab:update Sensor1_Status ON
```
Erwartung: Regel läuft an, bricht aber sofort ab (kein Fehler im Log), da `Sensor1_Status` selbst kein `_Status`-Ziel mehr hat.

### Variante: semantic

Voraussetzung: Items mit Equipment-Tag angelegt (`MySensorEquipment` als Equipment-Gruppe, `SomeSensor` und `SomeSensor_Status` als Mitglieder mit passenden Tags).

```
openhab:update SomeSensor ON
```
Erwartung: Log zeigt `SomeSensor -> SomeSensor_Status = ON`, `SomeSensor_Status` wird `ON`.

```
openhab:update SomeSensor OFF
```
Erwartung: `SomeSensor -> SomeSensor_Status = OFF`, `SomeSensor_Status` wird `OFF`.

---

## bayes

Baseline setzen:
```
openhab:update myObservation1 ON
openhab:update myObservation2 DAY
openhab:update myObservation3 ON
openhab:update myObservation4 OFF
```
Erwartung: Log zeigt `Schlafwahrscheinlichkeit: 50.0%`, `mySleepSensor` bleibt `OFF`.

Indizien nacheinander umschalten:
```
openhab:update myObservation1 OFF
openhab:update myObservation3 OFF
openhab:update myObservation2 NIGHT
openhab:update myObservation4 ON
```
Erwartung: Wahrscheinlichkeit steigt nach jedem Schritt kumulativ; sobald sie 85 % überschreitet, schaltet `mySleepSensor` auf `ON`.

---

## bewegungssensor-timer

### Variante A: einfacher Timer

```
openhab:update MotionDetector1 ON
```
Erwartung: Nach 5 Minuten schaltet `MotionDetector1` automatisch auf `OFF` (per Befehl).

Reset-Test: `MotionDetector1` erneut auf `ON` setzen, bevor die 5 Minuten um sind → Timer wird neu gestartet, nur ein finaler `OFF`-Befehl.

### Variante B: gruppenbasiert

```
openhab:send MotionDetector1 ON
```
Erwartung: Log zeigt `MotionDetector1: Timer gestartet (300s)`. Nach 5 Minuten `OFF`-Befehl.

```
openhab:send MotionDetector2 ON
```
Erwartung: Unabhängiger, eigener Timer für `MotionDetector2`.

---

## cancel-activity

Zielwert und Ausgangszustand setzen:
```
openhab:update DimTarget 20
openhab:update DimLamp 0
```

Test A – durchlaufen lassen:
```
openhab:send StartDimTrigger ON
```
Erwartung: `DimLamp` steigt jede Sekunde um 1 %, bis 20 % erreicht sind, dann `Dimmen beendet bei 20%` im Log.

Test B – mittendrin abbrechen:
```
openhab:update DimTarget 80
openhab:update DimLamp 0
openhab:send StartDimTrigger ON
```
Kurz warten, dann:
```
openhab:send CancelDimTrigger ON
```
Erwartung: Log zeigt `Dimmen wird abgebrochen`, spätestens eine Sekunde später `Dimmen beendet bei X%` – `DimLamp` steigt nicht weiter bis 80.

---

## countdown-timer

Hinweis: `test6`/`test3`/`test2`/`testabort` nur mit `ON` ansteuern, nie manuell `OFF` senden (würde erneut triggern).

```
openhab:send test6 ON
```
Erwartung: `myCounter` = `6`, `testLamp` = `ON`. Zählt automatisch jede Minute runter.

```
openhab:send test6 ON
```
(während `myCounter` z. B. bei 3 steht) Erwartung: `myCounter` springt auf `6` (Verlängerung).

```
openhab:send test2 ON
```
(während `myCounter` z. B. bei 5 steht) Erwartung: `myCounter` wird auf `2` gesetzt (erzwungenes Überschreiben, da `test2` einen negativen Rohwert sendet).

```
openhab:send testabort ON
```
Erwartung: `myCounter` → `0`, `testLamp` → `OFF`, sofort.

---

## debounce

### Variante: simple

```
openhab:update Person1PresenceSensor ON
```
Erwartung: `Person1Presence` sofort `ON`.

```
openhab:update Person1PresenceSensor OFF
```
Erwartung: `Person1Presence` bleibt zunächst `ON`, springt erst nach 2 Minuten auf `OFF`.

Flattern-Test:
```
openhab:update Person1PresenceSensor ON
```
kurz warten, dann
```
openhab:update Person1PresenceSensor OFF
```
kurz warten, dann wieder
```
openhab:update Person1PresenceSensor ON
```
Erwartung: `Person1Presence` bleibt durchgehend `ON`, kein verzögertes `OFF` schlägt durch.

### Variante: generic

```
openhab:update Person1_PresenceSensors ON
```
Erwartung: Log zeigt `Verzoegerung=0s`, `Person1_Present` sofort `ON`.

```
openhab:update Person1_PresenceSensors OFF
```
Erwartung: Log zeigt `Verzoegerung=120s`, `Person1_Present` bleibt 2 Minuten bei `ON`.

`Person2_PresenceSensors` parallel ändern → eigener Timer, beeinflusst `Person1_Present` nicht.

---

## decoupled-notification-service

```
openhab:update VT_Notify_Warn "Warnung: Fenster offen"
```
Erwartung: Log zeigt `[VT_Notify_Warn] Warnung: Fenster offen`.

```
openhab:update VT_Notify_Alert "ALARM: Einbruch erkannt"
```
Erwartung: Log zeigt `[VT_Notify_Alert] ALARM: Einbruch erkannt`.

Entkoppelter Weg:
```
openhab:send SomeCondition ON
```
Erwartung: Löst `InfoNotification` aus, die `VT_Notify_Info` setzt, was wiederum die zentrale Regel triggert → zwei Regel-Ausführungen kurz hintereinander im Log.

---

## encoding-and-accessing

```
openhab:send vPresent ON
```
Erwartung: Log zeigt `Room1_Thermostat -> 21` und `Room2_Thermostat -> 22`, beide Thermostate erhalten die Befehle.

```
openhab:send vPresent OFF
```
Erwartung: `Room1_Thermostat -> 17`, `Room2_Thermostat -> 18`.

---

## event-debouncer

```
openhab:update motionSensor ON
```
Erwartung: Log zeigt `Bewegung erkannt - Licht einschalten`, `light` → `ON`. Nach 2s: `Debounce beendet - neue Events moeglich`.

Mehrere schnelle Events innerhalb 2s:
```
openhab:update motionSensor ON
openhab:update motionSensor OFF
openhab:update motionSensor ON
```
Erwartung: Nur der erste Befehl löst aus, die folgenden zeigen `Event ignoriert - Timer laeuft noch`.

Nach Ablauf (>2s warten), dann:
```
openhab:update motionSensor OFF
```
Erwartung: Wird wieder akzeptiert.

---

## expire-binding-based-timer

```
openhab:send StartMyTimerTrigger ON
```
Erwartung: Log zeigt `MyTimer gestartet (5 Minuten)`, `MyTimer` → `ON`. Nach 5 Minuten automatisch `OFF` → `MyTimer abgelaufen - Code nach Ablauf wird ausgefuehrt`.

Neustart-Test (Timer verlängern):
```
openhab:send StartMyTimerTrigger ON
```
erneut, bevor 5 Minuten um sind. Erwartung: Log zeigt zusätzlich `Timer ist bereits aktiv - wird neu gestartet`.

---

## gate-keeper

```
openhab:send WirelessController "433-send xxxxx 1 1"
```
Erwartung: Log zeigt `Befehl in Warteschlange eingereiht: ...`, danach `433: ...` (Shell-Ausführung schlägt ohne echte Hardware erwartungsgemäß fehl, kein Absturz).

```
openhab:send Outlet_A ON
```
Erwartung: Löst `OutletA` aus, sendet Befehl an `WirelessController`, landet in der Warteschlange.

Mehrere Befehle schnell hintereinander:
```
openhab:send Outlet_A ON
openhab:send Outlet_A OFF
openhab:send Outlet_A ON
```
Erwartung: Alle drei werden nacheinander mit mindestens 100 ms Abstand abgearbeitet, nicht gleichzeitig.

---

## generic-is-alive

```
openhab:update Item1Sensor1 5
```
Erwartung: Kein Alarm (normaler Wert, kein `UNDEF`).

```
openhab:update Item1Sensor1 UNDEF
```
Erwartung: Log zeigt `Item1Sensor1 meldet sich nicht mehr (UNDEF) - Alarm/Meldung ausloesen`.

```
openhab:update Item2Sensor3 UNDEF
```
Erwartung: Analoge, eigene Log-Zeile für `Item2Sensor3`.

```
openhab:update Item1Sensor1 3
```
Erwartung: Kein neuer Log-Eintrag (Trigger reagiert nur auf Wechsel zu `UNDEF`).

---

## graceful-retry-actions

Konfiguration setzen:
```
openhab:update RetryMaxAttempts 3
openhab:update RetryInitialInterval 5
openhab:update RetryMaxInterval 60
openhab:update RetryAlternativeAction "Bitte manuell pruefen"
```

Retry auslösen (Geräte-Items noch nie gesetzt = `NULL` = „offline"):
```
openhab:send RetryTrigger ON
```
Erwartung: Für jedes „offline" gebliebene Gerät: `attempt #1 failed`, dann nach 10s `attempt #2 failed`, nach 20s `attempt #3 failed` → `max retries reached!` → `NotificationItem` erhält die Alarmnachricht.

Genesungs-Fall:
```
openhab:update LightSwitch OFF
openhab:send RetryTrigger ON
```
Erwartung: `LightSwitch` bekommt sofort `command sent successfully!` (kein Retry), andere Geräte retryen weiter.

---

## groups-in-rules

Ausgangszustand:
```
openhab:update vTimeOfDay DAY
openhab:update vPresent ON
```

```
openhab:update vFrontDoor OPEN
```
Erwartung: Log zeigt `vFrontDoor was opened` (kein Alarm), `vFrontDoor_Timer` → `ON`, `vFrontDoor_LastUpdate` bekommt aktuellen Zeitstempel.

Alarmfall:
```
openhab:update vTimeOfDay NIGHT
openhab:update vPresent OFF
openhab:update vBackDoor OPEN
```
Erwartung: Log zeigt `vBackDoor was opened at night and no one is home`, `aAlerts` erhält dieselbe Nachricht als Befehl.

```
openhab:update vFrontDoor CLOSED
```
Erwartung: `vFrontDoor was closed`, `vFrontDoor_Timer` → `OFF`.

Timer-Ablauf simulieren (zwei Türen offen):
```
openhab:update vFrontDoor OPEN
openhab:update vBackDoor OPEN
openhab:send vFrontDoor_Timer OFF
```
Erwartung: `aAlerts`/Log zeigt `vFrontDoor has been open for over an hour and also open: vBackDoor`.

---

## human-readable-names

Voraussetzung: Map-Transformation-Add-on installiert, `admin.map` unter `$OPENHAB_CONF/transform/` vorhanden.

### Variante: simple

```
openhab:update MyItem ON
```
Erwartung: Log zeigt `Mein menschenlesbares Item ist jetzt ON` (übersetzter Name).

### Variante: complex

Test A – Zustand bleibt stabil:
```
openhab:update vNetwork_cerberos OFF
openhab:update vNetwork_cerberos ON
```
Erwartung: Nach 60s Log-Zeile `cerberos ist jetzt online`, `vNetwork_cerberos_Alerted` → `ON`.

Test B – Flattern wird gefiltert:
```
openhab:update vNetwork_cerberos OFF
openhab:update vNetwork_cerberos ON
```
kurz warten, dann
```
openhab:update vNetwork_cerberos OFF
```
Erwartung: Nur der letzte, stabil gebliebene Zustand wird nach 60s gemeldet, keine Zwischen-Meldung.

---

## hysteresis

```
openhab:update MyHeater OFF
openhab:update MyTemp 65
```
Erwartung: Log zeigt `Temp=65.0 -> Heizung=ON`, `MyHeater` → `ON`.

```
openhab:update MyTemp 69
```
Erwartung: `keine Aenderung` (Hysterese-Bereich), `MyHeater` bleibt `ON`.

```
openhab:update MyTemp 71
```
Erwartung: `Temp=71.0 -> Heizung=OFF`, `MyHeater` → `OFF`.

```
openhab:update MyTemp 69
```
Erwartung: Wieder `keine Aenderung`, `MyHeater` bleibt `OFF`.

Flatter-Test:
```
openhab:update MyTemp 67.9
openhab:update MyTemp 68.1
openhab:update MyTemp 67.9
```
Erwartung: Nur beim ersten `67.9` wird `Heizung=ON` berechnet; danach keine unnötigen Wiederholbefehle, da Zielzustand schon erreicht.

---

## item-metadata

```
openhab:update vNetwork_cerberos OFF
```
kurz warten, dann
```
openhab:update vNetwork_cerberos ON
```
Erwartung: Timer läuft an (kein Fehler im Log).

Nach 60s: Log zeigt `cerberos is now online`. Metadaten (`Alert`-Namespace) sollten `alerted=ON` zeigen, prüfbar via:
```
curl http://localhost:8080/rest/items/vNetwork_cerberos/metadata/Alert
```

Flapping-Test:
```
openhab:update vNetwork_cerberos OFF
```
kurz warten (< 60s), dann
```
openhab:update vNetwork_cerberos ON
```
Erwartung: Timer wird abgebrochen, kein Log-Eintrag für den Zwischenzustand.

---

## kaskadierende-timer

Vorbereitung:
```
openhab:update Irrigation_Zone_1_Time 1
openhab:update Irrigation_Zone_2_Time 1
openhab:update Irrigation_Zone_3_Time 1
```

```
openhab:send Irrigation_Manual ON
```
Erwartung: Log zeigt `Bewaesserung gestartet, Zone 1 aktiv`, `Zone Irrigation_Zone_1 an fuer 1 Minuten`, `Irrigation_Zone_1` → `ON`.

Nach ~1 Minute: `Zone Irrigation_Zone_1 aus`, `Irrigation_Zone_2 an`, usw. Nach der letzten Zone: `Bewaesserung abgeschlossen`, `Irrigation_Manual` → `OFF`.

Abbruch mitten in der Kaskade:
```
openhab:send Irrigation_Manual ON
```
während eine Zone läuft:
```
openhab:send Irrigation_Manual OFF
```
Erwartung: Laufender Timer wird sofort abgebrochen, alle Zonen auf `OFF`, `Irrigation_Curr` → `OFF`.

---

## konfigurationsverwaltung

```
openhab:update SomeLight ON
```
Erwartung: Log zeigt `MaxDim: 90%, DimPeriod: 20s`.

---

## lichtsteuerungssystem

### Variante: bewegung

```
openhab:update Light1 OFF
openhab:update MotionSensor1 ON
```
Erwartung: Log zeigt `Bewegung erkannt - Light1 eingeschaltet (10 Min. Timer)`, `Light1` → `ON`.

```
openhab:update MotionSensor1 OFF
openhab:update MotionSensor1 ON
```
mit `Light1` bereits `ON`: Erwartung: `Bewegung erkannt, Light1 war aber bereits an`, kein neuer Timer.

### Varianten: zeit / dynamisch

Cron-getriggert (feste Uhrzeiten) – nicht direkt über Konsole auslösbar, nur durch Abwarten oder eine temporäre Kurzzeit-Cron-Version testbar.

---

## long-press

```
openhab:update ButtonState ON
```
sofort danach (< 500 ms):
```
openhab:update ButtonState OFF
```
Erwartung: Log zeigt `Kurzer Druck (Xms) -> Toggle`, `TargetLight` schaltet um, `ButtonPressTime` zeigt Dauer.

```
openhab:update ButtonState ON
```
mind. 1 Sekunde warten, dann:
```
openhab:update ButtonState OFF
```
Erwartung: `Langer Druck (Xms) -> Dimmen`, `TargetLight` erhält `INCREASE`.

Fallback-Mechanismus:
```
openhab:update ButtonState ON
```
und nichts weiter tun. Erwartung: Nach 5s greift Fallback, `ButtonState` wird automatisch auf `OFF` zurückgesetzt.

---

## looping-timers

Vorbereitung (Nachtszenario):
```
openhab:update vTimeOfDay NIGHT
openhab:update CurrentTemp 25
openhab:update TargetTemp 22
openhab:update Fan OFF
```

```
openhab:update MotionSensor ON
```
Erwartung: `Fan` → `ON` (weil `current > target`). Schleife läuft jede Minute weiter.

```
openhab:update CurrentTemp 20
```
Bis zu 60s warten. Erwartung: `Fan` → `OFF`.

```
openhab:update vTimeOfDay DAY
```
Bis zu 60s warten. Erwartung: Keine weiteren automatischen Durchläufe mehr.

---

## manuelle-trigger-erkennung

### Variante: deadman

```
openhab:send SomeRuleTrigger ON
```
Erwartung: `DeadMansSwitch` durchläuft `RULE` → `MANUAL`, `WatchedItem1` wird `ON`. Ergebnis timingabhängig (dokumentierte Schwäche des Patterns selbst).

```
openhab:send WatchedItem1 OFF
```
Erwartung: `Element wurde manuell ausgeloest` (kein vorheriges `RULE`-Signal).

### Variante: proxy

```
openhab:send HallLight_UI ON
```
Erwartung: Log zeigt `Quelle=UI -> HallLight = ON`, `HallLight_Proxy`/`HallLight_Rules` werden aktualisiert, `HallLight_Device` erhält Befehl.

### Variante: timestamp

```
openhab:update vTimeOfDay DAY
```
Erwartung: Log zeigt `vTimeOfDay=DAY -> Lichter angepasst`, `LightMorningRoom` → `ON`, `LightHallway` → `OFF`.

---

## mqtt-state-supervision

```
openhab:send MySwitch ON
```
Erwartung: Log zeigt `Ueberwachung gestartet, erwarte ON innerhalb 30s`. Da Autoupdate greift: kurz danach `Zustand hat sich geaendert, Ueberwachung wird abgebrochen`, kein Alarm.

Alarm-Fall erzwingen (Item mit `autoupdate="false"`):
```
openhab:send MySwitch ON
```
Erwartung: Kein Zustandswechsel-Log, nach 30s: `MySwitch hat den Zustand ON nicht erreicht`.

---

## multisensor-aggregation

### Gewichtete Summe

```
openhab:update MotionSensor OFF
openhab:update WindowSensor OPEN
openhab:update LightSensor 50
```
Erwartung: `Aggregierte Konfidenz: 0.0`, `Keine Anwesenheit.`

```
openhab:update MotionSensor ON
```
Erwartung: `0.7` → `Anwesenheit erkannt!`

```
openhab:update MotionSensor OFF
openhab:update WindowSensor CLOSED
openhab:update LightSensor 150
```
Erwartung: `0.8` → `Anwesenheit erkannt!`

### Bayes-Variante

```
openhab:update MotionSensor ON
openhab:update WindowSensor CLOSED
openhab:update LightSensor 150
```
Erwartung: Wahrscheinlichkeit deutlich über 60 % → `Anwesenheit erkannt!`

```
openhab:update MotionSensor OFF
openhab:update WindowSensor OPEN
openhab:update LightSensor 50
```
Erwartung: Deutlich unter 60 % → `Keine Anwesenheit.`

---

## notifications-in-groups

```
openhab:update Temp1 20
```
Erwartung: Kein Log-Eintrag.

```
openhab:update Temp2 27
```
Erwartung (zwischen 9–21 Uhr Serverzeit): `Temp warn Temp2: 27.0 Grad C`.

```
openhab:update Temp3 32
```
Erwartung: `Temp alert Temp3: 32.0 Grad C` (zeitunabhängig).

```
openhab:update Temp4 31
openhab:update Temp5 35
```
Erwartung: Für jedes Item eine eigene `Temp alert ...`-Zeile.

---

## primer-mit-hablladin

```
openhab:update GLSM 1
```
Erwartung: `GarageLights` → `ON`.

```
openhab:update GLSM 2
```
Erwartung: `GarageLights` → `ON`, nach 5 Minuten automatisch Wechsel zu Zustand `3` (Blinken).

```
openhab:update GLSM 0
```
Erwartung: `GarageLights` → `OFF`, laufender Timer abgebrochen.

```
openhab:update GarageLightsProxy ON
```
Erwartung: `GLSM` → `1`.

Tor-Ereignis nach Sonnenuntergang:
```
openhab:update Sun_Set 2020-01-01T00:00:00
openhab:update GLSM 0
openhab:update LeftGarageDoor OPEN
```
Erwartung: `Tor geoeffnet nach Sonnenuntergang -> Licht mit Timer an`, `GLSM` → `2`.

Gegentest (Sonnenuntergang in der Zukunft):
```
openhab:update Sun_Set 2030-01-01T00:00:00
openhab:update GLSM 0
openhab:update LeftGarageDoor CLOSED
openhab:update LeftGarageDoor OPEN
```
Erwartung: `kein Trigger (vor Sonnenuntergang...)`, `GLSM` bleibt `0`.

---

## proxy-item

### Variante: einfach

```
openhab:send ProxySwitch ON
```
Erwartung: Log zeigt `ProxySwitch -> BoundSwitch: ON`.

```
openhab:update BoundSwitchUpdates ON
```
Erwartung: `BoundSwitchUpdates -> ProxySwitch: ON`.

### Variante: garage

```
openhab:update GarageControllerComputer ON
openhab:update GarageControllerService ON
openhab:send Large_Garagedoor_Opener ON
```
Erwartung: Kein Alarm, `Large_Garagedoor_Opener_Linked` erhält Befehl.

```
openhab:update GarageControllerService OFF
openhab:send Small_Garagedoor_Opener ON
```
Erwartung: `AlertItem` erhält `Garagentor-Controller offline!`, zusätzlich wird trotzdem `Small_Garagedoor_Opener_Linked` angesteuert.

---

## rate-limit

```
openhab:send RateLimitTrigger ON
```
Erwartung: Log zeigt `Rate-limited action`.

```
openhab:send RateLimitTrigger ON
```
sofort nochmal: Erwartung: `Ereignis ignoriert, Sperrzeit laeuft noch`.

---

## rule-deaktivierung

```
openhab:send vChristmas ON
```
Erwartung: Log zeigt `enabled=True`/`enabled=False`-Meldung; „Christmas Lights"-Regel bleibt aktiviert, „MBR Humidifier"-Regel wird deaktiviert (in UI unter Einstellungen → Regeln prüfen).

```
openhab:send vChristmas OFF
```
Erwartung: Umgekehrt – „Christmas Lights" deaktiviert, „MBR Humidifier" aktiviert.

---

## rule-manager

```
openhab:send DummyExecTrigger ON
```
Erwartung: `isRunningExampleRule` → `ON`, Log zeigt `Teil 1`/`Teil 2 der Regel wird ausgefuehrt`, danach `isRunningExampleRule` → `OFF`.

```
openhab:send exampleRule OFF
```
Erwartung: Zielregel wird in der UI deaktiviert.

```
openhab:send DummyExecTrigger OFF
openhab:send DummyExecTrigger ON
```
Erwartung: Keine Log-Zeilen mehr (Regel deaktiviert).

```
openhab:send exampleRule ON
```
Erwartung: Regel wieder aktiv, nächster Trigger läuft wieder normal durch.

---

## rule-refresh

Reihenfolge beachten: Items vor dem Skript laden.

```
openhab:update DynamicTriggerItem1 ON
```
Erwartung: Log zeigt `DynamicTriggerItem1 hat sich geaendert (dynamischer Trigger)`.

```
openhab:send Reload_Item ON
```
Erwartung: Log zeigt `Trigger werden beim naechsten Neuladen des Skripts aktualisiert`.

---

## rule-strukturierung

### Variante: ohne Gruppen

```
openhab:update Foo ON
```
Erwartung: `One of the Items is NULL` (Bar/Baz noch nicht gesetzt).

```
openhab:update Bar OFF
openhab:update Baz OFF
```
Erwartung: `on_count=1` → `Buzz=OFF`.

```
openhab:update Bar ON
```
Erwartung: `on_count=2` → `Buzz=ON`.

### Variante: mit Gruppe

Gleicher Testablauf, gleiches erwartetes Verhalten über `MyGroup`.

---

## rule-verriegelung

```
openhab:update MyItem ON
```
Erwartung: Log zeigt `Regelcode ausgefuehrt, gesperrt bis <Zeitpunkt in 24h>`.

```
openhab:update MyItem OFF
```
Erwartung: `Event ignoriert, gesperrt bis <derselbe Zeitpunkt>`.

```
openhab:update MyItem ON
```
Erwartung: Wieder `Event ignoriert...` (Sperre gilt weiterhin).

---

## sensor-aggregation

Ausgangszustand:
```
openhab:update vPresent OFF
openhab:update tPresent OFF
```

```
openhab:send PersonOneSensorOne ON
```
Erwartung: `gPresent changed to 1.0`, `Someone came home`, `vPresent` → `ON`.

```
openhab:send PersonOneSensorOne OFF
```
Erwartung: `gPresent changed to 0.0`, `Everyone is away, setting timer`, `tPresent` → `ON`.

```
openhab:send tPresent OFF
```
Erwartung: `Everyone is away, setting house to away`, `vPresent` → `OFF`.

Anti-Flapping:
```
openhab:send PersonOneSensorOne ON
```
kurz warten, dann
```
openhab:send PersonOneSensorOne OFF
```
sofort danach
```
openhab:send PersonTwoSensorOne ON
```
Erwartung: `Someone came home`, `tPresent` sofort zurückgesetzt (Timer abgebrochen), `vPresent` bleibt `ON`.

---

## state-machine-driven-groups

### Variante: einfach

```
openhab:update vTimeOfDay MORNING
```
Erwartung: Log zeigt `vTimeOfDay=MORNING -> Lichtgruppen angesteuert`, entsprechende Lichter je nach Gruppenzugehörigkeit `ON`/`OFF`.

```
openhab:update vTimeOfDay NIGHT
```
Erwartung: Analog für die Nacht-Gruppen.

### Variante: komplex

Sollwerte zuerst setzen:
```
openhab:update aFrontLamp_MORNING ON
openhab:update aFrontLamp_DAY OFF
openhab:update aFamilyLamp_MORNING 30
openhab:update aFamilyLamp_DAY 80
```

```
openhab:update vTimeOfDay MORNING
```
Erwartung: `aFrontLamp -> ON`, `aFamilyLamp -> 30`.

```
openhab:update vTimeOfDay DAY
```
Erwartung: `aFrontLamp -> OFF`, `aFamilyLamp -> 80`.

Wichtig: Sollwerte immer **vor** der Tageszeit-Änderung setzen, sonst `NULL`-Warnung statt Aktion.

---

## switch-dimmer

Nur `switch_dimmer_light` ist ohne echte Hardware testbar (`switch_dimmer` selbst braucht echte EnOcean-Kanal-Ereignisse).

```
openhab:update MyColorLight 0,0,0
openhab:send MySwitch1UpShortPress ON
```
Erwartung: `MyColorLight` → `ON`-Befehl.

```
openhab:send MySwitch1UpLongPress ON
```
Erwartung: `MyColorLight` erhält `INCREASE`.

```
openhab:update MyColorLight 0,0,50
openhab:send MySwitch1UpShortPress ON
```
Erwartung: `MyColorLight` → `OFF`-Befehl.

```
openhab:send MySwitch1UpLongPress ON
```
Erwartung: `MyColorLight` erhält jetzt `DECREASE` (nicht mehr `INCREASE`).

---

## szenenmanagement

```
openhab:send callScriptItem SwitchOn_LightsStairs025
```
Erwartung: Alle `_DIMM`-Items → `25`, alle `_TOGGLE`-Items → `ON`.

```
openhab:send callScriptItem SwitchOn_LightsStairs100
```
Erwartung: Alle `_DIMM` → `100`.

```
openhab:send callScriptItem SwitchOff_LightsStairs
```
Erwartung: Alle `_TOGGLE` → `OFF`.

```
openhab:send callScriptItem NichtVorhandeneSzene
```
Erwartung: `Unbekannte Szene: NichtVorhandeneSzene`, kein Absturz.

---

## time-of-day

Kein manueller Trigger nötig – Cron feuert jede Minute.

Bis zu 60s warten, dann Log prüfen: Erwartung: `vTimeOfDay -> <erwartete Kategorie>` passend zur aktuellen Uhrzeit/Wochentag. Solange sich die Kategorie nicht ändert, erscheint keine weitere Log-Zeile.

---

## timer-management

```
openhab:update FrontDoor OPEN
```
Erwartung: Log zeigt `FrontDoor: Timer gestartet (1h)`.

```
openhab:update FrontDoor CLOSED
```
Erwartung: `FrontDoor: geschlossen, kein Timer noetig` (Timer abgebrochen).

```
openhab:update FrontDoor OPEN
openhab:update BackDoor OPEN
```
Erwartung: Zwei unabhängige Timer.

```
openhab:update FrontDoor CLOSED
```
Erwartung: Nur der `FrontDoor`-Timer wird abgebrochen, `BackDoor` läuft unberührt weiter.

---

## toggle-pattern

```
openhab:update modbusSwitchOut1 OFF
openhab:send mqttSwitchIn2 OFF
```
Erwartung: `modbusSwitchOut1` → `ON`.

```
openhab:send mqttSwitchIn2 OFF
```
Erwartung: `modbusSwitchOut1` → `OFF`.

(Bei der Feedback-Variante zusätzlich prüfen, dass die UI-Anzeige nach jedem Umschalten korrekt zum zuletzt gesendeten Befehl passt.)

---

## trennung-von-verhaltensweisen

### Variante: alarm

```
openhab:send Notification_Proxy_Info "Testnachricht Info"
```
Erwartung: Log zeigt `Info-Benachrichtigung: Testnachricht Info`.

```
openhab:send Notification_Proxy_Alert "Testalarm"
```
Erwartung: `Alarm-Benachrichtigung: Testalarm`.

### Variante: cloudy

```
openhab:update vCloudiness 30
```
Erwartung: `vCloudiness=30.0 -> vIsCloudy=OFF`.

```
openhab:update vCloudiness 70
```
Erwartung: `vCloudiness=70.0 -> vIsCloudy=ON`.

```
openhab:update vCloudiness 75
```
Erwartung: Keine neue Log-Zeile (Zustand bereits `ON`, Guard verhindert unnötige Aktualisierung).

---

## watering-system

```
openhab:update VT_Watering_Duration 10
```

```
openhab:send SomeCondition ON
```
Erwartung: `VT_Watering_Zone1` → `START`, triggert `WateringService` → Log zeigt `Starte Bewaesserung fuer Zone VT_Watering_Zone1 fuer 10 Sekunden`, `Zone1_Relay` → `ON`.

Nach 10 Sekunden: Erwartung: `Beende Bewaesserung fuer Zone VT_Watering_Zone1`, `Zone1_Relay` → `OFF`.

```
openhab:update VT_Watering_Zone2 START
```
Erwartung: Eigener Timer, `Zone2_Relay` → `ON`, nach 10s → `OFF`, unabhängig von Zone 1.

Schutzabfrage (Dauer nicht gesetzt): Bei frischem Zonen-Item ohne vorheriges `VT_Watering_Duration` sollte statt eines Absturzes nur `VT_Watering_Duration ist noch nicht gesetzt` im Log erscheinen.

---

## Nicht bzw. nur eingeschränkt testbar

- **cst** – Ergebnis beim letzten Test unklar/unbestätigt (Verdacht auf fehlerhaftes Triggerverhalten bei gleichzeitiger Änderung zweier Gruppenmitglieder), noch offen.
- **gruppenbasierte-persistenz** – reine Persistenz-Konfiguration ohne Rule-Code, nicht über Konsole testbar.
- **time-of-last-update** – Profile-Feature reagiert nur auf echte Channel-Events vom Gerät, nicht auf manuelle Konsolen-Updates.
- **simple-state-machine** – nur cron-getriggert (6 Uhr morgens), nicht direkt auslösbar.
- **lichtsteuerungssystem** (zeit/dynamisch) – cron-getriggert, nur mit temporär geänderter Cron-Angabe testbar.
- **switch-dimmer** (Hauptdatei) – benötigt echte EnOcean-Hardware.
