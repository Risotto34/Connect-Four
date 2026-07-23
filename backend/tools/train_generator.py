from collections import Counter
import os
import joblib


from ..model.Board import Board
from .board_generator import generate_random_board
from tqdm import tqdm


def generate_training_data(iterations: int) -> tuple[list[list[int]], list[int]]:
    """
    Generate a training set of random boards and their corresponding best moves.

    iterations : number of samples to generate
    """

    X = []
    Y = []

    # Use the AI to determine the best move for each random board
    from ..model.ai.Minimax import Minimax

    ai_model = Minimax(depth=4)

    for _ in tqdm(range(iterations), desc="Generating training data"):
        board = generate_random_board(allow_finished=False)

        best_move = ai_model.play(board)

        X.append(board.as_list())
        Y.append(best_move)

    return X, Y


def generate_training_file(path: str, iterations: int) -> None:
    """
    Generate a training set of random boards and their corresponding best moves,
    and save them to a file.

    path : path to save the training set
    iterations : number of samples to generate
    """

    if os.path.exists(path):
        raise FileExistsError(f"File already exists: {path}")

    X, Y = generate_training_data(iterations)

    joblib.dump((X, Y), path)


def read_training_file(path: str) -> None:
    """
    Read a training file and display basic information.

    path: path to the training file
    """

    X, Y = joblib.load(path)

    print(f"Number of samples: {len(X)}")

    # Distribution des coups
    print("\n=== Distribution of Y ===")

    move_counts = Counter(Y)
    total = len(Y)

    for column in range(Board.COLUMNS):
        count = move_counts.get(column, 0)
        percentage = 100 * count / total
        print(f"Column {column}: {count:5d} ({percentage:6.2f}% )")

    # Distribution du nombre de pièces
    print("\n=== Distribution of number of pieces ===")

    piece_counts = Counter()

    for board in X:
        # Si les cases vides valent 0
        nb_pieces = sum(cell != 0 for cell in board)
        piece_counts[nb_pieces] += 1

    for nb in sorted(piece_counts):
        count = piece_counts[nb]
        percentage = 100 * count / total
        print(f"{nb:2d} pieces: {count:5d} ({percentage:6.2f}% )")


if __name__ == "__main__":
    generate_training_file(path="backend/resources/train_set.pkl", iterations=1000000)
    #generate_training_file(path="backend/resources/test_set.pkl", iterations=10000)
    #read_training_file(path="backend/resources/train_set.pkl")
    # read_training_file(path="backend/resources/test_set.pkl")
