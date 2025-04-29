class Transition:
    def __init__(self, etat_suivant, ecrire_symbole, direction):
        self.etat_suivant = etat_suivant
        self.ecrire_symbole = ecrire_symbole
        self.direction=direction #L ou R

class MachineTuring:
    def __init__(self, etat_initial, etats_accept, transitions):
        self.etat_initial= etat_initial
        self.etats_accept= set(etats_accept)
        self.transitions= transitions #dico: (état, symbole) -> transi

class Configuration:
    def __init__(self, ruban, position, etat):
        self.ruban = ruban #dico: position -> symbole
        self.position = position #position de la tête
        self.etat = etat #l'état courant


# Lecture du fichier texte (Question 10)
def lire_machine_turing(fichier):
    """
    Fonction qui permet de lire un fichier txt en entrée et renvoyer la machine de Turing associé
    Sortie : un objet MachineTuring : avec l'état initial, son état d'acceptation, et ses transitions
    """
    transitions= {}
    etat_initial= None
    etats_accept= set()

    with open(fichier, "r") as f:
        for ligne in f:
            ligne = ligne.strip() #on sépare chq ligne
            if not ligne or ligne.startswith("#"): #si c'est pas une ligne ou qu'elle commence par # (commentaire)
                continue #on la passe
            if ligne.startswith("initial:"): #si elle commence par initial alors on prend l'état initial
                etat_initial = ligne.split(":")[1].strip()
            elif ligne.startswith("accept:"): #si elle commence par accept alors on prend l'état d'acceptation
                etats_accept = ligne.split(":")[1].strip().split()
            else: #else = une règle quelconque
                #ex: q0 0 -> q1 1 R
                gauche, droite = ligne.split("->") #on sépare la partie gauche et droite de la règle
                etat, symbole = gauche.strip().split() #on retire les saut de ligne avec strip et on split chaque mot (entre chaque espace) donc l'état et le symbole dans une règle à gauche
                n_etat, n_symbole, direction = droite.strip().split() # pareil ici mais on a l'état, le symbole à écrire, et la direction
                transitions[(etat, symbole)] = Transition(n_etat, n_symbole, direction) #n_etat = etat suivant, n_symbole = symbole à écrire, direction = la direction L ou R
                #ex: transitions[("q0", "1")] = Transition("q1", "0", "R")
    return MachineTuring(etat_initial, etats_accept, transitions)
    #renvoie une machine avec l'état initial, son état d'acceptation, et ses transitions


#initialisation de la configuration (Question 10)
def initialiser_configuration(mot, machine):
    """
    Fonction qui initialise la configuration de la machine de Turing
    Entrée : un mot qui est une suite de 0 et de 1 et une machine avec l'état initial, son état d'acceptation, et ses transitions 
    Sortie : renvoie une configuration de cette machine avec la taille de son ruban, la position de la tête et son etat initial
    """
    ruban = {}
    for i, c in enumerate(mot): 
        ruban[i] = c
    return Configuration(ruban, 0, machine.etat_initial) #ruban, position de la tête, etat initial


#Pour le pas(Question 11)
def un_pas(machine, config):
    """
    Fonction qui agis comme un pas de la machine de Turing (une transition)
    Entrée : une machine définit avec l'état initial, son état d'acceptation, et ses transitions
             une config contenant la position de la tête, l'état courant et le ruban
    Sortie : la configuration après l'application d'une transition
             ou None s'il n'y a pas de transition possible (machine bloquée)
    """
    symbole_lu = config.ruban.get(config.position, '□') #on lit le symbole de la tête, par défaut □
    cle = (config.etat, symbole_lu) #une clé etat courant + symbole pour rechercher la transition correspondante dans le dictionnaire
    if cle not in machine.transitions:
        return None #aucune transi = stop, la machine est bloqué
    transition = machine.transitions[cle] #on récupère la transition
    config.ruban[config.position] = transition.ecrire_symbole #on applique la transition : écriture du nouveau symbole sur la bande
    config.etat = transition.etat_suivant #on passe à l'état suivant
    if transition.direction == 'R': #on déplace la tête de lecture, droite si R et gauche si L
        config.position += 1
    else:
        config.position -= 1
    return config #on renvoie la configuration mis à jour


#Simulation de la machine de turing(Question 12)
def simuler(machine, config, max_etapes=1000):
    """
    Fonction qui simule l'éxécution complète d'une MT avec une configuration donnée
    Entrée : une MT avec ses transitions et ses états d'acceptation
             la configuration de départ : ruban, position de la tête, état courant
             max_etapes, nombre max de transi avant l'arrêt automatique de la MT 
    Sortie : Affiche la configuration obtenu à chaque étape
    La machine s'arrête dans 3 cas possibles :
        - on arrive dans l'état ACCEPT
        - aucune transition définie pour l'état actuel (REJECT)
        - nombre d'étapes trop élévé (STOP)"""
    for i in range(max_etapes+1):
        afficher(config) #on affiche la config : ruban, tête, état
        if config.etat in machine.etats_accept: #si la machine se retrouve dans un état accept alors on s'arrête et on ACCEPT
            print(f"\nACCEPT en {i} étapes")
            return
        nouvelle_config = un_pas(machine, config) #on applique une transition (un pas)
        if nouvelle_config is None: #si aucune transition n'existe on REJECT
            print(f"\nAucune transition définie : REJECT")
            return
    print(f"\nTrop d’étapes (> {max_etapes}) : on stop l'éxécution") #sinon trop d'étapes on STOP


#Affichage lisible du ruban (Fonction de débugage)
def afficher(config):
    """
    Fonction qui affiche le ruban de manière lisible dans la console
    Entrée : une configuration de la machine de turing
    Sortie : affichage console
    """
    min_pos = min(min(config.ruban), config.position)
    max_pos = max(max(config.ruban), config.position) #le max est soit la + grande clé du dico, soit la taille max de la configuration actuelle
    ruban_str = ""
    for i in range(min_pos, max_pos + 1):
        s = config.ruban.get(i, '□')
        if i == config.position:
            ruban_str += f"[{s}]" #tête de lecture
        else:
            ruban_str += f" {s} "
    print(f"État: {config.etat} | Ruban: {ruban_str}")


"""
if __name__ == "__main__":
    machine = lire_machine_turing("machine.txt") #on lit la machine de turing dans notre fichier txt
    config = initialiser_configuration("0101", machine) #on initialise la machine de turing avec un mot ici 0101 et la machine
    simuler(machine, config) #on simule l'éxécution de notre machine de turing
"""