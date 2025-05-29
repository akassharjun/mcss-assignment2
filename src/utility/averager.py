import pandas as pd
import ast
import numpy as np
import matplotlib.pyplot as plt

def calculate_and_display_averages(df: pd.DataFrame, num_turtles: int = 250):
    """
    Calculates and displays average Gini, wealth class percentages,
    and plots an average Lorenz curve from simulation data.

    Args:
        df (pd.DataFrame): DataFrame containing the simulation results.
                           Expected columns: 'gini_index', 'poor', 'middle_class',
                                             'rich', 'lorenz_list'.
        num_turtles (int): The total number of turtles in each simulation run.
    """
    if df.empty:
        print("DataFrame is empty. Cannot calculate averages.")
        return

    # --- 1. Average Gini Index ---
    avg_gini = df['gini_index'].mean()
    std_gini = df['gini_index'].std()
    print(f"Average Gini Index: {avg_gini:.4f} (Std Dev: {std_gini:.4f})")
    print("-" * 30)

    # --- 2. Average Wealth Class Percentages ---
    df['percent_poor'] = (df['poor'] / num_turtles) * 100
    df['percent_middle_class'] = (df['middle_class'] / num_turtles) * 100
    df['percent_rich'] = (df['rich'] / num_turtles) * 100

    avg_percent_poor = df['percent_poor'].mean()
    avg_percent_middle = df['percent_middle_class'].mean()
    avg_percent_rich = df['percent_rich'].mean()

    print("Average Wealth Class Percentages:")
    print(f"  Poor:         {avg_percent_poor:.2f}%")
    print(f"  Middle Class: {avg_percent_middle:.2f}%")
    print(f"  Rich:         {avg_percent_rich:.2f}%")
    print("-" * 30)

    # --- 3. Average Lorenz Curve ---
    all_lorenz_y_values_at_x = {} # Dict to store Ys for each X: {x_val: [y1, y2, ...]}
    lorenz_x_coords = None # To store the common X coordinates

    for index, row in df.iterrows():
        try:
            # Safely evaluate the string representation of the list of tuples
            lorenz_data_for_run = ast.literal_eval(row['lorenz_list'])
            if not lorenz_x_coords: # Get X coordinates from the first valid run
                lorenz_x_coords = [point[0] for point in lorenz_data_for_run]

            # Ensure all lorenz curves have the same x-coordinates and length for simple averaging
            current_x_coords = [point[0] for point in lorenz_data_for_run]
            if lorenz_x_coords and current_x_coords == lorenz_x_coords:
                for x_val, y_val in lorenz_data_for_run:
                    if x_val not in all_lorenz_y_values_at_x:
                        all_lorenz_y_values_at_x[x_val] = []
                    all_lorenz_y_values_at_x[x_val].append(y_val)
            else:
                print(f"Warning: Lorenz curve X-coordinates mismatch or not set for run_id {row.get('run_id', index)}. Skipping this run for Lorenz averaging.")
                continue

        except (ValueError, SyntaxError) as e:
            print(f"Error parsing lorenz_list for run_id {row.get('run_id', index)}: {e}. Skipping.")
            continue
        except TypeError as e:
            print(f"TypeError (likely non-string lorenz_list) for run_id {row.get('run_id', index)}: {e}. Skipping.")
            continue


    if lorenz_x_coords and all_lorenz_y_values_at_x:
        average_lorenz_y = []
        lorenz_y_std_dev = [] # For optional error bands

        sorted_x_coords = sorted(all_lorenz_y_values_at_x.keys())

        for x_val in sorted_x_coords:
            y_values_for_x = all_lorenz_y_values_at_x[x_val]
            if y_values_for_x:
                average_lorenz_y.append(np.mean(y_values_for_x))
                lorenz_y_std_dev.append(np.std(y_values_for_x))

        # Filter out None if any issues occurred
        valid_indices = [i for i, y in enumerate(average_lorenz_y) if y is not None]
        plot_x = [sorted_x_coords[i] for i in valid_indices]
        plot_y_avg = [average_lorenz_y[i] for i in valid_indices]
        plot_y_std = [lorenz_y_std_dev[i] for i in valid_indices]


        if plot_x and plot_y_avg:
            plt.figure(figsize=(8, 6))
            plt.plot(plot_x, plot_y_avg, label='Average Lorenz Curve', color='blue', marker='.')

            # Line of perfect equality
            plt.plot([0, 100], [0, 100], label='Line of Perfect Equality', color='red', linestyle='--')

            plt.title('Average Lorenz Curve')
            plt.xlabel('Cumulative Percentage of Population')
            plt.ylabel('Cumulative Percentage of Wealth')
            plt.xlim(0, 100)
            plt.ylim(0, 100)
            plt.legend()
            plt.grid(True)
            plt.show()
            print("Average Lorenz Curve plotted.")



df_results = pd.read_csv('default_world_results.csv')

calculate_and_display_averages(df_results)

