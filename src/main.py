# src/main.py

###########
# IMPORTS #
###########
from multiprocessing import Process
from scripts.simulations.electromagnetic_simulation import run_elec_simulation
from scripts.simulations.gravity_simulation import init_simulation_state, run_grav_simulation
from scripts.simulations.strong_force_simulation import run_strong_force_simulation
from scripts.funcs.timestamp_dec import *

#############
# FUNCTIONS #
#############
def run_gravity_simulation():
    init_simulation_state()
    run_grav_simulation()

#################
# MAIN FUNCTION #
#################
@timestamp_dec
def main():
    # Prozesse erstellen
    process1 = Process(target=run_elec_simulation)
    process2 = Process(target=run_gravity_simulation)
    process3 = Process(target=run_strong_force_simulation)

    # Prozesse starten
    process1.start()
    process2.start()
    process3.start()

    # Warten, bis beide Prozesse fertig sind
    process1.join()
    process2.join()
    process3.join()

    print("Simulationen sind abgeschlossen!")

###############
# ENTRY POINT #
###############
if __name__ == '__main__':
    main()
