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
        self.p_total_moves = 0
        self.p_optimal_moves = 0
        self.ai_total_moves = 0
        self.ai_optimal_moves = 0

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
        
    def evaluate_move(self, r, c, player):
        """
        Calculates and updates the accuracy score for the given player.
        updates the accuracy score based on how the player's move compares to the optimal minimax move.
        """
        is_maximizing = (player == AI_PLAYER)
        best_possible = -float('inf') if is_maximizing else float('inf')             # Find the Best Possible Score for this board state
                                                                                     #(What a perfect player would get)
        for i in range(3):
            for j in range(3):
                if self.engine.board[i][j] == EMPTY:
                    score = self.ai.get_move_score(i, j, is_maximizing)              # Score of move (i, j)
                    if is_maximizing:
                        best_possible = max(best_possible, score)
                    else:
                        best_possible = min(best_possible, score)

        actual_score = self.ai.get_move_score(r, c, is_maximizing)                   # Get Score of the Actual Move Chosen
        is_optimal = (actual_score == best_possible)
        
        if player == HUMAN_PLAYER:
            self.p_total_moves += 1
            if is_optimal:
                self.p_optimal_moves += 1
        else:
            self.ai_total_moves += 1
            if is_optimal:
                self.ai_optimal_moves += 1
        
        # UI Update logic to show accuracy percentages        
        p_acc = (self.p_optimal_moves / self.p_total_moves * 100) if self.p_total_moves > 0 else 100
        ai_acc = (self.ai_optimal_moves / self.ai_total_moves * 100) if self.ai_total_moves > 0 else 100

        self.gui.set_score(f"Player Acc: {p_acc:.0f}% | AI Acc: {ai_acc:.0f}%")
            
        
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
        For easy level, the AI doesn't calculate the best move, it just picks a random available move.
        This is done to make the game more fun and less predictable for the player.
        """

        self.gui.set_status("AI is thinking...")
        QApplication.processEvents() 
        
        depth = self.gui.get_depth() 
        chosen_move = None

        if depth >= 3: # Medium or Hard
            chosen_move, _ = self.ai.get_best_move(depth)
        else: # Easy
            chosen_move = self.engine.get_random_move()

        if chosen_move:
            r, c = chosen_move
            self.evaluate_move(r, c, AI_PLAYER)
            self.engine.make_move(r, c, AI_PLAYER)
            self.gui.set_cell(r, c, AI_PLAYER)
            
            if not self.check_game_over():
                self.gui.set_status("Human player turn (X)")
                self.gui.enable_board() 
                


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
            self.evaluate_move(r, c, HUMAN_PLAYER)
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
        
        self.p_total_moves = 0
        self.p_optimal_moves = 0
        self.ai_total_moves = 0
        self.ai_optimal_moves = 0

        for r in range(3):
            for c in range(3):
                self.gui.set_cell(r, c, EMPTY)
        
        self.gui.enable_board()
        self.gui.set_status("Your turn (X)")
        self.gui.set_score("Player Accuracy: 100%  |  AI Accuracy: 100%")

        if self.gui.mode_box.currentIndex() == 1:                                    # If PvP mode is selected, the second player (O) starts
            self.gui.set_status("Player 2's turn (O)")
            self.ai_move()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = GameController()
    controller.gui.show()
    sys.exit(app.exec_())
