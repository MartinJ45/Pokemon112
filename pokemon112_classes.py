import random
import os, pathlib

class Pokemon:
    def __init__(self, name, level, sprites=None):
        if str(name).isdigit():
            self.statsData = Pokemon.readData('pokemonData.txt', str(name), 1)
            self.name = self.statsData[0]
        else:
            self.name = name
        self.nickName = self.name.upper()
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
            self.frontSprite, self.backSprite, self.menuSprite = sprites[self.ID]
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
        self.name = self.statsData[0]
        self.ID = int(self.statsData[1])
        self.type1 = self.statsData[2]
        self.type2 = self.statsData[3]
        self.evoCondition = self.statsData[4]
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
                moveData = Pokemon.readData('moveData.txt', self.movesData[i + 1])
                if not moveData:
                    raise Exception(f'{self.movesData[i+1]} not found in moveData.txt')
                if moveData[0] not in self.moves:
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
            return True
        return False
    def levelUp(self):
        self.level += 1
        missingHP = self.hp - self.currentHP
        self.updateStats()
        self.updateMoves()
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
    def readData(fileName, name, index=0):
        with open(os.path.join(pathlib.Path(__file__).parent, f'data/{fileName}'), encoding='utf-8') as f:
            fileString = f.read()
            fileList = fileString.splitlines()
            fileList.pop(0)
            for line in fileList:
                lineData = line.split(',')
                if lineData[index] == name:
                    return lineData

class Trainer:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.money = 1000
        self.message1 = ''
        self.message2 = ''
        self.spriteCount = 0
        self.facing = 'front'
        self.isMoving = False
        self.x = x
        self.dx = 0
        self.y = y
        self.dy = 0
        self.move = False
        self.party = []
        self.items = dict()
        self.defeated = False
    def clone(self):
        clonedTrainer = Trainer(self.name)
        for pokemon in self.party:
            clonedTrainer.addToParty(pokemon.clone())
        for item in self.items:
            clonedTrainer.addItem(item)
        return clonedTrainer
    def addSprite(self, spriteSheet):
        self.frontSprites = [spriteSheet[0], spriteSheet[3], spriteSheet[0]]
        self.backSprites = [spriteSheet[1], spriteSheet[4], spriteSheet[1]]
        self.sideSprites = [spriteSheet[2], spriteSheet[5], spriteSheet[2]]
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
    def partyShift(self, pokemonIndex):
        pokemon1 = self.party[0]
        pokemon2 = self.party[pokemonIndex]
        self.party[0] = pokemon2
        self.party[pokemonIndex] = pokemon1
    def hasPokemon(self):
        count = 0
        for pokemon in self.party:
            if pokemon.currentHP == 0:
                count += 1
        if count == len(self.party):
            return False
        return True
    def healAll(self):
        for pokemon in self.party:
            pokemon.currentHP = pokemon.hp
            for i in range(len(pokemon.moves)):
                pokemon.currentMovePP[i] = pokemon.maxMovePP[i]
    def addItem(self, item):
        self.items[item] = self.items.get(item, 0) + 1
    def useItem(self, item, pokemon):
        if item == 'Potion':
            pokemon.currentHP += 20
            if pokemon.currentHP > pokemon.hp:
                pokemon.currentHP = pokemon.hp
        if item == 'Pokeball':
            if len(self.party) < 6:
                self.party.append(pokemon)
        self.items[item] -= 1
        if self.items[item] == 0:
            self.items.pop(item)
    def determineMove(self, opponent):
        bestMoveL = self.determineMoveHelper([], self.clone(), opponent.clone(), 0)
        if bestMoveL == []:
            return self.party[0].moves[0]
        # print(bestMoveL)
        return bestMoveL[0]
    def determineMoveHelper(self, bestMoveL, player, opponent, depth):
        depth += 1
        possibleMoves = player.getPossibleMoves(player.clone().party[0], opponent.clone().party[0])
        possibleOppMoves = opponent.getPossibleMoves(opponent.clone().party[0], player.clone().party[0])
        # base case
        if player.party[0].currentHP == 0:
            return []
        elif opponent.party[0].currentHP == 0:
            return bestMoveL
        # recursive case
        else:
            for oppMove in possibleOppMoves:
                if ((oppMove == 'Potion' and oppMove in opponent.items) or oppMove != 'Potion' or
                        isinstance(oppMove, Pokemon) and oppMove != 'Pokeball'\
                        and opponent.party[0].clone().attackPokemon(player.party[0].clone(), oppMove) > 0):
                    if oppMove == 'Potion' and oppMove not in opponent.items:
                        continue
                    if oppMove == 'Pokeball':
                        continue
                    if oppMove != 'Potion' and not isinstance(oppMove, Pokemon) and opponent.clone().party[0].attackPokemon(player.clone().party[0], oppMove) == 0:
                        continue
                    for move in possibleMoves:
                        # check if is legal
                        if (move == 'Potion' and move in player.items) or move != 'Potion':
                            if move == 'Potion' and move not in player.items:
                                continue
                            if move != 'Potion' and not isinstance(move, Pokemon) and player.clone().party[0].attackPokemon(opponent.clone().party[0], move) == 0:
                                continue
                            bestMoveL.append(move)
                            # make the move
                            clonedOpponent = opponent.clone()
                            clonedPlayer = player.clone()
                            clonedOpponent.doMove(clonedOpponent.party[0], clonedPlayer.party[0], oppMove)
                            clonedPlayer.doMove(clonedPlayer.party[0], clonedOpponent.party[0], move)
                            # recursively try and solve the puzzle:
                            solution = clonedPlayer.determineMoveHelper(bestMoveL, clonedPlayer, clonedOpponent, depth)
                            # we did it :)
                            if solution != []:
                                return solution
                            # we did not do it, undo move
                            bestMoveL.pop()
            # no solution found :(
            return []
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
                possibleMoves.append(pokemon)
        # print(possibleMoves)

        possibleScores = []
        for i in range(len(possibleDamage)):
            possibleScores.append(possibleDamage[i] + possibleHeal[i])
        # print(possibleDamage, possibleHeal)

        return possibleMoves
    def doMove(self, curPokemon, oppPokemon, move):
        if move == 'Potion':
            self.useItem(move, curPokemon)
        elif move == 'Pokeball':
            pass
        elif isinstance(move, Pokemon):
            index = self.party.index(move)
            self.partyShift(index)
        else:
            curPokemon.attackPokemon(oppPokemon, move)
