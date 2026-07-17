class Piece:
    """
    Represents a Connect Four piece.

    Allowed colors:
    - Red : 0
    - Yellow : 1
    """

    COLORS = [0, 1]

    def __init__(self, color: int) -> None:
        if color not in self.COLORS:
            raise ValueError("A piece must be Red or Yellow.")

        self.color: int = color

    def get_color(self) -> int:
        return self.color
    
    def to_dict(self) -> dict:
        return {
            "color": self.color
        }