import os
import json
import random
from player import Player

fp = input("Load names from filepath (or leave blank to build in the command prompt: ")

if len(fp) != 0:
    # Load from filepath
    with open(fp, "r") as f:
        names = json.load(f)
else:
    # Load from command prompt
    print("Input a name and press ENTER to add a name.")
    print("Leave input blank and press ENTER to finish roster creation.")

    names = []

    while True:
        name = input("> ")

        if len(name) == 0:
            break

        names.append(name)

# Create a unique roster name
while True:
    roster_name = input("Create a roster name: ")

    if os.path.exists(f"assets/custom_roster/{roster_name}"):
        print("This name already exists.")
    else:
        break

# Create roster directory if it doesn't exist yet
if not os.path.exists(f"src/assets/custom_roster/{roster_name}"):
    os.mkdir(f"src/assets/custom_roster/{roster_name}")

randomize = input("The roster builder can randomize offense, defense, and intervention score for each player. Individual players can "
      "also be modified randomly after data creation. Randomize stats? (Y/n) ") == 'Y'

if randomize:
    lower_bound = int(input("Lower bound: "))
    upper_bound = int(input("Upper bound: "))
else:
    lower_bound = 0
    upper_bound = 0

players_data = {}
# Generate data
for name in names:
    player = Player(name, random.randint(lower_bound, upper_bound), random.randint(lower_bound, upper_bound),
                    random.randint(lower_bound, upper_bound))
    players_data[name] = player.serialize()

with open(f"src/assets/custom_roster/{roster_name}/data.json", 'w') as f:
    json.dump(players_data, f)
    f.truncate()

with open(f"src/assets/custom_roster/{roster_name}/names.json", 'w') as f:
    json.dump(names, f)
    f.truncate()

print(f"Roster '{roster_name}' saved to src/assets/custom_roster/{roster_name}")
