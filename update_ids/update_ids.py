import json
import os

with open("unique_item_ids.txt", "r") as file:
     new_ids = file.readlines()

with open(os.path.join(os.path.dirname(__file__), os.pardir, "assets/data.json"), "r") as file:
     ids = json.load(file)

for id in new_ids:
     ids[id.strip("\n")] = id.strip("\n")

with open(os.path.join(os.path.dirname(__file__), os.pardir, "assets/data.json"), "w") as file:
     file.write(json.dumps(ids, indent=2))
