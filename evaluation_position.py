from game_rules import EMPTY, AI_PLAYER, HUMAN_PLAYER
from game_rules import GameEngine

def evaluate_board(engine):
    """ 
        This function evaluates the current state of the board and returns a score based on how favorable it is for the AI player.
        The higher the score is, the better the position is for the AI. A positive score means the AI is in a good position, while a negative score 
        means the human player is in a good position.
    """
    #game = GameEngine() 
    #game.board = board                             
    
    MAX = 1000
    MIN = -1000
    if engine.check_winner() != None:                                  # If there is a winner, high score for AI win, low score for human win, 0 for tie
        winner = engine.check_winner()
        if winner == AI_PLAYER:
            return MAX
        elif winner == HUMAN_PLAYER:
            return MIN
        else:
            return 0
    else:
        sum = 0
        for lines in engine.get_lines():                               # For each line (row, column, diagonal), checks the number of pieces for each player and updates the sum accordingly
            if lines.count(AI_PLAYER) >= 1 and lines.count(HUMAN_PLAYER) >= 1:
                pass
            elif lines.count(HUMAN_PLAYER) == 2:
                sum -= 30
            elif lines.count(HUMAN_PLAYER) == 1:
                sum -= 10
            elif lines.count(AI_PLAYER) == 2:
                sum += 30  
            elif lines.count(AI_PLAYER) == 1:
                sum += 10
        return sum