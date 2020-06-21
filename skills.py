from copy import copy


class Attack:
    skill_type = 'attack'

    def __init__(self, skill_user, damage_type, name):
        self.damage_type = damage_type
        self.skill_user = skill_user
        self.target = None
        self.damage = None
        self.name = name
        self.resulting_damage = None

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
        return f"{self.skill_user} dealt {self.resulting_damage} to {self.target} with {self.name}"  # noqa


class BasicAttack(Attack):
    def __init__(self, **kwargs):
        kwargs['damage_type'] = 'physical'
        kwargs['name'] = "Basic Attack"
        super().__init__(**kwargs)
        self.damage = self.skill_user.attack_damage


class MagicMissile(Attack):
    def __init__(self, **kwargs):
        kwargs['damage_type'] = 'magical'
        kwargs['name'] = "Magic Missile"
        super().__init__(**kwargs)
        self.damage = self.skill_user.arcane * 20


class Modifier:
    skill_type = 'modifier'

    def __init__(self, skill_user, name):
        self.skill_user = skill_user
        self.target = None
        self.name = name

    def modify_skills(self, attacks):
        """
        This needs to be changed for each skill
        """
        return attacks


class DoubleShot(Modifier):
    def __init__(self, **kwargs):
        kwargs['name'] = "Double Shot"
        super().__init__(**kwargs)

    def modify_skills(self, attacks):
        for attack in attacks:
            if attack.damage_type == 'physical':
                new_attack = copy(attack)
                new_attack.name = self.name
                attacks.append(new_attack)
                break


class CriticalStrike(Modifier):
    def __init__(self, **kwargs):
        kwargs['name'] = "Critical Strike"
        super().__init__(**kwargs)

    def modify_skills(self, attacks):
        for attack in attacks:
            if attack.damage_type == 'physical':
                attack.damage = attack.damage * 2
                attack.name = self.name
                break

