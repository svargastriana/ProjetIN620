import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from AutomateCellulaire import *

def question2():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 6
    Question : Proposer une structure de donn´ees pour représenter la configuration d’un automate cellulaire."""
    automate = Automate_cellulaire(['0', '1'], {}, '_')
    config = automate.construire_configuration('0101')
    print("Configuration construite :", config)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question2()