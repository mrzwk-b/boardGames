from .player import Player
from ..state import State
from util import getInput

class Human(Player):
    def pickSymbol(self, reservedChars: set[str]) -> str:
        self.symbol = getInput(
            lambda reply: len(reply) == 1 and reply not in reservedChars,
            prompt="choose a character to represent you",
            failMsg=f"must not be element of {reservedChars}"
        )
        return self.symbol

    def decide(self, state: State, prompt: str) -> tuple[int, int]:
        return state.parseMove(getInput(
            lambda move: state.isLegal(state.parseMove(move)),
            prompt=prompt
        ))

    pass
