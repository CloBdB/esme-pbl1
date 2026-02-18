from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QgridLayout, QComboBox
)
from PyQt5.QtCore import Qt

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__() # calls the Qwidget constructor to correctly build the window
        
        self.setWindowTitle("TicTacToe")
        self.setMinimumSize(500, 400)
        self.setStyleSheet("background-color: lightblue")

        self.title_label = QLabel("TicTacToe vs AI")
        self.title_label.setAlignement(Qt.AlignCenter)
        self.title_label.setStyleSheet("front-size: 16px; front-weight: bold;") # make the title bigger and bold

        self.status_label = QLabel("Your turn (X)") # creates another label for message
        self.status_label.setAlignement(Qt.Aligncenter)

        self.depth_box = QComboBox() # create a drop down list widget
        self.depth_box.addItems(["Easy", "Medium","Hard"])  # add our 3 choices inside the drop down list

        self.buttons = []
        grid_layout = QgridLayout # creates a grid layout with rows and columns 3x3

        for r in range(3): # loop for the rows
            row = []
            for c in range(3): # loop for the columns
                btn = QPushButton(" ")  # creates a button which starts empty " "
                btn.setFixedSize(90, 90)
                btn.setStyleSheet("front-size: 28px;")
                grid_layout.addWidget(btn, r, c) # add the button to the grid at position r and c
                row.append(btn) 
            self.buttons.append(row) #add the whole row in the self.buttons so self.button[r][c] is the button at r and c
            
        self.reset_btn = QPushButton("Reset")
        self.quit_btn = QPushButton("Quit")

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(30)
        bottom_layout.addWidget(self.reset_btn)
        bottom_layout.addWidget(self.quit_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.depth_box)
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout) # Applies main_layout to the window


    def set_cell(self, r, c, text): 
        """Takes row, column, text, then find the position of button [r][c] in the grid and changes the text of that button to text"""
        self.buttons[r][c].setText(text) 
        

    
    def set_status(self, text):
        """recieves a message string and udates the status label on the screen with new message"""
        self.status_label.setText(text)

    
    def get_depth(self):
        """returns the difficulty level selected by the user"""
        levels = [1, 3, 9]
        return levels[self.depth_box.currentIndex()]

    
    def disable_board(self):
        """disables all buttons on the board once game is over"""
        for row in self.buttons:
            for btn in row:
                btn.setEnabled(False)

    
    def enable_board(self):
        """enables all buttons on board, allows playing again after reset"""
        for row in self.buttons:
            for btn in row:
                btn.setEnabled(True)


