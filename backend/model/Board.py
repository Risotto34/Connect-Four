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
        self.grid: list[list[Piece | None]] = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]

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

        if column < 0 or column >= self.COLUMNS:
            return False

        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][column] is None:
                self.grid[row][column] = piece
                self.current_player = (self.current_player + 1) % 2
                return True

        return False

    def is_full(self) -> bool:
        """Check if the board is full."""

        for column in range(self.COLUMNS):
            if self.grid[0][column] is None:
                return False

        return True
    

    def check_win(self, piece: Piece) -> bool:
        """
        Check if a player has four pieces in a row.
        """

        color: str = piece.get_color()

        # Horizontal
        for row in range(self.ROWS):
            for col in range(self.COLUMNS - 3):
                if all(
                    self.grid[row][col + i] is not None
                    and self.grid[row][col + i].get_color() == color
                    for i in range(4)
                ):
                    return True

        # Vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS):
                if all(
                    self.grid[row + i][col] is not None
                    and self.grid[row + i][col].get_color() == color
                    for i in range(4)
                ):
                    return True

        # Diagonal \
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS - 3):
                if all(
                    self.grid[row + i][col + i] is not None
                    and self.grid[row + i][col + i].get_color() == color
                    for i in range(4)
                ):
                    return True

        # Diagonal /
        for row in range(3, self.ROWS):
            for col in range(self.COLUMNS - 3):
                if all(
                    self.grid[row - i][col + i] is not None
                    and self.grid[row - i][col + i].get_color() == color
                    for i in range(4)
                ):
                    return True

        return False
    
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
    
    def copy_board(self):
        """
        Create a copy of the board.
        """

        new_board = Board()

        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                piece = self.grid[row][col]

                if piece is not None:
                    new_board.grid[row][col] = Piece(piece.get_color())

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
                [
                    None if piece is None else piece.get_color()
                    for piece in row
                ]
                for row in self.grid
            ],
            "currentPlayer": self.current_player
        }