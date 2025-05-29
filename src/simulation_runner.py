#!/usr/bin/env python3
"""
Simulation Runner - Command-line interface for running batch simulations
Usage:
    python src/simulation_runner.py --scenario default --ticks 500 --runs 10
    python src/simulation_runner.py --scenario inheritance --ticks 500 --runs 10
    python src/simulation_runner.py --scenario uniform --ticks 500 --runs 10
"""

import argparse
import os
from utility.runner import run_batch_simulations


def get_scenario_params(scenario):
    """Get parameters for different simulation scenarios."""
    base_params = {
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
    }
    
    if scenario == 'default':
        base_params.update({
            'inheritance_flag': False,
            'uniform_wealth_flag': False
        })
    elif scenario == 'inheritance':
        base_params.update({
            'inheritance_flag': True,
            'uniform_wealth_flag': False
        })
    elif scenario == 'uniform':
        base_params.update({
            'inheritance_flag': False,
            'uniform_wealth_flag': True
        })
    else:
        raise ValueError(f"Unknown scenario: {scenario}")
    
    return base_params


def main():
    parser = argparse.ArgumentParser(description='Run wealth distribution simulation')
    parser.add_argument('--scenario', 
                       choices=['default', 'inheritance', 'uniform'],
                       required=True,
                       help='Simulation scenario to run')
    parser.add_argument('--ticks', 
                       type=int, 
                       default=1000,
                       help='Number of simulation ticks (default: 1000)')
    parser.add_argument('--runs', 
                       type=int, 
                       default=100,
                       help='Number of simulation runs (default: 100)')
    
    args = parser.parse_args()
    
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Get scenario parameters
    params = get_scenario_params(args.scenario)
    
    # Set output filename
    output_csv = f"results/{args.scenario}_results.csv"
    
    print(f"Running {args.scenario} scenario:")
    print(f"  • {args.runs} simulation runs")
    print(f"  • {args.ticks} ticks per run")
    print(f"  • Output: {output_csv}")
    print()
    
    # Run the simulation
    run_batch_simulations(
        output_csv=output_csv,
        num_runs=args.runs,
        num_ticks=args.ticks,
        world_kwargs=params
    )


if __name__ == "__main__":
    main() 