import json
from random import randint
from math import sqrt, floor, ceil

class Pokemon:
    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level
        self.calcIVs()
        self.initEVs()
        self.getPokedexEntry(name)
        self.calcStats(self.pokedexEntry)
        self.currentHealthStat = self.maxHealthStat
        self.getMovesByLevel(self.pokedexEntry, level)
        self.initMoves()

    """
    Obtain a pokedex entry from pokedex.json

    Args:
        name (string): the name of the pokedex entry
    """
    def getPokedexEntry(self, name: str):
        with open("pokedex.json", "r") as file:
            data = json.load(file)
            self.pokedexEntry = data[name]
        
    def calcIVs(self):
        self.attackIV = randint(0, 15)
        self.defenseIV = randint(0, 15)
        self.speedIV = randint(0, 15)
        self.specialIV = randint(0, 15)
        self.healthIV = 0
        self.healthIV += 8 if self.attackIV % 2 == 1 else 0
        self.healthIV += 4 if self.defenseIV % 2 == 1 else 0
        self.healthIV += 2 if self.speedIV % 2 == 1 else 0
        self.healthIV += 1 if self.specialIV % 2 == 1 else 0
    
    def initEVs(self):
        self.attackEV = 0
        self.defenseEV = 0
        self.speedEV = 0
        self.specialEV = 0
        self.healthEV = 0
    
    """
    Calculation of generation 1 pokemon based stats using a pokedex entry and the genration one pokemon stat calculation helper functions named calcStat and calcMaxHealth
    
    Args:
        pokedexEntry (Loaded in json data): data pertaining to the pokemon being processed
    """
    def calcStats(self, pokedexEntry):
        self.attackStat = self.calcStat(pokedexEntry["base stats"]["Attack"], self.attackIV, self.attackEV, self.level)
        self.defenseStat = self.calcStat(pokedexEntry["base stats"]["Defense"], self.defenseIV, self.defenseEV, self.level)
        self.speedStat = self.calcStat(pokedexEntry["base stats"]["Speed"], self.speedIV, self.speedEV, self.level)
        self.specialAttackStat = self.calcStat(pokedexEntry["base stats"]["Sp. Attack"], self.specialIV, self.specialEV, self.level)
        self.specialDefenseStat = self.calcStat(pokedexEntry["base stats"]["Sp. Defense"], self.specialIV, self.specialEV, self.level)
        self.maxHealthStat = self.calcMaxHealth(pokedexEntry["base stats"]["HP"], self.healthIV, self.healthEV, self.level)
    
    """
    Fills information for every possible level move for the pokemon and the current ones it would have had access to by now

    Args:
        pokedexEntry (Loaded in json data): data pertaining to the pokemon being processed
        level (int): the current level of the pokemon being processed
    """
    def getMovesByLevel(self, pokedexEntry, level: int):
        self.possibleLevelMoves = pokedexEntry["moves"]["level"]
        self.levelMoves = []

        for moveLevel, move in self.possibleLevelMoves.items():
            if int(moveLevel) <= level:
                if isinstance(move, list):
                    self.levelMoves.extend(move)
                else:
                    self.levelMoves.append(move)

    """
    A pokemon will be initialized with the last 4 possible level moves it would have attained through natural leveling
    If 4 moves are not available, the pokemon will have acces to the available moves at that time
    """
    def initMoves(self):
        self.moves = []
        if len(self.levelMoves) <= 4:
            self.moves = list(self.levelMoves)
        else:
            for i in range(4):
                self.moves.append(self.levelMoves[-4 + i])
            
    """
    Generation one general stat calculation helper function

    Args:
        base (int): the base stat pokedex entry for the pokemon being processed
        IV (int): the Individual Value for the stat of the pokemon being processed
        EV (int): the Effort Value for the stat of the pokemon being processed
        level (int): the current level of the pokemon being processed
    """
    def calcStat(self, base: int, IV: int, EV: int, level: int):
        return floor(((base + IV) * 2 + floor(ceil(sqrt(EV))/4) * level) / 100) + 5
    
    """
    Generation one health stat calculation helper function

    Args:
        base (int): the base stat pokedex entry for the pokemon being processed
        IV (int): the Individual Value for the stat of the pokemon being processed
        EV (int): the Effort Value for the stat of the pokemon being processed
        level (int): the current level of the pokemon being processed
    """
    def calcMaxHealth(self, base: int, IV: int, EV: int, level: int):
        return floor(((base + IV) * 2 + floor(ceil(sqrt(EV))/4) * level) / 100) + level + 10
    
    """
    Load the pokemon class member data into a TOML save file
    The data is loaded but not saved

    Args:
        slot (A section of a TOML file contiaining the slot (PC or Party) for the pokemon)
    """
    def loadPokemonTOML(self, slot):
        slot["name"] = self.name
        slot["primary"] = self.pokedexEntry["primary"]
        slot["secondary"] = self.pokedexEntry["secondary"]
        slot["level"] = self.level
        slot["moves"] = self.moves
        slot["HealthIV"] = self.healthIV
        slot["AttackIV"] = self.attackIV
        slot["DefenseIV"] = self.defenseIV
        slot["SpecialIV"] = self.specialIV
        slot["SpeedIV"] = self.speedIV
        slot["HealthEV"] = self.healthEV
        slot["AttackEV"] = self.attackEV
        slot["DefenseEV"] = self.defenseEV
        slot["SpecialEV"] = self.specialEV
        slot["SpeedEV"] = self.speedEV
        slot["maxHP"] = self.maxHealthStat
        slot["currentHP"] = self.currentHealthStat
        slot["Attack"] = self.attackStat
        slot["Defense"] = self.defenseStat
        slot["Sp. Attack"] = self.specialAttackStat
        slot["Sp. Defense"] = self.specialDefenseStat
        slot["Speed"] = self.speedStat