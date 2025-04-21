import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from AutomateCellulaire import *

def question1():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 6
    Question : Proposer une structure de données qui permet de représenter un automate cellulaire. Attention, l’espace d’états des cellules doit être préciser (ça n’est pas forcément {0, 1} comme dans l’exemple ou le jeu de la vie)."""
    automate = Automate_cellulaire(['0', '1'], {}, '_')
    print("Espace d'états :", automate.espace_etats)
    print("Transitions :", automate.transitions)
    print("État par défaut :", automate.etat_par_defaut)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question1()