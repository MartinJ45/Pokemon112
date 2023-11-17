from cmu_graphics import *
from pokemon112_classes import *

def onAppStart(app):
    app.player = Trainer()

    pokemon1 = Pokemon('Bulbasaur', 5)
    pokemon2 = Pokemon('Charmander', 5)
    pokemon1.updateMoves()
    pokemon2.updateMoves()
    print(pokemon1)
    print(pokemon2)

    print(pokemon1.attackPokemon(pokemon2, pokemon1.moves[1]))

    print(pokemon1)
    print(pokemon2)

    app.player.addToParty(pokemon2)

def redrawAll(app):
    pass

def onKeyPress(app, key):
    pass

def main():
    runApp(480, 432)
main()
