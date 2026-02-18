import sys
from GUI_layout import TicTacToe
from PyQt5 import QApplication
app = QApplication(sys.argv)
window = TicTacToe()
window.show()
sys.exit(app.exec())