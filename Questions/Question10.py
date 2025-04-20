import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from MachineTuring import lire_machine_turing, initialiser_configuration

def afficher_machine(machine):
    print("Machine de Turing :")
    print("- État initial :", machine.etat_initial)
    print("- États d'acceptation :", machine.etats_accept)
    print("- Transitions :")
    for (etat, symbole), trans in machine.transitions.items():
        print(f" ({etat}, '{symbole}') -> ({trans.etat_suivant}, '{trans.ecrire_symbole}', {trans.direction})")

def question10():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 10
    Question : Ecrire une fonction qui lit un fichier texte contenant le code d’une machine de Turing et un mot d’entrée et qui initialise la structure de données pour représenter cette machine."""
    machine = lire_machine_turing("Machines/machine_inversion1_0.txt") #on lit le fichier qui contient notre machine de Turing
    config = initialiser_configuration("101", machine) #on initialise la configuration avec la machine et un mot ici : 101
    print("Machine et configuration initialisée.")
    afficher_machine(machine) #on affiche notre machine dans la console
    print("\nConfiguration de départ :") #on affiche toute notre configuraiton de départ
    print("- État courant :", config.etat)
    print("- Ruban :", config.ruban)
    print("- Position de la tête :", config.position)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question10()