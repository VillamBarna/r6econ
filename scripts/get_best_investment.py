import json
import os
import margin
import time
import discord
from discord.ext import commands, tasks

with open(os.path.join(os.path.dirname(__file__), os.pardir, "assets/data.json"), "r") as file:
	data = json.load(file)

avg_profit = dict()
for weapon_id, weapon_info in data.items():
	weapon_name = weapon_info.get("name", "Unknown")
	first_tag = weapon_info.get("tags", ["Unknown"])[0]  # Get the first tag or "Unknown" if not present
	weapon_name += f' - {first_tag}'
	
	sold_values = weapon_info.get("sold", [])
	sold_values_list = [value[0] for value in sold_values if isinstance(value[0], (int, float))]  # Filter out non-numeric values
	
	if len(sold_values_list) > 30:
		low_avg, _, _, _, _, profit, low_size, high_size = margin.analyze_sold_values(sold_values_list)

		avg_profit[weapon_name] = (profit, low_avg, low_size, low_size*100/(low_size+high_size), weapon_id)

with open("avg_profit.json", "w") as file:
	json.dump(avg_profit, file)


def draw(invest_list):
	with open('assets/data.json', 'r') as file:
		data_margin = json.load(file)
	for id in len(invest_list):
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

		asv = margin.analyze_sold_values(sold_values_list)
		margin.plot_weapon_sales(sold_values_list, timestamp_list, asv, item_id, skin_name)
		file = discord.File(f'graphs/{item_id}.png')
		e = discord.Embed()
		e.set_image(url=f'attachment://{item_id}.png')