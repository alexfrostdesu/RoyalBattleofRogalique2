from characters import *
from skills import *

character_basic = Char()
print(character_basic)
character_greater = GreaterChar()
print(character_greater)

attack_response = character_greater.receive_attack(character_basic.attack())
character_basic.attack_response(attack_response)


character_basic.melee_damage = 40


# character_basic.add_skill(MagicFireball)
# character_basic.add_skill(MagicLightningBolt)
character_basic.melee_skill = "critical"
character_basic.critical_chance = 0.2
character_basic.refresh_melee_skill()

for i in range(5):
    attack_response = character_greater.receive_attack(character_basic.attack())
    character_basic.attack_response(attack_response)

print(character_greater)
print(character_basic)
