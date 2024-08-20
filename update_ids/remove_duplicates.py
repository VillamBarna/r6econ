import json
import os

with open(os.path.join(os.path.dirname(__file__), os.pardir, "assets/ids.json"), "r") as file:
     ids_dict = json.load(file)

ids = list(set(ids_dict.values()))

ids_unique = {}

for id in ids:
     ids_unique[id] = id


with open(os.path.join(os.path.dirname(__file__), os.pardir, "assets/ids.json"), "w") as file:
     file.write(json.dumps(ids_unique, indent=2))
