from cmu_graphics import *
from PIL import Image
import os, pathlib
from random import *
from pokemon112_classes import *

def test():
    # this is a test function that has no purpose in the actual game
    pokemon1 = Pokemon('Bulbasaur', 5)
    pokemon2 = Pokemon('Charmander', 5)
    pokemon1.updateMoves()
    pokemon2.updateMoves()
    print(pokemon1)
    print(pokemon2)

    print(pokemon1.attackPokemon(pokemon2, pokemon1.moves[0]))

    print(pokemon1)
    print(pokemon2)

    # route1grid = [
    #     [1] * 7 + [1] * 8 + [0] * 4 + [1] * 8 + [1] * 7,
    #     [1] * 7 + [1] * 8 + [0] * 2 + [100] + [0] + [1] * 8 + [1] * 7,
    #     [1] * 7 + [1] * 8 + [0] * 4 + [1] * 8 + [1] * 7,
    #     [1] * 7 + [1] * 8 + [0] * 4 + [1] * 8 + [1] * 7,
    #     [1] * 7 + [1] * 8 + [0] * 4 + [1] * 8 + [1] * 7,
    #     [1] * 7 + [1] * 8 + [0] * 4 + [1] * 8 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [0] * 6 + [1] * 2 + [0] * 12 + [1] * 7,
    #     [1] * 7 + [2] * 6 + [1] * 2 + [2] * 6 + [0] * 6 + [1] * 7,
    #     [1] * 7 + [0] * 6 + [1] * 2 + [3] * 12 + [1] * 7,
    #     [1] * 7 + [0] * 6 + [1] * 2 + [3] * 12 + [1] * 7,
    #     [1] * 7 + [0] * 6 + [1] * 2 + [3] * 12 + [1] * 7,
    #     [1] * 7 + [0] * 6 + [1] * 2 + [3] * 12 + [1] * 7,
    #     [1] * 7 + [2] * 6 + [1] * 2 + [3] * 12 + [1] * 7,
    #     [1] * 7 + [0] * 6 + [1] * 2 + [0] * 12 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [0] * 14 + [3] * 6 + [1] * 7,
    #     [1] * 7 + [0] * 14 + [3] * 6 + [1] * 7,
    #     [1] * 7 + [1] * 2 + [2] * 6 + [1] * 6 + [3] * 6 + [1] * 7,
    #     [1] * 7 + [1] * 2 + [0] * 6 + [1] * 6 + [3] * 6 + [1] * 7,
    #     [1] * 7 + [0] * 14 + [3] * 6 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [2] * 2 + [0] * 1 + [2] * 4 + [0] * 2 + [2] * 11 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [0] * 10 + [3] * 6 + [0] * 4 + [1] * 7,
    #     [1] * 7 + [1] * 10 + [3] * 6 + [0] * 4 + [1] * 7,
    #     [1] * 7 + [1] * 10 + [3] * 6 + [2] * 4 + [1] * 7,
    #     [1] * 7 + [0] * 10 + [3] * 6 + [0] * 4 + [1] * 7,
    #     [1] * 7 + [0] * 10 + [3] * 6 + [0] * 4 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [0] * 20 + [1] * 7,
    #     [1] * 7 + [2] * 4 + [0] * 3 + [1] * 1 + [2] * 12 + [1] * 7,
    #     [1] * 7 + [0] * 2 + [3] * 7 + [0] * 6 + [3] * 5 + [1] * 7,
    #     [1] * 7 + [0] * 2 + [3] * 7 + [0] * 6 + [3] * 5 + [1] * 7,
    #     [1] * 7 + [3] * 7 + [0] * 6 + [3] * 5 + [0] * 2 + [1] * 7,
    #     [1] * 7 + [3] * 7 + [0] * 3 + [3] * 2 + [0] * 1 + [3] * 5 + [0] * 2 + [1] * 7,
    #     [1] * 7 + [1] * 10 + [3] * 2 + [1] * 8 + [1] * 7,
    #     [1] * 7 + [1] * 10 + [3] * 2 + [1] * 8 + [1] * 7,
    #     [1] * 7 + [1] * 10 + [3] * 2 + [1] * 8 + [1] * 7,
    #     [1] * 7 + [1] * 10 + [3] * 2 + [1] * 8 + [1] * 7,
    # ]
    #
    # for r in route1grid:
    #     print(r)

def openImage(fileName):
    # opens up sprites (currently not in use since graphics will be added later)
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onAppStart(app):
    app.stepsPerSecond = 30
    app.counter = 0

    app.scenes = ['overworld', 'battle']
    # overworld - where the player can walk around and interact with trainers and items
    # battle - where the player battles either wild pokemon or other trainers
    # buildings - where the player can walk around and interact with the world, but in a building (different map)
    app.scene = 0

    app.cellWidth = app.cellHeight = 32
    app.mapGrid = loadMapGrid()
    app.overworld = setupOverworld(app)
    app.cameraPos = [5, 5]
    app.cameraPosD = [0, 0]
    app.cellD = [32, 32]
    app.playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]

    # temporary setup for trainer and one pokemon
    app.player = Trainer('Player')
    pokemon1 = Pokemon('Bulbasaur', 5)
    pokemon1.updateStats()
    pokemon1.updateMoves()
    app.player.addToParty(pokemon1)
    # app.curPokemon is used to keep track of which pokemon the player has out in battle when in a battle
    app.curPokemon = app.player.party[0]

    # temporary setup for opponent and one pokemon
    app.opponent = Trainer('Opponent')
    pokemon2 = Pokemon('Charmander', 5)
    pokemon2.updateStats()
    pokemon2.updateMoves()
    app.opponent.addToParty(pokemon2)
    # app.oppPokemon will keep track of the current pokemon that the opponent would have out in a battle
    app.oppPokemon = app.opponent.party[0]

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
        return mapGrid

def loadBattleGraphics(app):
    grassBackground = openImage('images/battleGrassBackground.png')
    app.battleBackgrounds = [grassBackground]
    battleBoxBackground = openImage('images/battleBoxBackground.png')
    app.battleSprites = [battleBoxBackground]

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
                color = (255, 255, 255)         # white
            elif app.mapGrid[row][col] == 1:    # tree
                color = (25, 100, 40)           # dark green
            elif app.mapGrid[row][col] == 2:    # barrier
                color = (115, 70, 30)           # brown
            elif app.mapGrid[row][col] == 3:    # grass
                color = (70, 180, 70)           # light green
            cell = Image.new('RGB', (app.cellWidth, app.cellHeight), color)
            overworld[row][col] = cell
    return overworld

def setupPokemonBattle(app, wild=True):
    app.scene = 1
    app.currentAction = ''
    app.actionIndex = [0, 0]
    if wild:
        app.oppPokemon = Pokemon('Pidgey', 2)
        app.oppPokemon.updateStats()
        app.oppPokemon.updateMoves()
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
            checkForBattle(app)
    if app.scene == 1:  # if the player is in a battle
        pass

def checkForBattle(app):
    if app.mapGrid[app.playerPos[0]][app.playerPos[1]] == 3:
        if randint(1, 10) == 1:
            setupPokemonBattle(app, True)

def redrawAll(app):
    if app.scene == 0:      # if the player is in the overworld
        drawOverworld(app)
        # for i in range(15):
        #     drawLine(0 + i*32, 0, 0 + i*32, app.height, opacity=50)
        #     drawLine(0, 0 + i*32, app.width, 0 + i*32, opacity=50)

        drawImage(CMUImage(app.image), app.width//2, app.height//2, align='center')
    elif app.scene == 1:    # if the player is in a battle
        drawBattleBackground(app)
        drawPokemonHealthBox(app)
        if app.currentAction == 'fight':
            drawMoveBox(app)
        else:
            drawBattleBoxMsg(app)
            drawActionBox(app)

def drawOverworld(app):
    rows, cols = 13, 17
    startRow, startCol = app.cameraPos[0]-1, app.cameraPos[1]-1

    row = 0
    col = 0
    for i in range(rows*cols):
        if col != 0 and col % cols == 0:
            col = 0
            row += 1
        drawImage(CMUImage(app.overworld[startRow+row][startCol+col]), col*32-app.cellD[1], row*32-app.cellD[0]-16)
        col += 1

    # for row in range(rows):
    #     for col in range(cols):
    #         drawImage(CMUImage(app.overworld[startRow+row][startCol+col]), col*32-app.cellD[1], row*32-app.cellD[0])

def drawBattleBackground(app):
    drawImage(CMUImage(app.battleBackgrounds[0]), 0, 0, width=480, height=224)
    drawImage(CMUImage(app.battleSceneSprites['battleBoxBackground']), 0, 224, width=480, height=96)

def drawPokemonHealthBox(app):
    # temporary labels for opponent and player pokemon
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

def playerCanMove(app, move):
    playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]
    if app.mapGrid[playerPos[0] + move[0]][playerPos[1] + move[1]] not in (1, 2):
        return True
    return False

def onKeyHold(app, keys):
    if app.counter % 8 == 0:
        if app.scene == 0:
            if keys[0] == 'up' and app.cameraPosD[1] == 0 and playerCanMove(app, [-1, 0]):
                app.cameraPosD[0] = -4
            if keys[0] == 'down' and app.cameraPosD[1] == 0 and playerCanMove(app, [1, 0]):
                app.cameraPosD[0] = 4
            if keys[0] == 'left' and app.cameraPosD[0] == 0 and playerCanMove(app, [0, -1]):
                app.cameraPosD[1] = -4
            if keys[0] == 'right' and app.cameraPosD[0] == 0 and playerCanMove(app, [0, 1]):
                app.cameraPosD[1] = 4

def onKeyPress(app, key):
    if app.scene == 1:
        if app.currentAction == '':
            if key == 'left' or key == 'right':
                app.actionIndex[0] = 1 if app.actionIndex[0] == 0 else 0
            if key == 'up' or key == 'down':
                app.actionIndex[1] = 1 if app.actionIndex[1] == 0 else 0
            if key == 'x':
                if app.actionIndex == [0, 0]:
                    app.currentAction = 'fight'
                if app.actionIndex == [1, 1]:
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

                move = app.curPokemon.moves[moveI]
                app.curPokemon.attackPokemon(app.oppPokemon, move)
                app.currentAction = ''

                if app.oppPokemon.currentHP == 0:
                    app.scene = 0
                    return
                app.oppPokemon.attackPokemon(app.curPokemon, app.oppPokemon.moves[0])
                if app.curPokemon.currentHP == 0:
                    app.scene = 0
                    app.stop()
                    return

def onStep(app):
    app.counter += 1
    updateScene(app)

def main():
    runApp(480, 320)
main()
