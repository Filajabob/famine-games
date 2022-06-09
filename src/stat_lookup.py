import json
from player import Player, load

player_name = input("Player name: ")
player = load(json_file="assets/custom_roster/students/data.json", player_name=player_name)

for stat_name, value in player.stats.items():
    print(f"{stat_name}: {value}")
