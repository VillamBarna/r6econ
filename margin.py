import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Function to analyze and split sold values into high and low groups using k-means clustering
def analyze_sold_values(sold_values):
    if len(sold_values) < 2:
        return None, None, None, None, [], [], None, None, 0, 0  # Not enough data to calculate statistics

    # Reshape the data for k-means
    sold_values_reshaped = np.array(sold_values).reshape(-1, 1)
    
    # Apply k-means clustering
    kmeans = KMeans(n_clusters=2, random_state=0).fit(sold_values_reshaped)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_.flatten()
    
    # Separate data into low and high clusters based on cluster centers
    low_cluster = sold_values_reshaped[labels == np.argmin(centers)]
    high_cluster = sold_values_reshaped[labels == np.argmax(centers)]
    

    # Determine which data points are in high and low groups based on clusters
    low_group_x = [i for i, v in enumerate(sold_values) if v in low_cluster]
    low_group_y = [sold_values[i] for i in low_group_x]
    
    high_group_x = [i for i, v in enumerate(sold_values) if v in high_cluster]
    high_group_y = [sold_values[i] for i in high_group_x]
    
    # Calculate averages for low and high groups
    low_avg = np.mean(low_group_y) if low_group_y else None
    high_avg = np.mean(high_group_y) if high_group_y else None
    
    # Calculate the difference between low and high averages
    avg_difference = (high_avg - low_avg) if low_avg is not None and high_avg is not None else None
    
    # Calculate profit
    profit = (high_avg * 0.9 - low_avg) if low_avg is not None and high_avg is not None else None

    return low_avg, high_avg, None, None, low_group_x, high_group_x, avg_difference, profit, len(low_group_y), len(high_group_y)

def plot_weapon_sales(sold_values, current_timestamp, asv, item_id):
    low_avg, high_avg, _, _, low_group_x, high_group_x, avg_difference, profit, low_group_size, high_group_size = asv
    
    # Plot the low group points
    low_group_x_time = [current_timestamp[i] for i in low_group_x]
    plt.scatter(low_group_x_time, [sold_values[i] for i in low_group_x], color='r', label='Low Group')

    # Plot the high group points
    high_group_x_time = [current_timestamp[i] for i in high_group_x]
    plt.scatter(high_group_x_time, [sold_values[i] for i in high_group_x], color='g', label='High Group')
    
    # Plot the low and high average lines
    if low_avg is not None:
        plt.axhline(y=low_avg, color='r', linestyle='--', label=f'Low Avg: {low_avg:.2f}')
    
    if high_avg is not None:
        plt.axhline(y=high_avg, color='g', linestyle='--', label=f'High Avg: {high_avg:.2f}')
    
    plt.xlabel('Time ago [hours]')
    plt.ylabel('Sold Value')
    plt.title(f"Id: {item_id}")
    plt.legend()
    plt.grid(True)
    plt.savefig( f"graphs/{item_id}.png" )
    plt.clf()
