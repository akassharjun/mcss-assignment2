from src.models.world import World
from src.runner import run_simulation

def main():
    world = World(uniform_wealth_flag=True)
    run_simulation(world)

if __name__ == "__main__":
    main()