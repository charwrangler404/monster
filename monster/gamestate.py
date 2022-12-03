import json

from monster import dice
from copy import copy

MOD = 20

class Monster:
    def __init__(self, template, id):
        with open(template, "r") as fh:
            file = fh.read()
        mtemplate = json.loads(file)
        self.name  = mtemplate["name"]
        self.initiative = dice.dX(1, MOD) + mtemplate["init"]
        # Because dice.dX returns an array of dice, we need to parse that into
        # a total, and then add the monster's template
        self.hit_dice = dice.dX(mtemplate["hd_num"], mtemplate["hd_size"])
        self.damage = 0
        self.alive = True
        self.id = id

        # Here we add up our hit dice and get a hit point total
        self.hit_points = 0
        for i in self.hit_dice:
            self.hit_points += i
        # We must add the hit point bonus found in the monster template
        self.hit_points += mtemplate["hit_bonus"]

        # some miscellaneous stuf
        self.experience = mtemplate["experience"]
        self.armour_class = mtemplate["armour_class"]

        # Finally, the attack section
        # self.attacks will contain an array of attacks that can be performed
        self.attacks = mtemplate["attacks"]
        self.num_attacks = mtemplate["num_attacks"]

    def __str__(self):
        return f'{self.initiative}%{self.name}-{self.id} [{self.armour_class}]({self.hit_points - self.damage}/{self.hit_points})'
    
    def __copy__():
        return self

    def hit(self, to_hit, damage):
        if to_hit > self.armour_class:
            self.damage += damage
        if self.damage >= self.hit_points:
            self.alive = False

    def attack(self):
        i = 0
        n = len(self.attacks)
        for attack in self.attacks:
            ans = input(f"Would you like to use {attack['atk_name']} - {i}/{n} > Y/n")
            if ans.lower() == "n":
                continue
            else:
                atk_roll = dice.dX(1, 20) + attack['atk_bonus']
                atk_dmg = dice.dX(attack['dmg_dice_num'], attack['dmg_dice_size']) + attack['dmg_bonus']
                attack = f'+{atk_roll}: {atk_dmg}'
                return attack

class Player:
    def __init__(self, name, armour_class, initiative):
        self.name = name
        self.initiative = initiative
        self.armour_class = armour_class

    def __str__(self):
        return f'{self.initiative}%{self.name}[{self.armour_class}]'

    def __copy__():
        return self
class Board:
    def __init__(self, monsters, players):
        self.monsters = copy(monsters)
        self.players = copy(players)

    def create_monster(self, file):
        newmonster = Monster(file)
        self.monsters.append(copy(newmonster))

    def create_player(self, initiative):
        newplayer = Player(initiative)
        self.players.append(copy(newplayer))

    def print_board(self):
        init_order = copy(self.players)
        for player in init_order.sort(reverse=True):
            print(player)
        for monster in self.monsters:
            print(monster)