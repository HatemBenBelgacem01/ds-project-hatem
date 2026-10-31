# Arbeitsregeln

## Arbeitsweise
- Plane vor jeder Änderung an Dateien und warte auf mein Ja. (Ich entscheide, was sich ändert.)
- Ein Paket pro Pull Request, mit einem Zweck und unter etwa 200 geänderten Zeilen. Schlage eine Aufteilung vor, wenn es grösser wird. (Kleine Pull Requests bleiben prüfbar.)
- Nie direkt auf `main` committen. Arbeite auf einem Branch und committe und pushe nur, wenn ich es sage. (`main` enthält nur geprüfte Arbeit.)
- Nach einem gemergten Pull Request zuerst auf `main` wechseln und pullen, bevor neue Arbeit beginnt. (Neue Arbeit startet vom geprüften Stand.)

## Daten und Pipeline
- Nur der Download-Schritt schreibt nach `data/raw`, mit genau einer Manifest-Zeile pro Download. (Rohdaten bleiben nachvollziehbar.)
- Jeder Schritt gibt genau eine Zeile aus, überspringt sich, wenn seine Ausgabe existiert, und baut mit `--force` neu. (Wiederholte Läufe sind billig und sichtbar.)
- Die Logik steckt in Funktionen, die eine Tabelle nehmen und eine Tabelle zurückgeben. (Ohne Dateien testbar.)

## Tests
- Tests laufen auf Fixtures in `tests/fixtures` und lesen nie aus `data/`. (Schnell und unabhängig vom Download.)
- Fixtures und erwartete Werte gehören mir: nicht ändern, und sag mir, wenn Code und Fixture sich widersprechen. (Sie sind die Spezifikation.)

## Notebooks
- Notebook-Zellen, die du anlegst, haben sichtbaren Code. (Ich lese, was gelaufen ist.)

## Dokumentation
- Entscheidungen, Hypothesen und KI-Nutzung gehen in `docs/log.md`, in der Form der bestehenden Einträge. (Ein nachvollziehbares Protokoll.)
- Wenn ich etwas noch nicht entschieden habe, frage nach oder markiere es als offen. Fülle die Lücke nicht selbst. (Lücken bleiben sichtbar.)
