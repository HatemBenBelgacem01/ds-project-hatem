# Ein-Seiter: Wächst das Radfahren in Zürich?

## Why

**Frage, wie sie gestellt wurde:** „Wächst das Radfahren in Zürich?"

**Wer liest das Ergebnis:** Eine Planerin im Verkehrsamt. Sie muss die Antwort öffentlich vertreten und braucht deshalb nachvollziehbare Belege, auch dafür, welche Standorte berücksichtigt wurden und welche nicht.

## What

**Was der Leser bekommt:** Eine Tabelle mit einer Zeile pro Ort und Jahr, darüber ein Satz, der die Antwort für die Stadt nennt.

**Einheit des Ergebnisses:** Änderung 2026-10-08: Die Einheit ist der Ort (Koordinatenpaar OST/NORD), nicht die Zählstellen-ID. Grund: Ein Ort bekommt im Lauf der Jahre neue IDs. Nach ID hält keine Zählstelle durch alle Jahre, nach Ort sind es 11 % der Velo-Orte. Siehe docs/log.md.

**Vergleich:** Zwei Jahre, 2019 und 2025, jeweils ein volles Kalenderjahr. Die Regeln für „vergleichbar", „gewachsen" und „ja" sind offen und werden vor der ersten Auswertung festgelegt.

## How

1. Jahresdaten der Velo- und Fußgängerzählungen der Stadt Zürich über das Open-Data-Portal herunterladen.
2. Zeitstempel in echte Datumswerte umwandeln.
3. Pro Ort und Jahr zählen: an wie vielen Tagen Daten vorliegen und wie viele Velos pro Tag im Mittel gezählt wurden.
4. Orte nach festgelegten Regeln als vergleichbar, gewachsen, geschrumpft oder unverändert einstufen.
5. Ergebnis als Tabelle und einen Satz für die Stadt ausgeben.

Zweite Runde, später: nur trockene Wochentage, mit Wetterdaten.

## Non-goals

- **Keine Gesamtzahl aller Velofahrenden in Zürich.** Die Zählstellen messen nur, was an ihrem Ort vorbeikommt.
- **Keine Ursachen.** Ob Veloinfrastruktur, Wetter oder Pandemie den Trend erklären, wird nicht untersucht.
- **Keine Prognose** für künftige Jahre.
- **Keine stillen Auslassungen.** Jeder Ort bekommt entweder einen Wert oder eine Begründung, warum er nicht vergleichbar ist.

## Done

- Jeder Ort hat entweder einen Wert für 2019 und 2025 oder einen genannten Grund, warum er nicht verglichen werden kann.
- Die Antwort für die Stadt steht in einem Satz, und die Regel dahinter ist benannt.
- Eine Person, die das Repository klont und den Befehl `uv run build` ausführt, bekommt dieselbe Tabelle.