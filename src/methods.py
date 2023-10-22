from random import randint

def rebuild_monster_table(monsters):
    newmonsters = {}
    for monster in monsters:
        if monster.alive == True:
           newmonsters.update(monster)
    return newmonsters

def rebuild_player_table(players):
    newplayers = {}
    for player in players:
        if player.alive == True:
            newplayers.update(player)
    return newplayers

def modifier(stat):
    """
    Returns the modifer of the stat passed
    """
    return ((stat - 10) // 2)

def roll_hp(template):
    """
     Rolls HP for a given template
        Returns:
            HP total or -1 if failed
    """
    try:
        num = template['hd'].split("d")[0]
    except Warning:
        print("Error in processing template")
        return -1
    hp = roll(template["hd"]) + (modifier(template["con"]) * num)
    return hp

def roll(rollstring):
    """Roll a number of dice of the same size and return the result

    Returns:
        Sum of the rolled dice
    """
    try:
        num, base = rollstring.strip().split("d")
    except Warning:
        print("Error, unrecognized roll string")
        return None
    result = 0
    while num != 0:
        result += randint(1, (base + 1))
        num -= 1
    return result
