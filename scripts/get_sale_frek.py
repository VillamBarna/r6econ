import json
import time

def get_sale_frek(id, data):
     weapon_info = data[id]
     sold_values = weapon_info.get("sold", [])
     sold_values = [x[0] for x in sold_values if\
               (time.time() - x[1])/86400 < 30]
     if len(sold_values) == 0 or weapon_info["data"][5] is None:
          print(id)
          return None
     return len(sold_values)/weapon_info["data"][5]


if __name__ == "__main__":
     with open('assets/data.json', 'r') as file:
          data = json.load(file)

     ids = data.keys()
     frekvent = []
     non_frekvent = []
     for id in ids:
          frek = get_sale_frek(id, data)
          if frek is None:
               continue
          elif frek > 1:
               frekvent.append(id)
          else:
               non_frekvent.append(id)
# for id in frekvent:
#      print(f"{data[id]['name']} {data[id]['tags'][0]}")
# print(len(frekvent), len(non_frekvent))
# print(data[non_frekvent[0]]['name'], data[non_frekvent[0]]['tags'][0])
# print(len(data[non_frekvent[0]]['sold']))
