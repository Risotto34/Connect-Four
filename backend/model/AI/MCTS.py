import math
import random

from .AI import AI
from ..Piece import Piece
from ..Board import Board


class MCTSNode:
    """
    Represents a state in the Monte Carlo Tree Search tree.

    Each node stores a board position, its connection to the
    previous node, the explored moves, and statistics used
    to evaluate the quality of the position.
    """

    def __init__(self, board: Board, parent: "MCTSNode" = None, column: int = None):
        """
        Creates a node representing a specific board state.

        The node keeps track of unexplored moves so that the
        search algorithm can progressively build the tree.
        """

        self.board: Board = board
        self.parent: "MCTSNode" = parent
        self.column: int = column

        self.children: list["MCTSNode"] = []
        self.visits: int = 0
        self.wins: int = 0
        self.untried_columns: list[int] = board.get_valid_columns()

    def is_fully_expanded(self) -> bool:
        """
        Checks whether all possible moves from this position
        have already been added to the search tree.
        """

        return len(self.untried_columns) == 0


class MCTS(AI):
    """
    Represents a Connect Four AI using the Monte Carlo Tree Search algorithm.

    The algorithm improves its decisions by repeatedly exploring
    possible moves, playing random simulations, and updating
    the tree according to the results.
    """

    def __init__(self, iterations: int = 50000):
        """
        Initializes the MCTS algorithm and defines the number
        of simulations used to search for the best move.
        """
         
        self.iterations: int = iterations
        self.ai_color: str = None
        self.human_color: str = None

    def selection(self, node: MCTSNode) -> MCTSNode:
        """
        Navigates through the existing search tree by selecting
        the most promising children using the UCT strategy.

        The process continues until reaching a node where
        new possibilities can be explored.
        """
         
        while node.is_fully_expanded() and node.children:
            node: MCTSNode = self.best_child(node)
        return node

    def expansion(self, node: MCTSNode) -> MCTSNode:
        """
        Expands the search tree by creating a new child from
        a move that has not been explored yet.

        The selected move is played on a copied board so that
        the new game state can be tested independently.
        """

        column: int = random.choice(node.untried_columns)
        node.untried_columns.remove(column)

        new_board: Board = node.board.copy()
        new_board.add_piece(column, new_board.current_player)

        child: MCTSNode = MCTSNode(new_board, node, column)
        node.children.append(child)
        return child

    def simulation(self, board: Board) -> int:
        """
        Performs a random game simulation from the current position.

        The algorithm plays random moves until the game ends,
        then evaluates the final result to determine whether
        the explored move was successful.
        """

        simulation: Board = board.copy()

        while not simulation.is_finished():
            column: int = random.choice(simulation.get_valid_columns())
            simulation.add_piece(column, simulation.current_player)

        if simulation.check_win(self.ai_color):
            return 1

        if simulation.check_win(self.human_color):
            return -1

        return 0

    def backpropagation(self, node: MCTSNode, result: int):
        """
        Updates the statistics of every node involved in the
        simulation path.

        The result of the simulation is propagated back to the
        root so that future searches can favor better moves.
        """
        
        while node:

            node.visits += 1

            if result == 1:
                node.wins += 5
            elif result == 0:
                node.wins += 1

            node = node.parent

    def best_child(self, node: MCTSNode, exploration: float = math.sqrt(2)) -> MCTSNode:
        """
        Selects the most promising child according to the UCT formula.

        This balances moves that already performed well with
        moves that have not been explored enough yet.
        """

        return max(
            node.children,
            key=lambda child: (child.wins / child.visits)
            + exploration * math.sqrt(math.log(node.visits) / child.visits),
        )

    def play(self, board):
        """
        Searches for the best move by repeatedly applying
        the four steps of MCTS:

        - Selection: find a promising position.
        - Expansion: explore a new possibility.
        - Simulation: test the move through a random game.
        - Backpropagation: update the tree with the result.

        After many simulations, the most explored move
        is chosen as the AI decision.
        """

        self.ai_color = board.current_player
        self.human_color = Piece.get_opposite_color(self.ai_color)

        root: MCTSNode = MCTSNode(board.copy())

        for _ in range(self.iterations):

            node: MCTSNode = self.selection(root)
            if not node.board.is_finished():
                node: MCTSNode = self.expansion(node)
            result: int = self.simulation(node.board)
            self.backpropagation(node, result)

        best: MCTSNode = max(root.children, key=lambda c: c.visits)

        return best.column
