import json
import os
import margin
import time
import discord
from discord.ext import commands, tasks

def draw(invest_list):
	with open('assets/data.json', 'r') as file:
		data_margin = json.load(file)
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

		asv = margin.analyze_sold_values(sold_values_list)
		margin.plot_weapon_sales(sold_values_list, timestamp_list, asv, item_id, skin_name)
		file = discord.File(f'graphs/{item_id}.png')
		e = discord.Embed()
		e.set_image(url=f'attachment://{item_id}.png')
