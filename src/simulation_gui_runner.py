#!/usr/bin/env python3
"""
Simulation GUI Runner - Command-line interface for running interactive simulations
Usage:
    python src/simulation_gui_runner.py --scenario=default
    python src/simulation_gui_runner.py --scenario=inheritance
    python src/simulation_gui_runner.py --scenario=uniform
"""

import argparse
from models.world import World
from visualization.interactive_visualizer import create_interactive_simulation


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


def print_welcome(scenario):
    """Print welcome message."""
    print("=" * 60)
    print("INTERACTIVE WEALTH DISTRIBUTION SIMULATION")
    print(f"Scenario: {scenario.upper()}")
    print("NetLogo-Style Interface with Start/Stop Controls")
    print("=" * 60)
    print()
    print("Features:")
    print("• Real-time visualization with four plots")
    print("• START/STOP button control")
    print("• Speed control slider")
    print("• RESET button to restart simulation")
    print("• Interactive NetLogo-style interface")
    print()


def run_simulation_gui(world: World, scenario: str):
    """Run function - creates interactive simulation interface."""

    print_welcome(scenario)

    # Display world parameters
    print("World Parameters:")
    print(f"• Size: {world.width} × {world.height}")
    print(f"• Population: {world.num_turtles} turtles")
    print(f"• Best Land: {world.percent_best_land * 100:.1f}%")
    print(f"• Vision: 1-{world.max_vision}")
    print(f"• Metabolism: 1-{world.max_metabolism}")
    print(f"• Life Expectancy: {world.min_life_expectancy}-{world.max_life_expectancy}")
    print(f"• Inheritance: {'Enabled' if world.inheritance_flag else 'Disabled'}")
    print(f"• Uniform Wealth: {'Enabled' if world.uniform_wealth_flag else 'Disabled'}")
    print()

    # Create interactive interface
    print("Creating interactive interface...")
    print("The simulation window will open with START/STOP controls.")
    print("Click START to begin the simulation!")
    print()

    try:
        # Create and show interactive visualizer
        visualizer = create_interactive_simulation(world)

        print("Interface created successfully!")
        print("Controls:")
        print("• START/STOP: Begin/pause simulation")
        print("• SETUP: Restart from beginning")
        print("• Speed slider: Control simulation speed")
        print("• Close window to exit")
        print()
        print("Opening simulation window... (this may take a moment)")

        # Show the interface (this will block until window is closed)
        visualizer.show()

    except Exception as e:
        print(f"Error creating interface: {e}")
        print("Try running with --help flag for usage information")
        import traceback
        traceback.print_exc()

    finally:
        print("Simulation ended.")


def main():
    parser = argparse.ArgumentParser(description='Run interactive wealth distribution simulation')
    parser.add_argument('--scenario', 
                       choices=['default', 'inheritance', 'uniform'],
                       required=True,
                       help='Simulation scenario to run')
    
    args = parser.parse_args()
    
    print(f"Starting {args.scenario} scenario with interactive GUI...")
    print()
    
    # Get scenario parameters
    params = get_scenario_params(args.scenario)
    
    # Create world
    world = World(**params)
    
    # Run GUI
    run_simulation_gui(world, args.scenario)


if __name__ == "__main__":
    main() 