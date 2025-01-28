import sqlite3
import time
import logging
import os
import math
import random

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

# Konstanten
STRONG_FORCE_CONSTANT = 1.0  # Starke Wechselwirkungskonstante (willkürlicher Wert für Simulation)
PARTICLE_COUNT = 5  # Anzahl der Teilchen in der Simulation
BOX_SIZE = 10.0  # Größe des Simulationsbereichs (willkürlicher Würfel in Einheiten)

def initialize_particles():
    """
    Initialisiert die Teilchen mit zufälligen Positionen und Massen.
    """
    particles = []
    for i in range(PARTICLE_COUNT):
        particle = {
            'id': i,
            'position': [random.uniform(0, BOX_SIZE) for _ in range(3)],
            'mass': random.uniform(1.0, 10.0)
        }
        particles.append(particle)
    return particles

def compute_strong_force(p1, p2):
    """
    Berechnet die starke Wechselwirkung zwischen zwei Teilchen.
    """
    distance = math.sqrt(sum((p1['position'][i] - p2['position'][i]) ** 2 for i in range(3)))
    if distance == 0:
        return 0  # Vermeidet Division durch Null
    force = STRONG_FORCE_CONSTANT * (p1['mass'] * p2['mass']) / (distance ** 2)
    return force

def update_particle_positions(particles, forces, dt):
    """
    Aktualisiert die Positionen der Teilchen basierend auf den Kräften.
    """
    for i, particle in enumerate(particles):
        acceleration = [forces[i][j] / particle['mass'] for j in range(3)]
        for j in range(3):
            particle['position'][j] += acceleration[j] * dt

def insert_strong_force_data(time_step, particles, forces):
    """
    Speichert die Daten der starken Wechselwirkung in der Datenbank.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for i, particle in enumerate(particles):
        force_magnitude = math.sqrt(sum(f ** 2 for f in forces[i]))
        cursor.execute("""
        INSERT INTO strong_force_data (time, particle_id, position_x, position_y, position_z, force)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            time_step,
            particle['id'],
            particle['position'][0],
            particle['position'][1],
            particle['position'][2],
            force_magnitude
        ))

    conn.commit()
    conn.close()
    logging.info(f'Daten für Zeitschritt {time_step} gespeichert.')

def run_strong_force_simulation():
    """
    Führt die Simulation der starken Wechselwirkung durch.
    """
    total_time = 3600 * 24  # Simulation für 24 Stunden
    dt = 60  # Zeitschritt in Sekunden

    logging.info(f'Simulation startet. Gesamtdauer: {total_time / 3600} Stunden, Zeitschritt: {dt} Sekunden.')

    particles = initialize_particles()
    current_time = 0

    while current_time <= total_time:
        # Berechne die Kräfte zwischen den Teilchen
        forces = [[0, 0, 0] for _ in particles]
        for i, p1 in enumerate(particles):
            for j, p2 in enumerate(particles):
                if i != j:
                    force_magnitude = compute_strong_force(p1, p2)
                    direction = [(p2['position'][k] - p1['position'][k]) for k in range(3)]
                    distance = math.sqrt(sum(d ** 2 for d in direction))
                    if distance > 0:
                        direction = [d / distance for d in direction]
                        forces[i] = [forces[i][k] + force_magnitude * direction[k] for k in range(3)]

        # Aktualisiere die Positionen der Teilchen
        update_particle_positions(particles, forces, dt)

        # Speichere die Ergebnisse in der Datenbank
        insert_strong_force_data(current_time, particles, forces)

        # Zeit inkrementieren
        current_time += dt
        time.sleep(0.1)  # Simulationsgeschwindigkeit steuern

    logging.info("Simulation der starken Wechselwirkung abgeschlossen.")

if __name__ == "__main__":
    run_strong_force_simulation()
