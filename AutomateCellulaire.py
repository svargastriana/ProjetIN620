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
    Cette fonction effectue une étape de simulation de l'automate cellulaire.
    Elle prend en entrée l'automate et la configuration actuelle.
    Elle renvoie la nouvelle configuration après une étape de simulation.
    """

    config_1 = {}
    indices = configuration.keys()
    # On récupère les indices de la configuration actuelle
    # On utilise min et max pour déterminer les bornes de la configuration
    min_i = min(indices)
    max_i = max(indices)

    # On ajoute une cellule de chaque côté pour gérer les transitions
    # hors bornes. On utilise l'état par défaut pour ces cellules.
    for i in range(min_i - 1, max_i + 2):
        gauche = configuration.get(i - 1, automate.etat_par_defaut)
        centre = configuration.get(i, automate.etat_par_defaut)
        droite = configuration.get(i + 1, automate.etat_par_defaut)

        # On crée un tuple avec les états gauche, centre et droite
        # et on utilise ce tuple pour trouver le nouvel état
        # dans le dictionnaire de transitions de l'automate
        config_tuple = (gauche, centre, droite)
        nouvel_etat = automate.transitions.get(config_tuple, centre) 

        print(f"config_tuple: {config_tuple} -> nouvel_etat: {nouvel_etat}")

        # On vérifie si l'indice est dans les bornes de la configuration actuelle
        # Si oui, on met à jour la configuration avec le nouvel état
        # Sinon, on laisse l'état par défaut
        if min_i <= i <= max_i or nouvel_etat != automate.etat_par_defaut:
            config_1[i] = nouvel_etat

    return config_1



def mot_lisible(config):
    """
    Cette fonction permet de convertir la configuration en une chaîne de caractères lisible.
    """
    # On trie les indices de la configuration pour garantir l'ordre
    # et on utilise une compréhension de liste pour créer la chaîne de caractères
    return "".join(config[i] for i in sorted(config.keys()))


def simulation(mot,automate, etapes = 1000, transition_speciale = None):

    """
    Cette fonction permet de simuler l'automate cellulaire sur un mot donné.
    On lance la simulation pour :
    - un mot donné
    - un nombre d'étapes donné
    - une transition spéciale (optionnelle) qui arrête la simulation si elle est rencontrée

    On affiche à chaque étape la configuration courante et on vérifie si la configuration a déjà été rencontrée.
    """
    config = automate.construire_configuration(mot)

    # On initialise une liste pour stocker les configurations déjà rencontrées
    # On ajoute la configuration initiale à cette liste
    config_effectues = []
    config_effectues.append(config)


    for i in range(etapes):
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



