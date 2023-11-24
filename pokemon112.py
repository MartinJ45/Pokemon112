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

    loadBattleGraphics()
    # initializes variables used during a battle
    app.battleBoxMsg = f''
    app.action = 0

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

def loadBattleGraphics():
    app.battleBackgrounds = []

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
    app.action = 0
    if wild:
        app.oppPokemon = Pokemon('Pidgey', 2)
        app.oppPokemon.updateStats()
        app.oppPokemon.updateMoves()

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
        if app.action == 0:     # no option pressed
            app.battleBoxMsg = f'What will {app.curPokemon.name} do?'
        elif app.action == 1:   # fight pressed
            app.battleBoxMsg = f'{app.curPokemon.moves}'
        elif app.action == 2:   # bag pressed
            app.battleBoxMsg = f'Bag not implemented'
        elif app.action == 3:   # pokemon pressed
            app.battleBoxMsg = f'Pokemon not implemented'
        elif app.action == 4:   # run pressed
            app.battleBoxMsg = f'Ran away'
            app.scene = 0

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
        drawPokemonHealthBox(app)
        drawBattleBox(app)
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
        drawImage(CMUImage(app.overworld[startRow+row][startCol+col]), col*32-app.cellD[1], row*32-app.cellD[0])
        col += 1

    # for row in range(rows):
    #     for col in range(cols):
    #         drawImage(CMUImage(app.overworld[startRow+row][startCol+col]), col*32-app.cellD[1], row*32-app.cellD[0])

def drawPokemonHealthBox(app):
    # temporary labels for opponent and player pokemon
    drawLabel(f'{app.oppPokemon.name} Lvl {app.oppPokemon.level} '
              f'HP: {app.oppPokemon.currentHP} / {app.oppPokemon.hp}',
              app.width // 4, app.height // 8)
    drawLabel(f'{app.curPokemon.name} Lvl {app.curPokemon.level} '
              f'HP: {app.curPokemon.currentHP} / {app.curPokemon.hp}',
              app.width - app.width // 4, app.height - app.height // 3)

def drawBattleBox(app):
    # temporary graphics for battle box
    drawRect(0, app.height - app.height // 4, app.width // 2, app.height // 4, fill=None, border='black')
    drawLabel(app.battleBoxMsg, app.width // 6, app.height - app.height // 6)

def drawActionBox(app):
    # temporary graphics for actionBox
    drawRect(app.width // 2, app.height - app.height // 4, app.width // 2, app.height // 4, fill=None, border='black')
    drawLabel(f'1:Fight 2:bag 3:Pokemon 4:Run Action:{app.action}', app.width - app.width // 4,
              app.height - app.height // 6)

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
        if key.isdigit() and 0 <= int(key) <= 4:
            app.action = int(key)
        if app.action == 1 and key == 'a':
            app.curPokemon.attackPokemon(app.oppPokemon, app.curPokemon.moves[0])
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
    runApp(480, 352)
main()
