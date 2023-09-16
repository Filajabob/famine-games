import json
from player import Player, load

roster_name = input("Roster: ")
player_name = input("Player name: ")
player = load(json_file=f"assets/custom_roster/{roster_name}/data.json", player_name=player_name)

for stat_name, value in player.stats.items():
    print(f"{stat_name}: {value}")
