import math

from .AI import AI
from ..Piece import Piece
from ..Board import Board


class Minimax(AI):
    """
    Represents a Connect Four AI using the Min-Max algorithm.
    """

    def __init__(self, piece: Piece, depth: int = 4):
        self.depth: int = depth
        self.ai_piece: Piece = piece
        self.human_piece: Piece = Piece(piece.adverse_color())

    def play(self, board: Board) -> int:
        """
        Choose the best column using Min-Max.
        """

        best_score = -math.inf
        best_column = None

        for column in board.get_valid_columns():

            # Simulate AI move
            new_board = board.copy_board()
            new_board.add_piece(column, self.ai_piece)

            score = self.minimax(new_board, self.depth - 1, False)

            if score > best_score:
                best_score = score
                best_column = column

        return best_column

    def minimax(self, board: Board, depth: int, maximizing: bool) -> int:
        """
        Min-Max recursive algorithm.
        """

        valid_columns = board.get_valid_columns()

        if depth == 0 or board.is_full():
            return self.evaluate(board)

        if maximizing:
            value = -math.inf

            for column in valid_columns:

                new_board = board.copy_board()
                new_board.add_piece(column, self.ai_piece)
                value = max(value, self.minimax(new_board, depth - 1, False))

            return value

        else:
            value = math.inf

            for column in valid_columns:

                new_board = board.copy_board()
                new_board.add_piece(column, self.human_piece)
                value = min(value, self.minimax(new_board, depth - 1, True))

            return value

    def evaluate(self, board: Board) -> int:
        """
        Evaluate the board.

        Returns:
            Positive score if AI wins.
            Negative score if human wins.
            0 otherwise.
        """

        if board.check_win(self.ai_piece):
            return 100

        if board.check_win(self.human_piece):
            return -100

        return 0
