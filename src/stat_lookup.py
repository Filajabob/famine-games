import json
from player import Player, load

player_name = input("Player name: ")
player = load(json_file="assets/custom_roster/students/data.json", player_name=player_name)

with open("assets/custom_roster/students/data.json", 'r') as f:
    data = json.load(f)

sorted_datasets = []

for stat_name in [
    "total_kills", "successful_defenses", "attempted_attacks", "attempted_defenses",
    "attempted_interventions", "kills_off_attacks", "kills_off_defenses", "kills_off_interventions",
    "rounds_survived", "wins", "total_games"
]:
    ranked = sorted(data, key=lambda d: d["stats"][stat_name])
    sorted_datasets.append(ranked)

print(sorted_datasets)

for stat_name, value in player.stats.items():
    print(f"{stat_name}: {value}")
