# **📦 \[Tic Tac Toe]**

**MVP Status:** v1.0-Production

**Group Members:** Raphaël Dussart, Clovis Bogdan de Badereau, Damien du Bourguet, Zahed Al-Kassous, Gabriel Barbier

## **🎯 Project Overview**

This application implements a Tic-Tac-Toe game with an Artificial Intelligence based on the Minimax algorithm with Alpha-Beta pruning. The system allows users to play against the computer, against another human, or let the AI play first.
The objective of this project was to simulate intelligent decision-making using game trees and evaluation functions while building a structured graphical application using PyQt.




## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**\
   git clone \[your-repo-link]\
   cd \[project-folder]

2. **Setup Virtual Environment:**\
   python -m venv .venv\
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies:**\
   pip install -r requirements.txt

4. **Run Application:**\
   python main.py


## **🛠️ Technical Architecture**

Explain how your code is organized. An "Architect-level" README should describe the separation of concerns.
The project follows a modular structure separating logic, AI, and user interface.

- **main.py**: Entry point of the application.
Contains the GameController class that connects the GUI, game engine, and AI.

- **game_rules.py**: Contains the GameEngine class.
Responsible for:
- Board representation
- Move validation
- Winner detection
- Returning available moves

- **evaluation_position.py**: Contains the evaluation function used by Minimax.
Assigns scores to board states depending on how favorable they are for the AI.

- **min_max_algo.py**: Implements:
- Minimax algorithm
- Alpha-Beta pruning optimization
- Depth-limited search (difficulty levels)
- Move scoring system

- **GUI_layout.py**: Contains the graphical interface built with PyQt.
Handles:
- Layout management
- Board display
- Mode selection
- Difficulty selection
- Highlighting winning lines
- Accuracy tracking display

This separation ensures clear responsibilities between:
- Game logic
- AI computation
- User interface


## **🧪 Testing & Validation**

The application can be validated by running:
python main.py

### Manual Validation Steps (Happy Path)
Launch the application.

Select a game mode:
- Human vs AI
- AI vs Human
- Human vs Human

Select a difficulty level:
- Easy (random AI)
- Medium (depth = 3)
- Hard (depth = 9)

Play until:
- A winner is declared (the winning line is highlighted in green), or
- A tie is reached.
- Click Reset to verify that the board and scores reset correctly.

### Expected Behavior
- The board updates correctly after each move.
- The AI chooses optimal moves in Hard mode.
- Accuracy percentages update dynamically.
- The board is disabled after the game ends.


## **📦 Dependencies**

- PyQt5: Used to build the graphical user interface.
- math: Used for infinity values in Minimax.
- random: Used for random moves in Easy mode and human-like delay simulation.


## **🔮 Future Roadmap (v2.0)**

If more development time were available, we would focus on extending and refining the system beyond the original scope:

- Add a leaderboard system to track player performance and high scores across multiple sessions.
- Generalize the engine to support larger boards like 4x4 gameplay.
- Implement a statistics dashboard showing win rate, average move quality, and AI performance metrics.
- Improve UI design with animations, sound effects, and smoother transitions.
- Add a hint button to help the player play the best move available



