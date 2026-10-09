"""Core Tic-Tac-Toe game engine."""

PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "
PLAYERS = (PLAYER_X, PLAYER_O)
WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class TicTacToe:
    """Represent a 3x3 board, turn state, and reversible move history."""

    def __init__(self, board=None, current_player=PLAYER_X):
        if current_player not in PLAYERS:
            raise ValueError("current_player must be 'X' or 'O'")
        if board is None:
            self.board = [EMPTY] * 9
        else:
            if len(board) != 9 or any(cell not in (PLAYER_X, PLAYER_O, EMPTY) for cell in board):
                raise ValueError("board must contain exactly 9 valid cells")
            self.board = list(board)
        self.current_player = current_player
        self.move_history = []
        self.winner = None
        self.winning_line = None
        self._refresh_state()

    def _refresh_state(self):
        self.winner = self.check_winner()
        self.winning_line = self._compute_winning_line() if self.winner is not None else None

    def clone(self):
        cloned = TicTacToe(board=self.board, current_player=self.current_player)
        cloned.move_history = self.move_history.copy()
        return cloned

    def get_available_moves(self):
        if self.is_game_over():
            return []
        return [idx for idx, cell in enumerate(self.board) if cell == EMPTY]

    def is_valid_move(self, pos, player=None):
        if isinstance(pos, bool) or not isinstance(pos, int) or not 0 <= pos < 9:
            return False
        if self.board[pos] != EMPTY or self.is_game_over():
            return False
        if player is not None and player != self.current_player:
            return False
        return True

    def make_move(self, pos, player=None):
        player = self.current_player if player is None else player
        if player not in PLAYERS or not self.is_valid_move(pos, player):
            return False
        self.board[pos] = player
        self.move_history.append((pos, player))
        self._refresh_state()
        if self.winner is None and not self.is_draw():
            self.current_player = PLAYER_O if player == PLAYER_X else PLAYER_X
        return True

    def undo_move(self, pos):
        if isinstance(pos, bool) or not isinstance(pos, int) or not 0 <= pos < 9:
            return False
        if self.board[pos] == EMPTY:
            return False

        for history_index in range(len(self.move_history) - 1, -1, -1):
            if self.move_history[history_index][0] == pos:
                removed_moves = self.move_history[history_index:]
                for move_pos, _ in removed_moves:
                    self.board[move_pos] = EMPTY
                self.current_player = removed_moves[0][1]
                del self.move_history[history_index:]
                self._refresh_state()
                return True

        removed_player = self.board[pos]
        self.board[pos] = EMPTY
        self.current_player = removed_player
        self._refresh_state()
        return True

    def check_winner(self):
        for line in WINNING_LINES:
            a, b, c = line
            first = self.board[a]
            if first != EMPTY and first == self.board[b] == self.board[c]:
                return first
        return None

    def get_winning_line(self):
        return self._compute_winning_line() if self.winner is not None else None

    def _compute_winning_line(self):
        for line in WINNING_LINES:
            a, b, c = line
            first = self.board[a]
            if first != EMPTY and first == self.board[b] == self.board[c]:
                return line
        return None

    def is_draw(self):
        return self.check_winner() is None and all(cell != EMPTY for cell in self.board)

    def is_game_over(self):
        return self.winner is not None or self.is_draw()

    def __str__(self):
        return "\n".join(
            " | ".join(self.board[idx:idx + 3])
            for idx in range(0, 9, 3)
        )
