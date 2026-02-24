from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()                                                           # Calls the Qwidget constructor to correctly build the window
        
        self.setWindowTitle("TicTacToe")
        self.setMinimumSize(700, 700)
        self.resize(800, 800)
        self.setStyleSheet("background-color: lightblue")

        self.title_label = QLabel("TicTacToe vs AI")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 32px; font-weight: bold;")        # Larger title

        self.status_label = QLabel("Your turn (X)")                                  # Creates another label for message
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px;")                          # Larger status text

        self.depth_box = QComboBox()                                                 # Creates a drop down list widget
        self.depth_box.addItems(["Easy", "Medium","Hard"])                           # Add the 3 difficulty choices inside the drop down list
        self.depth_box.setStyleSheet("font-size: 16px; padding: 6px;")               # Bigger dropdow text
        self.depth_box.setFixedWidth(200)                                            # Set a fixed width 

        # Center the dropdown horizontally
        depth_layout = QHBoxLayout()
        depth_layout.addStretch()
        depth_layout.addWidget(self.depth_box)
        depth_layout.addStretch()

        self.buttons = []
        grid_layout = QGridLayout()                                                  # Creates a grid layout with rows and columns 3x3
        grid_layout.setSpacing(8)                                                    # Spacing between buttons

        for r in range(3): # loop for the rows
            row = []
            for c in range(3): # loop for the columns
                btn = QPushButton(" ")                                               # Creates a button which starts empty " "
                btn.setFixedSize(160, 160)
                btn.setStyleSheet("font-size: 56px; font-weight: bold;")             # Bigger text on the buttons
                grid_layout.addWidget(btn, r, c)                                     # Add the button to the grid at position r and c
                row.append(btn) 
            self.buttons.append(row)                                                 # Add the whole row in the self.buttons so self.button[r][c] is the button at r and c
        
        # Center the grid horizontally
        grid_container = QHBoxLayout()
        grid_container.addStretch()
        grid_container.addLayout(grid_layout)
        grid_container.addStretch()

        self.reset_btn = QPushButton("Reset")                                        # Reset button
        self.reset_btn.setFixedHeight(50)
        self.reset_btn.setStyleSheet("font-size: 16px;")

        self.quit_btn = QPushButton("Quit")                                          # Quit button                                             
        self.quit_btn.setFixedHeight(50)
        self.quit_btn.setStyleSheet("font-size: 16px;")

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(30)
        bottom_layout.addWidget(self.reset_btn)
        bottom_layout.addWidget(self.quit_btn)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)                                                   # Space between each section
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.depth_box)
        main_layout.addLayout(grid_container)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)                                                  # Applies main_layout to the window


    def set_cell(self, r, c, text): 
        """ Takes row, column, text, then find the position of button [r][c] in the grid and changes the text of that button to text """
        self.buttons[r][c].setText(text) 
        

    
    def set_status(self, text):
        """ Recieves a message string and udates the status label on the screen with new message """
        self.status_label.setText(text)

    
    def get_depth(self):
        """ Returns the difficulty level selected by the user """
        levels = [1, 3, 9]
        return levels[self.depth_box.currentIndex()]

    
    def disable_board(self):
        """ Disables all buttons on the board once game is over """
        for row in self.buttons:
            for btn in row:
                btn.setEnabled(False)

    
    def enable_board(self):
        """ Enables all buttons on board, allows playing again after reset """
        for row in self.buttons:
            for btn in row:
                btn.setEnabled(True)


