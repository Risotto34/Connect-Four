import random

from ..Board import Board
from ..Piece import Piece


def generate_random_board(
    min_pieces: int = 0,
    max_pieces: int = Board.ROWS * Board.COLUMNS,
    avoid_finished: bool = True,
) -> Board:
    """
    Generate a random, legally reachable Connect Four board.

    Pieces are placed directly by tracking column heights (no repeated
    bottom-up scanning), and colors are drawn from a fixed red/yellow ratio
    so the result always matches a valid alternating-turns game.
    """

    num_pieces = random.randint(min_pieces, max_pieces)
    num_red = (num_pieces + 1) // 2
    num_yellow = num_pieces // 2

    colors = [0] * num_red + [1] * num_yellow
    random.shuffle(colors)

    board = Board()
    heights = [0] * Board.COLUMNS
    open_columns = list(range(Board.COLUMNS))

    for color in colors:
        index = random.randrange(len(open_columns))
        column = open_columns[index]

        row = Board.ROWS - 1 - heights[column]
        board.grid[row][column] = Piece(color, row, column)
        heights[column] += 1

        if heights[column] == Board.ROWS:
            open_columns[index] = open_columns[-1]
            open_columns.pop()

    board.current_player = 0 if num_red == num_yellow else 1

    if avoid_finished and board.is_finished():
        return generate_random_board(min_pieces, max_pieces, avoid_finished)

    return board
