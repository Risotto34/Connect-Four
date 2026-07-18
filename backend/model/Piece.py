class Piece:
    """
    Represents a Connect Four piece.

    Allowed colors:
    - Red : 0
    - Yellow : 1
    """

    COLORS = [0, 1]

    def __init__(self, color: int) -> None:
        """
        Initialize a piece with the specified color.
        """

        if color not in self.COLORS:
            raise ValueError("A piece must be Red or Yellow.")

        self.color: int = color

    def get_color(self) -> int:
        """
        Return the color of the piece.
        """

        return self.color
    
    def get_adverse_color(self) -> int:
        """
        Return the color of the opposing player.
        """

        return (self.color + 1) % 2
    
    def get_adverse_piece(self) -> "Piece":
        """
        Return a Piece object of the opposing player.
        """

        return Piece(self.get_adverse_color())
    
    def to_dict(self) -> dict:
        """
        Convert the piece to a dictionary for JSON serialization.
        Example:
            {
                "color": 0
            }
        """

        return {
            "color": self.color
        }