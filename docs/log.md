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