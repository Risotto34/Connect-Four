class Piece:
    """
    Represents a Connect Four piece.

    Allowed colors:
    - Red
    - Yellow
    """

    COLORS = ["Red", "Yellow"]

    def __init__(self, color: str) -> None:
        if color not in self.COLORS:
            raise ValueError("A piece must be Red or Yellow.")

        self.color: str = color

    def get_color(self) -> str:
        return self.color