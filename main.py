import sys
from MachineTuring import lire_machine_turing
from AutomateCellulaire import construire_automate_cellulaire, simuler_automate_cellulaire

#Ce code permet de répondre à la question 13
if len(sys.argv) != 3:
    print("Utilisation : python3 main.py <fichier_machine> <mot>")
    sys.exit(1)

fichier_machine = sys.argv[1] #ex: Machines/machine0egal1.txt
mot_initial = sys.argv[2] #ex: 0101

machine = lire_machine_turing(fichier_machine) #on lit le fichier de la machine choisit par l'utilisateur
regles = construire_automate_cellulaire(machine) #on construit l'automate cellulaire avec la machine
#configuration initiale
config = []
for i, c in enumerate(mot_initial):
    if i == 0:
        config.append((machine.etat_initial, c))  #tête au début
    else:
        config.append(("⋆", c))
for _ in range(3): #on rajoute trois slots vide à la fin
    config.append(("⋆", "□"))

simuler_automate_cellulaire(config, regles, nb_etapes=10) #on simule l'automate cellulaire