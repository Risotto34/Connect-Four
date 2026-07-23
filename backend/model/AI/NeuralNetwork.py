import os
import numpy as np
import joblib

from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier

from ..AI import AI
from ..Board import Board


class NeuralNetwork(AI):
    """
    Represents a Connect Four AI using a neural network.
    """

    def __init__(self, model_path: str = "backend/resources/brain.pkl", verbose: bool = False):
        self.model_path = model_path

        self.model = MLPClassifier(
            hidden_layer_sizes=(64, 64),
            learning_rate_init=0.0001,
            max_iter=10000,
            n_iter_no_change=100,
            activation="relu",
            solver="adam",
            random_state=42,
            verbose=verbose
        )

    def train(self, training_data_path: str = "backend/resources/train_set.pkl"):
        """
        Train the neural network.

        X : list of boards
        Y : list of chosen columns
        """

        X, Y = joblib.load(training_data_path)

        if len(X) == 0 or len(Y) == 0:
            raise ValueError("Training data is empty.")

        self.model.fit(X, Y)

        joblib.dump(self.model, self.model_path)

    def load(self):
        """
        Load a trained model.
        """

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}")

        self.model = joblib.load(self.model_path)

    def evaluate(self, train_data_file: str = "backend/resources/train_set.pkl", test_data_path: str = "backend/resources/test_set.pkl"):
        """
        Evaluate the neural network on test data.
        """

        X_train, Y_train = joblib.load(train_data_file)
        X_test, Y_test = joblib.load(test_data_path)

        if len(X_test) == 0 or len(Y_test) == 0:
            raise ValueError("Test data is empty.")

        predictions = self.model.predict(X_test)

        print("Train accuracy:", self.model.score(X_train, Y_train))
        print("Test accuracy:", self.model.score(X_test, Y_test))

        print("\nConfusion matrix:")
        print(confusion_matrix(Y_test, predictions))

    def play(self, board: Board) -> int:
        """
        Choose a column using the neural network.
        """

        X = board.as_list()

        prediction = self.model.predict([X])

        column = int(prediction[0])

        return column


if __name__ == "__main__":
    nn = NeuralNetwork(verbose=True)
    #nn.load()
    nn.train()
    nn.evaluate()