"""
Simulation d'une machine de Turing avec son équivalent en automate cellulaire.

Utilisation :
    python main.py <machine_turing.txt> <mot_initial> [nombre_de_pas]

Exemple :
    make q13 MACHINE=Machines/machine_annule_1.txt MOT=0101
"""

import sys
from typing import Dict
from AutomateCellulaire import Automate_cellulaire, etape_1, mot_lisible, simulation
from MachineTuring import lire_machine_turing, initialiser_configuration, simuler

def encoder_cellule(etat_tete, symbole):
    """
    Encode une cellule en fonction de si elle contient la tête de lecture ou non.
    -Si la tête est présente, on encode avec son état (ex : q1:0)
    -Sinon, on encode avec une étoile (ex : *:1)
    """
    return f"{etat_tete}:{symbole}"  #retourne la cellule encodée

def construire_automate_cellulaire_depuis_MT(machine):
    """
    Construit un automate cellulaire qui simule exactement la machine de Turing donnée.
    """
    ALPHABET = {'0', '1', '□'}  # alphabet utilisé par la machine de Turing
    AUCUNE_TETE = '*'  # symbole utilisé pour indiquer l'absence de tête
    tous_les_etats = {encoder_cellule(AUCUNE_TETE, symbole) for symbole in ALPHABET}  # tous les états sans tête

    # on ajoute les états avec la tête pour tous les états de la machine
    for (etat, _) in machine.transitions.keys():
        tous_les_etats.update({encoder_cellule(etat, symbole) for symbole in ALPHABET})

    # on ajoute aussi les états finaux
    for etat_final in machine.etats_accept:
        tous_les_etats.update({encoder_cellule(etat_final, symbole) for symbole in ALPHABET})

    regles_locales = {}  # dictionnaire des règles de transition locales
    # test si une règle essentielle est bien présente
    test_triplet = (
        encoder_cellule('*', '□'),    # gauche
        encoder_cellule('q0', '1'),   # centre avec la tête sur 1
        encoder_cellule('*', '1')     # droite
    )
    if test_triplet not in regles_locales:
        print("[ERROR] La règle essentielle (*:□, q0:1, *:1) est absente !")
    else:
        print("[DEBUG] Règle essentielle bien présente.")


    # Cas de base : si aucune cellule n'a la tête, le symbole central est conservé
    for gauche in ALPHABET:
        for centre in ALPHABET:
            for droite in ALPHABET:
                triplet = (
                    encoder_cellule(AUCUNE_TETE, gauche),
                    encoder_cellule(AUCUNE_TETE, centre),
                    encoder_cellule(AUCUNE_TETE, droite)
                )
                regles_locales[triplet] = encoder_cellule(AUCUNE_TETE, centre)  # on garde le centre inchangé

    # Cas où la tête est présente au centre : on applique les transitions de la MT
    for (etat, symbole_lu), transition in machine.transitions.items():
        for gauche_symbole in ALPHABET:
            for droite_symbole in ALPHABET:
                centre_symbole = symbole_lu  # on ne crée la règle que pour le symbole exact attendu

                # on encode chaque cellule
                gauche = encoder_cellule(AUCUNE_TETE, gauche_symbole)
                centre = encoder_cellule(etat, centre_symbole)  # cellule centrale avec la tête
                droite = encoder_cellule(AUCUNE_TETE, droite_symbole)

                # règle 1 : on écrit le nouveau symbole au centre sans tête
                triplet_central = (gauche, centre, droite)
                regles_locales[triplet_central] = encoder_cellule(AUCUNE_TETE, transition.ecrire_symbole)

                if transition.direction == 'R':  # si la tête va à droite
                    for symbole_suivant in ALPHABET:
                        # règle 2 : on place la tête dans la cellule de droite
                        triplet_droite = (
                            centre,  # ancienne position de la tête
                            droite,  # cellule qui reçoit la tête
                            encoder_cellule(AUCUNE_TETE, symbole_suivant)
                        )
                        regles_locales[triplet_droite] = encoder_cellule(transition.etat_suivant, droite_symbole)
                else:  # direction gauche
                    for symbole_precedent in ALPHABET:
                        # règle 2 : on place la tête dans la cellule de gauche
                        triplet_gauche = (
                            encoder_cellule(AUCUNE_TETE, symbole_precedent),
                            gauche,  # cellule qui reçoit la tête
                            centre  # ancienne position de la tête
                        )
                        regles_locales[triplet_gauche] = encoder_cellule(transition.etat_suivant, gauche_symbole)

    # état par défaut utilisé hors des bornes
    etat_par_defaut = encoder_cellule(AUCUNE_TETE, '□')

    # debug pour voir combien de règles ont été créées
    print(f"[DEBUG] Nombre de règles créées : {len(regles_locales)}")

    return Automate_cellulaire(tous_les_etats, regles_locales, etat_par_defaut)

def convertir_config_MT_en_config_CA(config_MT):
    """
    Convertit une configuration de machine de Turing en une configuration d'automate cellulaire
    """
    AUCUNE_TETE = '*'  #symbole pour cellule sans tête
    config_CA = {}  #dictionnaire position -> état encodé

    #on parcourt les cases définies du ruban
    for position, symbole in config_MT.ruban.items():
        etat_cellule = config_MT.etat if position == config_MT.position else AUCUNE_TETE
        config_CA[position] = encoder_cellule(etat_cellule, symbole)

    #si la tête est sur une cellule encore vide
    if config_MT.position not in config_MT.ruban:
        config_CA[config_MT.position] = encoder_cellule(config_MT.etat, '□')

    return config_CA  #on retourne la config encodée

def main():
    if len(sys.argv) < 3:
        print("Utilisation : python main.py <fichier_MT> <mot_initial> [nombre_de_pas] \nExemple :\npython main.py Machines/machine_Oegal1.txt 1010 25")
        sys.exit(1)  #on quitte si les arguments sont manquants

    fichier_mt = sys.argv[1]  #récupère le chemin du fichier MT
    mot_initial = sys.argv[2]  #récupère le mot initial
    nombre_de_pas = int(sys.argv[3]) if len(sys.argv) >= 4 else 20  #définit le nombre d'étapes

    machine = lire_machine_turing(fichier_mt)  #lit la machine depuis le fichier
    configuration_initiale = initialiser_configuration(mot_initial, machine)  #initialise la config MT

    import copy
    config_MT_copie = copy.deepcopy(configuration_initiale)  #on copie la config pour la simulation CA

    print(config_MT_copie)  #affiche la configuration initiale
    print("\n=====  Simulation directe de la machine de Turing  =====")
    simuler(machine, configuration_initiale, max_etapes=nombre_de_pas)  #simule la MT

    automate = construire_automate_cellulaire_depuis_MT(machine)  #construit l'automate depuis la MT
    config_CA = convertir_config_MT_en_config_CA(config_MT_copie)  #convertit la config MT en config CA

    print("\n=====  Simulation par l’automate cellulaire équivalent  =====")
    print("\n[DEBUG] Configuration initiale de l'automate cellulaire :")
    for k in sorted(config_CA.keys()):
        print(f"  {k}: {config_CA[k]}")
    simulation(config_CA, automate, etapes=nombre_de_pas)
if __name__ == "__main__":
    main()  #lancement du programme principal