# game_engine.py

# On définit des étiquettes pour ne pas se tromper dans le texte
VIDE = ' '
JOUEUR_IA = 'O'
JOUEUR_HUMAIN = 'X'

class GameEngine:
    def __init__(self):
        # On crée un plateau de 3x3 manuellement, c'est plus visuel
        # C'est une liste qui contient 3 listes (les lignes)
        self.board = [
            [VIDE, VIDE, VIDE],
            [VIDE, VIDE, VIDE],
            [VIDE, VIDE, VIDE]
        ]

    def is_moves_left(self):
        """ Vérifie s'il reste au moins une case vide """
        for ligne in self.board:
            for case in ligne:
                if case == VIDE:
                    return True # On a trouvé une case vide !
        return False # Tout est plein

    def get_lines(self):
        """ 
        Cette fonction rassemble toutes les lignes, colonnes et 
        diagonales pour que l'on puisse les vérifier facilement.
        """
        lignes_a_verifier = []
        
        # 1. On ajoute les 3 lignes horizontales
        for ligne in self.board:
            lignes_a_verifier.append(ligne)
        
        # 2. On fabrique les 3 colonnes verticales
        for c in range(3):
            colonne = [self.board[0][c], self.board[1][c], self.board[2][c]]
            lignes_a_verifier.append(colonne)
            
        # 3. On fabrique les 2 diagonales à la main
        diag1 = [self.board[0][0], self.board[1][1], self.board[2][2]]
        diag2 = [self.board[0][2], self.board[1][1], self.board[2][0]]
        
        lignes_a_verifier.append(diag1)
        lignes_a_verifier.append(diag2)
        
        return lignes_a_verifier

    def check_winner(self):
        """ Regarde si quelqu'un a aligné 3 symboles """
        toutes_les_lignes = self.get_lines()
        
        for ligne in toutes_les_lignes:
            # On vérifie si la ligne contient 3 fois le même symbole
            # Et on s'assure que ce n'est pas une ligne de cases vides !
            if ligne[0] == ligne[1] == ligne[2] and ligne[0] != VIDE:
                return ligne[0] # Renvoie 'X' ou 'O'
        return None # Personne n'a gagné

    def make_move(self, r, c, joueur):
        """ Place un pion si la case est libre """
        if self.board[r][c] == VIDE:
            self.board[r][c] = joueur
            return True
        return False

    def undo_move(self, r, c):
        """ Efface un pion (utile pour que l'IA puisse tester des coups) """
        self.board[r][c] = VIDE