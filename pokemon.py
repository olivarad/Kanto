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


    def getPokedexEntry(self, name):
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
    
    def calcStats(self, pokedexEntry):
        self.attackStat = self.calcStat(pokedexEntry["base stats"]["Attack"], self.attackIV, self.attackEV, self.level)
        self.defenseStat = self.calcStat(pokedexEntry["base stats"]["Defense"], self.defenseIV, self.defenseEV, self.level)
        self.speedStat = self.calcStat(pokedexEntry["base stats"]["Speed"], self.speedIV, self.speedEV, self.level)
        self.specialAttackStat = self.calcStat(pokedexEntry["base stats"]["Sp. Attack"], self.specialIV, self.specialEV, self.level)
        self.specialDefenseStat = self.calcStat(pokedexEntry["base stats"]["Sp. Defense"], self.specialIV, self.specialEV, self.level)
        self.maxHealthStat = self.calcMaxHealth(pokedexEntry["base stats"]["HP"], self.healthIV, self.healthEV, self.level)
    
    def getMovesByLevel(self, pokedexEntry, level):
        self.possibleLevelMoves = pokedexEntry["moves"]["level"]
        self.levelMoves = []

        for moveLevel, move in self.possibleLevelMoves.items():
            if int(moveLevel) <= level:
                if isinstance(move, list):
                    self.levelMoves.extend(move)
                else:
                    self.levelMoves.append(move)

    def initMoves(self):
        self.moves = []
        if len(self.levelMoves) <= 4:
            self.moves = list(self.levelMoves)
        else:
            for i in range(4):
                self.moves.append(self.levelMoves[-4 + i])
            
    
    def calcStat(self, base, IV, EV, level):
        return floor(((base + IV) * 2 + floor(ceil(sqrt(EV))/4) * level) / 100) + 5
    
    def calcMaxHealth(self, base, IV, EV, level):
        return floor(((base + IV) * 2 + floor(ceil(sqrt(EV))/4) * level) / 100) + level + 10
    
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