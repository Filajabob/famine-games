import json
from player import Player, load

player_name = input("Player name: ")
player = load(json_file="assets/custom_roster/students/data.json", player_name=player_name)

with open("assets/custom_roster/students/data.json", 'r') as f:
    data = json.load(f)

sorted_datasets = []

# TODO: fix
for p, value in data.items():
    ranked = sorted(value, key=lambda d: d[stat_name])
    sorted_datasets.append(ranked)

print(sorted_datasets)

for stat_name, value in player.stats.items():
    print(f"{stat_name}: {value}")

