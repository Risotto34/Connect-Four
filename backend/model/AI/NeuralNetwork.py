import numpy as np
import joblib

from sklearn.neural_network import MLPClassifier

from ..AI import AI
from ..Piece import Piece
from ..Board import Board


class NeuralNetwork(AI):
    """
    Represents a Connect Four AI using a neural network.
    """

    def __init__(self, model_path: str = "brain.pkl"):
        self.model_path = model_path

        self.model = MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation="relu",
            solver="adam",
            max_iter=1000,
            random_state=42,
        )

        self.ai_color = None

    def train(self, X, Y):
        """
        Train the neural network.

        X : list of boards
        Y : list of chosen columns
        """

        self.model.fit(X, Y)

        joblib.dump(self.model, self.model_path)

    def load(self):
        """
        Load a trained model.
        """

        self.model = joblib.load(self.model_path)

    def play(self, board: Board) -> int:
        """
        Choose a column using the neural network.
        """

        self.ai_color = board.current_player

        X = self.board_to_input(board)

        prediction = self.model.predict([X])

        column = int(prediction[0])

        # Sécurité si le réseau choisit une colonne impossible
        if column not in board.get_valid_columns():

            probabilities = self.model.predict_proba([X])[0]

            # Trie les colonnes par probabilité décroissante
            choices = np.argsort(probabilities)[::-1]

            for choice in choices:
                if choice in board.get_valid_columns():
                    return int(choice)

        return column

    def board_to_input(self, board: Board):
        """
        Convert board into neural network input.

        Own pieces     = 1
        Enemy pieces   = -1
        Empty          = 0
        """

        inputs = []

        for row in range(board.ROWS):

            for column in range(board.COLUMNS):

                piece = board.grid[row][column]

                if piece is None:
                    inputs.append(0)

                elif piece.get_color() == self.ai_color:
                    inputs.append(1)

                else:
                    inputs.append(-1)

        return inputs
