from cmu_graphics import *
from PIL import Image
import os, pathlib
from random import *
import numpy as np
from pokemon112_classes import *

# THINGS TO ADD:
# Fix experience gain (visual is broken or level up is broken)
# Add move selection after leveling up

def openImage(fileName):
    # opens up sprites (currently not in use since graphics will be added later)
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onAppStart(app):
    app.stepsPerSecond = 15
    app.mainMenu = True

    loadMenuGraphics(app)
    loadBattleGraphics(app)
    loadPokemonSprites(app)

    app.mainMenuBox1Visible = True
    app.mainMenuBox2Visible = True

def setupGame(app):
    app.counter = 0
    app.pause = False

    app.scenes = ['overworld', 'battle', 'menu', 'pokemonCenter', 'pokemart']
    # overworld - where the player can walk around and interact with trainers and items
    # battle - where the player battles either wild pokemon or other trainers
    # buildings - where the player can walk around and interact with the world, but in a building (different map)
    app.menuScreens = ['main', 'pokemon', 'item', 'player', 'option', 'chat']
    app.menuScreenIndex = 0

    app.cellWidth = app.cellHeight = 32
    app.mapGrid = loadGrid('mapGrid.txt')
    app.pokecenterGrid = loadGrid('pokecenterGrid.txt')
    app.pokemartGrid = loadGrid('pokemartGrid.txt')
    if app.scene == 0:
        app.curGrid = app.mapGrid
    elif app.scene == 3:
        app.curGrid = app.pokecenterGrid
    elif app.scene == 4:
        app.curGrid = app.pokemartGrid

    loadBackgrounds(app)
    app.cameraPosD = [0, 0]
    app.cellD = [32, 32]
    app.playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]

    # setup for trainer
    playerSpriteSheet = getPlayerSprites()
    app.player.addSprite(playerSpriteSheet)
    app.player.facing = 'back'

    # app.curPokemon is used to keep track of which pokemon the player has out in battle when in a battle
    app.curPokemon = app.player.party[0]

    # trainer setup
    setupTrainers(app)
    app.isBattling = False
    app.doBattleAnimation = False
    app.isSaving = False
    app.doorPos = {'pokecenter': [59, 22], 'pokemart': [68, 29]}

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
    app.pokemonIndex = 0
    app.isPokemonSelected = False
    app.pokecenterHeal = False
    app.buyingItems = False

    app.spriteList = []
    for frame in range(app.battleAnimation.n_frames):
        app.battleAnimation.seek(frame)
        fr = app.battleAnimation.resize((app.battleAnimation.size[0] // 2, app.battleAnimation.size[1] // 2))
        fr = CMUImage(fr)
        app.spriteList.append(fr)
    app.spriteCounter = 0

def createGameVariables(app):
    # game variables
    app.won = 0
    app.scene = 0
    app.cameraPos = [69, 19]
    # player variables
    app.player = Trainer('Player')
    pokemon = Pokemon('Bulbasaur', 5, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    app.player.addToParty(pokemon)
    app.player.money = 1000
    app.player.addItem('Potion')
    app.player.addItem('Pokeball')
    # trainer variables
    opponent1 = Trainer('Opponent1')
    opponent1.money = 100
    pokemon = Pokemon('Squirtle', 5, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent1.addToParty(pokemon)

    opponent2 = Trainer('Opponent2')
    opponent2.money = 300
    pokemon = Pokemon('Paras', 8, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent2.addToParty(pokemon)
    pokemon = Pokemon('Bellsprout', 10, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent2.addToParty(pokemon)

    opponent3 = Trainer('Opponent3')
    opponent3.money = 500
    pokemon = Pokemon('Meowth', 10, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent3.addToParty(pokemon)
    pokemon = Pokemon('Sandshrew', 12, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent3.addToParty(pokemon)

    opponent4 = Trainer('Opponent4')
    opponent4.money = 700
    opponent4.addItem('Potion')
    pokemon = Pokemon('Nidorina', 14, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent4.addToParty(pokemon)
    pokemon = Pokemon('Nidorino', 14, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent4.addToParty(pokemon)

    opponent5 = Trainer('Opponent5')
    opponent5.money = 900
    opponent5.addItem('Potion')
    pokemon = Pokemon('Geodude', 13, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent5.addToParty(pokemon)
    pokemon = Pokemon('Grimer', 16, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent5.addToParty(pokemon)

    opponent6 = Trainer('Opponent6')
    opponent6.money = 1100
    opponent6.addItem('Potion')
    opponent6.addItem('Potion')
    pokemon = Pokemon('Jolteon', 18, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent6.addToParty(pokemon)
    pokemon = Pokemon('Vaporeon', 18, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent6.addToParty(pokemon)

    opponent7 = Trainer('Opponent7')
    opponent7.money = 1300
    opponent7.addItem('Potion')
    opponent7.addItem('Potion')
    opponent7.addItem('Potion')
    pokemon = Pokemon('Haunter', 22, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent7.addToParty(pokemon)
    pokemon = Pokemon('Kadabra', 24, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent7.addToParty(pokemon)

    opponent8 = Trainer('Opponent8')
    opponent8.money = 9999
    opponent8.addItem('Potion')
    opponent8.addItem('Potion')
    opponent8.addItem('Potion')
    opponent8.addItem('Potion')
    pokemon = Pokemon('Mandi', 30, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent8.addToParty(pokemon)
    pokemon = Pokemon('Gyarados', 26, app.pokemonSprites)
    pokemon.updateStats()
    pokemon.updateMoves()
    opponent8.addToParty(pokemon)

    app.opponents = [opponent1, opponent2, opponent3, opponent4, opponent5, opponent6, opponent7, opponent8]

def loadGameVariables(app):
    try:
        with open(os.path.join(pathlib.Path(__file__).parent, 'data/save.txt'), 'r') as filein:
            # game variables
            app.won = int(filein.readline())
            app.scene = int(filein.readline())
            cameraPos = filein.readline().split(',')
            app.cameraPos = [int(cameraPos[0]), int(cameraPos[1])]
            # player variables
            playerInfo = filein.readline().split(',')
            app.player = Trainer(playerInfo[0])
            app.player.money = int(playerInfo[1])
            for i in range(int(playerInfo[2])):
                pokemonInfo = filein.readline().split(',')
                pokemon = Pokemon(pokemonInfo[0], int(pokemonInfo[2]), app.pokemonSprites)
                pokemon.updateStats()
                pokemon.updateMoves()
                pokemon.nickName = pokemonInfo[1]
                pokemon.experience = float(pokemonInfo[3])
                pokemon.currentHP = int(pokemonInfo[4])
                pokemonMovePPInfo = filein.readline().split(',')
                for i in range(len(pokemon.moves)):
                    pokemon.currentMovePP[i] = int(pokemonMovePPInfo[i])
                app.player.addToParty(pokemon)
            for i in range(int(playerInfo[3])):
                itemInfo = filein.readline().split(',')
                for i in range(int(itemInfo[1])):
                    app.player.addItem(itemInfo[0])
            # trainer variables
            app.opponents = []
            for i in range(8):
                opponentInfo = filein.readline().split(',')
                opponent = Trainer(opponentInfo[0])
                opponent.money = int(opponentInfo[1])
                opponent.defeated = bool(int(opponentInfo[2]))
                opponent.x = int(opponentInfo[3])
                opponent.y = int(opponentInfo[4])
                for i in range(int(opponentInfo[5])):
                    pokemonInfo = filein.readline().split(',')
                    pokemon = Pokemon(pokemonInfo[0], int(pokemonInfo[2]), app.pokemonSprites)
                    pokemon.updateStats()
                    pokemon.updateMoves()
                    pokemon.nickName = pokemonInfo[1]
                    opponent.addToParty(pokemon)
                for i in range(int(opponentInfo[6])):
                    itemInfo = filein.readline().split(',')
                    for i in range(int(itemInfo[1])):
                        opponent.addItem(itemInfo[0])
                app.opponents.append(opponent)
        return True
    except:
        return False

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
    with open(os.path.join(pathlib.Path(__file__).parent, f'data/{filename}'), encoding='utf-8') as f:
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

def loadBackgrounds(app):
    background = openImage('images/background.png')
    pokecenterBackground = openImage('images/pokecenterBackground.png')
    pokemartBackground = openImage('images/pokemartBackground.png')

    app.overworldSprites = {'background': background, 'pokecenter': pokecenterBackground,
                            'pokemart': pokemartBackground}

def loadMenuGraphics(app):
    menuSpriteSheet = openImage('images/menuElements.png')
    menuSpritesTL = []
    menuSpritesTM = []
    menuSpritesTR = []
    menuSpritesML = []
    menuSpritesMM = []
    menuSpritesMR = []
    menuSpritesBL = []
    menuSpritesBM = []
    menuSpritesBR = []
    startLeft = 4
    startTop = 17
    for i in range(30):
        menuSpritesTL.append(menuSpriteSheet.crop((startLeft, startTop, 8 + startLeft, 8 + startTop)))
        menuSpritesTM.append(menuSpriteSheet.crop((startLeft + 9, startTop, 8 + startLeft + 9, 8 + startTop)))
        menuSpritesTR.append(menuSpriteSheet.crop((startLeft + 18, startTop, 8 + startLeft + 18, 8 + startTop)))
        menuSpritesML.append(menuSpriteSheet.crop((startLeft, startTop + 9, 8 + startLeft, 8 + startTop + 9)))
        menuSpritesMM.append(menuSpriteSheet.crop((startLeft + 9, startTop + 9, 8 + startLeft + 9, 8 + startTop + 9)))
        menuSpritesMR.append(menuSpriteSheet.crop((startLeft + 18, startTop + 9, 8 + startLeft + 18, 8 + startTop + 9)))
        menuSpritesBL.append(menuSpriteSheet.crop((startLeft, startTop + 18, 8 + startLeft, 8 + startTop + 18)))
        menuSpritesBM.append(menuSpriteSheet.crop((startLeft + 9, startTop + 18, 8 + startLeft + 9, 8 + startTop + 18)))
        menuSpritesBR.append(menuSpriteSheet.crop((startLeft + 18, startTop + 18, 8 + startLeft + 18, 8 + startTop + 18)))
        startLeft += 30
        if startLeft > 274:
            startLeft = 4
            startTop += 30

    pokemonMenuSpritesSheet = openImage('images/pokemonMenuSprites.png')
    pokemonMenuBackground = pokemonMenuSpritesSheet.crop((250, 5, 240 + 250, 160 + 5))
    curPokemonSelectedBox = pokemonMenuSpritesSheet.crop((406, 170, 84 + 406, 57 + 170))
    curPokemonBox = pokemonMenuSpritesSheet.crop((317, 170, 84 + 317, 57 + 170))
    pokemonSelectedBox = pokemonMenuSpritesSheet.crop((162, 203, 150 + 162, 24 + 203))
    pokemonBox = pokemonMenuSpritesSheet.crop((162, 178, 150 + 162, 24 + 178))
    cancelSelectedButton = pokemonMenuSpritesSheet.crop((65, 251, 54 + 65, 24 + 251))
    cancelButton = pokemonMenuSpritesSheet.crop((6, 251, 54 + 6, 24 + 251))

    bagSpritesSheet = openImage('images/bagScreen.png')
    itemScreen = bagSpritesSheet.crop((112, 384, 240 + 112, 160 + 384))
    itemLabel = bagSpritesSheet.crop((16, 384, 79 + 16, 30 + 384))

    trainerCardSpritesSheet = openImage('images/trainerCardSprites.png')
    trainerCardBackground = trainerCardSpritesSheet.crop((250, 25, 240 + 250, 160 + 25))
    trainerCard = trainerCardSpritesSheet.crop((11, 216, 228 + 11, 148 + 216))
    trainerSprite = trainerCardSpritesSheet.crop((289, 555, 40 + 289, 55 + 555))
    starSprite = trainerCardSpritesSheet.crop((338, 534, 13 + 338, 13 + 534))

    app.menuSprites = {'tl': menuSpritesTL, 'tm': menuSpritesTM, 'tr': menuSpritesTR,
                       'ml': menuSpritesML, 'mm': menuSpritesMM, 'mr': menuSpritesMR,
                       'bl': menuSpritesBL, 'bm': menuSpritesBM, 'br': menuSpritesBR,
                       'pokemonMenuBackground': pokemonMenuBackground, 'curPokemonSelectedBox': curPokemonSelectedBox,
                       'curPokemonBox': curPokemonBox, 'pokemonSelectedBox': pokemonSelectedBox,
                       'pokemonBox': pokemonBox, 'cancelSelectedButton': cancelSelectedButton,
                       'cancelButton': cancelButton,
                       'itemScreen': itemScreen, 'itemLabel': itemLabel,
                       'trainerCardBackground': trainerCardBackground, 'trainerCard': trainerCard,
                       'trainerSprite': trainerSprite, 'starSprite': starSprite}

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

    app.battleAnimation = openImage('images/battleAnimation.gif')

def loadPokemonSprites(app):
    pokemonSpriteSheet = openImage('images/pokemonSpriteSheet.png')
    startLeft = 11
    startTop = 45
    app.pokemonSprites = dict()
    for i in range(1, 153):
        front = pokemonSpriteSheet.crop((startLeft, startTop, 64 + startLeft, 64 + startTop))
        back = pokemonSpriteSheet.crop((startLeft, 65 + startTop, 64 + startLeft, 64 + 65 + startTop))
        menu = pokemonSpriteSheet.crop((startLeft + 65, startTop - 25, 34 + 65 + startLeft, 24 - 25 + startTop))
        app.pokemonSprites[i] = (front, back, menu)

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
    return left

def setupTrainers(app):
    for i in range(len(app.opponents)):
        opponent = app.opponents[i]
        opponent.addSprite(getPlayerSprites())
        # first trainer
        if i == 0:
            if opponent.x == 0 and opponent.y == 0:
                opponent.x, opponent.y = 31, 71
            opponent.message1 = 'Ready for your first battle?'
            opponent.message2 = 'Don\'t worry, I\'ll go easy on ya.'
            opponent.facing = 'left'

        # second trainer
        if i == 1:
            if opponent.x == 0 and opponent.y == 0:
                opponent.x, opponent.y = 25, 40
            opponent.message1 = 'I\'m a place holder tehe'
            opponent.facing = 'left'

        # third trainer
        if i == 2:
            if opponent.x == 0 and opponent.y == 0:
                opponent.x, opponent.y = 23, 36
            opponent.message1 = 'I\'m also a place holder'
            opponent.facing = 'right'

        # fourth trainer
        if i == 3:
            if opponent.x == 0 and opponent.y == 0:
                opponent.x, opponent.y = 25, 32
            opponent.message1 = 'Guess what? Me place holder'
            opponent.message2 = 'UwU'
            opponent.facing = 'left'

        # fifth trainer
        if i == 4:
            if opponent.x == 0 and opponent.y == 0:
                opponent.x, opponent.y = 23, 28
            opponent.message1 = '1, 2, lick my shoe!'
            opponent.facing = 'right'

        # sixth trainer
        if i == 5:
            if opponent.x == 0 and opponent.y == 0:
                opponent.x, opponent.y = 25, 24
            opponent.message1 = 'Bet you\'re not as fast'
            opponent.message2 = 'as my Jolteon!'
            opponent.facing = 'left'

        # seventh trainer
        if i == 6:
            if opponent.x == 0 and opponent.y == 0:
                opponent.x, opponent.y = 23, 20
            opponent.message1 = 'You\'ll never get the reward!'
            opponent.facing = 'right'

        # eighth trainer
        if i == 7:
            if opponent.x == 0 and opponent.y == 0:
                opponent.x, opponent.y = 27, 7
            opponent.message1 = 'Mandi and I will stop you!'
            opponent.facing = 'left'

    #npcs
    nurse = Trainer('Nurse', 16, 8)
    nurse.addSprite(getPlayerSprites())
    nurse.message1 = 'Thank you for visiting the Pokecenter!'
    nurse.message2 = 'You\'re Pokemon have been healed!'

    clerk = Trainer('Clerk', 11, 8)
    clerk.addSprite(getPlayerSprites())
    clerk.message1 = 'How may I help you today?'
    clerk.facing = 'right'

    app.saveMessage = Trainer('Save Message')
    app.saveMessage.message1 = 'Saving...'
    app.saveMessage.message2 = 'Successfully saved the game!'

    app.winMessage = Trainer('Win Message')
    app.winMessage.message1 = 'You beat me!'
    app.winMessage.message2 = 'Here\'s your reward, 9999 money!'

    app.pokecenterNPCs = [nurse]
    app.pokemartNPCs = [clerk]

def setupPokemonBattle(app, trainer=None):
    # app.scene = 1
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
        app.curOpponent.addToParty(app.oppPokemon)
    else:
        app.oppPokemon = trainer.party[0]
        app.curOpponent = trainer
    app.battleBoxMsg = [f'What will', f'{app.curPokemon.nickName} do?']
    app.isBattling = True

def updateScene(app):
    counter = 0
    for opponent in app.opponents:
        if opponent.defeated:
            counter += 1
    if counter == 8 and app.won == 0:
        app.won = 1
        app.scene = 2
        app.menuScreenIndex = 5

    if app.doBattleAnimation:
        app.spriteCounter = (app.spriteCounter + 2) % len(app.spriteList)
        if app.spriteCounter == 46:
            app.spriteCounter = 0
            app.doBattleAnimation = False
            app.pause = False
            app.menuScreenIndex = 0
            app.scene = 1
    if app.scene in (0, 3, 4):
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
        for trainer in app.opponents:
            if trainer.move:
                if trainer.facing == 'left':
                    if trainer.x - (abs(trainer.dx) // 16) == app.playerPos[1] - 1:
                        trainer.move = False
                        trainer.isMoving = False
                        app.pause = False
                        app.scene = 2
                        app.menuScreenIndex = 5
                        trainer.x -= (abs(trainer.dx) // 32)
                        trainer.dx = 0
                    else:
                        trainer.dx -= 4
                if trainer.facing == 'right':
                    if trainer.x + (abs(trainer.dx) // 16) == app.playerPos[1] + 1:
                        trainer.move = False
                        trainer.isMoving = False
                        app.pause = False
                        app.scene = 2
                        app.menuScreenIndex = 5
                        trainer.x += (abs(trainer.dx) // 32)
                        trainer.dx = 0
                    else:
                        trainer.dx += 4
    if app.scene == 1:  # if the player is in a battle
        app.battleBoxMsg = [f'What will', f'{app.curPokemon.nickName} do?']

def checkForBattle(app):
    for trainer in app.opponents:
        if (app.playerPos[0] == trainer.y and trainer.x - 5 <= app.playerPos[1] <= trainer.x + 5
                and not trainer.defeated):
            trainer.move = True
            trainer.isMoving = True
            app.pause = True
            app.wildBattle = False
            setupPokemonBattle(app, trainer)
    if app.mapGrid[app.playerPos[0]][app.playerPos[1]] == 3:
        if randint(1, 10) == 1:
            app.wildBattle = True
            setupPokemonBattle(app)
            app.pause = True
            app.doBattleAnimation = True

def checkForBuilding(app):
    for door in app.doorPos:
        if app.playerPos == app.doorPos[door]:
            if door == 'pokecenter':
                app.scene = 3
                app.cameraPos = [9, 8]
                app.curGrid = app.pokecenterGrid
            if door == 'pokemart':
                app.scene = 4
                app.cameraPos = [8, 5]
                app.curGrid = app.pokemartGrid

def drawMainMenu(app):
    drawRect(0, 0, 480, 320, fill=rgb(79, 83, 143))
    drawMenuBox(app, 80, 16, (3, 19), type=0)
    drawAlphaNum(app, 112, 46, 'LOAD', spacing=10, size=(14, 16),
                 color1=(99, 99, 99), color2=(214, 214, 206))
    drawMenuBox(app, 80, 106, (3, 19), type=0)
    drawAlphaNum(app, 112, 136, 'NEW GAME', spacing=10, size=(14, 16),
                 color1=(99, 99, 99), color2=(214, 214, 206))

    drawRect(84, 20, 309, 69, opacity=30, visible=app.mainMenuBox1Visible)
    drawRect(84, 110, 309, 69, opacity=30, visible=app.mainMenuBox2Visible)

    drawMenuBox(app, 48, 190, (7, 23), type=-1)
    drawAlphaNum(app, 68, 204, 'CONTROLS', spacing=10, size=(10, 16),
                 color1=(248, 248, 248), color2=(115, 115, 115))
    drawAlphaNum(app, 68, 229, 'WASD to move', spacing=10, size=(10, 16),
                 color1=(248, 248, 248), color2=(115, 115, 115))
    drawAlphaNum(app, 68, 254, 'ENTER to enter menu', spacing=10, size=(10, 16),
                 color1=(248, 248, 248), color2=(115, 115, 115))
    drawAlphaNum(app, 68, 279, 'L to interact', spacing=10, size=(10, 16),
                 color1=(248, 248, 248), color2=(115, 115, 115))
    drawAlphaNum(app, 68, 304, 'K to go back', spacing=10, size=(10, 16),
                 color1=(248, 248, 248), color2=(115, 115, 115))

def drawLossMenu(app):
    drawRect(0, 0, 480, 320, opacity=50)
    drawMenuBox(app, 64, 56, (12, 22), type=0)
    drawAlphaNum(app, 210, 76, 'DEFEAT', spacing=14, size=(16, 20),
                 color1=(255, 16, 16), color2=(208, 208, 200))
    drawAlphaNum(app, 84, 106, f'{app.player.name} ran out of usable Pokemon!',
                 color1=(96, 96, 96), color2=(208, 208, 200))
    drawAlphaNum(app, 84, 136, f'Please restart game to continue from',
                 color1=(96, 96, 96), color2=(208, 208, 200))
    drawAlphaNum(app, 84, 156, f'a previous save.',
                 color1=(96, 96, 96), color2=(208, 208, 200))

def redrawAll(app):
    if app.mainMenu:
        drawMainMenu(app)
        return

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
        if app.menuScreenIndex in (0, 5):
            if app.curGrid is app.mapGrid:
                drawOverworld(app)
            elif app.curGrid is app.pokecenterGrid:
                drawPokemonCenter(app)
            elif app.curGrid is app.pokemartGrid:
                drawPokemart(app)
            drawTrainer(app.player, 240, 160)
            if app.menuScreens[app.menuScreenIndex] == 'chat':
                if app.pokecenterHeal:
                    drawConversation(app, app.pokecenterNPCs[0])
                elif app.buyingItems:
                    drawItemShopMenu(app)
                elif app.isSaving:
                    drawConversation(app, app.saveMessage)
                elif app.won == 1:
                    drawConversation(app, app.winMessage)
                else:
                    drawConversation(app, app.curOpponent)
        drawMenu(app)
    elif app.scene == 3:
        drawPokemonCenter(app)
        drawTrainer(app.player, 240, 160)
    elif app.scene == 4:
        drawPokemart(app)
        drawTrainer(app.player, 240, 160)

    if app.doBattleAnimation:
        image = app.spriteList[app.spriteCounter]
        drawImage(image, 0, 0, width=480, height=320)

    if app.player.defeated:
        drawLossMenu(app)

    drawLabel(app.playerPos, 20, 20, fill='red')

def drawItemShopMenu(app):
    drawConversation(app, app.pokemartNPCs[0])
    drawMenuBox(app, 16, 8, (6, 6), type=-2)
    drawAlphaNum(app, 44, 32, 'MONEY', spacing=10, size=(12, 18),
                 color1=(115, 115, 115), color2=(215, 215, 215))
    drawAlphaNum(app, 44, 62, f'{app.player.money}', spacing=10, size=(12, 18),
                 color1=(115, 115, 115), color2=(215, 215, 215))

    drawMenuBox(app, 192, 8, (6, 17), type=-2)
    startLeft = 220
    drawAlphaNum(app, startLeft, 32, 'BUY POTION --------- 300', spacing=10, size=(12, 18),
                 color1=(115, 115, 115), color2=(215, 215, 215))
    drawAlphaNum(app, startLeft, 62, 'BUY POKEBALL ------- 200', spacing=10, size=(12, 18),
                 color1=(115, 115, 115), color2=(215, 215, 215))
    drawAlphaNum(app, startLeft, 92, 'SEE YA!', spacing=10, size=(12, 18),
                 color1=(115, 115, 115), color2=(215, 215, 215))
    drawImage(CMUImage(app.battleSceneSprites['blackCursor']), startLeft - 16, 32 + 30 * app.menuIndex,
              width=12, height=12)

def drawConversation(app, trainer):
    drawMenuBox(app, 0, 228, (4, 30), type=-2)
    left1 = drawAlphaNum(app, 20, 246, trainer.message1, spacing=11, size=(10, 21),
                 color1=(115, 115, 115), color2=(215, 215, 215))
    left2 = drawAlphaNum(app, 20, 276, trainer.message2, spacing=11, size=(10, 21),
                 color1=(115, 115, 115), color2=(215, 215, 215))
    top = 246 if trainer.message2 == '' else 276
    left = left1 if trainer.message2 == '' else left2
    dy = 10 if app.counter % 10 <= 4 else 0
    drawImage(CMUImage(app.battleSceneSprites['redCursor']), left, top + dy, width=20, height=12)

def drawMenuBox(app, left, top, size, type=0):
    startLeft = left
    startTop = top
    drawImage(CMUImage(app.menuSprites['tl'][type]), startLeft, startTop, width=17, height=17)
    startLeft += 15
    for i in range(size[1]):
        drawImage(CMUImage(app.menuSprites['tm'][type]), startLeft, startTop, width=17, height=17)
        startLeft += 15
    drawImage(CMUImage(app.menuSprites['tr'][type]), startLeft, startTop, width=17, height=17)

    startLeft = left
    startTop += 15
    for i in range(size[0]):
        drawImage(CMUImage(app.menuSprites['ml'][type]), startLeft, startTop, width=17, height=17)
        startLeft += 15
        for i in range(size[1]):
            drawImage(CMUImage(app.menuSprites['mm'][type]), startLeft, startTop, width=17, height=17)
            startLeft += 15
        drawImage(CMUImage(app.menuSprites['mr'][type]), startLeft, startTop, width=17, height=17)
        startLeft = left
        startTop += 15

    drawImage(CMUImage(app.menuSprites['bl'][type]), startLeft, startTop, width=17, height=17)
    startLeft += 15
    for i in range(size[1]):
        drawImage(CMUImage(app.menuSprites['bm'][type]), startLeft, startTop, width=17, height=17)
        startLeft += 15
    drawImage(CMUImage(app.menuSprites['br'][type]), startLeft, startTop, width=17, height=17)

def drawMenu(app):
    if app.menuScreens[app.menuScreenIndex] == 'main':
        startLeft = 336
        startTop = 0
        drawMenuBox(app, startLeft, startTop, (13, 8))

        # draw labels
        startLeft = 368
        drawAlphaNum(app, startLeft, 32, 'POKEMON', spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 62, 'BAG', spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 92, app.player.name, spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 122, 'SAVE', spacing=10, size=(12, 18))
        drawAlphaNum(app, startLeft, 152, 'EXIT', spacing=10, size=(12, 18))

        drawImage(CMUImage(app.battleSceneSprites['blackCursor']), 352, 32 + 30 * app.menuIndex, width=12, height=12)

        drawMenuBox(app, 0, 228, (4, 30), type=-1)
        if app.menuIndex == 0:
            message1 = 'Check and organize POKEMON that are'
            message2 = 'traveling with you in your party.'
        elif app.menuIndex == 1:
            message1 = 'Equipped with pockets for storing items'
            message2 = 'you bought, received, or found.'
        elif app.menuIndex == 2:
            message1 = 'Check your money or other game data.'
            message2 = ''
        elif app.menuIndex == 3:
            message1 = 'Save your game with a complete record'
            message2 = 'of your progress to take a break.'
        elif app.menuIndex == 4:
            message1 = 'Adjust various game settings such as text'
            message2 = 'speed, game rules, etc.'
        elif app.menuIndex == 5:
            message1 = 'Close this MENU window.'
            message2 = ''
        else:
            message1 = ''
            message2 = ''
        drawAlphaNum(app, 6, 244, message1, spacing=11, size=(10, 21),
                     color1=(248, 248, 248), color2=(115, 115, 115))
        drawAlphaNum(app, 6, 274, message2, spacing=11, size=(10, 21),
                     color1=(248, 248, 248), color2=(115, 115, 115))

    if app.menuScreens[app.menuScreenIndex] == 'pokemon':
        drawImage(CMUImage(app.menuSprites['pokemonMenuBackground']), 0, 0, width=480, height=320)

        curPokemonBox = app.menuSprites['curPokemonSelectedBox'] if app.pokemonIndex == 0 \
            else app.menuSprites['curPokemonBox']
        drawImage(CMUImage(curPokemonBox), 6, 36, width=168, height=114)

        curPokemonAnimationSpeed = 5 if app.pokemonIndex == 0 else 1
        drawImage(CMUImage(app.curPokemon.menuSprite), 5, 65 - (curPokemonAnimationSpeed * (app.counter%4)),
                  width=68, height=48)
        drawAlphaNum(app, 75, 75, app.curPokemon.nickName, color1=(248, 248, 248), color2=(112, 112, 112))
        drawAlphaNum(app, 105, 94, str(app.curPokemon.level), color1=(248, 248, 248), color2=(112, 112, 112))
        drawAlphaNum(app, 100, 127, f'{app.curPokemon.currentHP}  {app.curPokemon.hp}',
                     color1=(248, 248, 248), color2=(112, 112, 112))
        drawHealthBar(app, 67, 118, app.curPokemon.currentHP, app.curPokemon.hp)

        for i in range(1, len(app.player.party)):
            pokemonBox = app.menuSprites['pokemonSelectedBox'] if app.pokemonIndex == i \
                else app.menuSprites['pokemonBox']
            drawImage(CMUImage(pokemonBox), 175, 18 + ((i-1) * 48), width=300, height=48)
            pokemon = app.player.party[i]
            pokemonAnimationSpeed = 5 if app.pokemonIndex == i else 1
            drawImage(CMUImage(pokemon.menuSprite), 170, 18 + ((i-1) * 48) - (pokemonAnimationSpeed * (app.counter % 4)),
                      width=68, height=48)
            drawAlphaNum(app, 235, 28 + ((i-1) * 48), pokemon.nickName, color1=(248, 248, 248), color2=(112, 112, 112))
            drawAlphaNum(app, 280, 46 + ((i-1) * 48), str(pokemon.level), color1=(248, 248, 248), color2=(112, 112, 112))
            drawAlphaNum(app, 405, 46 + ((i-1) * 48), f'{pokemon.currentHP}  {pokemon.hp}',
                         color1=(248, 248, 248), color2=(112, 112, 112))
            drawHealthBar(app, 367, 36 + ((i-1) * 48), pokemon.currentHP, pokemon.hp)

        cancelButton = app.menuSprites['cancelSelectedButton'] if app.pokemonIndex == len(app.player.party) \
            else app.menuSprites['cancelButton']

        drawImage(CMUImage(cancelButton), 370, 265, width=108, height=48)

        if app.isPokemonSelected:
            drawMenuBox(app, 4, 252, (2, 18), type=-2)
            drawAlphaNum(app, 20, 280, 'Do what with this    ?',
                         spacing=12, size=(14, 18), color1=(115, 115, 115), color2=(215, 215, 215))
            drawAlphaNum(app, 230, 276, 'P K',
                         spacing=10, size=(12, 16), color1=(115, 115, 115), color2=(215, 215, 215))
            drawAlphaNum(app, 240, 284, 'M N',
                         spacing=10, size=(12, 16), color1=(115, 115, 115), color2=(215, 215, 215))

            drawMenuBox(app, 304, 192, (6, 10))
            drawAlphaNum(app, 334, 210, 'SHIFT',
                         spacing=12, size=(14, 18), color1=(115, 115, 115), color2=(215, 215, 215))
            drawAlphaNum(app, 334, 240, 'SUMMARY',
                         spacing=12, size=(14, 18), color1=(115, 115, 115), color2=(215, 215, 215))
            drawAlphaNum(app, 334, 270, 'CANCEL',
                         spacing=12, size=(14, 18), color1=(115, 115, 115), color2=(215, 215, 215))

            drawImage(CMUImage(app.battleSceneSprites['blackCursor']), 320, 212 + 30 * app.menuIndex, width=12,
                      height=12)
        else:
            drawMenuBox(app, 4, 252, (2, 22), type=-2)
            drawAlphaNum(app, 20, 280, 'Choose POKEMON or CANCEL.',
                         spacing=12, size=(14, 18), color1=(115, 115, 115), color2=(215, 215, 215))

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

    if app.menuScreens[app.menuScreenIndex] == 'player':
        drawImage(CMUImage(app.menuSprites['trainerCardBackground']), 0, 0, width=480, height=320)
        drawImage(CMUImage(app.menuSprites['trainerCard']), 12, 12, width=456, height=296)
        drawImage(CMUImage(app.menuSprites['trainerSprite']), 320, 106, width=80, height=110)
        drawAlphaNum(app, 60, 80, f'NAME {app.player.name}', spacing=14, size=(16, 18),
                     color1=(96, 96, 96), color2=(208, 208, 200))
        drawAlphaNum(app, 60, 136, f'MONEY {app.player.money}', spacing=14, size=(16, 18),
                     color1=(96, 96, 96), color2=(208, 208, 200))
        drawAlphaNum(app, 60, 242, f'TRAINERS DEFEATED', size=(10, 12),
                     color1=(96, 96, 96), color2=(208, 208, 200))
        for i in range(len(app.opponents)):
            if app.opponents[i].defeated:
                drawImage(CMUImage(app.menuSprites['starSprite']), (i*47) + 67, 257, width=26, height=26)

def drawOverworld(app):
    startRow, startCol = app.cameraPos[0] - 1, app.cameraPos[1] - 1
    drawImage(CMUImage(app.overworldSprites['background']),
              (0 - startCol) * 32 - app.cellD[1], (0 - startRow) * 32 - app.cellD[0],
              width=1536, height=2560)
    for trainer in app.opponents:
        if startRow < trainer.y < startRow + 12 and startCol < trainer.x < startCol + 17:
            drawTrainer(trainer, (trainer.x - startCol) * 32 - app.cellD[1] - 16 + trainer.dx,
                        (trainer.y - startRow) * 32 - app.cellD[0] + trainer.dy)

def drawPokemonCenter(app):
    startRow, startCol = app.cameraPos[0] - 1, app.cameraPos[1] - 1
    drawImage(CMUImage(app.overworldSprites['pokecenter']),
              (0 - startCol) * 32 - app.cellD[1], (0 - startRow) * 32 - app.cellD[0],
              width=992, height=704)
    for npc in app.pokecenterNPCs:
        if startRow < npc.y < startRow + 12 and startCol < npc.x < startCol + 17:
            drawTrainer(npc, (npc.x - startCol) * 32 - app.cellD[1] - 16 + npc.dx,
                        (npc.y - startRow) * 32 - app.cellD[0] + npc.dy)

def drawPokemart(app):
    startRow, startCol = app.cameraPos[0] - 1, app.cameraPos[1] - 1
    drawImage(CMUImage(app.overworldSprites['pokemart']),
              (0 - startCol) * 32 - app.cellD[1], (0 - startRow) * 32 - app.cellD[0],
              width=896, height=672)
    for npc in app.pokemartNPCs:
        if startRow < npc.y < startRow + 12 and startCol < npc.x < startCol + 17:
            drawTrainer(npc, (npc.x - startCol) * 32 - app.cellD[1] - 16 + npc.dx,
                        (npc.y - startRow) * 32 - app.cellD[0] + npc.dy)

def drawTrainer(trainer, x, y):
    # sprite variables that are currently unused (graphics will be added on later)
    trainerSprite = trainer.getSprite()
    if trainer.facing == 'right':
        trainerSprite = trainerSprite.transpose(Image.FLIP_LEFT_RIGHT)
    drawImage(CMUImage(trainerSprite), x, y, width=28, height=40, align='center')

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

def drawHealthBar(app, left, top, currentHP, hp, size=48):
    healthPercent = currentHP / hp
    if healthPercent > .5:
        healthColor = 'greenHealth'
    elif .2 < healthPercent <= .5:
        healthColor = 'yellowHealth'
    else:
        healthColor = 'redHealth'
    healthBarWidth = size
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
        drawAlphaNum(app, startLeft, startTop, line, spacing=10, size=(12, 18),
                     color1=(248, 248, 248), color2=(104, 88, 112))
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

def checkEvo(app):
    app.player.party[0] = Pokemon(app.curPokemon.ID + 1, app.curPokemon.level, app.pokemonSprites)
    app.player.party[0].updateStats()
    app.player.party[0].updateMoves()
    app.curPokemon = app.player.party[0]

def advanceBattleTurn(app, playerMove):
    if playerMove != 'Pokeball':
        if playerMove == 'switch':
            playerTurn(app, playerMove)
        opponentMove = app.curOpponent.determineMove(app.player)

    if playerMove == 'Pokeball':
        app.scene = 0
        app.menuScreenIndex = 0
        app.isBattling = False
        app.currentAction = ''
        leveledUp = app.curPokemon.gainExperience(app.oppPokemon)
        if (leveledUp and app.curPokemon.evoCondition.isdigit() and
            int(app.curPokemon.evoCondition) == app.curPokemon.level):
            checkEvo(app)
        return

    if (app.curPokemon.speed > app.oppPokemon.speed and opponentMove != 'Potion' and
            not isinstance(opponentMove, Pokemon)):
        playerTurn(app, playerMove)
        if app.oppPokemon.currentHP == 0:
            if app.curOpponent.hasPokemon():
                for i in range(len(app.curOpponent.party)):
                    pokemon = app.curOpponent.party[i]
                    if pokemon.currentHP > 0:
                        app.curOpponent.partyShift(i)
                        app.oppPokemon = app.curOpponent.party[0]
                        app.currentAction = ''
                        return
            if not app.wildBattle:
                app.curOpponent.defeated = True
                app.player.money += app.curOpponent.money
            app.scene = 0
            app.isBattling = False
            app.currentAction = ''
            leveledUp = app.curPokemon.gainExperience(app.oppPokemon)
            if (leveledUp and app.curPokemon.evoCondition.isdigit() and
                    int(app.curPokemon.evoCondition) == app.curPokemon.level):
                checkEvo(app)
            return
        else:
            app.currentAction = ''
        opponentTurn(app, opponentMove)
        if app.curPokemon.currentHP == 0:
            if app.player.hasPokemon():
                app.currentAction = 'pokemon'
                app.menuScreenIndex = 1
                app.scene = 2
            else:
                app.currentAction = 'pokemon'
                app.scene = 2
                app.menuScreenIndex = 1
                app.player.defeated = True
                app.pause = True
                return
    else:
        opponentTurn(app, opponentMove)
        if app.curPokemon.currentHP == 0:
            if app.player.hasPokemon():
                app.currentAction = 'pokemon'
                app.menuScreenIndex = 1
                app.scene = 2
            else:
                app.currentAction = 'pokemon'
                app.scene = 2
                app.menuScreenIndex = 1
                app.player.defeated = True
                app.pause = True
                return
        else:
            app.currentAction = ''
        playerTurn(app, playerMove)
        if app.oppPokemon.currentHP == 0:
            if app.curOpponent.hasPokemon():
                for i in range(len(app.curOpponent.party)):
                    pokemon = app.curOpponent.party[i]
                    if pokemon.currentHP > 0:
                        app.curOpponent.partyShift(i)
                        app.oppPokemon = app.curOpponent.party[0]
                        app.currentAction = ''
                        return
            if not app.wildBattle:
                app.curOpponent.defeated = True
            app.scene = 0
            app.isBattling = False
            app.currentAction = ''
            leveledUp = app.curPokemon.gainExperience(app.oppPokemon)
            if (leveledUp and app.curPokemon.evoCondition.isdigit() and
                    int(app.curPokemon.evoCondition) == app.curPokemon.level):
                checkEvo(app)
            return

def playerTurn(app, playerMove):
    if playerMove == 'attack':
        moveI = app.moveIndex[0] * 2 ** 0 + app.moveIndex[1] * 2 ** 1
        move = app.curPokemon.moves[moveI]
        app.curPokemon.attackPokemon(app.oppPokemon, move)
    elif playerMove == 'item':
        pass
    elif playerMove == 'switch':
        pass

def opponentTurn(app, opponentMove):
    if opponentMove == 'Potion':
        app.curOpponent.useItem(opponentMove, app.oppPokemon)
    elif isinstance(opponentMove, Pokemon):
        index = app.curOpponent.party.index(opponentMove)
        app.curOpponent.partyShift(index)
        app.oppPokemon = app.curOpponent.party[0]
    else:
        app.oppPokemon.attackPokemon(app.curPokemon, opponentMove)

def playerCanMove(app, move, grid):
    playerPos = [app.cameraPos[0] + 5, app.cameraPos[1] + 7]
    if grid[playerPos[0] + move[0]][playerPos[1] + move[1]] in (1, 2):
        return False
    return True

def onKeyHold(app, keys):
    if app.mainMenu:
        return
    if app.pause:
        return
    if app.counter % 4 == 0:
        if app.scene in (0, 3, 4, 5):
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
    if app.mainMenu:
        return
    if app.pause:
        return
    if app.scene in (0, 3, 4, 5):
        if key == 'w':
            app.player.facing = 'back'
        if key == 's':
            app.player.facing = 'front'
            if app.scene == 3 and app.playerPos == [14, 15]:
                app.cameraPos = [55, 15]
                app.curGrid = app.mapGrid
                app.scene = 0
            if app.scene == 4 and app.playerPos == [13, 12]:
                app.cameraPos = [64, 22]
                app.curGrid = app.mapGrid
                app.scene = 0
        if key == 'a':
            app.player.facing = 'left'
        if key == 'd':
            app.player.facing = 'right'
        if key == 'enter':
            app.scene = 2
        if key == 'l':
            if app.scene == 3 and app.playerPos == [10, 15]:
                app.pokecenterHeal = True
                app.scene = 2
                app.menuScreenIndex = 5
            if app.scene == 4 and app.playerPos == [8, 12]:
                app.buyingItems = True
                app.scene = 2
                app.menuScreenIndex = 5
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
                elif app.actionIndex == [0, 1]:
                    app.currentAction = 'pokemon'
                    app.scene = 2
                    app.menuScreenIndex = 1
                elif app.actionIndex == [1, 1] and app.wildBattle:
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
        if app.menuScreens[app.menuScreenIndex] == 'chat' and app.isSaving == False:
            if app.curGrid is app.mapGrid:
                if key == 'l' or key == 'k':
                    if app.won:
                        app.scene = 0
                        app.menuScreenIndex = 0
                        app.won = 2
                    else:
                        app.doBattleAnimation = True
            elif app.curGrid is app.pokecenterGrid:
                if key == 'l' or key == 'k':
                    app.scene = 3
                    app.menuScreenIndex = 0
                    app.pokecenterHeal = False
                    app.player.healAll()
            elif app.curGrid is app.pokemartGrid:
                if key == 'w':
                    app.menuIndex = app.menuIndex - 1 if app.menuIndex > 0 else 2
                if key == 's':
                    app.menuIndex = app.menuIndex + 1 if app.menuIndex < 2 else 0
                if key == 'l':
                    if app.menuIndex == 0:
                        if app.player.money >= 300:
                            app.player.money -= 300
                            app.player.addItem('Potion')
                    elif app.menuIndex == 1:
                        if app.player.money >= 200:
                            app.player.money -= 200
                            app.player.addItem('Pokeball')
                    elif app.menuIndex == 2:
                        app.scene = 4
                        app.menuScreenIndex = 0
                        app.buyingItems = False
                if key == 'k':
                    app.scene = 4
                    app.menuScreenIndex = 0
                    app.buyingItems = False
        elif app.currentAction == '':
            if key == 'w':
                app.menuIndex = app.menuIndex - 1 if app.menuIndex > 0 else 4
            if key == 's':
                app.menuIndex = app.menuIndex + 1 if app.menuIndex < 4 else 0
            if key == 'l':
                if app.menuIndex == 0:
                    app.currentAction = 'pokemon'
                    app.menuScreenIndex = 1
                if app.menuIndex == 1:
                    app.currentAction = 'bag'
                    app.menuScreenIndex = 2
                if app.menuIndex == 2:
                    app.currentAction = 'player'
                    app.menuScreenIndex = 3
                if app.menuIndex == 3:
                    app.currentAction = 'save'
                    app.isSaving = True
                    app.scene = 2
                    app.menuScreenIndex = 5
                    saveGame(app)
                if app.menuIndex == 4:
                    if app.curGrid is app.mapGrid:
                        app.scene = 0
                    elif app.curGrid is app.pokecenterGrid:
                        app.scene = 3
                    elif app.curGrid is app.pokemartGrid:
                        app.scene = 4
            if key == 'k':
                if app.curGrid is app.mapGrid:
                    app.scene = 0
                elif app.curGrid is app.pokecenterGrid:
                    app.scene = 3
                elif app.curGrid is app.pokemartGrid:
                    app.scene = 4
            if key == 'enter':
                if app.curGrid is app.mapGrid:
                    app.scene = 0
                elif app.curGrid is app.pokecenterGrid:
                    app.scene = 3
                elif app.curGrid is app.pokemartGrid:
                    app.scene = 4
        elif app.currentAction == 'pokemon':
            if key == 'w':
                if app.isPokemonSelected:
                    app.menuIndex = app.menuIndex - 1 if app.menuIndex > 0 else 2
                else:
                    app.pokemonIndex = app.pokemonIndex - 1 if app.pokemonIndex > 0 else len(app.player.party)
            if key == 's':
                if app.isPokemonSelected:
                    app.menuIndex = app.menuIndex + 1 if app.menuIndex < 2 else 0
                else:
                    app.pokemonIndex = app.pokemonIndex + 1 if app.pokemonIndex < len(app.player.party) else 0
            if key == 'l':
                if app.isPokemonSelected:
                    if app.menuIndex == 0:
                        if app.player.party[app.pokemonIndex].currentHP > 0:
                            app.player.partyShift(app.pokemonIndex)
                            app.curPokemon = app.player.party[0]
                            app.menuIndex = 0
                            app.isPokemonSelected = False
                            if app.isBattling:
                                app.currentAction = ''
                                app.scene = 1
                                app.menuScreenIndex = 0
                                if app.player.party[app.pokemonIndex].currentHP > 0:
                                    advanceBattleTurn(app, 'switch')
                    elif app.menuIndex == 1:
                        pass
                    elif app.menuIndex == 2:
                        app.menuIndex = 0
                        app.isPokemonSelected = False
                else:
                    if app.pokemonIndex == len(app.player.party):
                        if app.curPokemon.currentHP == 0:
                            return
                        app.currentAction = ''
                        app.menuScreenIndex = 0
                        app.menuIndex = 0
                        app.pokemonIndex = 0
                        app.isPokemonSelected = False
                        if app.isBattling:
                            app.scene = 1
                    else:
                        app.isPokemonSelected = True
            if key == 'k':
                if app.isPokemonSelected:
                    app.menuIndex = 0
                    app.isPokemonSelected = False
                else:
                    app.currentAction = ''
                    app.menuScreenIndex = 0
                    app.menuIndex = 0
                    app.pokemonIndex = 0
                    app.isPokemonSelected = False
                    if app.isBattling:
                        app.scene = 1
        elif app.currentAction == 'bag':
            if key == 'w':
                app.itemIndex = app.itemIndex - 1 if app.itemIndex > 0 else len(app.player.items)
            if key == 's':
                app.itemIndex = app.itemIndex + 1 if app.itemIndex < len(app.player.items) else 0
            if key == 'l':
                if app.itemIndex == len(app.player.items):
                    app.currentAction = ''
                    app.menuScreenIndex = 0
                    app.itemIndex = 0
                    if app.isBattling:
                        app.scene = 1
                else:
                    i = 0
                    for element in app.player.items:
                        if app.itemIndex == i:
                            item = element
                        i += 1
                    if app.isBattling:
                        if item == 'Pokeball':
                            if not app.wildBattle:
                                return
                            pokemon = app.oppPokemon
                            playerMove = 'Pokeball'
                        else:
                            pokemon = app.curPokemon
                            playerMove = 'item'
                        app.scene = 1
                        app.player.useItem(item, pokemon)
                        advanceBattleTurn(app, playerMove)
                    else:
                        pokemon = app.curPokemon
                        app.player.useItem(item, pokemon)
                        app.currentAction = 'pokemon'
                        app.menuScreenIndex = 1

            if key == 'k':
                app.currentAction = ''
                app.menuScreenIndex = 0
                app.itemIndex = 0
                if app.isBattling:
                    app.scene = 1
        elif app.currentAction == 'player':
            if key == 'k':
                app.currentAction = ''
                app.menuScreenIndex = 0
        elif app.currentAction == 'save':
            if key == 'l' or key == 'k':
                app.currentAction = ''
                app.menuScreenIndex = 0
                app.isSaving = False

def onMousePress(app, mouseX, mouseY):
    if app.mainMenu:
        if 80 < mouseX < 397 and 16 < mouseY < 93:
            if loadGameVariables(app):
                setupGame(app)
                app.mainMenu = False
        elif 80 < mouseX < 397 and 106 < mouseY < 183:
            createGameVariables(app)
            setupGame(app)
            app.mainMenu = False

def onMouseMove(app, mouseX, mouseY):
    if app.mainMenu:
        if not (80 < mouseX < 397 and 16 < mouseY < 93):
            app.mainMenuBox1Visible = True
        else:
            app.mainMenuBox1Visible = False
        if not (80 < mouseX < 397 and 106 < mouseY < 183):
            app.mainMenuBox2Visible = True
        else:
            app.mainMenuBox2Visible = False

def saveGame(app):
    with open(os.path.join(pathlib.Path(__file__).parent, 'data/save.txt'), 'w') as fileout:
        if app.curGrid is app.mapGrid:
            scene = 0
        elif app.curGrid is app.pokecenterGrid:
            scene = 3
        elif app.curGrid is app.pokemartGrid:
            scene = 4
        fileout.write(f'{app.won}\n')
        fileout.write(f'{scene}\n')
        fileout.write(f'{app.cameraPos[0]},{app.cameraPos[1]}\n')
        fileout.write(f'{app.player.name},{app.player.money},{len(app.player.party)},{len(app.player.items)}\n')
        for pokemon in app.player.party:
            fileout.write(f'{pokemon.name},{pokemon.nickName},{pokemon.level},{pokemon.experience},'
                          f'{pokemon.currentHP}\n')
            for i in range(len(pokemon.moves)):
                fileout.write(f'{pokemon.currentMovePP[i]}')
                if i != len(pokemon.moves) - 1:
                    fileout.write(',')
            fileout.write('\n')
        for item in app.player.items:
            fileout.write(f'{item},{app.player.items[item]}\n')
        for trainer in app.opponents:
            fileout.write(f'{trainer.name},{trainer.money},{int(trainer.defeated)},{trainer.x},{trainer.y},'
                          f'{len(trainer.party)},{len(trainer.items)}\n')
            for pokemon in trainer.party:
                fileout.write(f'{pokemon.name},{pokemon.nickName},{pokemon.level}\n')
            for item in trainer.items:
                fileout.write(f'{item},{trainer.items[item]}\n')

def onStep(app):
    if app.mainMenu or app.player.defeated:
        return
    app.counter += 1
    updateScene(app)

def main():
    runApp(480, 320)
main()
