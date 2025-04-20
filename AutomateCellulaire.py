import re


class Automate_cellulaire:

    def __init__(self, espace_etats, transitions, etat_par_defaut):
        self.espace_etats = set(espace_etats)
        self.transitions = transitions
        self.etat_par_defaut = etat_par_defaut
        self.config = {}

    def construire_configuration(self, mot):
        config = {}
        for i, etat in enumerate(mot):
            config[i] = etat 
        self.config = config

        return config

    def get_etat(self, i):
        return self.config.get(i, self.etat_par_defaut)


def lire_automate(fichier):
    transitions = {}
    espace_etats = set()
    etat_par_defaut = "_"
    espace_etats.add("_")
    transitions[("_", "_", "_")] = "_" ### On initialise la transition par défaut et on l'ajoute à l'espace d'états

    with open(fichier, 'r') as f:
        lignes = f.readlines()
        config_initiale = lignes[0].strip()
        espace_etats.update(config_initiale)
        
        for ligne in lignes[1:]:
            ligne = ligne.strip()
            if not ligne or "->" not in ligne:
                continue

            config, etat = re.split(r'\s*->\s*', ligne)

            if config.startswith('(') and config.endswith(')'):
                config= config[1:-1]
            config_tuple = tuple(e.strip() for e in config.split(','))
            etat = etat.strip()


            transitions[config_tuple] = etat

            espace_etats.update(config_tuple)
            espace_etats.add(etat)


    return Automate_cellulaire(espace_etats, transitions, etat_par_defaut), config_initiale.strip()


def etape_1(automate, configuration):
    config_1 = {}
    indices = configuration.keys()
    min_i = min(indices)
    max_i = max(indices)

    for i in range(min_i - 1, max_i + 2):
        gauche = configuration.get(i - 1, automate.etat_par_defaut)
        centre = configuration.get(i, automate.etat_par_defaut)
        droite = configuration.get(i + 1, automate.etat_par_defaut)

        config_tuple = (gauche, centre, droite)
        nouvel_etat = automate.transitions.get(config_tuple, centre) # Si la transition n'est pas définie, on garde l'état actuel
        
        print(f"config_tuple: {config_tuple} -> nouvel_etat: {nouvel_etat}")

        if min_i <= i <= max_i or nouvel_etat != automate.etat_par_defaut:
            config_1[i] = nouvel_etat

    return config_1



def mot_lisible(config):
    return "".join(config[i] for i in sorted(config.keys()))


def simulation(mot,automate, etapes = 1000, transition_speciale = None):

    config = automate.construire_configuration(mot)

    config_effectues = []

    for i in range(etapes):
        config = etape_1(automate, config)
        
        if transition_speciale and mot_lisible(config) == transition_speciale:
            print("Transition spéciale trouvée :", transition_speciale)
            break


        if config in config_effectues:
            print("Configuration déjà rencontrée, arrêt de la simulation.")
            break

        config_effectues.append(config)

        print(f"Configuration après {i + 1} étapes :", mot_lisible(config))

    print("Fin de la simulation.")



