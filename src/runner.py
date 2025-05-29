from visualization.interactive_visualizer import create_interactive_simulation
from models.world import World
import csv
import time
from multiprocessing import Pool, cpu_count, current_process  # Import current_process
import os

# Runs batch simulations and saves results in a CSV file
def _run_single_simulation_for_batch(args):
    """
    Worker function for multiprocessing. Runs a single simulation instance.
    'args' is a tuple: (run_id, num_ticks, world_kwargs_dict)
    """
    run_id, num_ticks, world_kwargs_dict = args
    process_name = current_process().name # Get the name of the current process
    pid = os.getpid()

    print(f"🚀 [{process_name} - PID:{pid}] Starting Run ID: {run_id}...") # Log start

    world = World(**world_kwargs_dict)
    final_result_from_tick = {}

    for tick_num in range(num_ticks):
        final_result_from_tick = world.tick(tick_num)

    final_result_from_tick['run_id'] = run_id
    
    print(f"🏁 [{process_name} - PID:{pid}] Finished Run ID: {run_id}.") # Log finish
    return final_result_from_tick

def run_batch_simulations(
    output_csv: str,
    num_runs: int,
    num_ticks: int,
    world_kwargs: dict
) -> None:
    """Run multiple simulations in parallel and save summary stats to a CSV file."""

    fieldnames = [
        'run_id', 'min_wealth', 'max_wealth', 'total_wealth', 'gini_index',
        'lorenz_list', 'poor', 'middle_class', 'rich'
    ]

    tasks = []
    for run_id_counter in range(1, num_runs + 1):
        tasks.append((run_id_counter, num_ticks, world_kwargs.copy()))

    num_processes = max(1, cpu_count() - 1)
    if num_runs < num_processes:
        num_processes = num_runs

    print(
        f"🚀 Starting {num_runs} parallel simulation runs over {num_ticks} ticks each, using {num_processes} processes...")

    all_run_results = []
    start_time = time.time()

    with Pool(processes=num_processes) as pool:
        # Use imap_unordered for potentially better progress reporting if desired,
        # as results come in as they are completed.
        # Or stick with map if strict order of results (before sorting) is important.
        # For this logging, map is fine.

        # If you want to see progress as tasks complete (more complex to manage logs nicely):
        # results_iterator = pool.imap_unordered(_run_single_simulation_for_batch, tasks)
        # completed_count = 0
        # for result_dict in results_iterator:
        #     all_run_results.append(result_dict)
        #     completed_count += 1
        #     print(f"📊 Progress: {completed_count}/{num_runs} runs completed.")
        # else: just use map
        all_run_results = pool.map(_run_single_simulation_for_batch, tasks)

    end_time = time.time()
    print(
        f"\n🎉 All parallel runs completed in {end_time - start_time:.2f} seconds.")

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        if all_run_results:
            for result_dict in sorted(all_run_results, key=lambda x: x['run_id']):
                writer.writerow(result_dict)

    print(f"✅ Results for {num_runs} simulations saved to: {output_csv}")


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
    print(
        f"• Life Expectancy: {world.min_life_expectancy}-{world.max_life_expectancy}")
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
