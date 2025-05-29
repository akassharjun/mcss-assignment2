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

