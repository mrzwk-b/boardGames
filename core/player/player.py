from core.state import State
from typing import Callable

class Player:
    symbol: str

    def __init__(self) -> None:
        pass

    def decide(self,
                state: State,
                yBegin: int=0, xBegin: int=0,
                prompt: list[str]=[], 
                failMsg: Callable[[str], str] | str ="not an option"):
        pass
