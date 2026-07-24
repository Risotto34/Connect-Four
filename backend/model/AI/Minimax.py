import math
import time

from ..AI import AI
from ..Piece import Piece
from ..Board import Board


def _popcount(x: int) -> int:
    return x.bit_count()


def _build_windows(rows: int, columns: int) -> list[int]:
    """
    Build the bitmask of every four-in-a-row window on the board.

    Bit index for a cell is column * (rows + 1) + row (row 0 = bottom),
    with one sentinel row per column so vertical/diagonal shifts never
    bleed into the neighboring column.
    """

    stride = rows + 1
    windows = []

    def bit(row: int, col: int) -> int:
        return 1 << (col * stride + row)

    # Horizontal
    for row in range(rows):
        for col in range(columns - 3):
            windows.append(bit(row, col) | bit(row, col + 1) | bit(row, col + 2) | bit(row, col + 3))

    # Vertical
    for col in range(columns):
        for row in range(rows - 3):
            windows.append(bit(row, col) | bit(row + 1, col) | bit(row + 2, col) | bit(row + 3, col))

    # Diagonal (bottom-left to top-right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            windows.append(
                bit(row, col) | bit(row + 1, col + 1) | bit(row + 2, col + 2) | bit(row + 3, col + 3)
            )

    # Diagonal (top-left to bottom-right)
    for row in range(3, rows):
        for col in range(columns - 3):
            windows.append(
                bit(row, col) | bit(row - 1, col + 1) | bit(row - 2, col + 2) | bit(row - 3, col + 3)
            )

    return windows


class Minimax(AI):
    """
    Represents a Connect Four AI using the Min-Max algorithm.

    The search itself runs on a bitboard representation (two 64-bit ints:
    the occupancy mask and the side-to-move's pieces) instead of mutating
    the Board/Piece objects, so no allocation happens inside the search
    tree. Board/Piece are only used at the boundary (converting the
    incoming Board once in `play`).
    """

    ROWS = Board.ROWS
    COLUMNS = Board.COLUMNS
    STRIDE = ROWS + 1

    COLUMN_ORDER = [3, 2, 4, 1, 5, 0, 6]

    WINDOWS = _build_windows(ROWS, COLUMNS)

    TOP_ROW_MASK = 0
    for _col in range(COLUMNS):
        TOP_ROW_MASK |= 1 << (_col * STRIDE + (ROWS - 1))
    del _col

    FULL_MASK = 0
    for _col in range(COLUMNS):
        for _row in range(ROWS):
            FULL_MASK |= 1 << (_col * STRIDE + _row)
    del _col, _row

    CENTER_COL = COLUMNS // 2
    CENTER_MASK = 0
    for _row in range(ROWS):
        CENTER_MASK |= 1 << (CENTER_COL * STRIDE + _row)
    del _row

    def __init__(self, depth: int = 6):
        self.depth: int = depth
        self.ai_color: int = None
        self.human_color: int = None
        self.weights = {"win": 1000000, "three": 20, "two": 10, "center": 5, "overlap": 5}
        self._tt: dict = {}

    def play(self, board: Board) -> int:
        """
        Choose the best column using Min-Max (bitboard negamax internally).
        """

        self.ai_color = board.current_player
        self.human_color = Piece.get_opposite_color(self.ai_color)
        self._tt = {}

        mask, position = self._to_bitboard(board)
        height = self._compute_heights(mask)
        order = self._get_ordered_valid_columns(height)

        alpha = -math.inf
        beta = math.inf
        best_score = -math.inf
        best_column = order[0] if order else None

        for column in order:
            move, new_height = self._make_move(mask, height, column)
            new_mask = mask | move
            new_position = position ^ mask

            score = -self._negamax(
                new_position,
                new_mask,
                new_height,
                self.depth - 1,
                -beta,
                -alpha,
                move,
            )

            if score > best_score:
                best_score = score
                best_column = column

            alpha = max(alpha, best_score)

        return best_column

    def _negamax(
        self,
        position: int,
        mask: int,
        height: list[int],
        depth: int,
        alpha: float,
        beta: float,
        last_move: int,
    ) -> float:
        """
        Negamax with alpha-beta pruning over the bitboard representation.

        `position` is always the bitboard of the player about to move;
        the player who just moved owns `mask ^ position` and their move
        was `last_move`, checked for a win before recursing further.
        """

        opponent_bits = mask ^ position
        if self._has_won(opponent_bits):
            return -(self.weights["win"] + depth)

        if mask == self.FULL_MASK:
            return 0

        if depth == 0:
            return self._evaluate(position, opponent_bits, depth)

        key = (position, mask)
        tt_entry = self._tt.get(key)
        if tt_entry is not None and tt_entry[0] >= depth:
            tt_depth, flag, value = tt_entry
            if flag == 0:
                return value
            elif flag == 1:
                alpha = max(alpha, value)
            elif flag == 2:
                beta = min(beta, value)
            if alpha >= beta:
                return value

        original_alpha = alpha
        value = -math.inf

        for column in self._get_ordered_valid_columns(height):
            move, new_height = self._make_move(mask, height, column)
            new_mask = mask | move
            new_position = opponent_bits

            score = -self._negamax(new_position, new_mask, new_height, depth - 1, -beta, -alpha, move)

            if score > value:
                value = score

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        if value <= original_alpha:
            flag = 2
        elif value >= beta:
            flag = 1
        else:
            flag = 0
        self._tt[key] = (depth, flag, value)

        return value

    @staticmethod
    def _has_won(bitboard: int) -> bool:
        for shift in (1, Minimax.STRIDE, Minimax.STRIDE - 1, Minimax.STRIDE + 1):
            bb = bitboard & (bitboard >> shift)
            if bb & (bb >> (2 * shift)):
                return True
        return False

    def _make_move(self, mask: int, height: list[int], column: int) -> tuple[int, list[int]]:
        row = height[column]
        move = 1 << (column * self.STRIDE + row)
        new_height = height.copy()
        new_height[column] = row + 1
        return move, new_height

    def _get_ordered_valid_columns(self, height: list[int]) -> list[int]:
        return [col for col in self.COLUMN_ORDER if height[col] < self.ROWS]

    def _compute_heights(self, mask: int) -> list[int]:
        heights = []
        for col in range(self.COLUMNS):
            col_mask = mask >> (col * self.STRIDE)
            h = 0
            while h < self.ROWS and (col_mask & (1 << h)):
                h += 1
            heights.append(h)
        return heights

    def _to_bitboard(self, board: Board) -> tuple[int, int]:
        """
        Convert the Board's grid into (mask, position) bitboards, where
        `position` holds the bits of the player about to move (ai_color).
        """

        mask = 0
        ai_bits = 0

        for col in range(board.COLUMNS):
            for board_row in range(board.ROWS):
                piece = board.grid[board_row][col]
                if piece is None:
                    continue
                bit_row = board.ROWS - 1 - board_row
                bit = 1 << (col * self.STRIDE + bit_row)
                mask |= bit
                if piece.get_color() == self.ai_color:
                    ai_bits |= bit

        return mask, ai_bits

    def _evaluate(self, position: int, opponent_bits: int, depth: int) -> float:
        """
        Evaluate a leaf from the perspective of the player to move
        (`position`), mirroring the previous piece-based heuristic.
        """

        score = 0

        score += self.weights["center"] * (
            _popcount(position & self.CENTER_MASK) - _popcount(opponent_bits & self.CENTER_MASK)
        )

        overlap_bonus = [0] * (self.COLUMNS * self.STRIDE)

        for window in self.WINDOWS:
            own = _popcount(position & window)
            opp = _popcount(opponent_bits & window)

            if own and opp:
                continue

            if own == 3:
                score += self.weights["three"]
            elif own == 2:
                score += self.weights["two"]
            elif opp == 3:
                score -= self.weights["three"]
            elif opp == 2:
                score -= self.weights["two"]

            filled = own + opp
            if filled >= 2:
                bits = position & window if own else opponent_bits & window
                sign = 1 if own else -1
                w = bits
                while w:
                    lsb = w & (-w)
                    idx = lsb.bit_length() - 1
                    overlap_bonus[idx] += sign
                    w ^= lsb

        for delta in overlap_bonus:
            if delta > 0:
                score += (delta - 1) * self.weights["overlap"] if delta > 1 else 0
            elif delta < 0:
                score -= (abs(delta) - 1) * self.weights["overlap"] if delta < -1 else 0

        return score

    def evaluate(self, board: Board, depth: int) -> int:
        """
        Evaluate a Board object for the AI (kept for external/legacy callers).
        """

        mask, ai_bits = self._to_bitboard(board)
        human_bits = mask ^ ai_bits

        if self._has_won(ai_bits):
            return self.weights["win"] + depth
        if self._has_won(human_bits):
            return -self.weights["win"] - depth

        return self._evaluate(ai_bits, human_bits, depth)


if __name__ == "__main__":
    def _build_board(moves: list[int]) -> Board:
        """
        Build a board by playing a fixed sequence of column drops.
        """

        board = Board()

        for column in moves:
            if board.is_finished():
                break
            board.add_piece(column, board.current_player)

        return board

    boards = {
        "almost empty": _build_board([3, 2, 4]),
        "mid fill": _build_board([3, 4, 5] * 6),
        "almost finished": _build_board([0, 1, 2] * 6 + [4, 5, 6] * 6),
    }

    for label, board in boards.items():
        print(f"--- {label} ({board.count_pieces()} pieces) ---")
        print(board)

        ai = Minimax(depth=10)

        start = time.perf_counter()
        column = ai.play(board)
        elapsed = time.perf_counter() - start

        print(f"Chosen column: {column}")
        print(f"Time: {elapsed:.3f}s\n")
