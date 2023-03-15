from enum import Enum
import random, re

dmg_regex = r"(\d)d(\d+)(?:\+(\d+))?"

class RollResult(Enum):
    CRITICAL_SUCCESS = 'CRITICAL_SUCCESS'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    CRITICAL_FAILURE = 'CRITICAL_FAILURE'

def roll_check(modifier, dc):
    roll = random.randint(1, 20)
    if roll + modifier > dc + 10:
        return RollResult.CRITICAL_SUCCESS
    elif roll + modifier > dc:
        return RollResult.SUCCESS
    elif roll + modifier < dc - 10:
        return RollResult.CRITICAL_FAILURE
    else:
        return RollResult.FAILURE
    
def roll_dice(dice):
    matches = re.search(dmg_regex, dice)
    number_of_die = int(matches.group(1))
    die_size = int(matches.group(2))
    modifier = matches.group(3)
    result = int(modifier) if modifier else 0
    for i in range(0, number_of_die):
        result += random.randint(1, die_size)
    print("Roll {}, Result: {}".format(dice, result))
    return result