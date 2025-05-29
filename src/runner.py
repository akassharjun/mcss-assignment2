from models.world import World
from visualization.interactive_visualizer import create_interactive_simulation
import csv

# Runs batch simulations and saves results in a CSV file
def run_batch_simulations(
    output_csv: str,
    num_runs: int,
    num_ticks: int,
    world_kwargs: dict
) -> None:
    """
    Run multiple simulations and save summary stats to a CSV file.

    Args:
        output_csv (str): Path to output CSV file.
        num_runs (int): Number of simulation runs.
        num_ticks (int): Number of ticks per run.
        world_kwargs (dict): Parameters to initialize each World.
    """
    fieldnames = [
        'run_id',
        'min_wealth',
        'max_wealth',
        'total_wealth',
        'gini_index',
        'lorenz_list',
        'wealth_classes'
    ]

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for run_id in range(1, num_runs + 1):
            world = World(**world_kwargs)

            for tick in range(num_ticks):
                result = world.tick(tick)


            writer.writerow(result)

    print(f"✅ Completed {num_runs} simulations. Results saved to: {output_csv}")


def print_welcome():
    """Print welcome message."""
    print("=" * 60)
    print("INTERACTIVE WEALTH DISTRIBUTION SIMULATION")
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


def run_simulation_gui(world: World):
    """Run function - creates interactive simulation interface."""

    print_welcome()

    # Display world parameters
    print("World Parameters:")
    print(f"• Size: {world.width} × {world.height}")
    print(f"• Population: {world.num_turtles} turtles")
    print(f"• Best Land: {world.percent_best_land * 100:.1f}%")
    print(f"• Vision: 1-{world.max_vision}")
    print(f"• Metabolism: 1-{world.max_metabolism}")
    print(f"• Life Expectancy: {world.min_life_expectancy}-{world.max_life_expectancy}")
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
