# Wissenschafts Projekt

## Beschreibung
Das **Wissenschafts Projekt** ist ein Python-basiertes Forschungstool, das entwickelt wurde, um Simulationen im Bereich der Elektromagnetik und Gravitation durchzuführen. Ziel ist es, diese Simulationen zu nutzen, um die Einheitliche Feldtheorie besser zu verstehen.

## Projektstruktur
```
WissenschaftsProjekt/
├── src/
│   ├── main.py
│   ├── database/
│   │   ├── simulation_data.db
│   │   ├── conf/
│   │   │   ├── db_init.py
│   │   │   ├── db_reset.py
│   ├── logs/
│   │   ├── simulations.log
│   ├── scripts/
│   │   ├── conf/
│   │   │   ├── reset.py
│   │   ├── funcs/
│   │   │   ├── timestamp_dec.py
│   │   ├── simulations/
│   │   │   ├── electromagnetic_simulation.py
│   │   │   ├── gravity_simulation.py
│   │   │   ├── strong_force_simulation.py
│   │   │   ├── weak_force_simulation.py
├── LICENSE
├── README.md
├── .gitignore
```

## Installation
1. Stelle sicher, dass Python 3.10 oder höher installiert ist.
2. Klone dieses Repository:
   ```bash
   git clone https://github.com/HansKnolle08/EinheitlicheFeldtheorie.git
   ```
3. Installiere alle benötigten Abhängigkeiten (falls vorhanden):
   ```bash
   pip install -r requirements.txt
   ```
4. Stelle sicher, dass SQLite aktiviert ist.

## Nutzung
Starte die Simulationen, indem du den folgenden Befehl ausführst:
```bash
python src/main.py
```
Das Programm führt die elektromagnetischen und Gravitationssimulationen parallel aus und speichert die Ergebnisse in der SQLite-Datenbank.

## Features
- **Elektromagnetische Simulation:** Berechnung von elektrischen und magnetischen Feldern basierend auf physikalischen Konstanten.
- **Gravitationssimulation:** Modellierung von Gravitationsfeldern und deren Dynamiken.
- **Datenbankintegration:** Ergebnisse werden in einer SQLite-Datenbank gespeichert.
- **Logging:** Simulationsdetails werden in einer Log-Datei protokolliert.

## Voraussetzungen
- Python 3.10 oder höher
- SQLite

## Lizenz
Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert.

## Credits
Dieses Projekt wurde von **Hans-Christian Knolle** entwickelt.

---

Viel Erfolg bei der Erforschung der Einheitlichen Feldtheorie!
