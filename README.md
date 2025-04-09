# ScriptScheduler

Ein Python-Programm zum Planen und automatischen Neustarten von Python-Skripten mit einer benutzerdefinierten Zeitverzögerung.

## Funktionen

- **Zeitplanung**: Definiere eine Zeitspanne (in Stunden, Minuten, Sekunden), nach der Skripte geschlossen und neu gestartet werden.
- **Skriptverwaltung**: Füge Python-Skripte hinzu, entferne sie oder durchstöbere sie über eine grafische Benutzeroberfläche (GUI).
- **Automatischer Neustart**: Skripte werden in neuen Fenstern gestartet, nach der eingestellten Zeit geschlossen und wieder neu gestartet.
- **Stop-Funktion**: Beende alle laufenden Skripte und den Neustart-Prozess mit einem Stop-Button.
- **Timer-Anzeige**: Zeigt die verbleibende Zeit bis zum nächsten Neustart in Echtzeit an.
- **Konfigurationsspeicherung**: Speichert Zeit und Skriptpfade in einer JSON-Datei für die Wiederverwendung beim nächsten Start.

## Voraussetzungen

### Software
- **Python 3.x**: Das Programm wurde mit Python 3.11 getestet, sollte aber mit den meisten Python 3-Versionen kompatibel sein.
- **Betriebssystem**: Windows oder Linux/Mac (mit Anpassungen für die Fenstererstellung).

### Abhängigkeiten
Installiere die erforderlichen Python-Pakete mit pip:

```bash
pip install psutil
