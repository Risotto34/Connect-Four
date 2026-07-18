import math

from .AI import AI
from ..Piece import Piece
from ..Board import Board


class Minimax(AI):
    """
    Represents a Connect Four AI using the Min-Max algorithm.
    """

    def __init__(self, depth: int = 4):
        self.depth: int = depth
        self.ai_piece: Piece = None
        self.human_piece: Piece = None

    def play(self, board: Board) -> int:
        """
        Choose the best column using Min-Max.
        """

        self.ai_piece = board.current_player
        self.human_piece = self.ai_piece.get_adverse_piece()

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

        if depth == 0 or board.is_finished():
            return self.evaluate(board, depth)

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

    def evaluate(self, board: Board, depth: int) -> int:
        """
        Evaluate the board for the AI.
        """

        if board.check_win(self.ai_piece):
            return 100000 + depth

        if board.check_win(self.human_piece):
            return -100000 - depth

        score = 0

        # Center column bonus
        center = board.COLUMNS // 2

        for row in range(board.ROWS):
            piece = board.grid[row][center]

            if piece is not None:
                if piece.get_color() == self.ai_piece.get_color():
                    score += 5
                else:
                    score -= 5

        # Horizontal
        for row in range(board.ROWS):
            for col in range(board.COLUMNS - 3):
                window = [
                    board.grid[row][col + i]
                    for i in range(4)
                ]
                score += self.evaluate_window(window)

        # Vertical
        for row in range(board.ROWS - 3):
            for col in range(board.COLUMNS):
                window = [
                    board.grid[row + i][col]
                    for i in range(4)
                ]
                score += self.evaluate_window(window)

        # Diagonal \
        for row in range(board.ROWS - 3):
            for col in range(board.COLUMNS - 3):
                window = [
                    board.grid[row + i][col + i]
                    for i in range(4)
                ]
                score += self.evaluate_window(window)

        # Diagonal /
        for row in range(3, board.ROWS):
            for col in range(board.COLUMNS - 3):
                window = [
                    board.grid[row - i][col + i]
                    for i in range(4)
                ]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window: list[Piece|None]) -> int:
        """
        Evaluate a group of four cells.
        """

        ai = 0
        human = 0
        empty = 0

        for piece in window:

            if piece is None:
                empty += 1

            elif piece.get_color() == self.ai_piece.get_color():
                ai += 1

            else:
                human += 1

        # AI patterns
        if ai == 4:
            return 10000

        if ai == 3 and empty == 1:
            return 100

        if ai == 2 and empty == 2:
            return 10

        # Human patterns
        if human == 4:
            return -10000

        if human == 3 and empty == 1:
            return -100

        if human == 2 and empty == 2:
            return -10

        return 0