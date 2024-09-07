import curses
import curses.ascii

from core.player.human import Human
from core.player.player import Player
from org import games, bots
from util import InputWindow

def app(screen: curses.window):
    screen.clear()

    while True:
        # display window for list of choices
        optionsList = curses.newwin(len(games) + 2, curses.COLS, 0, 0)
        optionsList.border()
        for index, game in enumerate(games):
            optionsList.addstr(index + 1, 1, f"[{str(index)}] {"quit" if game == None else game.name}")
        optionsList.refresh()

        # get game choice
        gameSelector = InputWindow(optionsList.getmaxyx()[0], 0, ["select a game:"])
        choice = games[int(gameSelector.getInput(
            lambda reply: str.isdigit(reply) and int(reply) in range(len(games)),
            f"enter a number from 0 to {len(games) - 1}"
        ))]
        if choice == None:
            quit()
        gameSelector.erase()
        
        # update optionsList to display gameChoice
        for i in range(len(games)):
            optionsList.addch(i + 1, 2, '-' if choice == games[i] else ' ')
        optionsList.refresh()
        
        # get number of humans
        humanCensor = InputWindow(optionsList.getmaxyx()[0], 0, ["how many human players?"])
        numHumans = choice.numPlayers - int(humanCensor.getInput(
            lambda reply: reply in map(str, range(choice.numPlayers + 1)),
            f"enter a number from 0 to {choice.numPlayers}"
        ))
        humanCensor.erase()
        optionsList.erase()
        
        game = choice(
            [Human() for _ in range(numHumans)] + 
            [bots[choice]() for _ in range(choice.numPlayers - numHumans)]
        )
        game.play()

if __name__ == "__main__":
    curses.wrapper(app)
