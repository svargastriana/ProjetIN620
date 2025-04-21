import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from AutomateCellulaire import *

def question3():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 6
    Question : Ecrire une fonction qui lit un fichier texte contenant le code d’un automate cellulaire et un mot d’entrée et qui initialise la structure de donn´ees pour représenter cet automate."""
    print("Lecture du fichier règle_110.txt")
    automate, mot = lire_automate("Automates/règle_110.txt")
    print("Transitions :", automate.transitions)
    print("Mot initial :", mot)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question3()