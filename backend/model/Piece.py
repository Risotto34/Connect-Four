class Piece:
    """
    Represents a Connect Four piece.

    Allowed colors:
    - Red : 0
    - Yellow : 1
    """

    COLORS = [0, 1]

    def __init__(self, color: int, row: int = None, column: int = None) -> None:
        """
        Initialize a piece with the specified color.
        """

        if color not in self.COLORS:
            raise ValueError("A piece must be Red or Yellow.")

        self.color: int = color
        self.row: int = row
        self.column: int = column

    def get_color(self) -> int:
        """
        Return the color of the piece.
        """

        return self.color
    
    @staticmethod
    def get_opposite_color(color: int) -> int:
        """
        Return the color of the opposing player.
        """

        return (color + 1) % 2
    
    def get_coordinates(self) -> tuple[int, int]:
        """
        Return the coordinates of the piece as a tuple (row, column).
        """

        return (self.row, self.column)
    
    def __eq__(self, other: 'Piece') -> bool:
        """
        Compare two pieces based on their color and position.
        """

        if not isinstance(other, Piece):
            return False

        return (
            self.color == other.color
            and self.row == other.row
            and self.column == other.column
        )

    def __hash__(self) -> int:
        """
        Generate a hash based on the piece color and coordinates.
        """

        return hash((self.color, self.row, self.column))
    
    def copy(self):
        """
        Create a copy of the piece.
        """

        return Piece(self.color, self.row, self.column)
    
    def to_dict(self) -> dict:
        """
        Convert the piece to a dictionary for JSON serialization.
        Example:
            {
                "color": 0
            }
        """

        return {
            "color": self.color,
            "row": self.row,
            "column": self.column
        }