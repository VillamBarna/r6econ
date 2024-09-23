import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

# Function to analyze and split sold values into high and low groups using k-means clustering
def analyze_sold_values(sold_values, raw):
    high_threshold=3
    low_threshold = 1.5
    if len(sold_values) < 2:
        return None, None, [], [], None, None, 0, 0
    
    # Reshape the data for GMM
    sold_values_reshaped = np.array(sold_values).reshape(-1, 1)
    
    while True: 
        # Apply GMM with more robust settings
        gmm = GaussianMixture(n_components=2, covariance_type='full', reg_covar=1e-5, random_state=0)
        labels = gmm.fit_predict(sold_values_reshaped)
        
        # Identify the two clusters
        unique_labels = set(labels)
        
        if len(unique_labels) != 2:
            print("Could not find two distinct clusters. Adjust the parameters or check the data.")
            return None, None, [], [], None, None, 0, 0
        
        # Separate data into low and high clusters based on cluster means
        clusters = [sold_values_reshaped[labels == label] for label in unique_labels]
        cluster_means = [np.mean(cluster) for cluster in clusters]
        
        low_cluster = clusters[np.argmin(cluster_means)]
        high_cluster = clusters[np.argmax(cluster_means)]
        
        low_group_y = low_cluster.flatten()
        high_group_y = high_cluster.flatten()
        
        low_group_x = [i for i, v in enumerate(sold_values) if v in low_group_y]
        high_group_x = [i for i, v in enumerate(sold_values) if v in high_group_y]

        low_avg = np.mean(low_group_y) if low_group_y.size > 0 else None
        high_avg = np.mean(high_group_y) if high_group_y.size > 0 else None
        
        avg_difference = (high_avg - low_avg) if low_avg is not None and high_avg is not None else None
        profit = (high_avg * 0.9 - low_avg) if low_avg is not None and high_avg is not None else None
        
        high_percent = len(high_group_y) * 100 / (len(high_group_y) + len(low_group_y))
        low_percent = len(low_group_y) * 100 / (len(high_group_y) + len(low_group_y))

        if raw:
            return low_avg, high_avg, low_group_x, high_group_x, avg_difference, profit, len(low_group_y), len(high_group_y), len(sold_values)

        if high_percent < high_threshold:
            # Update sold_values_reshaped to exclude high group data
            sold_values_reshaped = low_group_y.reshape(-1, 1)
        elif low_percent < low_threshold:
            # Update sold_values_reshaped to exclude low group data
            sold_values_reshaped = high_group_y.reshape(-1, 1)
        else:
            break
    
    '''
     # Only for testing the number of removed data points:
    if len(sold_values) != len(low_group_y) + len(high_group_y):
        print(f'stargting data number{len(sold_values)}, ending data number {len(low_group_y) + len(high_group_y)}')
    '''
    
    return low_avg, high_avg, low_group_x, high_group_x, avg_difference, profit, len(low_group_y), len(high_group_y), len(sold_values)



def plot_weapon_sales(sold_values, current_timestamp, asv, item_id, item_name):
    low_avg, high_avg, low_group_x, high_group_x, avg_difference, profit, low_group_size, high_group_size, original_size = asv
    
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
    plt.title(f"Item name: {item_name}")
    plt.legend()
    plt.grid(True)
    plt.savefig( f"graphs/{item_id}.png" )
    plt.clf()
