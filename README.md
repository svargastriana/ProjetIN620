# Projet IN620 : Métasimulation

## Dépendances
- Python 3.x
Aucune bibliothèque externe n’est nécessaire.

## Fichiers principaux :
- MachineTuring.py : lecture et exécution de la machine de Turing
- AutomateCellulaire.py : construction et simulation d’un automate cellulaire
- main.py : script principal pour lancer la Question 13

## Sous-dossier :
- /Automates : contient tous nos automates cellulaires
- /Machines : contient toutes les machines de turing
- /Questions : contient les fichiers python permettant de répondre à chacune questions une à une
  
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

## Structure des fichiers

### `machine_xxx.txt`

Ces fichiers décrivent une **machine de Turing** :

- Commentaires (lignes commençant par `#`)
- État initial (défini avec `initial:`)
- États finaux (facultatifs, avec `accept:`)
- Transitions au format :  
  `état symbole_lu -> nouvel_état symbole_écrit direction`

### `automate_xxx.txt`

Ces fichiers décrivent un **automate cellulaire** :

- Première ligne : le mot à analyser
- Lignes suivantes : transitions de l’automate au format:  
  `(état, symbole, état) -> nouvel_état`

## A noter :

- Pour les automates celulaires, tou les exemples s'éxécute sur le fichier "règle_110.txt", le mot associé est donc : "0000100"
  
- pour les machines de Turing, tous les exemples s'éxécute sur le fichier "machine_inversion1_0.txt" avec comme mot "101", cette machine remplace les 1 par des 0 et les 0 par des 1.

- la question 5 est la même que la question 6 donc pas besoin de faire "make q5", qui lancera la même chose que "make q6". C'est donc pour la même raison que le fichier "Questions/Question5.py" n'existe pas.
