import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from MachineTuring import lire_machine_turing, initialiser_configuration, simuler

def question12():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 12
    Question : Ecrire une fonction qui prend comme argument un mot et une machine de Turing, qui simule le calcul de la machine sur ce mot et qui s’arête sur un état ACCEPT ou REJECT."""
    machine = lire_machine_turing("Machines/machine_inversion1_0.txt") #on lit notre machine de Turing contenu dans un fichier txt
    config = initialiser_configuration("101", machine) #on initialise la configuration initial de ma chine avec un mot en entrée ici : 101
    print("Simulation complète :") #on lance la simulation complète pour cette machine de turing
    simuler(machine, config)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question12()