from .Piece import Piece


class Board:
    """
    Represents the Connect Four board.

    Board indexing:
    - Rows: 0 (top) to 5 (bottom).
    - Columns: 0 (left) to 6 (right).
    """

    ROWS: int = 6
    COLUMNS: int = 7

    def __init__(self):
        self.current_player: int = 0
        self.grid: list[list[Piece | None]] = [
            [None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)
        ]

    def add_piece(self, column: int, color: int) -> bool:
        """
        Add a Piece object into a column.

        The piece falls from the top to the lowest available position.
        """

        if column < 0 or column >= self.COLUMNS:
            return False

        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][column] is None:
                piece: Piece = Piece(color, row, column)
                self.grid[row][column] = piece
                self.current_player = Piece.get_opposite_color(self.current_player)
                return True

        return False

    def is_full(self) -> bool:
        """Check if the board is full."""

        for column in range(self.COLUMNS):
            if self.grid[0][column] is None:
                return False

        return True

    def get_horizontal_windows(self) -> list[list[Piece | None]]:
        """
        Get all horizontal windows of 4 pieces on the board.
        """

        windows = []

        for row in range(self.ROWS):
            for col in range(self.COLUMNS - 3):
                windows.append([self.grid[row][col + i] for i in range(4)])

        return windows

    def get_vertical_windows(self) -> list[list[Piece | None]]:
        """
        Get all vertical windows of 4 pieces on the board.
        """
        windows = []

        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS):
                windows.append([self.grid[row + i][col] for i in range(4)])

        return windows

    def get_diagonal_down_windows(self) -> list[list[Piece | None]]:
        """
        Get all diagonal windows of 4 pieces on the board (from top-left to bottom-right).
        """

        windows = []

        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS - 3):
                windows.append([self.grid[row + i][col + i] for i in range(4)])

        return windows

    def get_diagonal_up_windows(self) -> list[list[Piece | None]]:
        """
        Get all diagonal windows of 4 pieces on the board (from bottom-left to top-right).
        """

        windows = []

        for row in range(3, self.ROWS):
            for col in range(self.COLUMNS - 3):
                windows.append([self.grid[row - i][col + i] for i in range(4)])

        return windows

    def get_all_windows(self) -> list[list[Piece | None]]:
        """
        Get all windows of 4 pieces on the board (horizontal, vertical, and diagonal).
        """

        return (
            self.get_horizontal_windows()
            + self.get_vertical_windows()
            + self.get_diagonal_down_windows()
            + self.get_diagonal_up_windows()
        )

    def check_win(self, color: int) -> bool:
        """
        Check if a player has four pieces in a row.
        """

        for window in self.get_all_windows():
            if all(
                piece is not None and piece.get_color() == color for piece in window
            ):
                return True

        return False

    def is_finished(self) -> bool:
        """
        Check if the game is finished (either a win or a draw).
        """

        return (
            self.is_full()
            or self.check_win(self.current_player)
            or self.check_win(Piece.get_opposite_color(self.current_player))
        )

    def column_is_full(self, column: int) -> bool:
        """
        Check if a column is full.
        """

        if column < 0 or column >= self.COLUMNS:
            raise ValueError("Column index out of bounds.")

        return self.grid[0][column] is not None

    def get_valid_columns(self) -> list[int]:
        """
        Return a list of valid columns where a piece can be added.
        """

        valid_columns = []

        for column in range(self.COLUMNS):
            if not self.column_is_full(column):
                valid_columns.append(column)

        return valid_columns

    def copy(self):
        """
        Create a copy of the board.
        """

        new_board = Board()

        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                piece = self.grid[row][col]

                if piece is not None:
                    new_board.grid[row][col] = piece.copy()

        new_board.current_player = self.current_player

        return new_board

    def to_dict(self):
        """
        Convert the board state to a dictionary for JSON serialization.
        Exemple:
            {
                "board": [
                    [None, "0", None, "1", None, None, None],
                    ...
                    [None, "1", None, "0", "1", "1", None]
                ],
                "currentPlayer": "0"
            }
        """

        return {
            "board": [
                [None if piece is None else piece.get_color() for piece in row]
                for row in self.grid
            ],
            "currentPlayer": self.current_player,
        }
