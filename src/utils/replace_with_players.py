from player import Player

# TODO: Make it possible to add stuff other than players to the text


def replace_with_players(text, attacker: Player = None, defender: Player = None, intervener: Player = None):
    if attacker:
        text = text.replace("{o}", attacker.name)

    if defender:
        text = text.replace("{d}", defender.name)

    if intervener:
        text = text.replace("{i}", intervener.name)

    return text
