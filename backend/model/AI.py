from abc import ABC, abstractmethod

from .Board import Board


class AI(ABC):
    """
    Abstract base class for Connect Four AIs.
    """

    @abstractmethod
    def play(self, board: Board) -> int:
        """
        Choose a column to play.

        Must be implemented by subclasses.
        """
        pass