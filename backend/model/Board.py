from Piece import Piece


class Board:
    """
    Represents the Connect Four board.

    Board indexing:
    - Rows: 0 (top) to 5 (bottom).
    - Columns: 0 (left) to 6 (right).
    """

    def __init__(self):
        self.rows: int = 6
        self.columns: int = 7
        self.grid: list[list[Piece | None]] = [[None for _ in range(self.columns)] for _ in range(self.rows)]

    def display(self):
        """Display the board."""

        print("\n  1 2 3 4 5 6 7")

        for row in self.grid:
            print("| ", end="")

            for piece in row:
                if piece is None:
                    print(" ", end=" ")
                else:
                    print(piece, end=" ")

            print("|")

        print("-" * 17)

    def add_piece(self, column: int, piece: Piece) -> bool:
        """
        Add a Piece object into a column.

        The piece falls from the top to the lowest available position.
        """

        if column < 0 or column >= self.columns:
            return False

        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column] is None:
                self.grid[row][column] = piece
                return True

        return False

    def is_full(self) -> bool:
        """Check if the board is full."""

        for column in range(self.columns):
            if self.grid[0][column] is None:
                return False

        return True

    def check_win(self, piece: Piece) -> bool:
        """
        Check if a player has four pieces in a row.
        """

        color: str = piece.get_color()

        # Horizontal
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if all(
                    self.grid[row][col + i] is not None
                    and self.grid[row][col + i].get_color() == color
                    for i in range(4)
                ):
                    return True

        # Vertical
        for row in range(self.rows - 3):
            for col in range(self.columns):
                if all(
                    self.grid[row + i][col] is not None
                    and self.grid[row + i][col].get_color() == color
                    for i in range(4)
                ):
                    return True

        # Diagonal \
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(
                    self.grid[row + i][col + i] is not None
                    and self.grid[row + i][col + i].get_color() == color
                    for i in range(4)
                ):
                    return True

        # Diagonal /
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(
                    self.grid[row - i][col + i] is not None
                    and self.grid[row - i][col + i].get_color() == color
                    for i in range(4)
                ):
                    return True

        return False
