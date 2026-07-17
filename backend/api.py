from flask import Flask, render_template, jsonify, request
import os
import json


from .model.Board import Board
from .model.Piece import Piece

from .model.AI.Random import Random
from .model.AI.Minimax import Minimax

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

current_ai = None


# ----------------------
# Functions
# ----------------------


def play(column: int) -> bool:
    """
    Play a piece in the specified column.
    """

    piece = Piece(board.current_player)

    if not board.add_piece(column, piece):
        return jsonify({"success": False, "message": "Column is full."})

    winner = board.check_win(piece)
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
    """

    column = current_ai.play(board)

    return play(column)


@app.post("/api/choose-ai")
def choose_ai():
    """
    Choose the AI to play against.
    Request body:
    {
        "ai": "random"
    }
    """

    data = request.get_json()
    ai_type = data["ai"]

    global current_ai

    match ai_type:
        case "random":
            current_ai = Random()
        case "minimax":
            current_ai = Minimax(Piece(board.current_player))
        case _:
            return jsonify({"success": False, "message": "Invalid AI type."})
    return jsonify({"success": True})


@app.get("/api/ais")
def get_ais():
    """
    Return the list of available AIs.
    """

    return jsonify(AI_REGISTRY)
