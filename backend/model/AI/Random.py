import random

from .AI import AI
from ..Board import Board


class Random(AI):
    """
    Represents a random Connect Four AI.
    """

    def play(self, board: Board) -> int:
        """
        Choose a random valid column from the board.
        """
        
        # Return a random available column
        return random.choice(board.get_valid_columns())