import sqlite3
import time
import math
import logging
import os

# Logging-Konfiguration
log_dir = 'src/logs'
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'electromagnetic_simulation.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Konstanten (Beispielwerte)
mu_0 = 4 * math.pi * 1e-7  # Magnetische Feldkonstante (H/m)
epsilon_0 = 8.854e-12  # Elektrische Feldkonstante (F/m)

# Beispiel-Parameter für elektromagnetische Felder
charge_q = 1e-6  # Beispielhafte Ladung in Coulomb
distance = 0.05  # Abstand in Metern
electric_field_strength = 1000  # Beispiel für die elektrische Feldstärke in N/C

# Anfangswerte (Position, Geschwindigkeit etc.)
position_charge = (0, 0, 0)  # Position der Ladung im Ursprung
velocity_charge = (0, 0, 0)  # Geschwindigkeit der Ladung

def compute_electric_field(charge, distance):
    """
    Berechnet das elektrische Feld einer Punktladung.
    """
    E = (1 / (4 * math.pi * epsilon_0)) * (charge / distance**2)
    logging.debug(f'Berechnetes elektrisches Feld: {E:.2e} N/C')
    return E

def compute_magnetic_field(current, distance):
    """
    Berechnet das Magnetfeld um einen Draht mit Strom.
    """
    B = (mu_0 / (2 * math.pi)) * (current / distance)
    logging.debug(f'Berechnetes Magnetfeld: {B:.2e} T')
    return B

def insert_electromagnetic_data(time, electric_field, magnetic_field):
    """
    Speichert die elektromagnetischen Felder in der Datenbank.
    """
    conn = sqlite3.connect('src/database/simulation_data.db')
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO electromagnetic_data (time, electric_field, magnetic_field)
    VALUES (?, ?, ?)
    """, (time, electric_field, magnetic_field))

    conn.commit()
    conn.close()
    logging.info(f'Daten für Zeit {time} gespeichert.')

def run_elec_simulation():
    """
    Führt die elektromagnetische Simulation durch und speichert die Ergebnisse.
    """
    total_time = 3600 * 24  # Simulation für 24 Stunden
    dt = 60  # Zeitschritt in Sekunden

    logging.info(f'Simulation startet. Gesamtdauer: {total_time / 3600} Stunden, Zeitschritt: {dt} Sekunden.')

    current_time = 0
    while current_time <= total_time:
        # Berechne das elektrische Feld
        electric_field = compute_electric_field(charge_q, distance)

        # Berechne das Magnetfeld
        current = 1  # Beispielhafter Stromwert (1 Ampere)
        magnetic_field = compute_magnetic_field(current, distance)

        # Speichere die Ergebnisse in der Datenbank
        insert_electromagnetic_data(current_time, electric_field, magnetic_field)

        # Zeit inkrementieren
        current_time += dt
        time.sleep(0.1)  # Simulationsgeschwindigkeit steuern

    logging.info("Elektromagnetische Simulation abgeschlossen.")

if __name__ == "__main__":
    run_elec_simulation()
