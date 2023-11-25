import string
import os
import re
import math
from collections import Counter

def lister_fichiers(dossier, extension):
    noms_fichiers = []
    for nom_fichier in os.listdir(dossier):
        if nom_fichier.endswith(extension):
            noms_fichiers.append(os.path.splitext(nom_fichier)[0])
    return noms_fichiers

def extraire_nom(nom_fichier):
    # Extraction du nom du président à partir du nom du fichier
    # En utilisant une approche basée sur la structure fixe des noms de fichiers
    nom_president=nom_fichier.split('_')[1]
    if nom_president[-1]=='1' or nom_president[-1]=='2':
        nom_president= nom_president[:-1]
    return nom_president

def associer_nom_prenom(nom_president):
    # Associer à chaque président un prénom
    # Cette fonction peut être étendue en fonction des prénoms associés à chaque président
    if nom_president == "Chirac":
        return "Jacques"
    elif nom_president == "Giscard dEstaing":
        return "Valéry"
    elif nom_president == "Mitterrand" or nom_president == "Hollande":
        return "François"
    elif nom_president == "Macron":
        return "Emmanuel"
    elif nom_president == "Sarkozy":
        return "Nicolas"
    else:
        president="Ce président n'est pas dans la liste ou n'existe pas."
        return president  # Retourne le nom tel quel si aucun prénom n'est associé

def associer_nom_prenom1(nom_president):
    str(nom_president)
    dictionnaire_nomprenom_president = {"Chirac": "Jacques", "Giscard dEstaing": "Valéry","Mitterrand": "François", "Hollande":"François","Macron" : "Emmanuel","Sarkozy":"Nicolas" }
    return(dictionnaire_nomprenom_president[nom_president])

def nom_president():
    # Afficher la liste des noms des présidents
    fichier=lister_fichiers("speeches-20231121", ".txt")
    liste_president=[]
    for i in range(len(fichier)):
        liste_president.append(extraire_nom(fichier[i]))
    liste_president=list(set(liste_president))
    return list(liste_president)

def convertir_en_minuscules_et_sauvegarder(dossier_entree, dossier_sortie, extension=".txt"):
    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # Liste des fichiers dans le dossier d'entrée
    fichiers_entree = lister_fichiers(dossier_entree, extension)

    # Boucle pour traiter chaque fichier
    for fichier_entree in fichiers_entree:
        chemin_fichier_entree = os.path.join(dossier_entree, fichier_entree + extension)

        # Lire le contenu du fichier
        with open(chemin_fichier_entree, 'r', encoding='utf-8') as file:
            contenu = file.read()

        # Convertir en minuscules
        contenu_minuscules = contenu.lower()

        # Créer le chemin du fichier de sortie dans le dossier "cleaned"
        chemin_fichier_sortie = os.path.join(dossier_sortie, fichier_entree + "_cleaned" + extension)

        # Écrire le contenu converti en minuscules dans le fichier de sortie
        with open(chemin_fichier_sortie, 'w', encoding='utf-8') as file:
            file.write(contenu_minuscules)

# Exemple d'utilisation
#convertir_en_minuscules_et_sauvegarder("speeches", "cleaned", ".txt")


def supprimer_ponctuation(contenu):
    # Remplacement caractères spéciaux
    contenu = contenu.replace("'", " ")
    contenu = contenu.replace("-", " ")
    # Suppression caractères normaux
    for char in string.punctuation:
        contenu = contenu.replace(char, "")
    return contenu

def supprimer_ponctuation_dans_dossier(dossier_entree, dossier_sortie):
    # Assurez-vous que le dossier de sortie existe
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # Liste des fichiers dans le dossier d'entrée
    fichiers_entree = os.listdir(dossier_entree)

    # Boucle pour traiter chaque fichier
    for fichier_entree in fichiers_entree:
        # Composez le chemin complet du fichier d'entrée
        chemin_fichier_entree = os.path.join(dossier_entree, fichier_entree)

        # Composez le chemin complet du fichier de sortie
        chemin_fichier_sortie = os.path.join(dossier_sortie, fichier_entree)

        # Lire le contenu du fichier d'entrée
        with open(chemin_fichier_entree, 'r', encoding='utf-8') as f:
            contenu = f.read()

        # Appliquer la fonction de suppression de ponctuation
        contenu_sans_ponctuation = supprimer_ponctuation(contenu)

        # Écrire le contenu sans ponctuation dans le fichier de sortie
        with open(chemin_fichier_sortie, 'w', encoding='utf-8') as f:
            f.write(contenu_sans_ponctuation)


def TF(texte):
    liste = texte.split()
    occurrences = {}
    for i in liste:
        if i in occurrences:
              occurrences[i] += 1
        else:
              occurrences[i] = 1
    return(occurrences)

def IDF(corpus_path):
    documents_contenant_mot = Counter()
    # Compteur total de documents dans le corpus
    total_documents = 0

    # Parcourir les fichiers dans le répertoire
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            # Ignorer les fichiers cachés
            if not file.startswith('.'):
                # Chemin complet du fichier
                filepath = os.path.join(root, file)
                # Incrémenter le compteur de documents
                total_documents += 1

                # Lire le contenu du fichier
                with open(filepath, 'r', encoding='utf-8') as f:
                    # Obtenir les mots uniques dans le fichier
                    mots_uniques = set(f.read().split())
                    # Mettre à jour le compteur de documents_contenant_mot
                    documents_contenant_mot.update(mots_uniques)
    # Calculer le score IDF pour chaque mot
    scores_idf = {mot: math.log10(total_documents / (documents_contenant_mot[mot]) ) for mot in documents_contenant_mot}

    return scores_idf


def calculer_matrice_tfidf(corpus_path):
    scores_idf = IDF(corpus_path)

    documents = []
    noms_fichiers = []

    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            if not file.startswith('.'):
                filepath = os.path.join(root, file)
                noms_fichiers.append(file)

                with open(filepath, 'r', encoding='utf-8') as f:
                    documents.append(f.read())

    matrice_tfidf = []

    for document in documents:
        vecteur_tfidf = [0] * len(scores_idf)  # Initialiser le vecteur à 0 pour chaque document
        for j, mot in enumerate(scores_idf.keys()):
            tf = TF(document).get(mot, 0) / len(document.split())
            tfidf = tf * scores_idf[mot]
            vecteur_tfidf[j] = tfidf
        matrice_tfidf.append(vecteur_tfidf)

    return matrice_tfidf, noms_fichiers, list(scores_idf.keys())

def mots_non_importants(matrice_tfidf, vocabulaire):
    mots_non_importants = []

    for j, mot in enumerate(vocabulaire):
        # Vérifier si le TF-IDF est toujours égal à zéro dans tous les documents
        if all(matrice_tfidf[i][j] == 0 for i in range(len(matrice_tfidf))):
            mots_non_importants.append(mot)

    return mots_non_importants

def mot_plus_important(matrice_tfidf, vocabulaire, noms_fichiers):
    mots_plus_importants = []

    for i, fichier in enumerate(noms_fichiers):
        # Trouver l'index du mot ayant le score TF-IDF le plus élevé dans le document
        index_max_tfidf = max(range(len(vocabulaire)), key=lambda j: matrice_tfidf[i][j])
        mots_plus_importants.append((fichier, vocabulaire[index_max_tfidf]))

    return mots_plus_importants