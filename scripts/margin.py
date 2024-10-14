import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from scipy.stats import zscore

def analyze_sold_values(sold_values, raw, fluctuation_threshold=0.2, window_size=50):
    if len(sold_values) < 2:
        return None

    # Convert to numpy array for easy calculation
    sold_values_np = np.array(sold_values)

    if raw:
        # Calculate the 10th and 90th percentiles for raw data
        low_percentile_value = np.percentile(sold_values_np, 10)
        high_percentile_value = np.percentile(sold_values_np, 90)

        # Below 10th percentile
        low_group_x = [i for i, v in enumerate(sold_values_np) if v <= low_percentile_value]
        
        # Between 10th and 90th percentile (neutral group)
        net_group_x = [i for i, v in enumerate(sold_values_np) if low_percentile_value < v < high_percentile_value]
        
        # Above 90th percentile
        high_group_x = [i for i, v in enumerate(sold_values_np) if v >= high_percentile_value]

        return low_group_x, net_group_x, high_group_x

    else:
        # Calculate Z-scores to filter out outliers
        z_scores = zscore(sold_values_np)
    
        # Set threshold for identifying outliers (±2 standard deviation commonly used)
        threshold_z = 2
    
        # Remove outliers by keeping values within the threshold
        filtered_values = sold_values_np[(z_scores > -threshold_z) & (z_scores < threshold_z)]

        if len(filtered_values) == 0:
            return None  # Return None if all values are outliers

        # Step 1: Start from the last window and calculate initial percentiles
        start_index = len(filtered_values) - window_size
        current_window = filtered_values[start_index:]
        low_percentile_value = np.percentile(current_window, 10)
        high_percentile_value = np.percentile(current_window, 90)

        last_stable_index = start_index  # Initialize with the last window index

        # Step 2: Move backward through the data
        for i in range(start_index - 1, -1, -1):
            # Create a new window by adding the current index
            current_window = filtered_values[i:i + window_size]

            # Calculate new percentiles for the updated window
            new_low_percentile_value = np.percentile(current_window, 10)
            new_high_percentile_value = np.percentile(current_window, 90)

            # Check if the new percentiles are consistent with the previous percentiles
            if (abs(new_low_percentile_value - low_percentile_value) <= fluctuation_threshold * low_percentile_value) and \
               (abs(new_high_percentile_value - high_percentile_value) <= fluctuation_threshold * high_percentile_value):
                last_stable_index = i  # Update the last stable index
                low_percentile_value = new_low_percentile_value  # Update the low percentile
                high_percentile_value = new_high_percentile_value  # Update the high percentile
            else:
                break  # Stop if not consistent

        # Step 3: Extract the stable window
        stable_window = filtered_values[last_stable_index:]

        # Step 4: Recalculate percentiles on the stable window
        low_percentile_value = np.percentile(stable_window, 10)
        high_percentile_value = np.percentile(stable_window, 90)

        # Identify groups based on stable values
        low_group_x = [i for i in range(last_stable_index, len(filtered_values)) if filtered_values[i] <= low_percentile_value]
        net_group_x = [i for i in range(last_stable_index, len(filtered_values)) if low_percentile_value < filtered_values[i] < high_percentile_value]
        high_group_x = [i for i in range(last_stable_index, len(filtered_values)) if filtered_values[i] >= high_percentile_value]

        return low_group_x, net_group_x, high_group_x, low_percentile_value, high_percentile_value




def plot_weapon_sales(sold_values, current_timestamp, asv, item_id, item_name):
    low_group_x, net_group_x, high_group_x, low_percentile, high_percentile = asv
    
    # Plot the low group points
    low_group_x_time = [current_timestamp[i] for i in low_group_x]
    plt.scatter(low_group_x_time, [sold_values[i] for i in low_group_x], color='r')

    # Plot the neutral group points
    net_group_x_time = [current_timestamp[i] for i in net_group_x]
    plt.scatter(net_group_x_time, [sold_values[i] for i in net_group_x], color='gray')

    # Plot the high group points
    high_group_x_time = [current_timestamp[i] for i in high_group_x]
    plt.scatter(high_group_x_time, [sold_values[i] for i in high_group_x], color='g')
    
    # Plot the low and high average lines
    if low_percentile is not None:
        plt.axhline(y=low_percentile, color='r', linestyle='--', label=f'Low: {low_percentile:.2f}')
    
    if high_percentile is not None:
        plt.axhline(y=high_percentile, color='g', linestyle='--', label=f'High: {high_percentile:.2f}')
    
    plt.xlabel('Time ago [hours]')
    plt.ylabel('Sold Value')
    plt.title(f"Item name: {item_name}")
    plt.legend()
    plt.grid(True)
    plt.savefig( f"graphs/{item_id}.png" )
    plt.clf()
