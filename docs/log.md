# Log

## Hypothesis · 2026-10-08 · Die Zählstellen-IDs bleiben über die Jahre gleich

**Expected:** Mindestens 80 % aller Zählstellen melden in jedem Jahr.

**Test:** Zählstellen pro Jahr zählen und den Anteil ermitteln, der in allen Jahren auftaucht, mit der Gesamtdatei des Open-Data-Portals.

**Result:** 0 von 171 Zählstellen melden in allen 18 Jahren (2009–2026), Erwartung verfehlt.

**Decision:** Die Einheit der Tabelle ist der Standort durch Koordinaten identifiziert.

Offen:
- Zwei Koordinatenpaare können ein Meter voneinander entfernt liegen (2683405/1251617 and 2683406/1251617) und den gleichen Ort bezeichnen

## Decision · 2026-10-08 · source und first table

Die Pipeline soll die aus dem Portal stammende Gesamtdatei (die alle Jahre umfasst) verwenden – und nicht die jährlichen CSV-Dateien –, da es sich um einen einzigen Download handelt und die Datenexploration bereits auf dieser Basis durchgeführt wurde. Eine bekannte Einschränkung: Zum Zeitpunkt unserer Überprüfung endeten die Daten am 6. Juni 2026. Die erste Tabelle enthält pro Ort und Jahr jeweils eine Zeile, in der die Anzahl der Tage mit verfügbaren Daten sowie die durchschnittliche Anzahl der Fahrräder pro Tag (an diesen Tagen) aufgeführt sind. Welche Kombinationen aus Ort und Jahr als „vergleichbar“ gelten, bleibt noch zu klären.

Offen: Es ist noch nicht festgelegt, wann neuere oder jährliche Daten benötigt werden.

## Decision · 2026-10-08 · one-sided counts and data range

Bei Datensätzen, die nur einen der Werte VELO_IN oder VELO_OUT enthalten, wird die fehlende Seite als 0 gewertet, da manche Zähleinrichtungen nur eine Fahrtrichtung erfassen. Die Testdatei (`tests/fixtures/counts_small.csv`) enthält einen entsprechenden Eintrag, der dies absichert. Die Datei endet am 6. Juni 2026; die Einschränkung aus dem Eintrag oben gilt weiterhin. Bekannte Einschränkung: Bei einem Wechsel der Standort-ID (ID-Switch) wird ein einzelnes Viertelstundenintervall unter zwei verschiedenen Standort-IDs erfasst und folglich doppelt gezählt (Eintrag 2682278/1248325, 08.09.2017 00:00 Uhr, Standort-IDs 1997 und 2319). Dieser Zustand bleibt vorerst unverändert.

## Decision · 2026-10-31 · end date of the source file

Die Datei aus dem Portal in data/raw/ (Download am 29. Oktober 2026) endet am 26. Oktober 2026. Die frühere Datei in data/ endet am 6. Juni 2026. Das Jahr 2026 ist in beiden Dateien nicht vollständig.

## AI use · 2026-10-31 · load and derive steps

Delegated: the load and derive steps of uv run build, the functions and the test code.

Mine: 
- Geschäftsregel „Fehlende Richtung“: Fehlende Richtungsangaben werden explizit als 0 gezählt (kein Imputieren, kein Verwurf).
- Definition der Einheit „Ort“: Ein Ort ist strikt durch das Koordinatenpaar OST/NORD definiert, nicht über die Zählstellen-ID.
- Fixture `tests/fixtures/counts_small.csv`: Testdatensatz manuell zusammengestellt, inklusive des gezielten Randfalls mit 5 Velos in nur eine Richtung.
- Erwartete Zielwerte (Ground Truth): Referenztabelle von Hand berechnet (5 Velos pro Tag an 2 Tagen, 6 Velos an 1 Tag, 15 Velos an 1 Tag).

Checks passed:
- Tests green, including the failure check.
- Same table after deleting data/derived and rebuilding.
- 44 places, 5 of them reporting in every year from 2010 to 2025, as in the notebook.

## Decision · 2026-10-31 · comparable years

Verglichen werden 2019 und 2025. Vergleichbar sind die Orte mit Velo-Daten in beiden Jahren (17 von 32 bzw. 25 Orten). Die übrigen Orte werden im Ergebnis mit Grund ausgewiesen.

## AI use · 2026-10-31 · empty table test

Delegated: the test code for `place_year_table` on an empty table (`tests/test_derive.py`).

Mine:
- Vorgabe: Eingabe ist die Kopfzeile der bestehenden Fixture, keine neue Datei.
- Erwartung: Eine leere Tabelle mit den Rohdaten-Spalten ergibt eine leere Tabelle mit den fünf Ausgabespalten.

Checks passed:
- Tests green (7 passed).
- Failure check: the test fails for three broken versions of `place_year_table` (extra column, renamed column, one row instead of none) and passes for the real one.

## Decision · 2026-10-31 · growing and shrinking places

Ein Ort ist gewachsen oder geschrumpft, wenn sich die Anzahl Fahrräder und Fussgänger reduzieren oder erhöhen. Fahrräder und Fussgänger werden zusammengezählt, gegenläufige Änderungen werden gegeneinander verrechnet. Jede kleine Änderung zählt, es gibt keine Schwelle. Gemessen wird die Anzahl als Summe pro Jahr. Die Kategorie „unverändert“ entfällt. Ist die Summe genau gleich, bekommt der Ort keine Einstufung, sondern wird mit dem Grund „Summe gleich“ ausgewiesen.

## Decision · 2026-10-31 · repository settings

Ruleset „Protect main“ (ID 26285361): Änderungen an main nur über Pull Request, Prüfung „tests“ muss grün sein, 0 Freigaben, keine Ausnahmen, Force-Push und Löschen blockiert. Automatisches Löschen gemergter Branches ist aus, siehe unten.

## Decision · 2026-10-31 · delete merged branches automatically

Die Einstellung „Automatically delete head branches“ ist eingeschaltet (delete_branch_on_merge: true). Gemergte Branches werden auf GitHub automatisch gelöscht. Damit korrigiert dieser Eintrag die Aussage „Automatisches Löschen gemergter Branches ist aus“ im Eintrag „repository settings“ vom selben Tag.

## Hypothesis · 2026-11-02 · enough places are comparable

**Expected:** Mindestens 80 % der 44 Orte sind vergleichbar, also mindestens 36 Orte.

**Test:** Orte zählen, die in 2019 und 2025 an mindestens 300 Tagen Velodaten haben. Nur zählen, keine Veränderung.

**Result:** 10 von 44 Orten sind in 2019 und 2025 an mindestens 300 Tagen vergleichbar (14 in 2019, 19 in 2025). Erwartung verfehlt.

**Decision:** Die Regeln bleiben unverändert. Die Antwort bezieht sich nur auf die 10 Orte, die in 2019 und 2025 an mindestens 300 Tagen Velodaten haben. Die übrigen 34 Orte werden mit Grund ausgewiesen.

## Decision · 2026-11-02 · rules for the answer

- **Zählung:** nur Velos (VELO_IN + VELO_OUT). Ersetzt den Punkt zu Fussgängern im Eintrag vom 2026-10-31.
- **Tag:** zählt, wenn mindestens eine Velo-Messung vorliegt.
- **Vergleichbar:** mindestens 300 Tage mit Velodaten in 2019 und 2025.
- **Gewachsen:** mehr als +5 % Velos pro Tag. **Geschrumpft:** mehr als −5 %. Dazwischen **unverändert**. Ersetzt „keine Schwelle“ und „unverändert entfällt“ im Eintrag vom 2026-10-31.
- **Antwort für die Stadt:** „ja“, wenn mehr als die Hälfte der vergleichbaren Orte gewachsen ist, sonst „nein“.
- **ID-Wechsel:** bleibt bekannte Grenze, siehe Eintrag vom 2026-10-08.

## Hypothesis · 2026-11-02 · growth among comparable places

**Expected:** 8 von 10 vergleichbaren Orten sind gewachsen.

**Test:** Antwort-Schritt auf den echten Daten laufen lassen. Die Orte nach den Regeln vom 2026-11-02 einstufen und die gewachsenen zählen.

**Result:** 8 von 10 vergleichbaren Orten sind gewachsen, 2 geschrumpft, 0 unverändert. Erwartung bestätigt.

**Decision:** Die Antwort für die Stadt lautet „ja“. Sie gilt nur für die 10 vergleichbaren Orte. Die übrigen 34 Orte sind nicht vergleichbar und werden im Ergebnis mit Grund ausgewiesen.

## Hypothesis · 2026-11-03 · enough dry weekdays remain

**Expected:** 90 trockene Werktage mit Velodaten pro Ort und Jahr, an allen 10 Orten.
**Test:** Für jeden der 10 Orte aus data/derived/answer.parquet und jedes der Jahre 2019 und 2025 zählen, wie viele Werktage trocken sind und Velodaten haben. Die Wetterdateien nur einmal herunterladen, außerhalb von data/raw.
**Result:** Erwartung bestätigt. Alle 10 vergleichbaren Orte haben mindestens 117 trockene Werktage mit Velodaten im Jahr 2019 und mindestens 119 im Jahr 2025 (Erwartung: 90). Die Station hat insgesamt 120 (2019) und 130 (2025) trockene Werktage.
**Decision:** Die Quelle darf in die Pipeline. Die Regeln für trockene Werktage bleiben wie festgelegt.