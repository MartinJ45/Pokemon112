import random

class Pokemon:
    def __init__(self, name, level, sprites=None):
        # self.data = dict()
        self.name = name
        self.nickName = name.upper()
        self.level = level
        self.experience = level ** 3
        self.moves = []
        self.moveTypes = []
        self.moveCategories = []
        self.movePowers = []
        self.moveAccuracies = []
        self.currentMovePP = []
        self.maxMovePP = []
        self.statsData = Pokemon.readData('pokemonData.txt', self.name)
        self.movesData = Pokemon.readData('movesetData.txt', self.name)
        self.updateStats()
        self.currentHP = self.hp
        if sprites:
            self.frontSprite, self.backSprite = sprites[self.ID]
    def __repr__(self):
        return (f"Name:{self.name} | Level:{self.level} | Current HP:{self.currentHP} | Moves:{self.moves} | "
                f"HP:{self.hp} | Atk:{self.attack} | Def:{self.defense} | SpAtk:{self.specialAttack} | "
                f"SpDef:{self.specialDefense} | Spd:{self.speed}")
    def __eq__(self, other):
        return str(self) == str(other)
    def clone(self):
        clonePokemon = Pokemon(self.name, self.level)
        clonePokemon.updateStats()
        clonePokemon.updateMoves()
        clonePokemon.currentHP = self.currentHP
        return clonePokemon
    def updateStats(self):
        self.ID = int(self.statsData[1])
        self.type1 = self.statsData[2]
        self.type2 = self.statsData[3]
        self.hp = Pokemon.updateHP(int(self.statsData[5]), self.level)
        self.attack = Pokemon.updateStat(int(self.statsData[6]), self.level)
        self.defense = Pokemon.updateStat(int(self.statsData[7]), self.level)
        self.specialAttack = Pokemon.updateStat(int(self.statsData[8]), self.level)
        self.specialDefense = Pokemon.updateStat(int(self.statsData[9]), self.level)
        self.speed = Pokemon.updateStat(int(self.statsData[10]), self.level)
    def updateMoves(self):
        for i in range(len(self.movesData)):
            elem = self.movesData[i]
            if elem.isdigit() and int(elem) <= self.level:
                moveData = Pokemon.readData('moveData.txt', self.movesData[i+1])
                if not moveData:
                    raise Exception(f'{self.movesData[i+1]} not found in moveData.txt')
                self.moves.append(moveData[0])
                self.moveTypes.append(moveData[1])
                self.moveCategories.append(moveData[2])
                self.movePowers.append(moveData[3])
                acc = int(moveData[4]) if moveData[4].isdigit() else moveData[4]
                self.moveAccuracies.append(acc)
                self.currentMovePP.append(int(moveData[5]))
                self.maxMovePP.append(int(moveData[5]))
                if len(self.moves) > 4:
                    self.moves.pop(0)
                    self.moveTypes.pop(0)
                    self.moveCategories.pop(0)
                    self.movePowers.pop(0)
                    self.moveAccuracies.pop(0)
                    self.currentMovePP.pop(0)
                    self.maxMovePP.pop(0)
    def attackPokemon(self, otherPokemon, move):
        moveIndex = self.moves.index(move)
        self.currentMovePP[moveIndex] -= 1

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

            return damage
            # return f"{self.name} used {moveName} and did {damage}HP to {otherPokemon.name}"
        return 0
        # return f"{self.name} used {moveName} on {otherPokemon.name}"
    def gainExperience(self, defeatedPokemon):
        baseStatTotal = (defeatedPokemon.hp + defeatedPokemon.attack + defeatedPokemon.specialAttack +
                         defeatedPokemon.defense + defeatedPokemon.specialDefense + defeatedPokemon.speed)
        expGain = (baseStatTotal * defeatedPokemon.level) / 2
        self.experience += expGain
        if self.experience > (self.level + 1) ** 3:
            self.levelUp()
    def levelUp(self):
        self.level += 1
        missingHP = self.hp - self.currentHP
        self.updateStats()
        # self.updateMoves()
        self.currentHP = self.hp - missingHP
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
    def __init__(self, name, spriteSheet=None, x=0, y=0):
        self.name = name
        self.spriteSheet = spriteSheet
        self.spriteCount = 0
        if spriteSheet:
            self.frontSprites = [spriteSheet[0], spriteSheet[3], spriteSheet[0]]
            self.backSprites = [spriteSheet[1], spriteSheet[4], spriteSheet[1]]
            self.sideSprites = [spriteSheet[2], spriteSheet[5], spriteSheet[2]]
        self.facing = 'front'
        self.isMoving = False
        self.x = x
        self.y = y
        self.party = []
        self.items = dict()
        self.defeated = False
    def getSprite(self):
        if self.isMoving:
            self.spriteCount += 1
            if self.spriteCount == 3:
                self.spriteCount = 0
        else:
            self.spriteCount = 0
        if self.facing == 'front':
            return self.frontSprites[self.spriteCount]
        if self.facing == 'back':
            return self.backSprites[self.spriteCount]
        if self.facing in ('left', 'right'):
            return self.sideSprites[self.spriteCount]
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
    def addItem(self, item):
        self.items[item] = self.items.get(item, 0) + 1
    def useItem(self, item, pokemon):
        if item == 'Potion':
            pokemon.currentHP += 20
            if pokemon.currentHP > pokemon.hp:
                pokemon.currentHP = pokemon.hp
        if item == 'Pokeball':
            pass
        self.items[item] -= 1
        if self.items[item] == 0:
            self.items.pop(item)

    def determineMove(self, curPokemon, oppPokemon):
        possibleMoves, possibleScores = self.getPossibleMoves(curPokemon.clone(), oppPokemon.clone())
        return self.determineMoveHelper(curPokemon.clone(), oppPokemon.clone(), possibleMoves, possibleScores, 0, '')
    def determineMoveHelper(self, curPokemon, oppPokemon, possibleMoves, possibleScores, score, bestMove):
        index = possibleScores.index(max(possibleScores))
        score = possibleScores[index]
        move = possibleMoves[index]
        print(possibleMoves)
        print(possibleScores)
        return score, move
    def getPossibleMoves(self, curPokemon, oppPokemon):
        possibleDamage = []
        for move in curPokemon.moves:
            damage = curPokemon.attackPokemon(oppPokemon, move)
            possibleDamage.append(damage)
        for i in range(len(self.items)):
            possibleDamage.append(0)
        for i in range(len(self.party) - 1):
            possibleDamage.append(0)

        possibleHeal = []
        for move in curPokemon.moves:
            possibleHeal.append(0)
        for item in self.items:
            if item == 'Potion':
                possibleHeal.append(curPokemon.hp - curPokemon.currentHP)
            else:
                possibleHeal.append(0)
        for i in range(len(self.party) - 1):
            possibleHeal.append(0)

        possibleMoves = []
        for move in curPokemon.moves:
            possibleMoves.append(move)
        for item in self.items:
            possibleMoves.append(item)
        for pokemon in self.party:
            if pokemon != curPokemon:
                possibleMoves.append(f'switch {pokemon.name}')
        # print(possibleMoves)

        possibleScores = []
        for i in range(len(possibleDamage)):
            possibleScores.append(possibleDamage[i] + possibleHeal[i])
        # print(possibleDamage, possibleHeal)

        return [possibleMoves, possibleScores]
    def doMove(self, curPokemon, oppPokemon, move):
        if move == 'Potion':
            self.useItem(move, curPokemon)
            self.addItem('Place Holder')
        elif move == 'Place Holder':
            pass
        elif move[:6] == 'switch':
            pass
        else:
            curPokemon.attackPokemon(oppPokemon, move)
    # def determineMoveHelper(self, curPokemon, oppPokemon, possibleMoves, possibleScores, score, bestMove):
    #     if oppPokemon.currentHP == 0:
    #         return score, bestMove
    #     else:
    #         bestScore = 0
    #         for i in range(len(possibleMoves)):
    #             move = possibleMoves[i]
    #             score += possibleScores[i]
    #             curPokemonBefore = curPokemon.clone()
    #             oppPokemonBefore = oppPokemon.clone()
    #             itemsBefore = dict(self.items)
    #             self.doMove(curPokemon, oppPokemon, move)
    #             newPossibleMoves, newPossibleScores = self.getPossibleMoves(curPokemon, oppPokemon)
    #             score, newMove = self.determineMoveHelper(curPokemon, oppPokemon, newPossibleMoves, newPossibleScores, score, move)
    #             if score > bestScore:
    #                 bestScore = score
    #                 bestMove = newMove
    #                 self.items = itemsBefore
    #             else:
    #                 curPokemon = curPokemonBefore
    #                 oppPokemon = oppPokemonBefore
    #                 self.items = itemsBefore
    #                 # score -= possibleScores[i]
    #         print(possibleMoves)
    #         print(possibleScores)
    #         return score, bestMove
    # def determineMove(self, curPokemon, opponent, oppPokemon):
    #     state = self.getPossibleMoves(curPokemon.clone(), oppPokemon.clone())
    #     self.gameAI(state, 5, True,
    #                 curPokemon.clone(), oppPokemon.clone(), 0)
    # def gameAI(self, state, depth, maximizing, curPokemon, oppPokemon, moveI):
    #     print('depth', depth)
    #     if depth == 0: # base case
    #         # return score of the state
    #         return state[1][moveI], moveI
    #     if maximizing:
    #         bestMoveI = 0
    #         bestScore = state[1][bestMoveI] * -1
    #         print(bestScore)
    #         for i in range(len(state[0])):
    #             move = state[0][i]
    #             curPokemonBefore = curPokemon.clone()
    #             oppPokemonBefore = oppPokemon.clone()
    #             self.doMove(curPokemon, oppPokemon, move)
    #             state = self.getPossibleMoves(curPokemon, oppPokemon)
    #             newScore, newMoveI = self.gameAI(state, depth-1, not maximizing, curPokemon, oppPokemon, bestMoveI)
    #             if newScore > bestScore:
    #                 bestScore = newScore
    #                 bestMoveI = newMoveI
    #             else:
    #                 curPokemon = curPokemonBefore.clone()
    #                 oppPokemon = oppPokemonBefore.clone()
    #         return bestScore, bestMoveI
    #     else:
    #         bestMoveI = 0
    #         bestScore = state[1][bestMoveI]
    #         print(bestScore)
    #         for i in range(len(state[0])):
    #             move = state[0][i]
    #             curPokemonBefore = curPokemon.clone()
    #             oppPokemonBefore = oppPokemon.clone()
    #             self.doMove(curPokemon, oppPokemon, move)
    #             state = self.getPossibleMoves(curPokemon, oppPokemon)
    #             newScore, newMoveI = self.gameAI(state, depth - 1, not maximizing, curPokemon, oppPokemon, bestMoveI)
    #             if newScore < bestScore:
    #                 bestScore = newScore
    #                 bestMoveI = newMoveI
    #             else:
    #                 curPokemon = curPokemonBefore.clone()
    #                 oppPokemon = oppPokemonBefore.clone()
    #         return bestScore, bestMoveI
