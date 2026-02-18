# We define labels to avoid making mistakes in the text
EMPTY = ' '
AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'

class GameEngine:
    def __init__(self):
        # We create a 3x3 board manually; it's more visual
        # It's a list containing 3 lists (the rows)
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]

    def is_moves_left(self):
        """ Checks if there is at least one empty cell left """
        for row in self.board:
            for cell in row:
                if cell == EMPTY:
                    return True # Found an empty cell!
        return False # The board is full

    def get_lines(self):
        """ 
        This function gathers all rows, columns, and 
        diagonals so we can check them easily.
        """
        lines_to_check = []
        
        # 1. Add the 3 horizontal rows
        for row in self.board:
            lines_to_check.append(row)
        
        # 2. Build the 3 vertical columns
        for c in range(3):
            column = [self.board[i][c] for i in range(3)]
            lines_to_check.append(column)
            
        # 3. Build the 2 diagonals manually
        diag1 = [self.board[i][i] for i in range(3)]
        diag2 = [self.board[i][2 - i] for i in range(3)]
        
        lines_to_check.append(diag1)
        lines_to_check.append(diag2)
        
        return lines_to_check

    def check_winner(self):
        """ Checks if someone has aligned 3 symbols """
        all_lines = self.get_lines()
        
        for line in all_lines:
            # Check if the line contains the same symbol 3 times
            # And ensure it's not a line of empty cells!
            if line[0] == line[1] == line[2] and line[0] != EMPTY:
                return line[0] # Returns 'X' or 'O'
        return None # No one has won yet

    def make_move(self, r, c, player):
        """ Places a piece if the cell is free """
        if self.board[r][c] == EMPTY:
            self.board[r][c] = player
            return True
        return False

    def undo_move(self, r, c):
        """ Clears a piece (useful for the AI to test potential moves) """
        self.board[r][c] = EMPTY