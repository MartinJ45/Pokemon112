from cmu_graphics import *
from PIL import Image
import os, pathlib
from random import *
import numpy as np
from pokemon112_classes import *

def openImage(fileName):
    # opens up sprites (currently not in use since graphics will be added later)
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onAppStart(app):
    app.stepsPerSecond = 15
    app.counter = 0

    app.scenes = ['overworld', 'battle', 'menu']
    # overworld - where the player can walk around and interact with trainers and items
    # battle - where the player battles either wild pokemon or other trainers
    # buildings - where the player can walk around and interact with the world, but in a building (different map)
    app.scene = 0
    app.menuScreens = ['pokemon', 'item']
    app.menuScreenIndex = 1

    app.cellWidth = app.cellHeight = 32
    app.mapGrid = loadMapGrid()
    loadOverworldGraphics(app)
    app.overworld = setupOverworld(app)
    app.cameraPos = [5, 5]
    app.cameraPosD = [0, 0]
    app.cellD = [32, 32]
    app.playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]

    # setup for trainer
    playerSpriteSheet = getPlayerSprites()
    app.player = Trainer('Player', playerSpriteSheet)
    app.player.addItem('Potion')
    app.player.addItem('Potion')
    pokemon1 = Pokemon('Bulbasaur', 5)
    pokemon1.updateStats()
    pokemon1.updateMoves()
    app.player.addToParty(pokemon1)
    # app.curPokemon is used to keep track of which pokemon the player has out in battle when in a battle
    app.curPokemon = app.player.party[0]

    # temporary setup for opponent and one pokemon
    app.opponent = Trainer('Opponent', playerSpriteSheet, 18, 12)
    app.opponent.facing = 'left'
    pokemon2 = Pokemon('Charmander', 5)
    pokemon2.updateStats()
    pokemon2.updateMoves()
    app.opponent.addToParty(pokemon2)
    app.wildBattle = True

    loadMenuGraphics(app)
    loadBattleGraphics(app)
    # initializes variables used during a battle
    app.battleBoxMsg = []
    app.currentAction = ''
    app.actionIndex = [0, 0]
    app.actionCursorPos = [[(258, 248), (370, 248)],
                           [(258, 280), (370, 280)]]
    app.moveIndex = [0, 0]
    app.moveCursorPos = [[(22, 254), (167, 254)],
                         [(22, 284), (167, 284)]]

    # sprite variables that are currently unused (graphics will be added on later)
    backgroundColor = (0, 255, 255)  # cyan
    app.image = Image.new('RGB', (app.cellWidth, app.cellHeight), backgroundColor)

def getPlayerSprites():
    npcOverworldSpriteSheet = openImage('images/npcOverworldSprites.png')
    playerFront = npcOverworldSpriteSheet.crop((109, 9, 14 + 109, 21 + 9))
    playerBack = npcOverworldSpriteSheet.crop((124, 9, 14 + 124, 21 + 9))
    playerSide = npcOverworldSpriteSheet.crop((139, 9, 13 + 139, 21 + 9))
    playerFrontWalking = npcOverworldSpriteSheet.crop((154, 9, 15 + 154, 21 + 9))
    playerBackWalking = npcOverworldSpriteSheet.crop((170, 9, 14 + 170, 21 + 9))
    playerSideWalking1 = npcOverworldSpriteSheet.crop((185, 10, 14 + 185, 20 + 10))
    playerSideWalking2 = npcOverworldSpriteSheet.crop((200, 10, 14 + 200, 20 + 10))
    return [playerFront, playerBack, playerSide, playerFrontWalking, playerBackWalking,
            playerSideWalking1, playerSideWalking2]

def loadMapGrid():
    with open('Pokemon112/mapGrid.txt', encoding='utf-8') as f:
        gridRows = f.readlines()
        gridRows.pop(0)
        mapGrid = [[] for i in range(len(gridRows))]
        for i in range(len(gridRows)):
            row = gridRows[i]
            row = row.rstrip('\n')
            for col in row.split(','):
                mapGrid[i].append(int(col))
        mapGrid = np.array(mapGrid)
        return mapGrid

def loadOverworldGraphics(app):
    tilesetSheet = openImage('images/tileset.png')
    blankTile = tilesetSheet.crop((6, 64, 16 + 6, 16 + 64))
    grassTile = tilesetSheet.crop((6, 81, 16 + 6, 16 + 81))

    app.overworldSprites = {'blankTile': blankTile, 'grassTile': grassTile}

def loadMenuGraphics(app):
    bagSpritesSheet = openImage('images/bagScreen.png')
    itemScreen = bagSpritesSheet.crop((112, 384, 240 + 112, 160 + 384))
    itemLabel = bagSpritesSheet.crop((16, 384, 79 + 16, 30 + 384))

    app.bagSprites = {'itemScreen': itemScreen, 'itemLabel': itemLabel}

def loadBattleGraphics(app):
    grassBackground = openImage('images/battleGrassBackground.png')
    app.battleBackgrounds = [grassBackground]

    battleSceneSpriteSheet = openImage('images/battleSceneSprites.png')
    oppHealthBox = battleSceneSpriteSheet.crop((3, 3, 3 + 100, 3 + 29))       # (left, top, left+width, top+height)
    playerHealthBox = battleSceneSpriteSheet.crop((3, 44, 3 + 104, 44 + 37))

    greenHealth = battleSceneSpriteSheet.crop((117, 9, 117 + 9, 9 + 3))
    yellowHealth = battleSceneSpriteSheet.crop((117, 13, 117 + 9, 13 + 3))
    redHealth = battleSceneSpriteSheet.crop((117, 17, 117 + 9, 17 + 3))
    noHealth = battleSceneSpriteSheet.crop((117, 21, 117 + 9, 21 + 3))
    expBar = battleSceneSpriteSheet.crop((129, 9, 129 + 7, 9 + 2))
    noExpBar = battleSceneSpriteSheet.crop((129, 12, 129 + 7, 12 + 2))

    actionBox = battleSceneSpriteSheet.crop((146, 4, 120 + 146, 48 + 4))
    moveBox = battleSceneSpriteSheet.crop((297, 4, 240 + 297, 48 + 4))
    battleBoxBackground = battleSceneSpriteSheet.crop((297, 56, 240 + 297, 48 + 56))
    blackCursor = battleSceneSpriteSheet.crop((269, 4, 6 + 269, 10 + 4))
    redCursor = battleSceneSpriteSheet.crop((544, 59, 10 + 544, 6 + 59))

    app.battleSceneSprites = {'oppHealthBox': oppHealthBox, 'playerHealthBox': playerHealthBox,
                              'greenHealth': greenHealth, 'yellowHealth': yellowHealth, 'redHealth': redHealth,
                              'noHealth': noHealth, 'expBar': expBar, 'noExpBar': noExpBar,
                              'actionBox': actionBox, 'moveBox': moveBox, 'battleBoxBackground': battleBoxBackground,
                              'blackCursor': blackCursor, 'redCursor': redCursor}

    app.alphaNum = loadAlphaNum(battleSceneSpriteSheet)

def loadAlphaNum(battleSceneSpriteSheet):
    startLeft = 171
    startTop = 124
    alphaNum = dict()
    keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z', '.', ',', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', ' ', '!', '?', '♂', '♀', '/', '-', '..', '\"', '\"', '\'', '\'']
    for char in keys:
        character = battleSceneSpriteSheet.crop((startLeft, startTop, startLeft + 6, startTop + 8))
        alphaNum[char] = character
        startLeft += 7
        if char == 'i':
            startLeft -= 2
        if char in ('I', 'T', 'p', '!'):
            startLeft -= 1
        if char in (',', 'z', ' '):
            startTop += 15
            startLeft = 171

    return alphaNum

def drawAlphaNum(app, left, top, string, size=(10, 16), color1=(64, 64, 64), color2=(216, 208, 176)):
    for char in string:
        character = app.alphaNum[char]

        character.convert('RGB')
        colorCharacter = Image.new(mode='RGBA', size=(6, 8))
        for x in range(6):
            for y in range(8):
                r,g,b,al = character.getpixel((x, y))
                if r == g == b == 64:
                    colorCharacter.putpixel((x, y), color1)
                elif r == 216 and g == 208 and b == 176:
                    colorCharacter.putpixel((x, y), color2)

        drawImage(CMUImage(colorCharacter), left, top, width=size[0], height=size[1])
        left += 8

def setupOverworld(app):
    rows, cols = len(app.mapGrid), len(app.mapGrid[0])
    overworld = [[None]*cols for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if app.mapGrid[row][col] == 0:      # blank
                cell = app.overworldSprites['blankTile']
            elif app.mapGrid[row][col] == 1:    # tree
                color = (25, 100, 40)           # dark green
                cell = Image.new('RGB', (app.cellWidth, app.cellHeight), color)
            elif app.mapGrid[row][col] == 2:    # barrier
                color = (115, 70, 30)           # brown
                cell = Image.new('RGB', (app.cellWidth, app.cellHeight), color)
            elif app.mapGrid[row][col] == 3:    # grass
                cell = app.overworldSprites['grassTile']
            overworld[row][col] = cell
    return overworld

def setupPokemonBattle(app, trainer=None):
    app.scene = 1
    app.currentAction = ''
    app.actionIndex = [0, 0]
    if app.wildBattle:
        randomPokemonNum = random.randint(1, 100)
        if 0 < randomPokemonNum <= 30:
            randomPokemon = 'Caterpie'
        elif 30 < randomPokemonNum <= 50:
            randomPokemon = 'Weedle'
        elif 50 < randomPokemonNum <= 70:
            randomPokemon = 'Oddish'
        elif 70 < randomPokemonNum <= 85:
            randomPokemon = 'Rattata'
        elif 85 < randomPokemonNum <= 94:
            randomPokemon = 'Pidgey'
        elif 94 < randomPokemonNum <= 98:
            randomPokemon = 'Spearow'
        else:
            randomPokemon = 'Pikachu'
        app.oppPokemon = Pokemon(randomPokemon, random.randint(2, 4))
        app.oppPokemon.updateStats()
        app.oppPokemon.updateMoves()
    else:
        app.oppPokemon = trainer.party[0]
    app.battleBoxMsg = [f'What will', f'{app.curPokemon.nickName} do?']

def updateScene(app):
    if app.scene == 0:
        app.cellD[0] += app.cameraPosD[0]
        app.cellD[1] += app.cameraPosD[1]
        if app.cellD[0] in (0, 64) or app.cellD[1] in (0, 64):
            app.cameraPos[0] += 1 if app.cellD[0] == 64 else 0
            app.cameraPos[0] += -1 if app.cellD[0] == 0 else 0
            app.cameraPos[1] += 1 if app.cellD[1] == 64 else 0
            app.cameraPos[1] += -1 if app.cellD[1] == 0 else 0
            app.cellD = [32, 32]
            app.cameraPosD = [0, 0]
            app.playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]
            app.player.isMoving = False

            checkForBattle(app)
    if app.scene == 1:  # if the player is in a battle
        pass

def checkForBattle(app):
    if (app.playerPos[0] == app.opponent.y and app.opponent.x - 5 < app.playerPos[1] < app.opponent.x
            and not app.opponent.defeated):
        app.wildBattle = False
        setupPokemonBattle(app, app.opponent)
    if app.mapGrid[app.playerPos[0]][app.playerPos[1]] == 3:
        if randint(1, 10) == 1:
            app.wildBattle = True
            setupPokemonBattle(app)

def redrawAll(app):
    if app.scene == 0:      # if the player is in the overworld
        drawOverworld(app)
        drawTrainer(app.player, 240, 160)
    elif app.scene == 1:    # if the player is in a battle
        drawBattleBackground(app)
        drawPokemonHealthBox(app)
        if app.currentAction == 'fight':
            drawMoveBox(app)
        else:
            drawBattleBoxMsg(app)
            drawActionBox(app)
    elif app.scene == 2:
        drawMenu(app)

def drawMenu(app):
    if app.menuScreens[app.menuScreenIndex] == 'item':
        drawImage(CMUImage(app.bagSprites['itemScreen']), 0, 0, width=480, height=320)
        drawImage(CMUImage(app.bagSprites['itemLabel']), 0, 0, width=158, height=60)

        startLeft = 196
        startTop = 28
        for item in app.player.items:
            drawAlphaNum(app, startLeft, startTop, "%-25s x %+3s" % (item, app.player.items[item]))
            startTop += 36
        drawAlphaNum(app, startLeft, startTop, 'CANCEL')

def drawOverworld(app):
    rows, cols = 13, 17
    startRow, startCol = app.cameraPos[0]-1, app.cameraPos[1]-1

    row = 0
    col = 0
    for i in range(rows*cols):
        if col != 0 and col % cols == 0:
            col = 0
            row += 1
        drawImage(CMUImage(app.overworld[startRow+row][startCol+col]), col*32-app.cellD[1], row*32-app.cellD[0]-16,
                  width=33, height=33)
        if app.opponent.x == startCol + col and app.opponent.y == startRow + row:
            drawTrainer(app.opponent, col*32-app.cellD[1], row*32-app.cellD[0]-16)
        col += 1

    # for row in range(rows):
    #     for col in range(cols):
    #         drawImage(CMUImage(app.overworld[startRow+row][startCol+col]), col*32-app.cellD[1], row*32-app.cellD[0])

def drawTrainer(trainer, x, y):
    # sprite variables that are currently unused (graphics will be added on later)
    drawImage(CMUImage(trainer.getSprite()), x, y, width=28, height=40, align='center')

def drawBattleBackground(app):
    drawImage(CMUImage(app.battleBackgrounds[0]), 0, 0, width=480, height=224)
    drawImage(CMUImage(app.battleSceneSprites['battleBoxBackground']), 0, 224, width=480, height=96)

def drawPokemonHealthBox(app):
    # opponent pokemon
    drawImage(CMUImage(app.battleSceneSprites['oppHealthBox']), 28, 34, width=200, height=58)
    left = 107
    top = 68
    drawHealthBar(app, left, top, app.oppPokemon.currentHP, app.oppPokemon.hp)
    left = 42
    top = 44
    drawAlphaNum(app, left, top, app.oppPokemon.nickName)
    left = 190
    top = 42
    drawAlphaNum(app, left, top, str(app.oppPokemon.level))
    # player pokemon
    drawImage(CMUImage(app.battleSceneSprites['playerHealthBox']), 254, 150, width=208, height=74)
    left = 350
    top = 184
    drawHealthBar(app, left, top, app.curPokemon.currentHP, app.curPokemon.hp)
    left = 286
    top = 160
    drawAlphaNum(app, left, top, app.curPokemon.nickName)
    left = 434
    top = 158
    drawAlphaNum(app, left, top, str(app.curPokemon.level))
    left = 384
    top = 196
    drawAlphaNum(app, left, top, f'{app.curPokemon.currentHP}/ {app.curPokemon.hp}')
    left = 318
    top = 216
    drawExpBar(app, left, top, app.curPokemon)

def drawHealthBar(app, left, top, currentHP, hp):
    healthPercent = currentHP / hp
    if healthPercent > .5:
        healthColor = 'greenHealth'
    elif .2 < healthPercent <= .5:
        healthColor = 'yellowHealth'
    else:
        healthColor = 'redHealth'
    healthBarWidth = 48
    healthWidth = int(healthBarWidth * healthPercent)

    if healthWidth > 0:
        drawImage(CMUImage(app.battleSceneSprites[healthColor]), left, top, width=healthWidth*2, height=6)

def drawExpBar(app, left, top, pokemon):
    currentExp = pokemon.experience - pokemon.level ** 3
    maxExp = (pokemon.level + 1) ** 3
    expPercent = currentExp / maxExp
    expBarWidth = 128
    expWidth = int(expBarWidth * expPercent)

    if expWidth > 0:
        drawImage(CMUImage(app.battleSceneSprites['expBar']), left, top, width=expWidth, height=4)

def drawBattleBoxMsg(app):
    startLeft = 22
    startTop = 252
    for line in app.battleBoxMsg:
        drawAlphaNum(app, startLeft, startTop, line, size=(12, 18), color1=(248, 248, 248), color2=(104, 88, 112))
        startTop += 34

def drawMoveBox(app):
    drawImage(CMUImage(app.battleSceneSprites['moveBox']), 0, 224, width=480, height=96)
    startLeft = 42
    startTop = 254
    for i in range(4):
        if i >= len(app.curPokemon.moves):
            move = '--'
        else:
            move = app.curPokemon.moves[i]
        drawAlphaNum(app, startLeft, startTop, move, color1=(72, 72, 72), color2=(208, 208, 200))
        startLeft += 145
        if i == 1:
            startTop += 30
            startLeft = 42
    cursorX, cursorY = app.moveCursorPos[app.moveIndex[1]][app.moveIndex[0]]
    drawImage(CMUImage(app.battleSceneSprites['blackCursor']), cursorX, cursorY, width=12, height=20)

    moveI = app.moveIndex[0] * 2 ** 0 + app.moveIndex[1] * 2 ** 1
    if moveI >= len(app.curPokemon.moves):
        currentPP = '--'
        maxPP = '--'
        type = '--'
    else:
        currentPP = app.curPokemon.currentMovePP[moveI]
        maxPP = app.curPokemon.maxMovePP[moveI]
        type = app.curPokemon.moveType[moveI].upper()

    drawAlphaNum(app, 410, 246, str(currentPP), color1=(72, 72, 72), color2=(208, 208, 200))
    drawAlphaNum(app, 440, 246, str(maxPP), color1=(72, 72, 72), color2=(208, 208, 200))
    drawAlphaNum(app, 410, 286, type, color1=(72, 72, 72), color2=(208, 208, 200))

def drawActionBox(app):
    drawImage(CMUImage(app.battleSceneSprites['actionBox']), 242, 226, width=240, height=96)
    cursorX, cursorY = app.actionCursorPos[app.actionIndex[1]][app.actionIndex[0]]
    drawImage(CMUImage(app.battleSceneSprites['blackCursor']), cursorX, cursorY, width=12, height=20)

def advanceBattleTurn(app, playerMove, opponentMove):
    if app.curPokemon.speed > app.oppPokemon.speed:
        playerTurn(app, playerMove)

        if app.oppPokemon.currentHP == 0:
            if not app.wildBattle:
                app.opponent.defeated = True
            app.scene = 0
            app.curPokemon.gainExperience(app.oppPokemon)
            return

        opponentTurn(app, opponentMove)

        if app.curPokemon.currentHP == 0:
            app.scene = 0
            app.stop()
            return
    else:
        opponentTurn(app, opponentMove)

        if app.curPokemon.currentHP == 0:
            app.scene = 0
            app.stop()
            return

        playerTurn(app, playerMove)

        if app.oppPokemon.currentHP == 0:
            if not app.wildBattle:
                app.opponent.defeated = True
            app.scene = 0
            app.curPokemon.gainExperience(app.oppPokemon)
            return

    app.currentAction = ''

def playerTurn(app, playerMove):
    if playerMove == 'attack':
        moveI = app.moveIndex[0] * 2 ** 0 + app.moveIndex[1] * 2 ** 1
        move = app.curPokemon.moves[moveI]
        app.curPokemon.attackPokemon(app.oppPokemon, move)
    elif playerMove == 'item':
        pass

def opponentTurn(app, opponentMove):
    if opponentMove == 'attack':
        app.oppPokemon.attackPokemon(app.curPokemon, app.oppPokemon.moves[0])

def playerCanMove(app, move):
    playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]
    if app.mapGrid[playerPos[0] + move[0]][playerPos[1] + move[1]] not in (1, 2):
        return True
    return False

def onKeyHold(app, keys):
    if app.counter % 4 == 0:
        if app.scene == 0:
            if keys[0] == 'up' and app.cameraPosD[1] == 0 and playerCanMove(app, [-1, 0]):
                app.cameraPosD[0] = -8
                app.player.isMoving = True
            if keys[0] == 'down' and app.cameraPosD[1] == 0 and playerCanMove(app, [1, 0]):
                app.cameraPosD[0] = 8
                app.player.isMoving = True
            if keys[0] == 'left' and app.cameraPosD[0] == 0 and playerCanMove(app, [0, -1]):
                app.cameraPosD[1] = -8
                app.player.isMoving = True
            if keys[0] == 'right' and app.cameraPosD[0] == 0 and playerCanMove(app, [0, 1]):
                app.cameraPosD[1] = 8
                app.player.isMoving = True

def onKeyPress(app, key):
    if app.scene == 0:
        if key == 'up':
            app.player.facing = 'back'
        if key == 'down':
            app.player.facing = 'front'
        if key == 'left':
            app.player.facing = 'left'
        if key == 'right':
            app.player.facing = 'right'
    if app.scene == 1:
        if app.currentAction == '':
            if key == 'left' or key == 'right':
                app.actionIndex[0] = 1 if app.actionIndex[0] == 0 else 0
            if key == 'up' or key == 'down':
                app.actionIndex[1] = 1 if app.actionIndex[1] == 0 else 0
            if key == 'x':
                if app.actionIndex == [0, 0]:
                    app.currentAction = 'fight'
                elif app.actionIndex == [1, 0]:
                    app.currentAction = 'bag'
                    app.scene = 2
                elif app.actionIndex == [1, 1] and app.wildBattle:
                    app.currentAction = 'run'
                    app.scene = 0
        elif app.currentAction == 'fight':
            if key == 'left' or key == 'right':
                app.moveIndex[0] = 1 if app.moveIndex[0] == 0 else 0
            if key == 'up' or key == 'down':
                app.moveIndex[1] = 1 if app.moveIndex[1] == 0 else 0
            if key == 'x':
                moveI = app.moveIndex[0]*2**0 + app.moveIndex[1]*2**1
                if moveI >= len(app.curPokemon.moves):
                    return
                if app.curPokemon.currentMovePP[moveI] == 0:
                    return

                advanceBattleTurn(app, 'attack', 'attack')
            if key == 'z':
                app.currentAction = ''
    elif app.scene == 2:
        if app.currentAction == 'bag':
            if key == 'x':
                if app.player.items:
                    app.player.useItem('Potion', app.player.party[0])
                    app.scene = 1
                    advanceBattleTurn(app, 'item', 'attack')
            if key == 'z':
                app.currentAction = ''
                app.scene = 1

def onStep(app):
    app.counter += 1
    updateScene(app)

def main():
    runApp(480, 320)
main()
