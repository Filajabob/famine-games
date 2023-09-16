import time
import random
import json
import os

from player import Player, load
from game import Game
import utils

players = []

utils.typewriter_print("Welcome to the Famine Games!")
roster_name = utils.typewriter_input("Input a roster name, or leave blank to build a temporary one: ")
roster_fp = f"assets/custom_roster/{roster_name}"

if len(roster_fp) != 0:
    if not os.path.exists(roster_fp):
        raise KeyError("Roster does not exist.")

    utils.typewriter_print("Loading roster...")
    roster_data = roster_fp + "/data.json"

    with open(roster_data, 'r') as f:
        names = json.load(f)  # sussy amogus

    for player_name in names:
        players.append(load(json_file=roster_data, player_name=player_name))

else:
    amount_of_players = int(utils.typewriter_input("How many players should we have? "))
    utils.typewriter_print(f"Good. We'll have {amount_of_players} players. What will their names be?")

    for i in range(1, amount_of_players + 1):
        name = utils.typewriter_input(f"Player #{i}: ")
        players.append(Player(name))

    utils.typewriter_print("Good! Time to start!")

utils.typewriter_print("Disclaimer: No harm or offense is intended. May contain inappropriate or offensive content.",
                       end='\n')

game = Game(players)

# Load texts that we will print for different game components

with open("assets/game/sightings.json", 'r') as f:
    sightings = json.load(f)

with open("assets/game/attacks.json", 'r') as f:
    attacks = json.load(f)

with open("assets/game/turn_results.json", 'r') as f:
    turn_results_texts = json.load(f)

with open("assets/game/intervention_attacks.json", 'r') as f:
    intervention_attacks = json.load(f)

day = 1

try:
    while game.can_run():
        utils.typewriter_print(f"Day {day}\n")

        turn_results = game.rotate()

        # Print sighting (cosmetic)
        utils.typewriter_print(
            utils.replace_with_players(
                random.choice(sightings), turn_results["attacker"], turn_results["defender"]
            )
        )

        time.sleep(0.75)

        # Print attack (cosmetic)
        utils.typewriter_print(
            utils.replace_with_players(
                random.choice(attacks), turn_results["attacker"], turn_results["defender"]
            )
        )

        time.sleep(0.75)

        # Print intervener attack if there is an intervention
        if turn_results["intervener"]:
            utils.typewriter_print(utils.replace_with_players(
                random.choice(intervention_attacks), turn_results["attacker"], turn_results["defender"],
                turn_results["intervener"]
            ))

            time.sleep(0.75)

        # Print results (necessary)
        utils.typewriter_print(
            utils.replace_with_players(
                random.choice(turn_results_texts[str(turn_results["case"])]), turn_results["attacker"],
                turn_results["defender"], turn_results["intervener"]
            )
        )

        # Print survivors if there are 10 or less people
        if len(game.players) <= 10:
            print("")
            utils.typewriter_print(f"Players left\n")

            for player in game.players:
                print(f"{player.name}: {game.stats[player.name]['total_kills']} kills this game")
                time.sleep(0.25)

        print("")

        print(f"Players left: {len(game.players)}")

        print("")

        time.sleep(1.5)

        day += 1

except KeyboardInterrupt:
    print("")
    print("")
    utils.typewriter_print("Exiting...")
    quit(-1)

game.finish_game()
utils.typewriter_print(f"The game has finished! The winner is {game.players[0].name}!")
