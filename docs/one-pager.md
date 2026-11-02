# Ein-Seiter: Wächst das Radfahren in Zürich?

## Why

**Frage, wie sie gestellt wurde:** „Wächst das Radfahren in Zürich?"

**Wer liest das Ergebnis:** Eine Planerin im Verkehrsamt. Sie muss die Antwort öffentlich vertreten und braucht deshalb nachvollziehbare Belege, auch dafür, welche Standorte berücksichtigt wurden und welche nicht.

## What

**Was der Leser bekommt:** Eine Tabelle mit einer Zeile pro Ort und Jahr, darüber ein Satz, der die Antwort für die Stadt nennt.

**Einheit des Ergebnisses:** Änderung 2026-10-08: Die Einheit ist der Ort (Koordinatenpaar OST/NORD), nicht die Zählstellen-ID. Grund: Ein Ort bekommt im Lauf der Jahre neue IDs. Nach ID hält keine Zählstelle durch alle Jahre, nach Ort sind es 11 % der Velo-Orte. Siehe docs/log.md.

**Vergleich:** Zwei Jahre, 2019 und 2025, jeweils ein volles Kalenderjahr. Gezählt werden nur Velos.

**Aussage:** Die Antwort gilt nur für die vergleichbaren Orte. Der Satz für die Stadt nennt, wie viele Orte das sind.

## Regeln

Festgelegt am 2026-11-02, siehe docs/log.md.

| Regel | Entscheidung |
|---|---|
| Zählung | nur Velos (VELO_IN + VELO_OUT) |
| Tag | zählt, wenn mindestens eine Velo-Messung vorliegt |
| Vergleichbar | an mindestens 300 Tagen Velodaten in 2019 und in 2025 |
| Gewachsen | mehr als +5 % Velos pro Tag |
| Geschrumpft | mehr als −5 % Velos pro Tag |
| Unverändert | dazwischen |
| Antwort „ja“ | mehr als die Hälfte der vergleichbaren Orte ist gewachsen |
| ID-Wechsel | bekannte Grenze, siehe Eintrag vom 2026-10-08 |

Die Hypothese „genug Orte sind vergleichbar“ wurde nicht bestätigt: 10 von 44 Orten erfüllen die Bedingung. Die Regeln bleiben, die Aussage wird auf diese 10 Orte begrenzt.

## How

1. Jahresdaten der Velo- und Fußgängerzählungen der Stadt Zürich über das Open-Data-Portal herunterladen.
2. Zeitstempel in echte Datumswerte umwandeln.
3. Pro Ort und Jahr zählen: an wie vielen Tagen Daten vorliegen und wie viele Velos pro Tag im Mittel gezählt wurden.
4. Orte nach den Regeln oben als vergleichbar, gewachsen, geschrumpft oder unverändert einstufen.
5. Ergebnis als Tabelle und einen Satz für die Stadt ausgeben.

Zweite Runde, später: nur trockene Wochentage, mit Wetterdaten.

## Non-goals

- **Keine Gesamtzahl aller Velofahrenden in Zürich.** Die Zählstellen messen nur, was an ihrem Ort vorbeikommt.
- **Keine Ursachen.** Ob Veloinfrastruktur, Wetter oder Pandemie den Trend erklären, wird nicht untersucht.
- **Keine Prognose** für künftige Jahre.
- **Keine stillen Auslassungen.** Jeder Ort bekommt entweder einen Wert oder eine Begründung, warum er nicht vergleichbar ist.

## Done

- Jeder Ort hat entweder einen Wert für 2019 und 2025 oder einen genannten Grund, warum er nicht verglichen werden kann.
- Die Antwort für die Stadt steht in einem Satz, nennt die Zahl der vergleichbaren Orte und die Regel dahinter.
- Eine Person, die das Repository klont und den Befehl `uv run build` ausführt, bekommt dieselbe Tabelle.
