import math
import random
from skills import AttackSkill


class DefaultMeleeSkill(AttackSkill):
    def __init__(self, modifiers):
        name = "Melee Attack"
        damage_type = "Normal"
        super().__init__(modifiers, damage_type, name)

    @staticmethod
    def skill_type():
        return "Melee"


def melee_attack_factory(attack, modifiers, on_hit=None, attributes=None):
    """
    Fancy factory to create melee attack skills
    :param attack: attack function to calculate damage and damage type
    :param modifiers: which modifiers to use with this attack skill
    :param on_hit: on_hit effects, applicable to this skill
    :param attributes: additional attributes, if any
    :return: MeleeAttack class based on DefaultMeleeSkill
    """
    class_methods = {"skill_modifiers": lambda: modifiers,
                     "get_damage": attack}
    if on_hit is not None:
        class_methods["get_on_hit_effect"] = on_hit
    if attributes is not None:
        class_methods.update(attributes)
    MeleeAttack = type('MeleeAttack', (DefaultMeleeSkill,), class_methods)
    return MeleeAttack


def select_modifiers(modifiers):
    return modifiers


def standard_attack(obj):
    return obj.modifiers["MELEE_ATTACK"]() * random.uniform(0.95, 1.05), obj.damage_type


def critical_attack(obj):
    if random.random() <= obj.modifiers["CRITICAL_CHANCE"]():
        return obj.modifiers["MELEE_ATTACK"]() * obj.modifiers["CRITICAL_MULTIPLIER"]() * random.uniform(0.95, 1.05),\
               "Critical"
    else:
        return obj.modifiers["MELEE_ATTACK"]() * random.uniform(0.95, 1.05), obj.damage_type


def lifesteal(obj):
    return "Heal", obj.modifiers["LIFE_STEAL"]()


class Char:
    def __init__(self):
        self.name = "Char"
        self.max_hp = self.hp = 100

        self.armour = 20

        self.magic_damage = 10
        self.resistance = 0.1

        self.melee_damage = 10
        self.melee_skill = "standard"
        self.melee_skills_dict = {"standard": standard_attack, "critical": critical_attack}
        self.melee_upgrade = None
        self.melee_on_hit = None

        self.critical_chance = 0
        self.critical_multiplier = 1.5

        self.life_steal = 0

        self.attack_skills = {"Melee": {self.melee_attack_skill(): self.get_modifiers(("MELEE_ATTACK",
                                                                                       "CRITICAL_CHANCE",
                                                                                       "CRITICAL_MULTIPLIER",
                                                                                       "LIFE_STEAL"))},
                              "Magic": {}}

        self.defences = {"Normal": self.receive_normal_damage, "Magic": self.receive_magic_damage,
                         "Critical": self.receive_normal_damage}

    def __repr__(self):
        return "hp {}, attack {}, armour {}, magic resistance {}".format(self.hp, self.melee_damage, self.armour,
                                                                         self.resistance)
    # melee attack
    @property
    def melee_modifier(self):
        return 1

    def full_melee_attack(self):
        return self.melee_damage * self.melee_modifier

    def melee_attack_skill(self):
        """
        Using fancy factory to dynamically define melee attack skill class
        :return: MeleeAttack class
        """
        return melee_attack_factory(self.melee_skills_dict[self.melee_skill],
                                    ("MELEE_ATTACK", "CRITICAL_CHANCE", "LIFE_STEAL"),
                                    on_hit=self.melee_on_hit)

    def refresh_melee_skill(self):
        """
        Creating melee skill anew, because I dunno how to do it dynamically
        """
        self.attack_skills["Melee"] = {self.melee_attack_skill(): self.get_modifiers(("MELEE_ATTACK",
                                                                                      "CRITICAL_CHANCE",
                                                                                      "CRITICAL_MULTIPLIER",
                                                                                      "LIFE_STEAL"))}
    # magic power
    @property
    def magic_modifier(self):
        return 1

    def magic_power(self):
        return self.magic_damage * self.magic_modifier

    # critical chance
    @property
    def critical_modifier(self):
        return 0.1

    def full_critical_chance(self):
        return self.critical_chance + self.critical_modifier

    def full_critical_multiplier(self):
        return self.critical_multiplier

    # life steal
    def life_steal_percent(self):
        return self.life_steal

    # creating an attack
    def attack(self):
        """
        Creating attack list from attack skills
        One melee skill and N magical skills
        """
        attack = {}
        attack.update(self.attack_skills["Melee"])
        attack.update(self.attack_skills["Magic"] if not None else {})
        return [skill(stats) for skill, stats in attack.items()]

    # receiving attack
    # normal damage
    @property
    def armour_modifier(self):
        return 1 / (math.pow(0.02 * self.armour, 2) + 1)

    def receive_normal_damage(self, damage):
        actual_damage = damage * self.armour_modifier
        self.hp -= actual_damage
        return actual_damage

    # magic damage
    @property
    def magic_resistance(self):
        return 1 - self.resistance

    def receive_magic_damage(self, damage):
        actual_damage = damage * self.magic_resistance
        self.hp -= actual_damage
        return actual_damage

    # working on attack
    def receive_damage(self, damage, damage_type):
        received_damage = self.defences[damage_type](damage)
        return received_damage, damage_type

    def receive_attack(self, attack_skills):
        attack_result = {}
        for attack in attack_skills:
            received_damage, damage_type = self.receive_damage(*attack.get_damage())
            attack_result[attack] = (received_damage, damage_type)
        return attack_result

    # attack response
    def heal(self, amount):
        self.hp += amount
        print("{} healed for {}".format(self.name, amount))

    def attack_response(self, attack_result):
        on_hit_effects = {"Heal": self.heal}
        for attack in attack_result:
            damage, damage_type = attack_result[attack]
            on_hit_effect = attack.get_on_hit_effect()
            if on_hit_effect is not None:
                effect, amount = on_hit_effect
                on_hit_effects[effect](amount * damage)
            print("{} made {} {} damage with {}".format(self.name, damage, damage_type, attack.get_name()))

    # adding skills
    def add_skill(self, skill):
        if skill.skill_type() == "Magic":
            self.attack_skills["Magic"].update({skill: self.get_modifiers(skill.skill_modifiers())})
        else:
            print("Wrong skill type")

    def get_modifiers(self, modifiers):
        all_modifiers = {"MELEE_DAMAGE": self.melee_damage, "MELEE_ATTACK": self.full_melee_attack,
                         "MAGIC_DAMAGE": self.magic_damage, "MAGIC_POWER": self.magic_power,
                         "CRITICAL_CHANCE": self.full_critical_chance,
                         "CRITICAL_MULTIPLIER": self.full_critical_multiplier,
                         "LIFE_STEAL": self.life_steal_percent,
                         "CURRENT_HP": self.hp, "MAX_HP": self.max_hp,
                         "MELEE_DEFENSE": self.armour}
        return {modifier: all_modifiers[modifier] for modifier in modifiers}


class GreaterChar(Char):
    def __init__(self):
        super().__init__()
        self.hp = 1000
        self.name = "GreaterChar"
