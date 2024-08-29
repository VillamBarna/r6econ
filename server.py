from __future__ import annotations

from datetime import datetime, timezone

import time
import json
import copy
import contextlib
import os
import discord
from discord.ext import commands, tasks
from os.path import exists
from auth import Auth
import scripts.margin as margin
from scripts.get_best_investment import draw

import matplotlib.pyplot as plt
import numpy as np

account_platform_blocklist = [
	'Coders Rank', 'Fiverr', 'HackerNews', 'Modelhub (NSFW)', 'metacritic', 'xHamster (NSFW)',
	'CNET', 'YandexMusic', 'HackerEarth', 'OpenStreetMap', 'Pinkbike', 'Slides', 'Strava'
]

intents = discord.Intents.default()
intents.message_content = True

if ( not exists("assets/data.json") ):
	with open('assets/data.json', 'w') as f:
		f.write("{}")

if ( not exists("assets/ids.json") ):
	with open('assets/ids.json', 'w') as f:
		f.write('{"black ice r4-c": "aee4bdf2-0b54-4c6d-af93-9fe4848e1f76"}')

data_file = open("assets/data.json", "r")
data = json.loads(data_file.read())
data_file.close()


client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
	print("[ Connected to Discord ]")
	print(time.time())

	print("[ Starting market scan daemon ]")
	scan_market.start()
	print("[ Started market scan daemon ]")

@client.event
async def on_message(message):
	if message.author != client.user:
		cmd = message.content.split(" ")

		name_map_file = open("assets/ids.json", "r")
		name_map = json.loads(name_map_file.read())
		name_map_file.close()

		match cmd.pop(0):
			case "econ":
				try:
					print(os.environ["NO_COMMANDS"])

					embed=discord.Embed(title=f'Not available!', description=f'This bot no longer uses the `econ` prefix.\nInterested in seeing what it can do now? Run `r6 help`!\n\n*If you would like to purchase access or this message is in error, contact Barna on Discord!*', color=0xFF5733)
					await message.channel.send(embed=embed)

					return
				except:
					print("Commands are enabled, continuing...")
					pass

				match cmd.pop(0):
					case "list":
						msg = ""
						item_no = 0
						for key, value in name_map.items():
							msg += f'{key}\n'
							item_no += 1
							if ( item_no > 99 ):
								break
						embed=discord.Embed(title=f'Tracked Skins', description=f'# Ask Barna for new Items.\n\n# Skins:\n{msg}', color=0xFF5733)
						await message.channel.send(embed=embed)
						return
					case "id":
						item_id = " ".join(cmd).lower()
						_data = None
						print(json.dumps(data, indent=2))
						try:
							_data = data[item_id]
						except:
							msg = "We aren't tracking this item ID!"
							embed=discord.Embed(title=f'Help', description=f'# Ask Barna on GH/DC for help!\n\n## {msg}', color=0xFF5733)
							await message.channel.send(embed=embed)
						if ( _data == None):
							return

						cleaned_data = [x[0] for x in _data["sold"] if x[0]]
						sold_len = len(cleaned_data)
						ten_RAP = round(sum(cleaned_data[-10:]) / max(1, min(10, sold_len)))
						hundred_RAP = round(sum(cleaned_data[-100:]) / max(1, min(100, sold_len)))
						all_time_RAP = round(sum(cleaned_data) / max(1, sold_len))

						msg = f'# Buy:\n\tMinimum Buyer: **{_data["data"][0]}** R6 credits\n\tMaximum Buyer: **{_data["data"][1]}** R6 credits\n\tVolume Buyers: **{_data["data"][2]}**\n'
						msg += f'# Sell:\n\tMinimum Seller: **{_data["data"][3]}** R6 credits\n\tMaximum Seller: **{_data["data"][4]}** R6 credits\n\tVolume Sellers: **{_data["data"][5]}**\n\tLast Sold: **{_data["sold"][-1][0]}**\n\n'
						msg += f'### Quick Analysis:\n\tHighest Buyer vs. Lowest Seller: **{(_data["data"][3] or 0) - (_data["data"][1] or 0)}** R6 credits\n\tLast Sale vs. Lowest Seller: **{(_data["data"][3] or 0) - (_data["sold"][-1][0] or 0)} ({round(100 -((_data["sold"][-1][0] or 0) / (_data["data"][3] or 1)) * 100, 2)}%)** R6 credits\n'
						msg += f'### RAP:\n\t10 - **{ten_RAP}**\n\t100 - **{hundred_RAP}**\n\tAll Time - **{all_time_RAP}**\n\n\t*(Total Data: {sold_len})*\n### Tags:\n\n{_data["tags"]}\n### Item ID:\n\t{item_id}'
						embed=discord.Embed(title=f'{_data["name"]} ({_data["type"]})', url=f'https://www.ubisoft.com/en-us/game/rainbow-six/siege/marketplace?route=buy%252Fitem-details&itemId={item_id}', description=f'{msg}', color=0xFF5733)
						embed.set_thumbnail(url=_data["asset_url"])
						await message.channel.send(embed=embed)
					case "name":
						_data = None
						try:
							item_id = name_map[" ".join(cmd).lower()]
							_data = data[item_id]
						except:
							msg = "We aren't tracking this item name, try a different name or run 'econ list'!"
							embed=discord.Embed(title=f'Help', description=f'# Ask Barna on GH/DC for help!\n\n## {msg}', color=0xFF5733)
							await message.channel.send(embed=embed)
						if ( _data == None):
							return

						cleaned_data = [x[0] for x in _data["sold"] if x[0]]
						sold_len = len(cleaned_data)
						ten_RAP = round(sum(cleaned_data[-10:]) / max(1, min(10, sold_len)))
						hundred_RAP = round(sum(cleaned_data[-100:]) / max(1, min(100, sold_len)))
						all_time_RAP = round(sum(cleaned_data) / max(1, sold_len))

						msg = f'# Buy:\n\tMinimum Buyer: **{_data["data"][0]}** R6 credits\n\tMaximum Buyer: **{_data["data"][1]}** R6 credits\n\tVolume Buyers: **{_data["data"][2]}**\n'
						msg += f'# Sell:\n\tMinimum Seller: **{_data["data"][3]}** R6 credits\n\tMaximum Seller: **{_data["data"][4]}** R6 credits\n\tVolume Sellers: **{_data["data"][5]}**\n\tLast Sold: **{_data["sold"][-1][0]}**\n\n'
						msg += f'### Quick Analysis:\n\tHighest Buyer vs. Lowest Seller: **{(_data["data"][3] or 0) - (_data["data"][1] or 0)}** R6 credits\n\tLast Sale vs. Lowest Seller: **{(_data["data"][3] or 0) - (_data["sold"][-1][0] or 0)} ({round(100 -((_data["sold"][-1][0] or 0) / (_data["data"][3] or 1)) * 100, 2)}%)** R6 credits\n'
						msg += f'### RAP:\n\t10 - **{ten_RAP}**\n\t100 - **{hundred_RAP}**\n\tAll Time - **{all_time_RAP}**\n\n\t*(Total Data: {sold_len})*\n### Tags:\n\n{_data["tags"]}\n### Item ID:\n\t{item_id}'
						embed=discord.Embed(title=f'{_data["name"]} ({_data["type"]})', url=f'https://www.ubisoft.com/en-us/game/rainbow-six/siege/marketplace?route=buy%252Fitem-details&itemId={item_id}', description=f'{msg}', color=0xFF5733)
						embed.set_thumbnail(url=_data["asset_url"])
						await message.channel.send(embed=embed)
					case "graph":
						num = cmd.pop(0)
						unit_type = cmd.pop(0)

						item_id = " ".join(cmd).lower()
						_data = copy.deepcopy(data[item_id])
						unit = "days"
						dividend = 86400
						
						match num:
							case "all":
								pass
							case _:
								_data["sold"] = [x for x in _data["sold"] if x[0]]
								_data["sold"] = _data["sold"][-int(num):]
								
						match unit_type:
							case "days":
								pass
							case "hours":
								unit = "hours"
								dividend = 86400 / 24
							case "minutes":
								unit = "minutes"
								dividend = 86400 / 24 / 60
							case _:
								msg = "The following units are available:\n\t- days\n\t- hours\n\t- minutes"
								embed=discord.Embed(title=f'Help', description=f'# Ask Barna on GH/DC for help!\n\n# Skins:\n{msg}', color=0xFF5733)
								await message.channel.send(embed=embed)

						cleaned_data = [x[0] for x in _data["sold"] if x[0]]
						cleaned_times = [(time.time() - x[1]) / dividend for x in _data["sold"] if x[0]]
					 
						print(f'{cleaned_times} vs {cleaned_data}')

						plt.scatter( np.array(cleaned_times), np.array(cleaned_data) )
						plt.xlabel( f' Time ({unit} ago) ' )
						plt.ylabel( " Purchase Amount " )

						trendline = np.polyfit( np.array(cleaned_times), np.array(cleaned_data), 1 )
						trendline_function = np.poly1d( trendline )
						plt.plot( cleaned_times, trendline_function(cleaned_times) )
						plt.title( f'{_data["name"]} ({_data["type"]})' )
						plt.savefig( f"graphs/{item_id}.png" )
						plt.clf()

						file = discord.File(f'graphs/{item_id}.png')
						e = discord.Embed()
						e.set_image(url=f'attachment://{item_id}.png')
						await message.channel.send(file = file, embed=e)
					case "profit":
						purchase_price = float(cmd.pop(0))
						profitable_sell = purchase_price * 1.1

						item_id = " ".join(cmd).lower()
						_data = None
						try:
							_data = data[item_id]
						except:
							msg = "We aren't tracking this item ID!"
							embed=discord.Embed(title=f'Help', description=f'# Ask Barna on GH/DC for help!\n\n## {msg}', color=0xFF5733)
							await message.channel.send(embed=embed)
						if ( _data == None):
							return
						
						cleaned_data = [x[0] for x in _data["sold"] if x[0]]
						sold_len = len(cleaned_data)
						ten_RAP = round(sum(cleaned_data[-10:]) / max(1, min(10, sold_len)))

						msg = f'\n### Purchased At:\n\t**{purchase_price}** R6 credits\n### Sale Price to Break Even:\n\t**{profitable_sell}** R6 credits\n### Current Net Gain if Sold:\n\t**{((ten_RAP or 0) - purchase_price) * 0.90}** R6 credits'
						embed=discord.Embed(title=f'Profit Margins', description=f'{msg}', color=0xFF5733)
						await message.channel.send(embed=embed)

					case "margin":
					    with open('assets/data.json', 'r') as file:
						    data_margin = json.load(file)
					    item_id = " ".join(cmd).lower()
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
					    await message.channel.send(file = file, embed=e)

					case "invest":
						with open('avg_profit.json', 'r') as file:
							data_profit = json.load(file)
						max_price = float(cmd.pop(0))
						min_percent = float(cmd.pop(0))
						min_data_points = float(cmd.pop(0))
						data_profit = sorted(data_profit.items(), key=lambda x: x[1][0], reverse=True)
						msg = ""
						invest_list =[]
						item_no = 0
						for weapon in data_profit:
							if weapon[1][1] <= max_price and weapon[1][2] > min_data_points and weapon[1][3] > min_percent:
								msg += f"{weapon[0]} | Profit: {weapon[1][0]:.0f} | Price: {weapon[1][1]:.0f} | Low percentage: {weapon[1][3]:.0f}\n" 
								invest_list[item_no] = weapon[4]
								item_no += 1
								if ( item_no > 9 ):
									break		
						embed=discord.Embed(title='Average profit', description=f'{msg}', color=0xFF5733)
						draw(invest_list)
						await message.channel.send(embed=embed)

					case _:
					    msg = "The following commands are available:\n\n\t- econ id <item id>\n\n\t- econ graph <# entries (1, 2, ... | all)> <unit (days | hours | minutes)>\n\n\t- econ profit <what you purchased for> <item id>\n\n\t - econ invest <max_price min_percent min_data_points>"
					    embed=discord.Embed(title=f'Help', description=f'# Ask Barna on GH/DC for help!\n\n# Skins:\n{msg}', color=0xFF5733)
					    await message.channel.send(embed=embed)



@tasks.loop(minutes=5)
async def scan_market():
	with contextlib.suppress(Exception):
		print("[ Opening Session ]")

		auth = Auth(os.getenv("AUTH_EMAIL"), os.getenv("AUTH_PW"))

		print("[ Scanning market... ]")
		item_id_file = open("assets/ids.json", "r")
		item_ids = json.loads(item_id_file.read())
		item_id_file.close()
		for key, item_id in item_ids.items():
			print(f'[ - [ Scanning {key} ] ]')

			auth.item_id = item_id
			res = await auth.try_query_db()
			if (not res):
				print("Rate Limited in scan_market")
				continue

			# Meta: NAME | TYPE | TAGS - Buyers: LOW | HIGH | VOL - Sellers: LOW | HIGH | VOL
			try:
				data[item_id]
			except:
				data[item_id] = {
					"name": res[0],
					"type": res[1],
					"tags": res[2],
					"asset_url": res[10],
					"sold": [],
					"data": None
				}
			if data[item_id]["data"] == None or data[item_id]["data"] != [res[3], res[4], res[5], res[6], res[7], res[8]]:
				data[item_id]["data"] = [res[3], res[4], res[5], res[6], res[7], res[8]]
				print('[ - - NEW PRIMARY DATA ]')
			
			if len(data[item_id]["sold"]) == 0 or data[item_id]["sold"][len(data[item_id]["sold"]) - 1][0] != res[9]:
				data[item_id]["sold"] = data[item_id]["sold"] + [[res[9], time.time()]]
				print('[ - - NEW LAST SOLD ]')

			print(f'[ ~ [ Done checking {key} ] ]')
			
		print("[ Closing Session ]")
		await auth.close()

		print("[ WRITING TO 'data.json' ]")

		data_file = open("assets/data.json", "w")
		data_file.write(json.dumps(data, indent=2))
		data_file.close()

		print("[ FINISHED WRITING TO 'data.json' ]")
							

client.run(os.getenv("TOKEN"))
