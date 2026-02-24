import sys
from typing import Self
from PyQt5.QtWidgets import QApplication
from GUI_layout import TicTacToe
from game_rules import GameEngine, EMPTY, AI_PLAYER, HUMAN_PLAYER
from min_max_algo import MinMaxAlgo

class GameController:
    def __init__(self):
        self.gui = TicTacToe()
        self.engine = GameEngine()
        self.ai = MinMaxAlgo(self.engine)

        # Connect buttons to their respective functions
        for r in range(3):
            for c in range(3):
                self.gui.buttons[r][c].clicked.connect(lambda checked, 
                                                       row = r, 
                                                       col = c:
                                                       self.player_move(row, col))   # Use of a lambda function to tell teh button which row and column it is when clicked
                
            self.gui.reset_btn.clicked.connect(self.reset_game)                      # Connect reset and quit buttons
            self.gui.quit_btn.clicked.connect(sys.exit)

    def check_game_over(self):

        """ 
        This method checks if the game is over. If it is it declares the winner or if it is a tie. 
        Returns False if the game can go on.
        """

        winner = self.engine.check_winner()
        if winner:
            self.gui.set_status(f"Winner: {winner}")                                # Tells if there is a winner
            self.gui.disable_board()
            return True
        if not self.engine.is_moves_left():
            self.gui.set_status("The game is a tie")                                # Tell if the game is a tie
            return True
        return False                                                                # Returns False if there is no winner

    def player_move(self, r, c):
        if self.engine.board[r][c] == EMPTY:                                         # Check if the move is valid
            self.engine.make_move(r, c, HUMAN_PLAYER)
            self.gui.set_cell(r, c, HUMAN_PLAYER)

            if self.check_game_over():
                return
            
        self.gui.set_status("AI is thinking")                                        # AI's turn
        QApplication.processEvents()                                                 # Refreshes the screen to show the status
        depth = self.gui.get_depth()                                                 # Get the depth from QComboBox
        move, move_scores = self.ai.get_best_move(depth)                             # AI chooses it's best move (get_best_move returns a tuple)

        if move is not None:
            ai_row, ai_col = move
            self.engine.make_move(ai_row, ai_col, AI_PLAYER)
            self.gui.set_cell(ai_row, ai_col, AI_PLAYER)
            
            if not self.check_game_over():
                    self.gui.set_status("Human player turn (X)")
        else:
            self.check_game_over()                                                   # If the board is full or game ended, don't try to unpack

    def reset_game(self):
        self.engine = GameEngine() 
        self.ai.engine = self.engine
        for r in range(3):
            for c in range(3):
                self.gui.set_cell(r, c, EMPTY)
            self.gui.enable_board()
            self.gui.set_status("Your turn (X)")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = GameController()
    controller.gui.show()
    sys.exit(app.exec_())
