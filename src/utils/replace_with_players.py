def replace_with_players(text, attacker, defender, intervener=None):
    result = text.replace("{o}", attacker.name)