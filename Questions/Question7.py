import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #on doit ajouter le parent du fichier pour accéder à machineturing.py
from AutomateCellulaire import *

def question7():
    """Fonction qui permet d'éxécuter ce que l'on nous demande pour la question 7
    Question : Donner les automates cellulaires suivants :
        — Un automate qui fait grandir sa configuration à l’infini en propageant l’information sur ses bords.
        — Un automate qui fait cycler les valeurs de ses cases (les cases doivent prendre toutes les valeurs de S).
        — Deux automates de votre choix qui ont un comportement int´eressant.
        Exécutez ces machines sur des exemples à l’aide de votre simulateur."""
    fichiers = [
        "Automates/automate_infini.txt",
        "Automates/automate_cycle.txt",
        "Automates/automate_alterne.txt",
        "Automates/automate_course.txt"
    ]

    noms = ["Automate infini", "Automate cycle", "Automate alternance", "Automate Course"]

    for nom, fichier in zip(noms, fichiers):
        print(f"\n=== {nom} ===")
        automate, mot = lire_automate(fichier)
        simulation(mot, automate, etapes=10)
    print("---------------------------------------------------------")

if __name__ == "__main__":
    question7()