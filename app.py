"""Flask API and web application for the Tic-Tac-Toe AI visualizer."""

from flask import Flask, jsonify, render_template, request

from agent import HeuristicAgent, MinimaxAgent, RandomAgent, simulate_match
from game import PLAYER_O, PLAYER_X, TicTacToe

app = Flask(__name__)
AGENT_TYPES = {
    "easy": RandomAgent,
    "medium": HeuristicAgent,
    "hard": MinimaxAgent,
}


def _json_payload():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None
    return payload


def _game_from_payload(payload, player_key="player"):
    board = payload.get("board")
    player = payload.get(player_key, payload.get("current_player", PLAYER_X))
    if board is None:
        raise ValueError("board is required")
    game = TicTacToe(board=board, current_player=player)
    x_count = game.board.count(PLAYER_X)
    o_count = game.board.count(PLAYER_O)
    if x_count not in (o_count, o_count + 1):
        raise ValueError("board has an impossible number of X and O moves")
    if not game.is_game_over():
        expected_player = PLAYER_X if x_count == o_count else PLAYER_O
        if player != expected_player:
            raise ValueError(f"it is {expected_player}'s turn")
    elif game.winner == PLAYER_X and x_count != o_count + 1:
        raise ValueError("board has an impossible X win")
    elif game.winner == PLAYER_O and x_count != o_count:
        raise ValueError("board has an impossible O win")
    return game


def _game_response(game):
    return {
        "board": game.board,
        "current_player": game.current_player,
        "winner": game.check_winner(),
        "winning_line": game.get_winning_line(),
        "draw": game.is_draw(),
        "game_over": game.is_game_over(),
        "legal_moves": game.get_available_moves(),
    }


def _error(message, status=400):
    return jsonify({"error": message}), status


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/reset", methods=["POST"])
def reset_game():
    return jsonify(_game_response(TicTacToe()))


@app.route("/api/move", methods=["POST"])
def make_move():
    payload = _json_payload()
    if payload is None:
        return _error("a JSON object is required")
    try:
        game = _game_from_payload(payload)
    except (TypeError, ValueError) as error:
        return _error(str(error))

    position = payload.get("position")
    player = payload.get("player", game.current_player)
    if not game.make_move(position, player=player):
        return _error("illegal move")
    return jsonify(_game_response(game))


@app.route("/api/ai_move", methods=["POST"])
def ai_move():
    payload = _json_payload()
    if payload is None:
        return _error("a JSON object is required")
    try:
        game = _game_from_payload(payload, player_key="current_player")
    except (TypeError, ValueError) as error:
        return _error(str(error))

    difficulty = payload.get("difficulty", "hard")
    if not isinstance(difficulty, str) or difficulty not in AGENT_TYPES:
        return _error("difficulty must be 'easy', 'medium', or 'hard'")
    agent = AGENT_TYPES[difficulty](player=game.current_player)
    move = agent.get_move(game)
    if move is None:
        return _error("there are no legal moves", 409)
    if not game.make_move(move, player=agent.player):
        return _error("AI selected an illegal move", 500)

    response = _game_response(game)
    response.update({
        "move": move,
        "difficulty": difficulty,
        "nodes_evaluated": agent.nodes_evaluated,
        "move_scores": [agent.move_scores.get(position) for position in range(9)],
    })
    return jsonify(response)


@app.route("/api/benchmark", methods=["POST"])
def benchmark():
    payload = _json_payload()
    if payload is None:
        return _error("a JSON object is required")

    games = payload.get("games", 10)
    if isinstance(games, bool) or not isinstance(games, int) or not 1 <= games <= 500:
        return _error("games must be an integer between 1 and 500")
    agent1_type = payload.get("agent1", "hard")
    agent2_type = payload.get("agent2", "easy")
    if (
        not isinstance(agent1_type, str)
        or agent1_type not in AGENT_TYPES
        or not isinstance(agent2_type, str)
        or agent2_type not in AGENT_TYPES
    ):
        return _error("agents must be 'easy', 'medium', or 'hard'")

    agent1 = AGENT_TYPES[agent1_type](player=PLAYER_X)
    agent2 = AGENT_TYPES[agent2_type](player=PLAYER_O)
    results = simulate_match(agent1, agent2, num_games=games)
    results.update({
        "games": games,
        "agent1": agent1_type,
        "agent2": agent2_type,
        "agent1_win_rate": results["agent1_wins"] / games,
        "agent2_win_rate": results["agent2_wins"] / games,
        "draw_rate": results["draws"] / games,
    })
    return jsonify(results)


if __name__ == "__main__":
    app.run()
