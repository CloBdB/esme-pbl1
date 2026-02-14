# game_engine.py

# These are constants. We use them so we don't accidentally type 'x' instead of 'X'
EMPTY = ' '
AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'

class GameEngine:
    def __init__(self):
        # This creates a 3x3 grid (a list containing 3 lists)
        # It starts filled with EMPTY spaces
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]

    def is_moves_left(self):
        """Checks if there is at least one empty square left on the board."""
        for row in self.board:
            if EMPTY in row:
                return True
        return False

    def get_lines(self):
        """
        This is the most complex part. It gathers all possible 3-in-a-row 
        combinations (rows, columns, and diagonals) into one big list 
        so the 'Winner Checker' can look through them easily.
        """
        lines = []
        
        # 1. Add all horizontal rows
        lines.extend(self.board)
        
        # 2. Add all vertical columns
        for col in range(3):
            # This 'list comprehension' grabs the same index from every row
            column_cells = [self.board[row][col] for row in range(3)]
            lines.append(column_cells)
            
        # 3. Add the two diagonals
        # Top-left to bottom-right: [0,0], [1,1], [2,2]
        diag1 = [self.board[i][i] for i in range(3)]
        # Top-right to bottom-left: [0,2], [1,1], [2,0]
        diag2 = [self.board[i][2 - i] for i in range(3)]
        
        lines.append(diag1)
        lines.append(diag2)
        
        return lines

    def check_winner(self):
        """Looks at every line. If one line has 3 of the same symbol, they win!"""
        all_possible_lines = self.get_lines()
        
        for line in all_possible_lines:
            # Check if the first slot isn't empty AND all 3 items in the line are the same
            if line[0] != EMPTY and line.count(line[0]) == 3:
                return line[0] # Returns 'X' or 'O'
        return None # No winner yet

    def make_move(self, r, c, player):
        """Places a symbol on the board if the spot is empty."""
        if self.board[r][c] == EMPTY:
            self.board[r][c] = player
            return True # Success!
        return False # Spot was already taken

    def undo_move(self, r, c):
        """Clears a spot. This is vital for the AI to 'imagine' future moves."""
        self.board[r][c] = EMPTY