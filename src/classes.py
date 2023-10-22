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
        self.hp += min(self.data['max_hp'] - self.hp, heal)

    def damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
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
        elif success <= 3:
            self.last_stand_status = False
            self.hp = 1
            self.alive = True


class InitiativeOrder:
    order = []
