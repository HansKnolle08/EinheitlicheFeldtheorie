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
    level=logging.DEBUG,  # Setzt das Log-Level auf DEBUG, um alle Log-Nachrichten zu erfassen
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),  # Loggen in eine Datei
        logging.StreamHandler()  # Loggen im Terminal
    ]
)

# Konstanten
G = 6.67430e-11  # Gravitationskonstante in m^3 kg^-1 s^-2
M1 = 5.972e24  # Masse der Erde in kg
M2 = 7.348e22  # Masse des Mondes in kg
R0 = 384400000  # Anfangsabstand zwischen Erde und Mond in m

# Anfangswerte für die Simulation
position_earth = (0, 0, 0)  # Erde im Ursprung
position_moon = (R0, 0, 0)  # Mond am Anfang entlang der X-Achse
velocity_earth = (0, 0, 0)  # Erde ist unbewegt
velocity_moon = (0, 1022, 0)  # Mond bewegt sich mit einer Geschwindigkeit von 1022 m/s

def init_simulation_state():
    """
    Erstellt die Tabelle für den letzten gespeicherten Zeitpunkt, falls noch nicht vorhanden.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabelle für den letzten gespeicherten Zeitpunkt
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulation_state (
        id INTEGER PRIMARY KEY,
        last_time INTEGER NOT NULL
    )
    """)

    # Falls noch kein Zeitpunkt gespeichert ist, setzen wir den Startwert auf 0
    cursor.execute("""
    INSERT OR IGNORE INTO simulation_state (id, last_time) VALUES (1, 0)
    """)

    conn.commit()
    conn.close()

def get_last_simulation_time():
    """
    Lädt den letzten gespeicherten Zeitpunkt aus der Datenbank.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT last_time FROM simulation_state WHERE id = 1")
    last_time = cursor.fetchone()

    if last_time:
        return last_time[0]
    else:
        return 0  # Falls noch kein Zeitpunkt gespeichert wurde, starten wir bei 0

def update_simulation_time(current_time):
    """
    Aktualisiert den gespeicherten Zeitpunkt in der Datenbank.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("UPDATE simulation_state SET last_time = ? WHERE id = 1", (current_time,))
    conn.commit()
    conn.close()

def compute_gravitational_force(mass1, mass2, distance):
    """
    Berechnet die Gravitationskraft zwischen zwei Massen.
    """
    force = G * mass1 * mass2 / distance ** 2
    logging.debug(f'Berechnete Gravitationskraft: {force:.2e} N')
    return force

def update_positions_and_velocities(position1, velocity1, position2, velocity2, force, mass1, mass2, dt):
    """
    Aktualisiert die Positionen und Geschwindigkeiten der beiden Objekte.
    """
    # Berechne die Richtung der Kraft
    dx = position2[0] - position1[0]
    dy = position2[1] - position1[1]
    dz = position2[2] - position1[2]
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    
    # Berechne die Beschleunigung durch die Gravitationskraft
    ax1 = force * dx / (mass1 * distance)
    ay1 = force * dy / (mass1 * distance)
    az1 = force * dz / (mass1 * distance)

    ax2 = -force * dx / (mass2 * distance)
    ay2 = -force * dy / (mass2 * distance)
    az2 = -force * dz / (mass2 * distance)

    # Aktualisiere Position und Geschwindigkeit
    new_velocity1 = (velocity1[0] + ax1 * dt, velocity1[1] + ay1 * dt, velocity1[2] + az1 * dt)
    new_velocity2 = (velocity2[0] + ax2 * dt, velocity2[1] + ay2 * dt, velocity2[2] + az2 * dt)

    new_position1 = (position1[0] + new_velocity1[0] * dt, position1[1] + new_velocity1[1] * dt, position1[2] + new_velocity1[2] * dt)
    new_position2 = (position2[0] + new_velocity2[0] * dt, position2[1] + new_velocity2[1] * dt, position2[2] + new_velocity2[2] * dt)

    logging.debug(f'Aktualisierte Positionen: Erde: {new_position1}, Mond: {new_position2}')
    logging.debug(f'Aktualisierte Geschwindigkeiten: Erde: {new_velocity1}, Mond: {new_velocity2}')
    
    return new_position1, new_velocity1, new_position2, new_velocity2

def insert_gravity_data(time, position_earth, position_moon, velocity_earth, velocity_moon):
    """
    Speichert die aktuellen Daten in der Datenbank.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(""" 
    INSERT INTO gravity_data (time, position_x, position_y, position_z, velocity_x, velocity_y, velocity_z)
    VALUES (?, ?, ?, ?, ?, ?, ?) 
    """, (
        time,
        position_earth[0], position_earth[1], position_earth[2],
        velocity_earth[0], velocity_earth[1], velocity_earth[2]
    ))

    cursor.execute(""" 
    INSERT INTO gravity_data (time, position_x, position_y, position_z, velocity_x, velocity_y, velocity_z)
    VALUES (?, ?, ?, ?, ?, ?, ?) 
    """, (
        time,
        position_moon[0], position_moon[1], position_moon[2],
        velocity_moon[0], velocity_moon[1], velocity_moon[2]
    ))

    conn.commit()
    conn.close()
    logging.info(f'Daten für Zeit {time} gespeichert.')

def run_grav_simulation():
    """
    Führt die Simulation durch und speichert die Ergebnisse.
    """
    global position_earth, velocity_earth, position_moon, velocity_moon

    # Simulationszeitraum und Schrittweite
    total_time = 3600 * 24  # Simuliere für 24 Stunden (1 Tag)
    dt = 60  # Zeitschritt in Sekunden

    logging.info(f'Simulation startet. Gesamtdauer: {total_time / 3600} Stunden, Zeitschritt: {dt} Sekunden.')

    # Hole den letzten gespeicherten Zeitpunkt
    current_time = get_last_simulation_time()
    logging.info(f'Simulation fortgesetzt bei Zeit {current_time}s.')

    # Simulation starten
    while current_time <= total_time:
        # Berechne die Gravitationskraft
        distance = math.sqrt((position_moon[0] - position_earth[0]) ** 2 + (position_moon[1] - position_earth[1]) ** 2 + (position_moon[2] - position_earth[2]) ** 2)
        force = compute_gravitational_force(M1, M2, distance)

        # Update Positionen und Geschwindigkeiten
        position_earth, velocity_earth, position_moon, velocity_moon = update_positions_and_velocities(position_earth, velocity_earth, position_moon, velocity_moon, force, M1, M2, dt)

        # Daten in die Datenbank speichern
        insert_gravity_data(current_time, position_earth, position_moon, velocity_earth, velocity_moon)

        # Zeit inkrementieren
        current_time += dt
        update_simulation_time(current_time)  # Speichere den aktuellen Zeitpunkt in der DB

        time.sleep(0.1)  # Pause für 0.1 Sekunden (Simulationsgeschwindigkeit steuern)

    logging.info("Gravitationssimulation abgeschlossen.")

if __name__ == "__main__":
    init_simulation_state()  # Nur beim ersten Start oder nach Zurücksetzen der Datenbank ausführen
    run_grav_simulation()
