import random


class AttackSkill:
    def __init__(self, modifiers, damage_type, name):
        self.modifiers = modifiers
        self.damage_type = damage_type
        self.name = name

    def __repr__(self):
        return "{}: {}".format(self.name, self.modifiers)

    @staticmethod
    def skill_modifiers():
        """
        You absolutely need to write this for each skill differently
        Should return iterable of skill modifiers
        """
        return None,

    @staticmethod
    def skill_type():
        """
        You absolutely need to write this for each skill differently
        Should return type of skill
        """
        return None

    def get_damage(self):
        """
        You absolutely need to write this for each skill differently
        Should return damage and damage_type
        """
        return 0, "Normal"

    def get_name(self):
        return self.name

    def get_on_hit_effect(self):
        return None


class MeleeAttack(AttackSkill):
    def __init__(self, modifiers):
        name = "Melee Attack"
        damage_type = "Normal"
        super().__init__(modifiers, damage_type, name)

    @staticmethod
    def skill_modifiers():
        return "MELEE_ATTACK",

    @staticmethod
    def skill_type():
        return "Melee"

    def get_damage(self):
        return self.modifiers["MELEE_ATTACK"]() * random.uniform(0.95, 1.05), self.damage_type


class CriticalAttack(AttackSkill):
    def __init__(self, modifiers):
        name = "Melee Attack"
        damage_type = "Normal"
        super().__init__(modifiers, damage_type, name)

    @staticmethod
    def skill_modifiers():
        return "MELEE_ATTACK", "CRITICAL_CHANCE"

    @staticmethod
    def skill_type():
        return "Melee"

    def get_damage(self):
        if random.random() <= self.modifiers["CRITICAL_CHANCE"]():
            return self.modifiers["MELEE_ATTACK"]() * random.uniform(0.95, 1.05), self.damage_type
        else:
            return self.modifiers["MELEE_ATTACK"]() * 2 * random.uniform(0.95, 1.05), "Critical"


class LifeStealAttack(AttackSkill):
    def __init__(self, modifiers):
        name = "Melee Attack"
        damage_type = "Normal"
        super().__init__(modifiers, damage_type, name)

    @staticmethod
    def skill_modifiers():
        return "MELEE_ATTACK",

    @staticmethod
    def skill_type():
        return "Melee"

    def get_damage(self):
        return self.modifiers["MELEE_ATTACK"]() * random.uniform(0.95, 1.05), self.damage_type

    def get_on_hit_effect(self):
        return "Heal", 0.2


class MagicFireball(AttackSkill):
    def __init__(self, modifiers):
        name = "Fireball"
        damage_type = "Magic"
        super().__init__(modifiers, damage_type, name)

    @staticmethod
    def skill_modifiers():
        return "MAGIC_POWER",

    @staticmethod
    def skill_type():
        return "Magic"

    def get_damage(self):
        return self.modifiers["MAGIC_POWER"]() * 5, self.damage_type


class MagicLightningBolt(AttackSkill):
    def __init__(self, modifiers):
        name = "Lightning Bolt"
        damage_type = "Magic"
        super().__init__(modifiers, damage_type, name)

    @staticmethod
    def skill_modifiers():
        return "MAGIC_POWER",

    @staticmethod
    def skill_type():
        return "Magic"

    def get_damage(self):
        return self.modifiers["MAGIC_POWER"]() * 5 * random.uniform(0.8, 1.2), self.damage_type
