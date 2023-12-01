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

    app.scenes = ['overworld', 'battle', 'menu', 'pokemonCenter']
    # overworld - where the player can walk around and interact with trainers and items
    # battle - where the player battles either wild pokemon or other trainers
    # buildings - where the player can walk around and interact with the world, but in a building (different map)
    app.scene = 0
    app.menuScreens = ['main', 'pokemon', 'item']
    app.menuScreenIndex = 0

    app.cellWidth = app.cellHeight = 32
    app.mapGrid = loadGrid('mapGrid.txt')
    app.pokemonCenterGrid = loadGrid('pokemonCenterGrid.txt')
    app.curGrid = app.mapGrid

    loadOverworldGraphics(app)
    loadBuildingGraphics(app)
    app.overworld = setupOverworld(app)
    app.pokemonCenter = setupPokemonCenter(app)
    app.cameraPos = [5, 5]
    app.cameraPosD = [0, 0]
    app.cellD = [32, 32]
    app.playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]

    # setup for trainer
    playerSpriteSheet = getPlayerSprites()
    loadPokemonSprites(app)
    app.player = Trainer('Player', playerSpriteSheet)
    app.player.addItem('Potion')
    app.player.addItem('Potion')
    app.player.addItem('Pokeball')
    pokemon1 = Pokemon('Bulbasaur', 5, app.pokemonSprites)
    pokemon1.updateStats()
    pokemon1.updateMoves()
    app.player.addToParty(pokemon1)
    # app.curPokemon is used to keep track of which pokemon the player has out in battle when in a battle
    app.curPokemon = app.player.party[0]

    # trainer setup
    setupTrainers(app)
    app.isBattling = False

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
    app.itemIndex = 0
    app.menuIndex = 0

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

def loadGrid(filename):
    with open(f'Pokemon112/{filename}', encoding='utf-8') as f:
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
    pokemonCenter = tilesetSheet.crop((8, 158, 80 + 8, 70 + 158))
    app.pokemonCenterPos = [10, 4]
    app.pokemonCenterDoorPos = [12, 7]

    app.overworldSprites = {'blankTile': blankTile, 'grassTile': grassTile, 'pokemonCenter': pokemonCenter}

def loadMenuGraphics(app):
    menuSpriteSheet = openImage('images/menuElements.png')
    menuSpriteTL = menuSpriteSheet.crop((4, 98, 8 + 4, 8 + 98))
    menuSpriteTM = menuSpriteSheet.crop((13, 98, 8 + 13, 8 + 98))
    menuSpriteTR = menuSpriteSheet.crop((22, 98, 8 + 22, 8 + 98))
    menuSpriteML = menuSpriteSheet.crop((4, 107, 8 + 4, 8 + 107))
    menuSpriteMM = menuSpriteSheet.crop((13, 107, 8 + 13, 8 + 107))
    menuSpriteMR = menuSpriteSheet.crop((22, 107, 8 + 22, 8 + 107))
    menuSpriteBL = menuSpriteSheet.crop((4, 116, 8 + 4, 8 + 116))
    menuSpriteBM = menuSpriteSheet.crop((13, 116, 8 + 13, 8 + 116))
    menuSpriteBR = menuSpriteSheet.crop((22, 116, 8 + 22, 8 + 116))

    pokemonMenuSpritesSheet = openImage('images/pokemonMenuSprites.png')
    pokemonMenuBackground = pokemonMenuSpritesSheet.crop((250, 5, 240 + 250, 160 + 5))
    curPokemonSelectedBox = pokemonMenuSpritesSheet.crop((406, 170, 84 + 406, 57 + 170))
    curPokemonBox = pokemonMenuSpritesSheet.crop((317, 170, 84 + 317, 57 + 170))

    bagSpritesSheet = openImage('images/bagScreen.png')
    itemScreen = bagSpritesSheet.crop((112, 384, 240 + 112, 160 + 384))
    itemLabel = bagSpritesSheet.crop((16, 384, 79 + 16, 30 + 384))

    app.menuSprites = {'tl': menuSpriteTL, 'tm': menuSpriteTM, 'tr': menuSpriteTR,
                       'ml': menuSpriteML, 'mm': menuSpriteMM, 'mr': menuSpriteMR,
                       'bl': menuSpriteBL, 'bm': menuSpriteBM, 'br': menuSpriteBR,
                       'pokemonMenuBackground': pokemonMenuBackground, 'curPokemonSelectedBox': curPokemonSelectedBox,
                       'curPokemonBox': curPokemonBox,
                       'itemScreen': itemScreen, 'itemLabel': itemLabel}

def loadBuildingGraphics(app):
    pokemonCenterSheet = openImage('images/pokemonCenterInterior.png')
    pokemonCenterInterior = pokemonCenterSheet.crop((0, 0, 250, 152))

    app.buildingSprites = {'pokemonCenterInterior': pokemonCenterInterior}

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

def loadPokemonSprites(app):
    pokemonSpriteSheet = openImage('images/pokemonSpriteSheet.png')
    startLeft = 11
    startTop = 45
    app.pokemonSprites = dict()
    for i in range(1, 152):
        front = pokemonSpriteSheet.crop((startLeft, startTop, 64 + startLeft, 64 + startTop))
        back = pokemonSpriteSheet.crop((startLeft, 65 + startTop, 64 + startLeft, 64 + 65 + startTop))
        app.pokemonSprites[i] = (front, back)

        startLeft += 130
        if startLeft > 1831:
            startLeft = 11
            startTop += 164

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

def drawAlphaNum(app, left, top, string, spacing=8, size=(10, 16), color1=(64, 64, 64), color2=(216, 208, 176)):
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
        left += spacing

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
                color = (0, 0, 0)               # black
                cell = Image.new('RGB', (app.cellWidth, app.cellHeight), color)
            elif app.mapGrid[row][col] == 3:    # grass
                cell = app.overworldSprites['grassTile']
            overworld[row][col] = cell
    return overworld

def setupPokemonCenter(app):
    rows, cols = len(app.pokemonCenterGrid), len(app.pokemonCenterGrid[0])
    pokemonCenter = [[None]*cols for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if app.pokemonCenterGrid[row][col] == 0:
                color = (255, 255, 255)
                cell = Image.new('RGB', (app.cellWidth, app.cellHeight), color)
            elif app.pokemonCenterGrid[row][col] == 2:    # barrier
                color = (0, 0, 0)               # black
                cell = Image.new('RGB', (app.cellWidth, app.cellHeight), color)
            pokemonCenter[row][col] = cell
    return pokemonCenter
def setupTrainers(app):
    # first trainer
    opponent1 = Trainer('Opponent', getPlayerSprites(), 22, 13)
    opponent1.facing = 'back'

    opponent1.addItem('Potion')
    pokemon = Pokemon('Charmander', 5, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent1.addToParty(pokemon)

    # second trainer
    opponent2 = Trainer('Opponent', getPlayerSprites(), 26, 13)
    opponent2.facing = 'back'

    opponent2.addItem('Potion')
    pokemon = Pokemon('Paras', 10, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent2.addToParty(pokemon)

    # third trainer
    opponent3 = Trainer('Opponent', getPlayerSprites(), 30, 13)
    opponent3.facing = 'back'

    opponent3.addItem('Potion')
    pokemon = Pokemon('Meowth', 15, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent3.addToParty(pokemon)

    app.opponents = [opponent1, opponent2, opponent3]

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
        app.oppPokemon = Pokemon(randomPokemon, random.randint(2, 4), app.pokemonSprites)
        app.oppPokemon.updateStats()
        app.oppPokemon.updateMoves()
        app.curOpponent = Trainer('Wild Pokemon')
    else:
        app.oppPokemon = trainer.party[0]
        app.curOpponent = trainer
    app.battleBoxMsg = [f'What will', f'{app.curPokemon.nickName} do?']
    app.isBattling = True

def updateScene(app):
    if app.scene == 0 or app.scene == 3:
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

            if app.scene == 0:
                checkForBattle(app)
                checkForBuilding(app)
    if app.scene == 1:  # if the player is in a battle
        pass

def checkForBattle(app):
    for trainer in app.opponents:
        if (trainer.y - 5 < app.playerPos[0] < trainer.y and app.playerPos[1] == trainer.x
                and not trainer.defeated):
            app.wildBattle = False
            setupPokemonBattle(app, trainer)
    if app.mapGrid[app.playerPos[0]][app.playerPos[1]] == 3:
        if randint(1, 10) == 1:
            app.wildBattle = True
            setupPokemonBattle(app)

def checkForBuilding(app):
    if [app.playerPos[1], app.playerPos[0]] == app.pokemonCenterDoorPos:
        app.scene = 3
        app.cameraPos = [9, 8]
        app.curGrid = app.pokemonCenterGrid

def redrawAll(app):
    if app.scene == 0:      # if the player is in the overworld
        drawOverworld(app)
        drawTrainer(app.player, 240, 160)
    elif app.scene == 1:    # if the player is in a battle
        drawImage(CMUImage(app.battleBackgrounds[0]), 0, 0, width=480, height=224)
        drawPokemon(app)
        drawImage(CMUImage(app.battleSceneSprites['battleBoxBackground']), 0, 224, width=480, height=96)
        drawPokemonHealthBox(app)
        if app.currentAction == 'fight':
            drawMoveBox(app)
        else:
            drawBattleBoxMsg(app)
            drawActionBox(app)
    elif app.scene == 2:
        if app.menuScreenIndex == 0:
            drawOverworld(app)
            drawTrainer(app.player, 240, 160)
        drawMenu(app)
    elif app.scene == 3:
        drawPokemonCenter(app)
        drawTrainer(app.player, 240, 160)

def drawMenu(app):
    if app.menuScreens[app.menuScreenIndex] == 'main':
        startLeft = 336
        startTop = 0

        drawImage(CMUImage(app.menuSprites['tl']), startLeft, startTop, width=17, height=17)
        startLeft += 15
        for i in range(8):
            drawImage(CMUImage(app.menuSprites['tm']), startLeft, startTop, width=17, height=17)
            startLeft += 15
        drawImage(CMUImage(app.menuSprites['tr']), startLeft, startTop, width=17, height=17)

        startLeft = 336
        startTop += 15
        for i in range(13):
            drawImage(CMUImage(app.menuSprites['ml']), startLeft, startTop, width=17, height=17)
            startLeft += 15
            for i in range(8):
                drawImage(CMUImage(app.menuSprites['mm']), startLeft, startTop, width=17, height=17)
                startLeft += 15
            drawImage(CMUImage(app.menuSprites['mr']), startLeft, startTop, width=17, height=17)
            startLeft = 336
            startTop += 15

        drawImage(CMUImage(app.menuSprites['bl']), startLeft, startTop, width=17, height=17)
        startLeft += 15
        for i in range(8):
            drawImage(CMUImage(app.menuSprites['bm']), startLeft, startTop, width=17, height=17)
            startLeft += 15
        drawImage(CMUImage(app.menuSprites['br']), startLeft, startTop, width=17, height=17)

        # draw labels
        startLeft = 368
        drawAlphaNum(app, startLeft, 32, 'POKEMON', spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 62, 'BAG', spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 92, app.player.name, spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 122, 'SAVE', spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 152, 'OPTION', spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 182, 'EXIT', spacing=10, size=(12, 18))

        drawImage(CMUImage(app.battleSceneSprites['blackCursor']), 352, 32 + 30 * app.menuIndex, width=12, height=12)

    if app.menuScreens[app.menuScreenIndex] == 'pokemon':
        drawImage(CMUImage(app.menuSprites['pokemonMenuBackground']), 0, 0, width=480, height=320)
        drawImage(CMUImage(app.menuSprites['curPokemonSelectedBox']), 6, 36, width=168, height=114)

    if app.menuScreens[app.menuScreenIndex] == 'item':
        drawImage(CMUImage(app.menuSprites['itemScreen']), 0, 0, width=480, height=320)
        drawImage(CMUImage(app.menuSprites['itemLabel']), 0, 0, width=158, height=60)
        drawImage(CMUImage(app.battleSceneSprites['blackCursor']), 180, 30 + 36*app.itemIndex, width=12, height=12)

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
        for trainer in app.opponents:
            if trainer.x == startCol + col and trainer.y == startRow + row:
                pass
                drawTrainer(trainer, col*32-app.cellD[1], row*32-app.cellD[0]-16)

        col += 1

    # draws the pokemon center
    row = 0
    col = 0
    for i in range(rows*cols):
        if col != 0 and col % cols == 0:
            col = 0
            row += 1
        if app.pokemonCenterPos[0] == startCol + col and app.pokemonCenterPos[1] == startRow + row:
            drawImage(CMUImage(app.overworldSprites['pokemonCenter']), col * 32 - app.cellD[1],
                      row * 32 - app.cellD[0] - 16, width=160, height=140)
        col += 1

    # for row in range(rows):
    #     for col in range(cols):
    #         drawImage(CMUImage(app.overworld[startRow+row][startCol+col]), col*32-app.cellD[1], row*32-app.cellD[0])

def drawPokemonCenter(app):
    rows, cols = 13, 17
    startRow, startCol = app.cameraPos[0] - 1, app.cameraPos[1] - 1

    row = 0
    col = 0
    for i in range(rows * cols):
        if col != 0 and col % cols == 0:
            col = 0
            row += 1
        drawImage(CMUImage(app.pokemonCenter[startRow + row][startCol + col]), col * 32 - app.cellD[1],
                  row * 32 - app.cellD[0] - 16,
                  width=33, height=33)
        col += 1

    col = 8
    row = 6
    drawImage(CMUImage(app.buildingSprites['pokemonCenterInterior']), (col - startCol) * 32 - app.cellD[1] - 16,
              (row - startRow) * 32 - app.cellD[0] - 16, width=500, height=304)

def drawTrainer(trainer, x, y):
    # sprite variables that are currently unused (graphics will be added on later)
    drawImage(CMUImage(trainer.getSprite()), x, y, width=28, height=40, align='center')

def drawPokemon(app):
    drawImage(CMUImage(app.curPokemon.backSprite), 82, 132, width=128, height=128)
    drawImage(CMUImage(app.oppPokemon.frontSprite), 290, 46, width=128, height=128)

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
        type = app.curPokemon.moveTypes[moveI].upper()

    drawAlphaNum(app, 410, 246, str(currentPP), color1=(72, 72, 72), color2=(208, 208, 200))
    drawAlphaNum(app, 440, 246, str(maxPP), color1=(72, 72, 72), color2=(208, 208, 200))
    drawAlphaNum(app, 410, 286, type, color1=(72, 72, 72), color2=(208, 208, 200))

def drawActionBox(app):
    drawImage(CMUImage(app.battleSceneSprites['actionBox']), 242, 226, width=240, height=96)
    cursorX, cursorY = app.actionCursorPos[app.actionIndex[1]][app.actionIndex[0]]
    drawImage(CMUImage(app.battleSceneSprites['blackCursor']), cursorX, cursorY, width=12, height=20)

def advanceBattleTurn(app, playerMove):
    score, opponentMove = app.curOpponent.determineMove(app.oppPokemon, app.curPokemon)
    print('outcome', score, opponentMove)

    if app.curPokemon.speed > app.oppPokemon.speed:
        playerTurn(app, playerMove)
        if app.oppPokemon.currentHP == 0:
            if not app.wildBattle:
                app.curOpponent.defeated = True
            app.scene = 0
            app.isBattling = False
            app.curPokemon.gainExperience(app.oppPokemon)
            return
        opponentTurn(app, opponentMove)
        if app.curPokemon.currentHP == 0:
            app.scene = 0
            app.isBattling = False
            app.stop()
            return
    else:
        opponentTurn(app, opponentMove)
        if app.curPokemon.currentHP == 0:
            app.scene = 0
            app.isBattling = False
            app.stop()
            return
        playerTurn(app, playerMove)
        if app.oppPokemon.currentHP == 0:
            if not app.wildBattle:
                app.curOpponent.defeated = True
            app.scene = 0
            app.isBattling = False
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
    if opponentMove == 'Potion':
        app.curOpponent.useItem(opponentMove, app.oppPokemon)
    else:
        app.oppPokemon.attackPokemon(app.curPokemon, opponentMove)

def playerCanMove(app, move, grid):
    playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]
    if grid[playerPos[0] + move[0]][playerPos[1] + move[1]] not in (1, 2):
        return True
    return False

def onKeyHold(app, keys):
    if app.counter % 4 == 0:
        if app.scene == 0 or app.scene == 3:
            if keys[0] == 'w' and app.cameraPosD[1] == 0 and playerCanMove(app, [-1, 0], app.curGrid):
                app.cameraPosD[0] = -8
                app.player.isMoving = True
            if keys[0] == 's' and app.cameraPosD[1] == 0 and playerCanMove(app, [1, 0], app.curGrid):
                app.cameraPosD[0] = 8
                app.player.isMoving = True
            if keys[0] == 'a' and app.cameraPosD[0] == 0 and playerCanMove(app, [0, -1], app.curGrid):
                app.cameraPosD[1] = -8
                app.player.isMoving = True
            if keys[0] == 'd' and app.cameraPosD[0] == 0 and playerCanMove(app, [0, 1], app.curGrid):
                app.cameraPosD[1] = 8
                app.player.isMoving = True

def onKeyPress(app, key):
    if app.scene == 0 or app.scene == 3:
        if key == 'w':
            app.player.facing = 'back'
        if key == 's':
            app.player.facing = 'front'
            if app.scene == 3 and app.playerPos == [14, 15]:
                app.cameraPos = [2, 5]
                app.curGrid = app.mapGrid
                app.scene = 0
        if key == 'a':
            app.player.facing = 'left'
        if key == 'd':
            app.player.facing = 'right'
        if key == 'enter':
            app.scene = 2
    elif app.scene == 1:
        if app.currentAction == '':
            if key == 'a' or key == 'd':
                app.actionIndex[0] = 1 if app.actionIndex[0] == 0 else 0
            if key == 'w' or key == 's':
                app.actionIndex[1] = 1 if app.actionIndex[1] == 0 else 0
            if key == 'l':
                if app.actionIndex == [0, 0]:
                    app.currentAction = 'fight'
                elif app.actionIndex == [1, 0]:
                    app.currentAction = 'bag'
                    app.scene = 2
                    app.menuScreenIndex = 2
                elif app.actionIndex == [1, 1] and app.wildBattle:
                    app.currentAction = 'run'
                    app.scene = 0
        elif app.currentAction == 'fight':
            if key == 'a' or key == 'd':
                app.moveIndex[0] = 1 if app.moveIndex[0] == 0 else 0
            if key == 'w' or key == 's':
                app.moveIndex[1] = 1 if app.moveIndex[1] == 0 else 0
            if key == 'l':
                moveI = app.moveIndex[0]*2**0 + app.moveIndex[1]*2**1
                if moveI >= len(app.curPokemon.moves):
                    return
                if app.curPokemon.currentMovePP[moveI] == 0:
                    return

                advanceBattleTurn(app, 'attack')
            if key == 'k':
                app.currentAction = ''
    elif app.scene == 2:
        if app.currentAction == '':
            if key == 'w' and app.menuIndex > 0:
                app.menuIndex -= 1
            if key == 's':
                app.menuIndex += 1
                if app.menuIndex > 5:
                    app.menuIndex = 0
            if key == 'l':
                if app.menuIndex == 0:
                    app.currentAction = 'pokemon'
                    app.menuScreenIndex = 1
                if app.menuIndex == 1:
                    app.currentAction = 'bag'
                    app.menuScreenIndex = 2
                if app.menuIndex == 5:
                    app.scene = 0
            if key == 'k':
                app.scene = 0
            if key == 'enter':
                app.scene = 0
        if app.currentAction == 'bag':
            if key == 'w' and app.itemIndex > 0:
                app.itemIndex -= 1
            if key == 's':
                app.itemIndex += 1
                if app.itemIndex > len(app.player.items):
                    app.itemIndex = 0
            if key == 'l':
                if app.itemIndex == len(app.player.items):
                    app.currentAction = ''
                    app.menuScreenIndex = 0
                    if app.isBattling:
                        app.scene = 1
                elif app.isBattling:
                    i = 0
                    for element in app.player.items:
                        if app.itemIndex == i:
                            item = element
                        i += 1
                    app.player.useItem(item, app.player.party[0])
                    app.scene = 1
                    advanceBattleTurn(app, 'item')
            if key == 'k':
                app.currentAction = ''
                app.menuScreenIndex = 0
                if app.isBattling:
                    app.scene = 1

def onStep(app):
    app.counter += 1
    updateScene(app)

def main():
    runApp(480, 320)
main()
