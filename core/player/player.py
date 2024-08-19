from ..state import State

class Player:
    symbol: str

    def __init__(self) -> None:
        pass

    def pickSymbol(self, reservedChars: set[str]):
        pass

    def decide(self, state: State, prompt: str=""):
        pass

    pass
