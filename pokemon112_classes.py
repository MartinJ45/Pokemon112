import random

class Pokemon:
    def __init__(self, name, level):
        # self.data = dict()
        self.name = name
        self.nickName = name.upper()
        self.level = level
        self.experience = level ** 3
        self.moves = []
        self.statsData = Pokemon.readData('pokemonData.txt', self.name)
        self.movesData = Pokemon.readData('movesetData.txt', self.name)
        self.updateStats()
        self.currentHP = self.hp
    def __repr__(self):
        return (f"Name:{self.name} | Level:{self.level} | Current HP:{self.currentHP} | Moves:{self.moves} | "
                f"HP:{self.hp} | Atk:{self.attack} | Def:{self.defense} | SpAtk:{self.specialAttack} | "
                f"SpDef:{self.specialDefense} | Spd:{self.speed}")
    def updateStats(self):
        self.type1 = self.statsData[1]
        self.type2 = self.statsData[2]
        self.hp = Pokemon.updateHP(int(self.statsData[4]), self.level)
        self.attack = Pokemon.updateStat(int(self.statsData[5]), self.level)
        self.defense = Pokemon.updateStat(int(self.statsData[6]), self.level)
        self.specialAttack = Pokemon.updateStat(int(self.statsData[7]), self.level)
        self.specialDefense = Pokemon.updateStat(int(self.statsData[8]), self.level)
        self.speed = Pokemon.updateStat(int(self.statsData[9]), self.level)
    def updateMoves(self):
        for i in range(len(self.movesData)):
            elem = self.movesData[i]
            if elem.isdigit() and int(elem) <= self.level:
                self.moves.append(self.movesData[i+1])
                if len(self.moves) > 4:
                    self.moves.pop(0)
    def attackPokemon(self, otherPokemon, move):
        moveData = Pokemon.readData('moveData.txt', move)
        moveName = moveData[0]
        moveType = moveData[1]
        category = moveData[2]

        if category != 'Status':
            power = moveData[3]
            if power.isdigit():
                power = int(power)
            else:
                power = 0
            level = self.level
            attack = self.attack if category == 'Physical' else self.specialAttack
            defense = otherPokemon.defense if category == 'Physical' else otherPokemon.specialDefense
            burn = 1
            screen = 1
            critical = 2 if random.randint(1, 16) == 16 else 1
            stab = 1.5 if moveType in (self.type1, self.type2) else 1
            type1Eff = Pokemon.getTypeEffectiveness(moveType, otherPokemon.type1)
            if otherPokemon.type2:
                type2Eff = Pokemon.getTypeEffectiveness(moveType, otherPokemon.type2)
            else:
                type2Eff = 1
            rand = random.randint(85,100) / 100
            damage = ((((2 * level) / 5 + 2) * power * (attack / defense) / 50) * burn * screen + 2) * critical * stab * type1Eff * type2Eff * rand
            damage = int(round(damage))

            if damage > otherPokemon.currentHP:
                damage = otherPokemon.currentHP
                otherPokemon.currentHP -= damage
            else:
                otherPokemon.currentHP -= damage

            return f"{self.name} used {moveName} and did {damage}HP to {otherPokemon.name}"
        return f"{self.name} used {moveName} on {otherPokemon.name}"
    @staticmethod
    def getTypeEffectiveness(type1, type2):
        typeChartIndex = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground',
                          'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel']
        typeChart = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, .5, 0, 1, 1, .5], # normal
                     [1, .5, .5, 2, 1, 2, 1, 1, 1, 1, 1, 2, .5, 1, .5, 1, 2], # fire
                     [1, 2, .5, .5, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, .5, 1, 1], # water
                     [1, .5, 2, .5, 1, 1, 1, .5, 2, .5, 1, .5, 2, 1, .5, 1, .5], # grass
                     [1, 1, 2, .5, .5, 1, 1, 1, 0, 2, 1, 1, 1, 1, .5, 1, 1], # electric
                     [1, .5, .5, 2, 1, .5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, .5], # ice
                     [2, 1, 1, 1, 1, 2, 1, .5, 1, .5, .5, .5, 2, 0, 1, 2, 2], # fighting
                     [1, 1, 1, 2, 1, 1, 1, .5, .5, 1, 1, 1, .5, .5, 1, 1, 0], # poison
                     [1, 2, 1, .5, 2, 1, 1, 2, 1, 0, 1, .5, 2, 1, 1, 1, 2], # ground
                     [1, 1, 1, 2, .5, 1, 2, 1, 1, 1, 1, 2, .5, 1, 1, 1, .5], # flying
                     [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, .5, 1, 1, 1, 1, 0, .5], # psychic
                     [1, .5, 1, 2, 1, 1, .5, .5, 1, .5, 2, 1, 1, .5, 1, 2, .5], # bug
                     [1, 2, 1, 1, 1, 2, .5, 1, .5, 2, 1, 2, 1, 1, 1, 1, .5], # rock
                     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, .5, 1], # ghost
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, .5], # dragon
                     [1, 1, 1, 1, 1, 1, .5, 1, 1, 1, 2, 1, 1, 2, 1, .5, 1], # dark
                     [0, .5, .5, 1, .5, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, .5]] # steel
        type1Index = typeChartIndex.index(type1)
        type2Index = typeChartIndex.index(type2)
        return typeChart[type1Index][type2Index]
    @staticmethod
    def updateHP(baseHP, level):
        iv = ev = 0
        hp = (((2 * baseHP + iv + (ev/4)) * level) / 100) + level + 10
        hp = int(round(hp))
        return hp
    @staticmethod
    def updateStat(baseStat, level):
        iv = ev = 0
        nature = 1
        stat = ((((2 * baseStat + iv + (ev / 4)) * level) / 100) + 5) * nature
        stat = int(round(stat))
        return stat
    @staticmethod
    def readData(fileName, name):
        with open('Pokemon112/' + fileName, encoding='utf-8') as f:
            fileString = f.read()
            fileList = fileString.splitlines()
            fileList.pop(0)
            for line in fileList:
                lineData = line.split(',')
                if lineData[0] == name:
                    return lineData

class Trainer:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0
        self.party = []
        self.items = []
    def addToParty(self, pokemon):
        if len(self.party) < 6:
            self.party.append(pokemon)
            return f'Added {pokemon} to party!'
        return None
    def removeFromParty(self, pokemon):
        if len(self.party) > 0:
            self.party.remove(pokemon)
            return f'Removed {pokemon} from party!'
        return None
