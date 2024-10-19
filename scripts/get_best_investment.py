import json
import os
import scripts.margin as margin
import time
import discord
from discord.ext import commands, tasks
import numpy as np
from scipy.stats import zscore

def draw(invest_list):
	with open('assets/data.json', 'r') as file:
		data_margin = json.load(file)
	file = []
	for id in range(len(invest_list)):
		item_id = invest_list[id]
		weapon_info = data_margin[item_id]
		sold_values = weapon_info.get("sold", [])
		skin_name = f"{weapon_info.get('name', [])} {weapon_info.get('tags', [None])[0]}"
		sold_values_list = [value[0] for value in sold_values if isinstance(value[0], (int, float))]  # Filter out non-numeric values
		timestamp_list = [value[1] for value in sold_values if isinstance(value[0], (int, float))]
		current_time = time.time()
		for i in range(len(timestamp_list)):
			tmp = timestamp_list[i]
			timestamp_list[i]= -(current_time - tmp) / 3600

		asv = margin.analyze_sold_values(sold_values_list, False)
		margin.plot_weapon_sales(sold_values_list, timestamp_list, asv, item_id, skin_name)
		file.append(discord.File(f'graphs/{item_id}.png'))
	return file


def filtered_profit(sold_values):
	if len(sold_values) < 2:
		return None
	
	# Convert to numpy array for easy calculation
	sold_values_np = np.array(sold_values)
    
    # Calculate Z-scores
	z_scores = zscore(sold_values_np)
    
    # Set threshold for identifying outliers (common threshold is ±3)
	threshold = 2
    
    # Remove outliers (keep values within threshold)
	filtered_values = sold_values_np[(z_scores > -threshold) & (z_scores < threshold)]
    
	if len(filtered_values) == 0:
		return None, None  # Return None if all values are outliers
    
    # Calculate the 10th and 90th percentiles on the filtered data
	low_percentile_value = np.percentile(filtered_values, 10)
	high_percentile_value = np.percentile(filtered_values, 90)
		
	return low_percentile_value, high_percentile_value