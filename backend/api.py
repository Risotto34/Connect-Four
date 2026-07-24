from flask import Flask, render_template, jsonify, request
import os
import json


from .model.Board import Board
from .model.Piece import Piece


from .model.AI import AI
from .model.ai.Random import Random
from .model.ai.Minimax import Minimax
from .model.ai.MCTS import MCTS
from .model.ai.NeuralNetwork import NeuralNetwork


# ----------------------
# App
# ----------------------


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend/templates"),
    static_folder=os.path.join(BASE_DIR, "frontend/static"),
)


def start():
    app.run(host="0.0.0.0", port=5000, debug=True)


# ----------------------
# Variables
# ----------------------

with open(os.path.join(BASE_DIR, "backend/registry.json"), "r") as file:
    AI_REGISTRY = json.load(file)

board = Board()

current_ai_0: AI = None
current_ai_1: AI = None


# ----------------------
# Functions
# ----------------------


def play(column: int) -> bool:
    """
    Play a piece in the specified column.
    """

    color = board.current_player

    if not board.add_piece(column, color):
        return jsonify({"success": False, "message": "Column is full."})

    winner = board.check_win(color)
    draw = board.is_full()

    return jsonify(
        {"success": True, "winner": winner, "draw": draw, "board": board.to_dict()}
    )


# ----------------------
# Pages
# ----------------------


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/game")
def game():
    return render_template("game.html")


# ----------------------
# API
# ----------------------


@app.get("/api/board")
def get_board():
    """
    Return the current board.
    """

    return jsonify(board.to_dict())


@app.post("/api/new-game")
def new_game():
    """
    Start a new game.
    """

    global board

    board = Board()

    return jsonify({"success": True})


@app.post("/api/user-play")
def user_play():
    """
    User plays a piece in the specified column.
    Request body:
    {
        "column": 0
    }
    """

    data = request.get_json()
    column = data["column"]

    return play(column)


@app.post("/api/ai-play")
def ai_play():
    """
    AI plays a piece.
    Request body:
    {
        "number": 0
    }
    """

    data = request.get_json()
    number = data["number"]
    column = None

    if number == 0:
        column = current_ai_0.play(board)
    elif number == 1:
        column = current_ai_1.play(board)

    return play(column)


@app.post("/api/choose-ai")
def choose_ai():
    """
    Choose the AI to play against.
    Request body:
    {
        "ai": "random",
        "number": 0
    }
    """

    data = request.get_json()
    ai_type = data["ai"]
    number = data["number"]

    global current_ai_0, current_ai_1
    ai = None

    match ai_type:
        case "random":
            ai = Random()
        case "minimax":
            ai = Minimax(depth=10)
        case "mcts":
            ai = MCTS(iterations=50000)
        case "neuralnetwork":
            ai = NeuralNetwork()
            ai.load()
        case _:
            return jsonify({"success": False, "message": "Invalid AI type."})

    if number == 0:
        current_ai_0 = ai
    elif number == 1:
        current_ai_1 = ai

    return jsonify({"success": True})


@app.get("/api/current-player")
def get_current_player():
    """
    Return the current player.
    """

    return jsonify({"current_player": board.current_player})


@app.get("/api/ais")
def get_ais():
    """
    Return the list of available AIs.
    """

    return jsonify(AI_REGISTRY)
