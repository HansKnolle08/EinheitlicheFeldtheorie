from multiprocessing import Process
from models.simulations.electromagnetic_simulation import run_elec_simulation
from models.simulations.gravity_simulation import init_simulation_state, run_grav_simulation


def run_gravity_simulation():
    init_simulation_state()
    run_grav_simulation()


if __name__ == '__main__':
    # Prozesse erstellen
    process1 = Process(target=run_elec_simulation)
    process2 = Process(target=run_gravity_simulation)

    # Prozesse starten
    process1.start()
    process2.start()

    # Warten, bis beide Prozesse fertig sind
    process1.join()
    process2.join()

    print("Beide Simulationen sind abgeschlossen!")
