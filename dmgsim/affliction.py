from roll import RollResult, roll_check, roll_dice

afflictions = {
    "potent curare": {
        "dc": 30,
        "duration": 6,
        "stages": {
            1: "3d6",
            2: "4d6",
            3: "5d6",
            4: "death"
        },
        "virulent": False
    },
    "giant scorpion venom": {
        "dc": 18,
        "duration": 6,
        "stages": {
            1: "1d10",
            2: "2d10",
            3: "2d10",
        },
        "virulent": False
    },
}

class Affliction:
    def __init__(self, initial_stage, affliction, time_passed = 0):
        self.affliction = affliction
        self.duration = time_passed
        self.stage = min(initial_stage, len(affliction["stages"]))
        self.virulent_attempt = False

    def isCured(self):
        return self.stage <= 0 or self.duration >= self.affliction["duration"]

    def isDeath(self):
        return self.affliction["stages"][self.stage] == "death"

    def getDuration(self):
        return self.duration
    
    def getDamage(self):
        if self.isCured():
            return 0
        stage_dmg = self.affliction["stages"][self.stage]
        return roll_dice(stage_dmg)
    
    def rollStage(self, modifier):
        self.duration += 1
        if self.duration >= self.affliction["duration"]:
            return
        result = roll_check(modifier, self.affliction["dc"])
        self.stage += self.__determine_stage_change(result)
        if self.stage <= 0:
            self.stage = 0
        else:
            self.stage = min(self.stage, len(self.affliction["stages"]))
        return result
    
    def __determine_stage_change(self, result):
        if self.affliction["virulent"]:
            if result is RollResult.CRITICAL_SUCCESS:
                return -2
            elif result is RollResult.SUCCESS:
                if self.virulent_attempt:
                    self.virulent_attempt = False
                    return -1
                else:
                    self.virulent_attempt = True
                    return 0
            elif result is RollResult.FAILURE:
                self.virulent_attempt = False
                return 1
            else:
                self.virulent_attempt = False
                return 2
        else:
            if result is RollResult.CRITICAL_SUCCESS:
                return -2
            elif result is RollResult.SUCCESS:
                return -1
            elif result is RollResult.FAILURE:
                return 1
            else:
                return 2

def calc_affliction(modifier, affliction):
    initial_save = roll_check(modifier, affliction["dc"])
    if initial_save is RollResult.CRITICAL_FAILURE:
        initial_stage = 2
    elif initial_save is RollResult.FAILURE:
        initial_stage = 1
    else:
        # print("Success on initial save.")
        return [0, False]
    affliction = Affliction(initial_stage, affliction)
    dmg = affliction.getDamage()
    total_dmg = dmg

    while not affliction.isCured():
        affliction.rollStage(modifier)
        if affliction.isCured():
            # print("Affliction is cured after {} rounds. Total damage: {}".format(affliction.getDuration(), total_dmg))
            return [total_dmg, False]
        if affliction.isDeath():
            # print("Victim died after {} rounds.".format(affliction.getDuration()))
            return [total_dmg, True]
        dmg = affliction.getDamage()
        total_dmg += dmg