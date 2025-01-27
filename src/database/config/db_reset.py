import sqlite3

def reset_database():
    """
    Setzt die gesamte Datenbank zurück, indem alle Tabellen gelöscht und neu erstellt werden.
    """
    conn = sqlite3.connect('src/database/simulation_data.db')
    cursor = conn.cursor()

    # Lösche alle Tabellen, falls sie existieren
    cursor.execute("DROP TABLE IF EXISTS gravity_data")
    cursor.execute("DROP TABLE IF EXISTS electromagnetic_data")
    cursor.execute("DROP TABLE IF EXISTS strong_force_data")
    cursor.execute("DROP TABLE IF EXISTS weak_force_data")
    cursor.execute("DROP TABLE IF EXISTS simulation_results")
    cursor.execute("DROP TABLE IF EXISTS simulation_state")

    # Erstelle die Tabellen erneut
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gravity_data (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        time REAL,
        position_x REAL,
        position_y REAL,
        position_z REAL,
        velocity_x REAL,
        velocity_y REAL,
        velocity_z REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS electromagnetic_data (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        time REAL,
        electric_field REAL,
        magnetic_field REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS strong_force_data (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        time REAL,
        particle_id INTEGER,
        position_x REAL,
        position_y REAL,
        position_z REAL,
        force REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weak_force_data (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        time REAL,
        particle_id INTEGER,
        decay_rate REAL,
        position_x REAL,
        position_y REAL,
        position_z REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        calculated_force REAL,
        unified_theory REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulation_state (
        id INTEGER PRIMARY KEY,
        last_time INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("Database reset complete.")

if __name__ == "__main__":
    reset_database()
