from statistics import mean

from affliction import Affliction, afflictions
from roll import RollResult, roll_check, roll_dice

deaths = 0

samples = 10000
for i in range(samples):
    affliction = Affliction(2, afflictions["giant scorpion venom"], 4)
    hp = 0
    healing_potion = roll_dice("1d8")
    hp += healing_potion
    fort_modifier = 7
    treat_poison = roll_check(4, 18)
    if treat_poison is RollResult.CRITICAL_SUCCESS:
        fort_modifier += 4
    elif treat_poison is RollResult.SUCCESS:
        fort_modifier += 2
    elif treat_poison is RollResult.CRITICAL_FAILURE:
        fort_modifier -= 2
    poison_check = affliction.rollStage(fort_modifier)
    dmg = affliction.getDamage()
    if dmg >= hp:
        print("Himar died. HP gained: {}, Treat Poison Check: {}, Poison Check: {}, Damage: {}".format(healing_potion, treat_poison, poison_check, dmg))
        deaths += 1
    else:
        print("Himar survived. HP gained: {}, Treat Poison Check: {}, Poison Check: {}, Damage: {}".format(healing_potion, treat_poison, poison_check, dmg))

    
print("Deaths: {} {} %".format(deaths, deaths / samples * 100))