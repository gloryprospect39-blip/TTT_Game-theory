"""Random, heuristic, and minimax Tic-Tac-Toe agents."""

import random

from game import EMPTY, PLAYER_O, PLAYER_X, WINNING_LINES, TicTacToe


def _opponent(player):
    return PLAYER_O if player == PLAYER_X else PLAYER_X


class RandomAgent:
    """Choose uniformly from the currently legal moves."""

    def __init__(self, player=PLAYER_X):
        if player not in (PLAYER_X, PLAYER_O):
            raise ValueError("player must be 'X' or 'O'")
        self.player = player
        self.nodes_evaluated = 0
        self.move_scores = {}

    def get_move(self, game):
        legal_moves = game.get_available_moves()
        self.move_scores = {move: None for move in legal_moves}
        self.nodes_evaluated = len(legal_moves)
        if game.current_player != self.player or not legal_moves:
            return None
        return random.choice(legal_moves)


class HeuristicAgent:
    """Prioritize wins, blocks, the center, corners, then edges."""

    MOVE_PRIORITY = (4, 0, 2, 6, 8, 1, 3, 5, 7)

    def __init__(self, player=PLAYER_X):
        if player not in (PLAYER_X, PLAYER_O):
            raise ValueError("player must be 'X' or 'O'")
        self.player = player
        self.nodes_evaluated = 0
        self.move_scores = {}

    @staticmethod
    def _has_winner(board, player):
        return any(
            board[a] == board[b] == board[c] == player
            for a, b, c in WINNING_LINES
        )

    def _winning_move(self, game, player):
        for move in game.get_available_moves():
            board = game.board.copy()
            board[move] = player
            if self._has_winner(board, player):
                return move
        return None

    def get_move(self, game):
        legal_moves = game.get_available_moves()
        self.nodes_evaluated = len(legal_moves)
        self.move_scores = {}
        if game.current_player != self.player or not legal_moves:
            return None

        opponent = _opponent(self.player)
        winning_move = self._winning_move(game, self.player)
        blocking_move = self._winning_move(game, opponent)

        for move in legal_moves:
            if move == winning_move:
                score = 5
            elif move == blocking_move:
                score = 4
            else:
                score = 3 if move == 4 else 2 if move in (0, 2, 6, 8) else 1
            self.move_scores[move] = score

        return max(
            legal_moves,
            key=lambda move: (self.move_scores[move], -self.MOVE_PRIORITY.index(move)),
        )


class MinimaxAgent:
    """Search the complete game tree, optionally pruning with alpha-beta."""

    MOVE_PRIORITY = HeuristicAgent.MOVE_PRIORITY

    def __init__(self, player=PLAYER_O, use_alpha_beta=True):
        if player not in (PLAYER_X, PLAYER_O):
            raise ValueError("player must be 'X' or 'O'")
        self.player = player
        self.use_alpha_beta = use_alpha_beta
        self.nodes_evaluated = 0
        self.move_scores = {}

    def _terminal_score(self, game, depth):
        winner = game.check_winner()
        if winner == self.player:
            return 10 - depth
        if winner is not None:
            return depth - 10
        return 0

    def _minimax(self, game, depth, alpha, beta):
        self.nodes_evaluated += 1
        if game.is_game_over():
            return self._terminal_score(game, depth)

        maximizing = game.current_player == self.player
        best_score = float("-inf") if maximizing else float("inf")
        for move in game.get_available_moves():
            next_game = game.clone()
            next_game.make_move(move)
            score = self._minimax(next_game, depth + 1, alpha, beta)
            if maximizing:
                best_score = max(best_score, score)
                if self.use_alpha_beta:
                    alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, score)
                if self.use_alpha_beta:
                    beta = min(beta, best_score)
            if self.use_alpha_beta and alpha >= beta:
                break
        return best_score

    def get_move(self, game):
        legal_moves = game.get_available_moves()
        self.nodes_evaluated = 0
        self.move_scores = {}
        if game.current_player != self.player or not legal_moves:
            return None

        # Give each candidate a full window so its displayed score is exact,
        # while still allowing alpha-beta cutoffs within that candidate tree.
        for move in sorted(legal_moves, key=self.MOVE_PRIORITY.index):
            next_game = game.clone()
            next_game.make_move(move)
            self.move_scores[move] = self._minimax(
                next_game,
                depth=1,
                alpha=float("-inf"),
                beta=float("inf"),
            )

        return max(
            legal_moves,
            key=lambda move: (self.move_scores[move], -self.MOVE_PRIORITY.index(move)),
        )


def simulate_match(agent1, agent2, num_games=1):
    """Play complete games and return win/draw counts for both agents."""
    if isinstance(num_games, bool) or not isinstance(num_games, int) or num_games < 0:
        raise ValueError("num_games must be a non-negative integer")
    if agent1.player == agent2.player:
        raise ValueError("agents must play different symbols")

    results = {"agent1_wins": 0, "agent2_wins": 0, "draws": 0}
    agents = {agent1.player: agent1, agent2.player: agent2}

    for _ in range(num_games):
        game = TicTacToe()
        while not game.is_game_over():
            agent = agents[game.current_player]
            move = agent.get_move(game)
            if move is None or not game.make_move(move, agent.player):
                raise RuntimeError(
                    f"{type(agent).__name__} returned an illegal move: {move!r}"
                )

        winner = game.check_winner()
        if winner == agent1.player:
            results["agent1_wins"] += 1
        elif winner == agent2.player:
            results["agent2_wins"] += 1
        else:
            results["draws"] += 1

    return results
