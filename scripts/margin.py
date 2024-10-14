import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Function to analyze and split sold values into high and low groups using k-means clustering
def analyze_sold_values(sold_values, raw):
    if len(sold_values) < 2:
        return None

    # Convert to numpy array for easy calculation
    sold_values_np = np.array(sold_values)

    if raw:
        # Calculate the 10th and 90th percentiles
        low_percentile_value = np.percentile(sold_values_np, 10)
        high_percentile_value = np.percentile(sold_values_np, 90)
        
        # Below 10th percentile
        low_group_x = [i for i, v in enumerate(sold_values_np) if v < low_percentile_value]
        
        # Between 10th and 90th percentile (neutral group)
        net_group_x = [i for i, v in enumerate(sold_values_np) if low_percentile_value <= v <= high_percentile_value]
        
        # Above 90th percentile
        high_group_x = [i for i, v in enumerate(sold_values_np) if v > high_percentile_value]

        return low_group_x, net_group_x, high_group_x
    
    # Calculate Z-scores
    z_scores = zscore(sold_values_np)
    
    # Set threshold for identifying outliers (common threshold is ±2)
    threshold = 2
    
    # Remove outliers (keep values within threshold)
    filtered_values = sold_values_np[(z_scores > -threshold) & (z_scores < threshold)]
    
    if len(filtered_values) == 0:
        return None  # Return None if all values are outliers

    # Calculate the 10th and 90th percentiles on the filtered data
    low_percentile_value = np.percentile(filtered_values, 10)
    high_percentile_value = np.percentile(filtered_values, 90)

    # Below 10th percentile
    low_group_x = [i for i, v in enumerate(sold_values_np) if v < low_percentile_value]
    
    # Between 10th and 90th percentile (neutral group)
    net_group_x = [i for i, v in enumerate(sold_values_np) if low_percentile_value <= v <= high_percentile_value]
    
    # Above 90th percentile
    high_group_x = [i for i, v in enumerate(sold_values_np) if v > high_percentile_value]

    return low_group_x, net_group_x, high_group_x, low_percentile_value, high_percentile_value




def plot_weapon_sales(sold_values, current_timestamp, asv, item_id, item_name):
    low_group_x, net_group_x, high_group_x, low_percentile, high_percentile = asv
    
    # Plot the low group points
    low_group_x_time = [current_timestamp[i] for i in low_group_x]
    plt.scatter(low_group_x_time, [sold_values[i] for i in low_group_x], color='r', label='Low Group')

    # Plot the neutral group points
    net_group_x_time = [current_timestamp[i] for i in net_group_x]
    plt.scatter(net_group_x_time, [sold_values[i] for i in net_group_x], color='k', label='Net Group')

    # Plot the high group points
    high_group_x_time = [current_timestamp[i] for i in high_group_x]
    plt.scatter(high_group_x_time, [sold_values[i] for i in high_group_x], color='g', label='High Group')
    
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
