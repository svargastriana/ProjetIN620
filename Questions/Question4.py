import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from AutomateCellulaire import *

def question4():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 6
    Question : : Donner une fonction qui prend en argument un automate cellulaire et une configuration et qui donne la configuration obtenue après un pas de calcul de l’automate."""
    print("Lecture du fichier règle_110.txt")
    automate, mot = lire_automate("Automates/règle_110.txt")
    config = automate.construire_configuration(mot)
    config = etape_1(automate, config)
    print("Nouvelle configuration :", mot_lisible(config))
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question4()