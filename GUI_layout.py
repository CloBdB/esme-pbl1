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

