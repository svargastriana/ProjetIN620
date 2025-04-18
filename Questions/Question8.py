import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from MachineTuring import Transition, MachineTuring

def question8():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 8
    Question : Proposer une structure de donn´ees qui permet de repr´esenter une machine de Turing."""
    transitions = {("q0", "0"): Transition("q1", "1", "R"),("q0", "1"): Transition("q1", "0", "R"),} #simulation de transitions
    machine = MachineTuring(etat_initial="q0", etats_accept=["qf"], transitions=transitions) #on créer une machine avec ces transi
    print("Machine de Turing créée.")
    print("Transitions :")
    for (etat, symbole), trans in machine.transitions.items():
        print(f"  ({etat}, '{symbole}') -> ({trans.etat_suivant}, '{trans.ecrire_symbole}', {trans.direction})")
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question8()