import math

from .AI import AI
from ..Piece import Piece
from ..Board import Board


class Minimax(AI):
    """
    Represents a Connect Four AI using the Min-Max algorithm.
    """

    SCORES = {"win": 1000000, "three": 20, "two": 10, "center": 5, "overlap": 5}

    def __init__(self, depth: int = 4):
        self.depth: int = depth
        self.ai_color: int = None
        self.human_color: int = None

    def play(self, board: Board) -> int:
        """
        Choose the best column using Min-Max.
        """

        self.ai_color = board.current_player
        self.human_color = Piece.get_opposite_color(self.ai_color)

        best_score = -math.inf
        best_column = None

        for column in board.get_valid_columns():

            # Simulate AI move
            new_board = board.copy()
            new_board.add_piece(column, self.ai_color)

            score = self.minimax(new_board, self.depth - 1, False, -math.inf, math.inf)

            if score > best_score:
                best_score = score
                best_column = column

        return best_column

    def minimax(
        self, board: Board, depth: int, maximizing: bool, alpha: float, beta: float
    ) -> int:
        """
        Min-Max recursive algorithm with alpha-beta pruning.

        Alpha represents the best score guaranteed for the AI.
        Beta represents the best score guaranteed for the opponent.

        When alpha becomes greater than or equal to beta, the remaining
        branches can no longer influence the final decision and are skipped.
        """

        valid_columns = board.get_valid_columns()

        if depth == 0 or board.is_finished():
            return self.evaluate(board, depth)

        if maximizing:
            value = -math.inf

            for column in valid_columns:

                new_board = board.copy()
                new_board.add_piece(column, self.ai_color)

                value = max(
                    value, self.minimax(new_board, depth - 1, False, alpha, beta)
                )

                alpha = max(alpha, value)

                # Alpha is the best score the AI can guarantee.
                if alpha >= beta:
                    break

            return value

        else:
            value = math.inf

            for column in valid_columns:

                new_board = board.copy()
                new_board.add_piece(column, self.human_color)

                value = min(
                    value, self.minimax(new_board, depth - 1, True, alpha, beta)
                )

                beta = min(beta, value)

                # Beta is the best score the opponent can guarantee.
                if beta <= alpha:
                    break

            return value

    def evaluate(self, board: Board, depth: int) -> int:
        """
        Evaluate the board for the AI.
        """

        # Check for terminal states
        if board.check_win(self.ai_color):
            return self.SCORES["win"] + depth

        if board.check_win(self.human_color):
            return -self.SCORES["win"] - depth

        score = 0

        # Center column bonus
        center = board.COLUMNS // 2

        for piece in [board.grid[row][center] for row in range(board.ROWS)]:
            if piece is not None:
                if piece.get_color() == self.ai_color:
                    score += self.SCORES["center"]
                else:
                    score -= self.SCORES["center"]

        # Evaluate all possible windows of four
        score += self.evaluate_windows(board)

        return score

    def evaluate_windows(self, board: Board) -> int:
        """
        Evaluate all possible windows of four and calculate:
        - the value of immediate threats (two/three pieces)
        - the bonus for pieces appearing in multiple valid windows.
        """

        score = 0

        ai_pieces = []
        human_pieces = []

        for window in board.get_all_windows():

            pieces = [piece for piece in window if piece is not None]

            if not pieces:
                continue

            colors = [piece.get_color() for piece in pieces]

            # Ignore windows containing both players
            if len(set(colors)) > 1:
                continue

            # Evaluate normal window patterns
            ai = sum(piece.get_color() == self.ai_color for piece in pieces)
            human = sum(piece.get_color() == self.human_color for piece in pieces)
            empty = window.count(None)

            if ai == 3 and empty == 1:
                score += self.SCORES["three"]
            elif ai == 2 and empty == 2:
                score += self.SCORES["two"]

            if human == 3 and empty == 1:
                score -= self.SCORES["three"]
            elif human == 2 and empty == 2:
                score -= self.SCORES["two"]

            # Store pieces for overlap evaluation
            if len(pieces) >= 2:
                if colors[0] == self.ai_color:
                    ai_pieces.extend(pieces)
                else:
                    human_pieces.extend(pieces)

        # Calculate overlap bonus
        for piece in set(ai_pieces):
            score += (ai_pieces.count(piece) - 1) * self.SCORES["overlap"]

        for piece in set(human_pieces):
            score -= (human_pieces.count(piece) - 1) * self.SCORES["overlap"]

        return score