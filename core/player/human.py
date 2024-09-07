from core.player.player import Player
from core.state import State
from typing import Callable
from util import InputWindow

class Human(Player):
    def decide(
            self,
            state: State,
            yBegin: int=0, xBegin: int=0,
            prompt: list[str]=[],
            failMsg: Callable[[str], str] | str="not an option"
        ):
        window = InputWindow(yBegin, xBegin, prompt)
        decision = state.parseMove(window.getInput(
            lambda move: state.isLegal(state.parseMove(move)),
            failMsg
        ))
        window.erase()
        return decision
