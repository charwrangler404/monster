import cmd2
from pathlib import Path
import json
import re
from random import randint
from collections import defaultdict

initiative = 100
initiative_order = {}
monster_catalogue = []
player_catalogue = []
monsters = {}
players = {}

#def none_split(string):
#    """Splits a string into two different strings, one of which will always be filled, the other of which should be filled with None if there is nothing left after the split.
#
#  Args:
#    string: The string to split.
#
#  Returns:
#    A tuple of two strings, where the first string is always filled and the second string is filled with None if there is nothing left after the split.
#    """
#    # Split the string at the first whitespace character.
#    parts = string.split("d", maxsplit=1)
#
#    # If there is only one part, then return the first part and None.
#    if len(parts) == 1:
#        return parts[0], None
#
#    # Otherwise, return the two parts.
#    return parts[0], parts[1]
#
class Character:
    alive = True
    def __init__(self, template):
        self.data = json.loads(template)
    def heal(self, heal):
        self.hp += min(self.data['max_hp'] - self.hp, heal)
    def damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.alive = False
            

class Monster(Character):
    def __init__(self, template):
        self.__init__()
        self.hp = roll_hp(self.data["hd"])
        self.init = roll("1d20") + modifier(self.data["dex"])
    
    def at_death(self):
        monsters = rebuild_monster_table(monsters)



class Player(Character):
    last_stand = False
    last_stand_rolls = []

    def __init__(self, template, initiative):
        self.__init__()
        self.init = initiative
    def damage(self, damage):
        self.hp -= damage
        if self.hp < 1:
            self.last_stand = True

    def last_stand(self, roll):
        success = 0
        failure = 0
        if len(self.last_stand_rolls) < 6:
            self.last_stand_rolls.append(roll)
        for iterroll in self.last_stand_rolls:
            if iterroll < 10:
                success += 1
            else:
                failure -= 1
        
        if failure <= 3:
            self.alive = False

    def at_death(self):
        players = rebuild_player_table(players)


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

def search_dict(dict, value):
      """Searches the different keys of a dictionary for a certain value and returns the key if it is found, or None if it is not found.

      Args:
        dict: The dictionary to search.
        value: The value to search for.

      Returns:
        The key if the value is found, or None if it is not found.
      """

      for key in dict.keys():
        if dict[key] == value:
          return key
      return None

def search_set(set, value):
    """
    Searches a set for a particular value

    Returns:
        True or False
    """
    return value in set

class MonsterSimulator(cmd2.Cmd):
    """A command-line shell that executes Python functions."""

    def __init__(self):
        super().__init__()

        # Load the Python functions that you want to make available to the shell.
        self.functions = {
            "add_monster": self.add_monster,
            "add_player": self.add_player,
            "load_monster_catalogue": self.load_monster_catalogue,
            "load_player_catalogue": self.load_player_catalogue,
            "clear_init": self.clear_init,
            "show_init": self.show_init,
            "heal": self.heal,
            "remove_monster": self.remove_monster,
            "damage_monster": self.damage_monster,
        }

    def add_monster(self, key):
        """Add a monster to the initiative from the catalogue
            Returns:
                0 if successful, -1 if unsuccessful
        """
        if monsters[key] is None:
            try:
                for monster in monster_catalogue:
                    if monster["name"].lower() == key.lower():
                        monster["init"] = roll("1d20") + modifier(monster["dex"])
                        monster['hp'] = roll_hp(monster)
                        monsters[key].lower()
                        return 0
                return -1
            except Warning:
                print(f"Error, allocating monster {key} from catalogue") 
                return -1
        else:
            try:
                for monster in monster_catalogue:
                    if monster["name"].lower() == key.lower():
                        monster["init"] = roll("1d20") + modifier(monster["dex"])
                        monster["hp"] = roll_hp(monster)
                    monsters[key].update(monster)
                return 0
            except Warning:
                print(f"Error, could not add monster: {key}")
                return -1
                
    def add_player(self, name, initiative):
        """Add a player to the initiative order."""
        for player in player_catalogue:
            if player["name"].lower() == name.lower():
                player["init"] = initiative
                players.update(player)
        

    def load_monster_catalogue(self, folder):
        """Loads a monster's config file into memory"""
        p = Path(folder)
        for file in p.iterdir():
            if file.is_file():
                with open(str(file), 'r') as fh:
                    contents = fh.read()
                monster = json.loads(contents)
                monster_catalogue.append(monster)

    def load_player_catalogue(self, folder):
        p = Path(folder)
        for file in p.iterdir():
            if file.is_file():
                with open(str(file), "r") as fh:
                    contents = fh.read()
                    player = json.loads(contents)
                    player_catalogue.append(player)

    def next_init(self):
        initiative -= 1
        i = 0
        if initiative == 0:
            initiative = 100

        for value in initiative_order:
            if initiative == value:
                i += 1
        for player in players:
            if player["init"] == initiative:
                print(f"Next player: {player['name']} with initiative {player['init']}")
        for monster in monsters:
            if monster["init"] == initiative:
                print(f"Next monster {monster['name']} with initiative {monster['init']}")


    def damage_monster(self, monsterstring, damage):
        pass

    def remove_monster(self, monsterstring):

        pass

    def show_init(self):
        pass

    def heal(self, keytype, key, amount):
        pass

    def clear_init(self):
        """Clear the initiative order"""
        players = {}
        monsters = {}
        return 0
                
    def default(self, line):
        """Executes a Python function if it exists."""
        function_name = line.split(" ")[0]

        if function_name in self.functions:
            args = line.split(" ")[1:]
            result = self.functions[function_name](*args)

            if result is not None:
                print(result)
        else:
            print("Unknown command: {}".format(line))

if __name__ == "__main__":
    MonsterSimulator().cmdloop()