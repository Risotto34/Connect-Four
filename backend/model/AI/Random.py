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

        available_columns = []

        # Find all columns that are not full
        for column in range(board.COLUMNS):
            if not board.column_is_full(column):
                available_columns.append(column)

        # Return a random available column
        return random.choice(available_columns)