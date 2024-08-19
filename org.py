from typing import Type

from checkers.checkers import Checkers
from core.game import Game
from core.player.bot import Bot
from gameOfUr.gameOfUr import GameOfUr
from gameOfUr.gameOfUrBot import GameOfUrBot

games: list[Type[Game] | None] = [None, GameOfUr, Checkers]
bots: dict[Type[Game], Type[Bot]]  = {GameOfUr: GameOfUrBot}
