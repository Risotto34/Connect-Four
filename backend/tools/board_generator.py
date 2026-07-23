import math
import random


from ..model.Board import Board


def choose_num_pieces(allow_finished=False):
    """
    Chooses a number of pieces to place with a bias towards the end of the board.
    """

    max_pieces = Board.ROWS * Board.COLUMNS

    if not allow_finished:
        max_pieces -= 1

    center = 30
    sigma = 10
    weights = [
        math.exp(-((i - center) ** 2) / (2 * sigma ** 2))
        for i in range(max_pieces + 1)
    ]

    return random.choices(range(max_pieces + 1), weights=weights, k=1)[0]


def generate_random_board(allow_finished: bool = True) -> Board:
    """
    Generate a legal random Connect Four board with a specified number of pieces.
    """

    num_pieces = choose_num_pieces(allow_finished)

    if num_pieces < 0 or num_pieces > Board.ROWS * Board.COLUMNS:
        raise ValueError(
            f"num_pieces must be between 0 and {Board.ROWS * Board.COLUMNS}."
        )

    while True:
        board = _generate_random_board(num_pieces)

        if board.count_pieces() == num_pieces and (
            not board.is_finished() or allow_finished
        ):
            return board


def _generate_random_board(num_pieces: int) -> Board:
    """
    Generate a random Connect Four board with a specified number of pieces.
    """

    board = Board()

    for _ in range(num_pieces):
        valid_columns = board.get_valid_columns()

        column = random.choice(valid_columns)
        board.add_piece(column, board.current_player)

        if board.is_finished():
            break

    return board


if __name__ == "__main__":
    board = generate_random_board(allow_finished=False)
    print(board)
