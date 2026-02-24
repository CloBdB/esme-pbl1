# We define labels to avoid making mistakes in the text
EMPTY = ' '
AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'

class GameEngine:
    def __init__(self):                                                     # The board is a list of list (empty at first)
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]

    def is_moves_left(self):
        """ Checks if there are any moves left (at least one empty cell) """
        for row in self.board:
            for cell in row:
                if cell == EMPTY:
                    return True 
        return False

    def get_lines(self):
        """ 
        This function gathers all rows, columns, and 
        diagonals so we can check them easily.
        """
        lines_to_check = []
        
        for row in self.board:                                              # Add the 3 rows
            lines_to_check.append(row)
        
        for c in range(3):                                                  # Add the 3 columns
            column = [self.board[i][c] for i in range(3)]
            lines_to_check.append(column)
            
        diag1 = [self.board[i][i] for i in range(3)]                        # Add the 2 diagonals 
        diag2 = [self.board[i][2 - i] for i in range(3)]
        
        lines_to_check.append(diag1)
        lines_to_check.append(diag2)
        
        return lines_to_check

    def check_winner(self):
        """ Checks if someone has aligned 3 symbols """
        all_lines = self.get_lines()
        
        for line in all_lines:
            if line[0] == line[1] == line[2] and line[0] != EMPTY:          # If all 3 cells in the line are the same and not empty, we have a winner
                    return line[0]                                          # Returns 'X' or 'O'
        return None 
    
    def make_move(self, r, c, player):
        """ Places a piece if the cell is free """
        if self.board[r][c] == EMPTY:
            self.board[r][c] = player
            return True
        return False

    def undo_move(self, r, c):
        """ Clears a piece (useful for the AI to test potential moves) """
        self.board[r][c] = EMPTY