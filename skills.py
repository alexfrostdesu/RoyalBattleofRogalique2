class GenericSkill:
    def __init__(self, type_, attacker, name, modifiers=None):
        self.type_ = type_
        self.modifiers = modifiers
        self.attacker = attacker
        self.target = None
        self.name = name
        self.resulting_damage = None

    @property
    def damage_type(self):
        return self.type_

    @property
    def damage(self):
        """
        This needs to be changed for each skill
        """
        return None

    def set_target(self, target):
        if self.target is None:
            self.target = target

    def store_damage(self, resulting_damage):
        if self.resulting_damage is None:
            self.resulting_damage = resulting_damage

    def return_damage(self):
        """
        Returns damage in printable format
        """
        return f"{self.attacker} dealt {self.resulting_damage} to {self.target} with {self.name}"  # noqa


class Attack(GenericSkill):
    def __init__(self, **kwargs):
        kwargs['type_'] = 'physical'
        kwargs['name'] = "Basic Attack"
        super().__init__(**kwargs)

    @property
    def damage(self):
        return self.attacker.attack_damage


class MagicMissile(GenericSkill):
    def __init__(self, **kwargs):
        kwargs['type_'] = 'magical'
        kwargs['name'] = "Magic Missile"
        super().__init__(**kwargs)

    @property
    def damage(self):
        return self.attacker.arcane * 20