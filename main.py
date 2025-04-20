"""
Simulation d'une machine de Turing avec son équivalent en automate cellulaire.

Utilisation :
    python main.py <machine_turing.txt> <mot_initial> [nombre_de_pas]

Exemple :
    python main.py exemple_MT.txt 1101 25
"""

import sys
from typing import Dict
from AutomateCellulaire import Automate_cellulaire, etape_1, mot_lisible
from MachineTuring import lire_machine_turing, initialiser_configuration, simuler

def encoder_cellule(etat_tete, symbole):
    """
    Encode une cellule en fonction de si elle contient la tête de lecture ou non.
    -Si la tête est présente, on encode avec son état (ex : q1:0)
    -Sinon, on encode avec une étoile (ex : *:1)
    """
    return f"{etat_tete}:{symbole}"

def construire_automate_cellulaire_depuis_MT(machine):
    """
    Construit un automate cellulaire qui simule exactement la machine de Turing donnée.
    """
    ALPHABET = {'0', '1', '□'}  #alphabet que l'on utilise
    AUCUNE_TETE = '*' #correspond au symbole quand la tête n'est pas dans la case
    tous_les_etats = {encoder_cellule(AUCUNE_TETE, symbole) for symbole in ALPHABET} #tous les états possibles
    #ajoute les états qui sont dans la machine
    for (etat, _) in machine.transitions.keys():
        tous_les_etats.update({encoder_cellule(etat, symbole) for symbole in ALPHABET})
    #on vérif que les états finaux sont bien pris en compte
    for etat_final in machine.etats_accept:
        tous_les_etats.update({encoder_cellule(etat_final, symbole) for symbole in ALPHABET})
    regles_locales = {} #on définit les règles de bases sous forme de dictionnaire
    #on aura dedans un tuple de 3 str, un str, exemple : (gauche, centre, droite), nouvelle valeur
    #cas où aucune cellule n'a la tête
    for gauche in ALPHABET:
        for centre in ALPHABET:
            for droite in ALPHABET:
                triplet = (encoder_cellule(AUCUNE_TETE, gauche),encoder_cellule(AUCUNE_TETE, centre),encoder_cellule(AUCUNE_TETE, droite))
                regles_locales[triplet] = encoder_cellule(AUCUNE_TETE, centre) #on garde le symbole
    #le cas où la tête se trouve au centre
    for (etat, symbole_lu), transition in machine.transitions.items():
        for gauche_symbole in ALPHABET:
            for droite_symbole in ALPHABET:
                cellule_avec_tete = encoder_cellule(etat, symbole_lu)
                gauche = encoder_cellule(AUCUNE_TETE, gauche_symbole)
                droite = encoder_cellule(AUCUNE_TETE, droite_symbole)
                #on écrit le nouveau symbole qui remplace la tête
                regles_locales[(gauche, cellule_avec_tete, droite)] = encoder_cellule(AUCUNE_TETE, transition.ecrire_symbole)
                if transition.direction == 'R': #droite = R
                    for symbole_suivant in ALPHABET:
                        regles_locales[(cellule_avec_tete, droite, encoder_cellule(AUCUNE_TETE, symbole_suivant))] = encoder_cellule(transition.etat_suivant, droite_symbole)
                else :#gauche = L
                    for symbole_precedent in ALPHABET:
                        regles_locales[(encoder_cellule(AUCUNE_TETE, symbole_precedent), gauche, cellule_avec_tete)] = encoder_cellule(transition.etat_suivant, gauche_symbole)
    #l'état par défault d'une cellule vide qui n'a pas de tête
    etat_par_defaut = encoder_cellule(AUCUNE_TETE, '□')
    return Automate_cellulaire(tous_les_etats, regles_locales, etat_par_defaut)

def convertir_config_MT_en_config_CA(config_MT):
    """
    Convertit une configuration de machine de Turing en une configuration d'automate cellulaire
    """
    AUCUNE_TETE = '*'
    config_CA = {} #un dico avec un [int,str]
    #on parcourt toutes les cases connues du ruban
    for position, symbole in config_MT.ruban.items():
        etat_cellule = config_MT.etat if position == config_MT.position else AUCUNE_TETE
        config_CA[position] = encoder_cellule(etat_cellule, symbole)
    #Si la tête est sur une cellule vide encore non définie
    if config_MT.position not in config_MT.ruban:
        config_CA[config_MT.position] = encoder_cellule(config_MT.etat, '□')
    return config_CA

def simuler_automate_cellulaire(automate: Automate_cellulaire, config: Dict[int, str], nombre_etapes: int = 20):
    """
    Affiche une trace simple de l’évolution de l’automate cellulaire, comme pour la MT.
    """
    AUCUNE_TETE = '*'
    for temps in range(nombre_etapes + 1):
        #état et position de la tête
        etat_courant = None
        ruban_str = ""
        positions = sorted(config.keys())
        for i in range(min(positions), max(positions)+1):
            cellule = config.get(i, automate.etat_par_defaut)
            etat_cellule, symbole = cellule.split(":")
            if etat_cellule != AUCUNE_TETE:
                ruban_str += f"[{symbole}] "
                etat_courant = etat_cellule
            else:
                ruban_str += f" {symbole}  "
        etat_affichage = f"État: {etat_courant}" if etat_courant else "État: (inconnu)"
        print(f"{etat_affichage} | Ruban: {ruban_str.strip()}")
        config = etape_1(automate, config)

def main():
    if len(sys.argv) < 3:
        print("Utilisation : python main.py <fichier_MT> <mot_initial> [nombre_de_pas] \n Exemple :\npython main.py Machines/machine_Oegal1.txt 1010 25")
        sys.exit(1)
    fichier_mt = sys.argv[1]
    mot_initial= sys.argv[2]
    nombre_de_pas = int(sys.argv[3]) if len(sys.argv) >= 4 else 20
    machine = lire_machine_turing(fichier_mt) #on lance la simulation de la mahcine du turing pour comparer
    configuration_initiale = initialiser_configuration(mot_initial, machine)
    import copy #on fait une copie de la config initialial
    config_MT_copie = copy.deepcopy(configuration_initiale)
    print(config_MT_copie)
    print("\n=====  Simulation directe de la machine de Turing  =====")
    simuler(machine, configuration_initiale, max_etapes=nombre_de_pas)
    #on simule l'automate cellulaire depuis la machine de turing
    automate = construire_automate_cellulaire_depuis_MT(machine)
    config_CA = convertir_config_MT_en_config_CA(config_MT_copie)
    print("\n=====  Simulation par l’automate cellulaire équivalent  =====")
    simuler_automate_cellulaire(automate, config_CA, nombre_de_pas)


if __name__ == "__main__":
    main()