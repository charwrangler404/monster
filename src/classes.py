import json
import methods
from main.MonsterSimulator import players
from main.MonsterSimulator import monsters

class Character:
    alive = True
    hp = 1
    def __init__(self, template):
        self.data = json.loads(template)

    def heal(self, heal):
        """Called to heal this object"""
        self.hp += min(self.data['max_hp'] - self.hp, heal)

    def damage(self, damage):
        """Called to deal damage to this object"""
        self.hp -= damage
        if self.hp < 1:
            self.alive = False
            

class Monster(Character):
    def __init__(self, template):
        super().__init__(template)
        self.hp = methods.roll_hp(self.data["hd"])
        self.init = methods.roll("1d20") + methods.modifier(self.data["dex"])
    

class Player(Character):
    last_stand_status  = False
    last_stand_rolls = []

    def __init__(self, template, initiative):
        super().__init__(template)
        self.init = initiative

    def damage(self, damage):
        """Called when this object is dealt damage"""
        self.hp -= damage
        if self.hp < 1:
            self.last_stand_status = True

    def last_stand(self, roll):
        """Called when this object is fighting for it's life"""
        success = 0
        failure = 0
        if len(self.last_stand_rolls) < 6:
            self.last_stand_rolls.append(roll)
        for iterroll in self.last_stand_rolls:
            if iterroll< 10:
                success += 1
            else:
                failure -= 1
        if failure <= 3:
            self.alive = False
            self.hp = -1
            self.last_stand_status = False
        elif success <= 3:
            self.last_stand_status = False
            self.hp = 1
            self.alive = True


class InitiativeOrder:
    order = []
    position = 100
    next_init= []

    def advance_order(self):
        """Called to advance the order to the next initiative group"""
        self.position -= 1
        for character in self.order:
            if character.init == self.position:
                self.next_init.append(character)
        self.next_init = sorted(self.order, key=lambda character: character.data['dex'])
        
        if len(self.next_init) == 0:
            self.advance_order()

    def add_to_order(self, character):
        """Called to add a character object to the order"""
        self.order.append(character)