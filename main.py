import sys
import random
from typing import Self
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QEventLoop
from GUI_layout import TicTacToe
from game_rules import GameEngine, EMPTY, AI_PLAYER, HUMAN_PLAYER
from min_max_algo import MinMaxAlgo

class GameController:
    def __init__(self):
        self.gui = TicTacToe()
        self.engine = GameEngine()
        self.ai = MinMaxAlgo(self.engine)
        self.current_player = HUMAN_PLAYER                                           # Track the current player for PvP mode (starts with human player)

        # Connect buttons to their respective functions
        for r in range(3):
            for c in range(3):
                self.gui.buttons[r][c].clicked.connect(lambda checked, 
                                                       row = r, 
                                                       col = c:
                                                       self.player_move(row, col))   # Use of a lambda function to tell teh button which row and column it is when clicked
                
        self.gui.reset_btn.clicked.connect(self.reset_game)                          # Connects reset and quit buttons
        self.gui.quit_btn.clicked.connect(sys.exit)
        self.gui.mode_box.currentIndexChanged.connect(self.reset_game)               # Resets the board when the game mode is changed 

    def sleep(self, milliseconds):
        """ Creates a non-blocking delay """
        loop = QEventLoop()
        QTimer.singleShot(milliseconds, loop.quit)
        loop.exec_()
    
    def check_game_over(self):

        """ 
        This method checks if the game is over. If it is it declares the winner or if it is a tie. 
        Returns False if the game can go on.
        Highlights the winning line if there is a winner. 
        """

        winner, coords = self.engine.check_winner()                                 # Unpacks the tuple returned by check_winner into winner and coords

        if winner:
            self.gui.set_status(f"Winner: {winner}")                                # Tells if there is a winner
            self.gui.highlight_winning_line(coords)                                 # Highlights the winning line if there is a winner
            self.gui.disable_board()
            return True
        
        if not self.engine.is_moves_left():
            self.gui.set_status("The game is a tie")                                # Tells if the game is a tie
            self.gui.disable_board()                                                # Disables the board if there is a winner or if it is a tie to prevent further moves
            return True
        return False                                                                # Returns False if there is no winner

    def ai_move(self):

        """
        Handles the AI's decision-making and execution cycle.

        Updates the UI status, calculates the optimal move using Minimax, 
        updates the game state, and checks for game termination.
        """

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
                self.gui.enable_board()
        else:
            self.check_game_over()                                                   # If the board is full or game ended, don't try to unpack

    def player_move(self, r, c):

        """
        Processes the human player's turn at the specified coordinates.

        Validates the move, updates the game state and interface, and 
        triggers the AI turn if the match is still active. 

        Args:
            r (int): The row index of the clicked button.
            c (int): The column index of the clicked button.
        """

        if self.engine.board[r][c] != EMPTY:                                         # Check if the move is valid
            self.gui.set_status("Invalid move. Try again.")
            return
        
        mode = self.gui.mode_box.currentIndex()                                      # Check the game mode (PvP or PvE)

        if mode == 2:                                                                # PvP mode
            self.engine.make_move(r, c, self.current_player)                                    
            self.gui.set_cell(r, c, self.current_player)

            if not self.check_game_over():                                           # Switch player between X and O 
                self.current_player = AI_PLAYER if self.current_player == HUMAN_PLAYER else HUMAN_PLAYER   
                self.gui.set_status(f"Player {self.current_player}'s turn")

        else:                                                                        # Human vs AI mode

            self.engine.make_move(r, c, HUMAN_PLAYER)                                # Player's turn
            self.gui.set_cell(r, c, HUMAN_PLAYER)

            if not self.check_game_over():
                self.gui.disable_board()
                self.gui.set_status("AI is thinking")                                # Update status to show AI is thinking before the next move
                QApplication.processEvents()                                         # Force UI update so user sees text immediately
                delay = random.randint(200, 400)                                     # Random delay between 200-400ms to make AI seem more human-like
                self.sleep(delay)
                self.ai_move()                                                       # AI's turn

    def reset_game(self):

        """ Resets the game state and updates the UI for a new game. """

        self.engine = GameEngine() 
        self.ai.engine = self.engine

        for r in range(3):
            for c in range(3):
                self.gui.set_cell(r, c, EMPTY)
        
        self.gui.enable_board()
        self.gui.set_status("Your turn (X)")

        if self.gui.mode_box.currentIndex() == 1:                                    # If PvP mode is selected, the second player (O) starts
            self.gui.set_status("Player 2's turn (O)")
            self.ai_move()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = GameController()
    controller.gui.show()
    sys.exit(app.exec_())
