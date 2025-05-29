from models.world import World
from runner import run_simulation_gui, run_batch_simulations

def main():
    world = World(inheritance_flag=True)
    run_simulation_gui(world)

if __name__ == "__main__":
    main()