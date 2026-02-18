# minmax_algo.py
import math
from game_rules import EMPTY, AI_PLAYER, HUMAN_PLAYER
from evaluation_position import evaluate_board

class MinMaxAlgo:
    def __init__(self, engine):
        self.engine = engine

    def minimax(self, depth, is_max, max_depth, alpha, beta):
        score = evaluate_board(self.engine)

        # Terminal states (Win/Loss/Tie/MaxDepth)
        if abs(score) == 1000:
            return score - depth if score > 0 else score + depth
        if not self.engine.is_moves_left() or depth >= max_depth:
            return score

        if is_max:
            best = -math.inf
            for r in range(3):
                for c in range(3):
                    if self.engine.board[r][c] == EMPTY:
                        self.engine.board[r][c] = AI_PLAYER
                        val = self.minimax(depth + 1, False, max_depth, alpha, beta)
                        self.engine.board[r][c] = EMPTY
                        best = max(best, val)
                        alpha = max(alpha, best)
                        if beta <= alpha: break
            return best
        else:
            best = math.inf
            for r in range(3):
                for c in range(3):
                    if self.engine.board[r][c] == EMPTY:
                        self.engine.board[r][c] = HUMAN_PLAYER
                        val = self.minimax(depth + 1, True, max_depth, alpha, beta)
                        self.engine.board[r][c] = EMPTY
                        best = min(best, val)
                        beta = min(beta, best)
                        if beta <= alpha: break
            return best

    def get_best_move(self, max_depth):
        best_val = -math.inf
        best_move = None
        move_scores = []

        for r in range(3):
            for c in range(3):
                if self.engine.board[r][c] == EMPTY:
                    self.engine.board[r][c] = AI_PLAYER
                    val = self.minimax(0, False, max_depth, -math.inf, math.inf)
                    self.engine.board[r][c] = EMPTY
                    
                    move_scores.append(f"({r},{c}): {val}")
                    if val > best_val:
                        best_val = val
                        best_move = (r, c)
        return best_move, move_scores
