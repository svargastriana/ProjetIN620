import re

class Automate_cellulaire:
    '''
    Classe qui permet de modéliser un automate cellulaire unidimensionnel.
    -espaces_etats : ensemble d'états possibles
    -transitions : dictionnaire de transitions
    -etat_par_defaut : état utilisé hors des bornes de l'espace d'états
    '''

    def __init__(self, espace_etats, transitions, etat_par_defaut):
        self.espace_etats = set(espace_etats)
        self.transitions = transitions
        self.etat_par_defaut = etat_par_defaut
        # Permet de stocker la configuration courante {indice: état}
        self.config = {}

    def construire_configuration(self, mot):
        """
        Cette méthode permet de construire la configuration à partir d'un mot donné.
        Elle prend en entrée un mot (une chaîne de caractères) et renvoie un dictionnaire.
        """
        config = {}
        for i, etat in enumerate(mot):
            config[i] = etat 
        self.config = config

        return config

    def get_etat(self, i):
        """
        Cette méthode permet de récupérer l'état d'une cellule à un indice donné.
        """
        return self.config.get(i, self.etat_par_defaut)


def lire_automate(fichier):
    """
    Cetter fonction permet de lire un automate cellulaire à partir d'un fichier.
    On suppose que le fichier contient également le mot que l'on souhaite simuler sur la première ligne.
    Ensuite, on lit les transitions de l'automate.
    Chaque ligne de transition est au format : (etat_gauche, etat_centre, etat_droite) -> nouvel_etat
    Par exemple : (0, 1, 0) -> 1
    """
    transitions = {}
    espace_etats = set()
    etat_par_defaut = "_"
    espace_etats.add("_")
    transitions[("_", "_", "_")] = "_" 
    # Nous avons décidé de définir '_' comme état par défaut pour les cellules hors bornes car 
    # c'est un état qui n'est pas utilisé dans les transitions. De plus, le caractère '□' n'était pas 
    # reconnu par le terminal, ce qui posait problème pour l'affichage.

    with open(fichier, 'r') as f:
        lignes = f.readlines()
        config_initiale = lignes[0].strip()
        espace_etats.update(config_initiale)
        
        for ligne in lignes[1:]:
            ligne = ligne.strip()
            # Ignore les lignes vides ou les commentaires
            if not ligne or "->" not in ligne:
                continue

            # Permet de gérer les espaces autour de '->' et de séparer la configuration de l'état
            config, etat = re.split(r'\s*->\s*', ligne)

            # Enlève les espaces autour de la configuration et de l'état
            if config.startswith('(') and config.endswith(')'):
                config= config[1:-1]
            
            ## Enlève les espaces autour de chaque état dans la configuration
            # et crée un tuple d'états
            # Exemple : (0, 1, 0) -> 1 devient ((0, 1, 0), 1)

            config_tuple = tuple(e.strip() for e in config.split(','))
            etat = etat.strip()


            transitions[config_tuple] = etat

            espace_etats.update(config_tuple)
            espace_etats.add(etat)


    return Automate_cellulaire(espace_etats, transitions, etat_par_defaut), config_initiale.strip()

def etape_1(automate, configuration):
    """
    Cette fonction effectue une étape de simulation d’un automate cellulaire.
    Elle parcourt toutes les cellules connues et applique les règles locales
    en fonction du triplet (gauche, centre, droite) de chaque position.
    """

    config_1 = {}  # nouvelle configuration après une étape
    indices = configuration.keys()  # ensemble des indices actuellement définis
    min_i = min(indices)  # indice minimum connu
    max_i = max(indices)  # indice maximum connu

    # on parcourt les indices élargis de -1 à +1 pour appliquer les règles correctement
    for i in range(min_i - 1, max_i + 2):

        # on récupère les 3 états locaux : gauche, centre, droite
        gauche = configuration.get(i - 1, automate.etat_par_defaut)
        centre = configuration.get(i, automate.etat_par_defaut)
        droite = configuration.get(i + 1, automate.etat_par_defaut)

        # on forme le triplet qui sert de clé de transition
        config_tuple = (gauche, centre, droite)
        """
        # === LOG DE DEBUG : utile pour comprendre l’évolution ===
        print(f"[DEBUG] i={i}")
        print(f"    gauche : {repr(gauche)}")
        print(f"    centre : {repr(centre)}")
        print(f"    droite : {repr(droite)}")
        print(f"    tuple  : {config_tuple}")
"""
        # on cherche la transition à appliquer pour ce triplet
        if config_tuple in automate.transitions:
            nouvel_etat = automate.transitions[config_tuple]
            #print(f"    → MATCHED → {nouvel_etat}")
        else:
            nouvel_etat = centre  # si pas de règle, on conserve l’état central
            #print(f"    → NO MATCH, default → {nouvel_etat}")

        # on ajoute l’état à la nouvelle config si nécessaire
        if min_i <= i <= max_i or nouvel_etat != automate.etat_par_defaut:
            config_1[i] = nouvel_etat

    return config_1  # on retourne la configuration mise à jour

def mot_lisible(config):
    """
    Cette fonction permet de convertir une configuration de l'automate en une chaîne lisible.
    Elle affiche les symboles, et encadre ceux où la tête de lecture est présente.
    """

    resultat = []  # liste contenant les symboles à afficher

    for i in sorted(config.keys()):  # on parcourt les indices triés (gauche à droite)
        etat = config[i]  # on récupère l'état de la cellule à cet indice

        if ':' in etat:  # cas d'une cellule encodée avec format "etat:symbole"
            etat_tete, symbole = etat.split(":")  # on sépare l'état de la tête et le symbole

            if etat_tete != '*':  # si la tête est présente (différent de '*')
                # on affiche le symbole entre crochets pour signaler la tête
                resultat.append(f"[{symbole}]")
            else:
                # sinon, on affiche le symbole tel quel, encadré par des espaces pour lisibilité
                resultat.append(f" {symbole} ")
        else:
            # cas d'un mot classique : on affiche directement le caractère (ex : '1', '0', etc.)
            resultat.append(f" {etat} ")

    return "".join(resultat)  # on retourne la chaîne finale

def simulation(config_ou_mot,automate, etapes = 1000, transition_speciale = None):

    """
    Cette fonction permet de simuler l'automate cellulaire sur un mot donné.
    On lance la simulation pour :
    - un mot donné
    - un nombre d'étapes donné
    - une transition spéciale (optionnelle) qui arrête la simulation si elle est rencontrée

    On affiche à chaque étape la configuration courante et on vérifie si la configuration a déjà été rencontrée.
    """
    if isinstance(config_ou_mot, str):
        config = automate.construire_configuration(config_ou_mot)
    else:
        config = config_ou_mot.copy()  # si c'est déjà une config, on la copie

    automate.config = config 
    #print(automate.transitions)
    # On initialise une liste pour stocker les configurations déjà rencontrées
    # On ajoute la configuration initiale à cette liste
    config_effectues = []
    
    for i in range(etapes-1):
        # On effectue une étape de simulation
        # et on met à jour la configuration courante
        config = etape_1(automate, config)
        mot_courant = mot_lisible(config)
        
        # On vérifie si la configuration courante est égale à la transition spéciale
        # Si oui, on arrête la simulation
        if transition_speciale and mot_courant== transition_speciale:
            print("Transition spéciale trouvée :", transition_speciale)
            break

        # On vérifie si la configuration courante a déjà été rencontrée
        # Si oui, on arrête la simulation
        if config in config_effectues:
            print("Configuration déjà rencontrée, arrêt de la simulation.")
            break

        config_effectues.append(config)

        print(f"Configuration après {i + 1} étapes :", mot_lisible(config))

    print("Fin de la simulation.")



