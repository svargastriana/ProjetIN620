import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from AutomateCellulaire import *

def question6():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 6
    Question : Ecrire une fonction qui prend comme argument un mot et un automate cellulaire et qui simule le calcul de l’automate. Vous proposerez plusieurs modes pour arrêter le calcul :
        — après un nombre de pas de calcul donné
        — après l’application d’une transition particulière
        — quand il n’y a pas de changements entre deux configurations successives"""
    print("Lecture du fichier règle_110.txt")
    automate, mot = lire_automate("Automates/règle_110.txt")
    simulation(mot, automate, etapes=5)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question6()