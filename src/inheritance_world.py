from models.world import World
from runner import run_simulation_gui, run_batch_simulations

def main():
    
    params = {
    'width': 51,
    'height': 51,
    'num_turtles': 250,
    'percent_best_land': 10.0,
    'max_vision': 5,
    'max_metabolism': 15,
    'min_life_expectancy': 1,
    'max_life_expectancy': 83,
    'uniform_wealth': 50,
    'max_grain': 50,
    'grain_growth_interval': 1,
    'num_grain_grown': 4,
    'inheritance_flag': True,
    'uniform_wealth_flag': False
    }
    
    run_batch_simulations(
    output_csv="inheritance_world_results.csv",
    num_runs=10,
    num_ticks=1000,
    world_kwargs=params
    )
    
    
    # world = World(inheritance_flag=True)
    # run_simulation_gui(world)

if __name__ == "__main__":
    main()