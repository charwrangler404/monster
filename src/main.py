from cmd2 import Cmd
from pathlib import Path
import json
import re
from collections import defaultdict
from classes import Player, Monster
import methods

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
class MonsterSimulator(Cmd):
    """A command-line shell that executes Python functions."""
    initiative = 100
    initiative_order = {}
    monster_catalogue = []
    player_catalogue = []
    monsters = {}
    players = {}


    def __init__(self):
        super().__init__()

        # Load the Python functions that you want to make available to the shell.
        self.functions = {
            "add_monster": self.do_add_monster,
            "add_player": self.do_add_player,
            "load_monster_catalogue": self.do_load_monster_catalogue,
            "load_player_catalogue": self.do_load_player_catalogue,
            "clear_init": self.do_clear_init,
            "show_init": self.do_show_init,
            "heal": self.do_heal,
            "damage": self.do_damage,
        }

    def do_add_monster(self, key):
        """Add a monster to the initiative from the catalogue
            Returns:
                0 if successful, -1 if unsuccessful
        """
        if self.monsters[key] is None:
            try:
                for monster in self.monster_catalogue:
                    if monster["name"].lower() == key.lower():
                        monster["init"] = methods.roll("1d20") + methods.modifier(monster["dex"])
                        monster['hp'] = methods.roll_hp(monster)
                        self.monsters[key].lower()
                        return 0
                return -1
            except Warning:
                print(f"Error, allocating monster {key} from catalogue") 
                return -1
        else:
            try:
                for monster in self.monster_catalogue:
                    if monster["name"].lower() == key.lower():
                        monster["init"] = methods.roll("1d20") + methods.modifier(monster["dex"])
                        monster["hp"] = methods.roll_hp(monster)
                    self.monsters[key].update(monster)
                return 0
            except Warning:
                print(f"Error, could not add monster: {key}")
                return -1
                
    def do_add_player(self, name, initiative):
        """Add a player to the initiative order."""
        for player in self.player_catalogue:
            if player["name"].lower() == name.lower():
                player["init"] = initiative
                self.players.update(player)
        

    def do_load_monster_catalogue(self, folder):
        """Loads a monster's config file into memory"""
        p = Path(folder)
        for file in p.iterdir():
            if file.is_file():
                with open(str(file), 'r') as fh:
                    contents = fh.read()
                monster = json.loads(contents)
                self.monster_catalogue.append(monster)

    def do_load_player_catalogue(self, folder):
        """Loads a catalogue of players from a folder"""
        p = Path(folder)
        for file in p.iterdir():
            if file.is_file():
                with open(str(file), "r") as fh:
                    contents = fh.read()
                    player = json.loads(contents)
                    self.player_catalogue.append(player)

    def do_next_init(self):
        """Iterates to the next in the initiative order"""
        self.initiative -= 1
        i = 0
        if self.initiative == 0:
            self.initiative = 100

        for value in self.initiative_order:
            if self.initiative == value:
                i += 1
        for player in self.players:
            if player["init"] == self.initiative:
                print(f"Next player: {player['name']} with initiative {player['init']}")
        for monster in self.monsters:
            if monster["init"] == self.initiative:
                print(f"Next monster {monster['name']} with initiative {monster['init']}")

        if i == 0:
            self.next_init()

    def do_show_init(self):
        """Show the initiative order"""
        pass

    def do_heal(self, target, amount):
        """Heal a target a number of hit points"""
        target.heal(amount)

    def do_damage(self, target, amount):
        """Deal damage to a target"""
        target.damage(amount)

    def do_clear_init(self):
        """Clear the initiative order"""
        self.monsters = methods.rebuild_monster_table(self.monsters)
        self.players = methods.rebuild_player_table(self.players)

                
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