import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from MachineTuring import lire_machine_turing, initialiser_configuration, un_pas, afficher

def question11():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 11
    Question : Donner une fonction qui prend en argument une machine de Turing et une configuration et qui donne la configuration obtenue après un pas de calcul de la machine."""
    machine = lire_machine_turing("Machines/machine_inversion1_0.txt") #on lit notre machine qui est contenu dans un fichier txt
    config = initialiser_configuration("101", machine) #on initialise notre configuration de base avec un mot et la machine
    print("Avant un pas (la transition) :")
    afficher(config)
    un_pas(machine, config)
    print("Après un pas (la transition):")
    afficher(config)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question11()