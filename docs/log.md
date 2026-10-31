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
