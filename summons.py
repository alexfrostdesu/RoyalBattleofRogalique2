import math

from utils import SkillCooldown
from skills import BasicAttack, MagicMissile, DoubleShot, CriticalStrike


class Summon:
    BASE_STATS = {'hp': 100,
                  'attack': 10,
                  'armour': 1,
                  'arcane': 1}

    CLASS_LIBRARY = {
        'F': ('Fighter', {'hp': 1.5,
                          'attack': 1,
                          'armour': 1.5,
                          'arcane': 0.5,
                          'attack_type': 'melee',
                          'skills': []
                          }),

        'S': ('Shooter', {'hp': 1,
                          'attack': 1.5,
                          'armour': 1.5,
                          'arcane': 0.5,
                          'attack_type': 'ranged',
                          'skills': [(DoubleShot, 4), ]
                          }),

        'C': ('Caster', {'hp': 1,
                         'attack': 1,
                         'armour': 1,
                         'arcane': 1,
                         'attack_type': 'ranged',
                         'skills': [(MagicMissile, 5), ]
                         }),

        'A': ('Assassin', {'hp': 1,
                           'attack': 1.5,
                           'armour': 1,
                           'arcane': 0.75,
                           'attack_type': 'melee',
                           'skills': [(CriticalStrike, 3)]
                           })
    }

    RACE_LIBRARY = {
        'H': ('Human', {'Fighter': 1.5,
                        'Shooter': 1,
                        'Caster': 1,
                        'Assassin': 1}),

        'E': ('Elf', {'Fighter': 0.5,
                      'Shooter': 1.5,
                      'Caster': 0.75,
                      'Assassin': 1.5}),

        'O': ('Orc', {'Fighter': 1.5,
                      'Shooter': 1.5,
                      'Caster': 0.5,
                      'Assassin': 0.5}),

        'U': ('Undead', {'Fighter': 1,
                         'Shooter': 1,
                         'Caster': 1.5,
                         'Assassin': 0.5}),

        'L': ('Lizard', {'Fighter': 0.75,
                         'Shooter': 0.5,
                         'Caster': 1.5,
                         'Assassin': 1.5})
    }

    def __init__(self, cls, **kwargs):
        class_code, race_code, = cls

        self.DAMAGE_LIBRARY = {'physical': self.take_physical_damage,
                               'magical': self.take_magical_damage,
                               'pure': self.take_pure_damage}

        self.SKILLS_LIBRARY = {'modifier': {},
                               'attack': {},
                               'defense': {}}

        self.cls, class_mods = self.select_class(class_code)
        self.race, race_mods = self.select_race(race_code)
        self.level = 1
        self.grade = 0
        self.attack_type = class_mods['attack_type']

        if kwargs.get('lvl'):
            char_stats = self.level_up(self.BASE_STATS, kwargs['lvl'])
        else:
            char_stats = self.BASE_STATS

        if kwargs.get('grade'):
            char_stats = self.upgrade(char_stats, kwargs['grade'])

        char_stats = {stat: value * race_mods[self.cls] * class_mods[stat] for
                      stat, value in char_stats.items()}

        self.max_hp = char_stats['hp']
        self.attack_damage = char_stats['attack']
        self.armour = char_stats['armour']
        self.arcane = char_stats['arcane']

        if kwargs.get('hp'):
            self.current_hp = kwargs['hp']
        else:
            self.current_hp = self.max_hp

        if kwargs.get('exp'):
            self.current_exp = kwargs['exp']
        else:
            self.current_exp = 0

        self.basic_attack = {"attack": BasicAttack}

        self.skills = []
        if class_mods.get('skills'):
            for skill in class_mods.get('skills'):
                self.add_skill(*skill)

    def __str__(self):
        return f"{self.cls} {self.race} {self.level}+{self.grade}"

    def select_class(self, cls_code):
        return self.CLASS_LIBRARY[cls_code]

    def select_race(self, race_code):
        return self.RACE_LIBRARY[race_code]

    def level_up(self, stats, lvl):
        for i in range(lvl):
            self.level += 1
            stats['hp'] += 10
            stats['attack'] += 1
            stats['arcane'] += 0.5
            stats['armour'] += 0.1
        return stats

    def upgrade(self, stats, grade):
        for i in range(grade):
            self.grade += 1
            stats['hp'] *= 1.1
            stats['attack'] *= 1.2
            stats['arcane'] *= 1.1
            stats['armour'] *= 1.05
        return stats

    def add_skill(self, skill, cooldown):
        self.SKILLS_LIBRARY[skill.skill_type][skill] = SkillCooldown(cooldown)

    def skill_available(self, skill):
        """
        Check if skill is available to use
        """
        return self.SKILLS_LIBRARY[skill.skill_type][skill].check_cooldown()

    def select_attacks(self):
        attacks = []
        for skill in self.SKILLS_LIBRARY['attack']:
            if self.skill_available(skill):
                attacks.append(skill(skill_user=self))
        # if no available skill was found, add basic attack
        if not attacks:
            attacks.append(self.get_basic_attack())
        return attacks

    def use_modifiers(self, attacks):
        for modifier in self.SKILLS_LIBRARY['modifier']:
            if self.skill_available(modifier):
                modifier(skill_user=self).modify_skills(attacks=attacks)

    # Attacking and receiving damage

    def take_damage(self, damage):
        self.current_hp -= damage

    def take_physical_damage(self, damage):
        damage = damage * (4 / 3 + math.sqrt(self.armour / 2))
        self.take_damage(damage)
        return damage

    def take_magical_damage(self, damage):
        # TODO: magical damage
        self.take_damage(damage)
        return damage

    def take_pure_damage(self, damage):
        self.take_damage(damage)
        return damage

    def receive_attack(self, attack):
        damage_mechanism = self.DAMAGE_LIBRARY[attack.damage_type]
        attack.store_damage(damage_mechanism(attack.damage))

    def get_basic_attack(self):
        basic_attack = self.basic_attack['attack'](skill_user=self)
        return basic_attack

    def attack_target(self, target):
        attacks = self.select_attacks()
        self.use_modifiers(attacks)
        for attack in attacks:
            attack.set_target(target)
        return attacks

    # Healing

    def heal(self, heal):
        if self.current_hp + heal <= self.max_hp:
            self.current_hp += heal
        else:
            self.current_hp = self.max_hp

    @property
    def is_alive(self):
        return self.current_hp > 0

    # misc

    @property
    def current_status(self):
        """
        Returns hp in printable format
        """
        return f"{self} Current HP: {self.current_hp}/{self.max_hp}"
