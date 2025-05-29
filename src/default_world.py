from runner import run_batch_simulations


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
        'inheritance_flag': False,
        'uniform_wealth_flag': False
    }

    run_batch_simulations(
        output_csv="default_world_results.csv",
        num_runs=10000,
        num_ticks=1000,
        world_kwargs=params
    )

if __name__ == "__main__":
    main()
