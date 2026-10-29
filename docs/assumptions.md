# Assumption

Annahmen, die wahr sein müssen, damit die Schritte in „How" die Tabelle in „What" liefern.
Sortiert nach Wichtigkeit (hoch zuerst), bei gleicher Wichtigkeit nach Belegen (wenig zuerst).
Die Nummer verweist auf die ursprüngliche Liste.

| Nr. | Annahme | Wichtigkeit | Belege | Status |
|----:|---------|-------------|--------|--------|
| 1 | Im Open-Data-Portal gibt es für 2019 und für 2025 je eine Jahresdatei, und jede deckt das ganze Kalenderjahr ab. | hoch | wenig | ungeprüft |
| 5 | Die Zählmethode und das Gerät an einem Ort sind 2019 und 2025 gleich, sodass die Zahlen dasselbe messen. | hoch | wenig | ungeprüft |
| 8 | Jedes Zeitintervall steht nur einmal in den Daten, sodass beim Summieren pro Tag nichts doppelt zählt. | hoch | wenig | ungeprüft |
| 4 | Mehrere IDs am selben Ort messen verschiedene Ströme, zum Beispiel Richtungen oder Spuren, die man addieren darf, und nicht zweimal denselben Strom. | hoch | viel | ungeprüft |
| 10 | Der Mittelwert über die Tage mit Daten steht für das ganze Jahr, weil die Lücken nicht gehäuft in einer Jahreszeit liegen. | hoch | viel | ungeprüft |
| 7 | Die Zeitstempel haben ein eindeutiges Format mit klarer Zeitzone, und jeder Wert lässt sich genau einem Kalendertag zuordnen. | mittel | wenig | ungeprüft |
| 2 | Ein Ort hat 2019 und 2025 genau dasselbe Koordinatenpaar OST/NORD, sodass gleiche Koordinaten auch wirklich den gleichen Ort bedeuten. | mittel | viel | teilweise geprüft |
| 3 | Die Daten trennen Velos von Fussgängern, also gibt es eine eigene Spalte oder Kennung nur für Velos. | niedrig | wenig | ungeprüft |
| 6 | Fehlende Messungen sind leer und nicht als Null eingetragen, sodass „keine Daten" und „keine Velos" zu unterscheiden sind. | niedrig | wenig | ungeprüft |
| 9 | Ein Tag mit Daten ist ein vollständig gemessener Tag, sodass halbe Tage den Mittelwert pro Tag nicht nach unten ziehen. | niedrig | wenig | ungeprüft |
