# Projet IN620 : Métasimulation

## Dépendances
- Python 3.x
Aucune bibliothèque externe n’est nécessaire.

## Fichiers principaux :
- MachineTuring.py : lecture et exécution de la machine de Turing
- AutomateCellulaire.py : construction et simulation d’un automate cellulaire
- main.py : script principal pour tout lancer
- machine.txt : description de la machine de Turing (état, transitions…)

## Utilisation
Tester chacune des questions une à une:
    
    make qx
    
    avec x allant de 1 à 12

Lancer toute les questions du projet sur les automates cellulaires:
    
    make ac

Lancer toute les questions du projet sur les machines de Turing :
    
    make mt

Pour la question 13 :
    
    make q13
    
    Il faut faire par exemple: make q13 MACHINE=Machines/machine_0egal1.txt MOT=0101

## A noter :

- pour les machines de Turing, tous les exemples s'éxécute sur le fichier "machine_inversion1_0.txt" avec comme mot "101", cette machine remplace les 1 par des 0 et les 0 par des 1.

- la question 5 est la même que la question 6 donc pas besoin de faire "make q5", qui lancera la même chose que "make q6".