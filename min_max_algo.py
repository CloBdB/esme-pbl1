# minmax_algo.py
import math
from game_rules import EMPTY, AI_PLAYER, HUMAN_PLAYER
from evaluation_position import evaluate_board

class MinMaxAlgo:
    def __init__(self, engine):
        self.engine = engine

    def minimax(self, depth, is_max, max_depth, alpha, beta):
        """
        Recursively calculates the best score for a move using the Minimax algorithm 
        with Alpha-Beta pruning.
        """
        score = evaluate_board(self.engine)

        if abs(score) == 1000:                                                              # Terminal states (Win/Loss/Tie/MaxDepth)
            return score - depth if score > 0 else score + depth                            # Adjust score by depth to favor faster wins or longer survival
        
        if not self.engine.is_moves_left() or depth >= max_depth:                           # Base case: no moves left or reached the search limit
            return score

        if is_max:
            best = -math.inf                                                                # Floating-point negative infinity
            for r in range(3):
                for c in range(3):
                    if self.engine.board[r][c] == EMPTY:
                        self.engine.board[r][c] = AI_PLAYER                                 # Simulate move
                        val = self.minimax(depth + 1, False, max_depth, alpha, beta)            
                        self.engine.board[r][c] = EMPTY                                     # Undo move (Backtrack)
                        best = max(best, val)
                        alpha = max(alpha, best)                                            # Update lower bound
                        
                        if beta <= alpha:                                                   # Alpha-Beta Pruning
                            break
            return best
        else:
            best = math.inf                                                                 # Floating-point positive infinity
            for r in range(3):
                for c in range(3):
                    if self.engine.board[r][c] == EMPTY:
                        self.engine.board[r][c] = HUMAN_PLAYER                              # Simulate move
                        val = self.minimax(depth + 1, True, max_depth, alpha, beta)
                        self.engine.board[r][c] = EMPTY                                     # Undo move
                        best = min(best, val)
                        beta = min(beta, best)                                              # Update upper bound
                        
                        if beta <= alpha:                                                   # Alpha-Beta Pruning
                            break
            return best

    def get_best_move(self, max_depth):
        """
        Evaluates all possible immediate moves and returns the optimal move 
        along with a list of scores for debugging/analysis.
        """
        best_val = -math.inf
        best_move = None
        move_scores = []

        for r in range(3):
            for c in range(3):
                if self.engine.board[r][c] == EMPTY:
                    self.engine.board[r][c] = AI_PLAYER                                     # Try a move
                    val = self.minimax(0, False, max_depth, -math.inf, math.inf)            # Evaluate this move using minimax starting at depth 0
                    self.engine.board[r][c] = EMPTY                                         # Reset board state
                    
                    move_scores.append(f"({r},{c}): {val}")
                    
                    if val > best_val:                                                      # Update best move if current score is higher
                        best_val = val
                        best_move = (r, c)
                        
        return best_move, move_scores
    
    def get_move_score(self, row, col, is_maximizing_player):
        """
        Evaluates the score of a specific move by simulating it 
        and running Minimax at full depth.
        """
        player = AI_PLAYER if is_maximizing_player else HUMAN_PLAYER                        # Simulate the move
        self.engine.board[row][col] = player
        
        score = self.minimax(0, not is_maximizing_player, 9, -math.inf, math.inf)           # Run Minimax on the resulting board
                                                                                            # We use a large depth (9) to get the "Perfect" truth
        self.engine.board[row][col] = EMPTY                                                 # Undo the move
        
        return score