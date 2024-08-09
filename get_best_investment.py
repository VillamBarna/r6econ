from margin import analyze_sold_values
import json

with open("assets/data.json", "r") as file:
	data = json.load(file)

avg_profit = dict()
for weapon_id, weapon_info in data.items():
	weapon_name = weapon_info.get("name", "Unknown")
	first_tag = weapon_info.get("tags", ["Unknown"])[0]  # Get the first tag or "Unknown" if not present
	weapon_name += f' - {first_tag}'
	
	sold_values = weapon_info.get("sold", [])
	sold_values_list = [value[0] for value in sold_values if isinstance(value[0], (int, float))]  # Filter out non-numeric values
	
	_, _, _, _, _, _, _, profit, _, _ = analyze_sold_values(sold_values_list)

	avg_profit[weapon_name] = profit

with open("avg_profit.json", "w") as file:
	json.dump(avg_profit, file)
