import sqlite3
import time
import math
import logging
import os

# Logging-Konfiguration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', '..', 'database', 'simulation_data.db')
LOG_PATH = os.path.join(BASE_DIR, '..', '..', 'logs', 'simulations.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

# Konstanten für die starke Wechselwirkung
STRONG_FORCE_CONSTANT = 1.0  # Beispielkonstante (keV*fm^2)
QUARK_DISTANCE_THRESHOLD = 1e-15  # Maximale Reichweite der starken Wechselwirkung in Metern

# Beispielteilchen
particles = [
    {"id": 1, "position": (0.0, 0.0, 0.0)},
    {"id": 2, "position": (1e-16, 0.0, 0.0)}  # Abstand innerhalb der Reichweite
]

def compute_strong_force(p1, p2):
    """
    Berechnet die starke Wechselwirkung zwischen zwei Teilchen.
    """
    # Abstand zwischen den Teilchen berechnen
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    distance = math.sqrt(dx**2 + dy**2 + dz**2)

    if distance > QUARK_DISTANCE_THRESHOLD:
        force = 0  # Keine starke Wechselwirkung außerhalb der Reichweite
    else:
        force = STRONG_FORCE_CONSTANT / (distance**2)

    logging.debug(f"Berechnete starke Wechselwirkung: {force:.2e} N bei Abstand {distance:.2e} m")
    return force

def insert_strong_force_data(time, particle_id, position, force):
    """
    Speichert die Daten der starken Wechselwirkung in der Datenbank.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO strong_force_data (time, particle_id, position_x, position_y, position_z, force)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (time, particle_id, position[0], position[1], position[2], force))

    conn.commit()
    conn.close()
    logging.info(f"Daten für Teilchen {particle_id} bei Zeit {time}s gespeichert.")

def run_strong_force_simulation():
    """
    Führt die Simulation der starken Wechselwirkung durch und speichert die Ergebnisse.
    """
    total_time = 3600  # Simulation für 1 Stunde
    dt = 60  # Zeitschritt in Sekunden

    logging.info(f"Starke Wechselwirkungssimulation startet. Gesamtdauer: {total_time / 60} Minuten, Zeitschritt: {dt} Sekunden.")

    current_time = 0
    while current_time <= total_time:
        for particle in particles:
            other_particles = [p for p in particles if p["id"] != particle["id"]]

            for other in other_particles:
                force = compute_strong_force(particle["position"], other["position"])
                insert_strong_force_data(current_time, particle["id"], particle["position"], force)

        # Zeit inkrementieren
        current_time += dt
        time.sleep(0.1)  # Simulationsgeschwindigkeit steuern

    logging.info("Simulation der starken Wechselwirkung abgeschlossen.")

if __name__ == "__main__":
    run_strong_force_simulation()
