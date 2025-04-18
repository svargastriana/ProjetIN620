import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from MachineTuring import Configuration

def question9():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 9
    Question : Proposer une structure de donn´ees pour repr´esenter la configuration d’une machine de Turing."""
    ruban = {0: "1", 1: "0", 2: "1"}
    position = 1
    etat = "q0"
    config = Configuration(ruban, position, etat)
    print("Configuration initiale :")
    print("Ruban :", config.ruban)
    print("Position :", config.position)
    print("État :", config.etat)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question9()