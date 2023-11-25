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
#convertir_en_minuscules_et_sauvegarder("speeches-20231121", "cleaned", ".txt")


def supprimer_ponctuation(contenu):
    # Remplacement caractères spéciaux
    contenu = contenu.replace("'", " ")
    contenu = contenu.replace("-", " ")
    # Suppression caractères normaux
    for char in string.punctuation:
        contenu = contenu.replace(char, "")
    return contenu


def associer_nom_prenom1(nom_president):
    dictionnaire_nomprenom_president = {"Chirac": "Jacques", "Giscard dEstaing": "Valéry","Mitterrand": "François", "Hollande":"François","Macron" : "Emmanuel","Sarkozy":"Nicolas" }
    return(dictionnaire_nomprenom_president[nom_president])



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
    scores_idf = {mot: math.log10(total_documents / (documents_contenant_mot[mot] + 1)) for mot in documents_contenant_mot}

    return scores_idf





def calculer_matrice_tfidf(corpus_path):
    # Dictionnaire pour stocker le nombre de documents dans lesquels chaque mot apparaît
    documents_contenant_mot = Counter()
    # Liste pour stocker le contenu de chaque document
    documents = []
    # Liste pour stocker les noms de fichiers (pour référence ultérieure)
    noms_fichiers = []

    # Parcourir les fichiers dans le répertoire
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            # Ignorer les fichiers cachés
            if not file.startswith('.'):
                # Chemin complet du fichier
                filepath = os.path.join(root, file)
                # Ajouter le nom de fichier à la liste des noms de fichiers
                noms_fichiers.append(file)

                # Lire le contenu du fichier
                with open(filepath, 'r', encoding='utf-8') as f:
                    # Ajouter le contenu du fichier à la liste des documents
                    documents.append(f.read())

                    # Obtenir les mots uniques dans le fichier
                    mots_uniques = set(f.read().split())
                    # Mettre à jour le compteur de documents_contenant_mot
                    documents_contenant_mot.update(mots_uniques)

    # Calculer le nombre total de documents
    total_documents = len(documents)

    # Fonction pour calculer le score IDF d'un mot
    def calculer_idf(mot):
        return math.log10(total_documents / (documents_contenant_mot[mot] + 1))

    # Dictionnaire pour stocker les scores IDF de chaque mot
    scores_idf = {mot: calculer_idf(mot) for mot in documents_contenant_mot}

    # Fonction pour calculer le score TF-IDF d'un mot dans un document
    def calculer_tfidf(mot, document):
        tf = document.split().count(mot) / len(document.split())
        idf = scores_idf[mot]
        return tf * idf

    # Liste pour stocker les vecteurs TF-IDF de chaque document
    vecteurs_tfidf = []

    # Calculer les vecteurs TF-IDF pour chaque document
    for document in documents:
        vecteur_tfidf = [calculer_tfidf(mot, document) for mot in scores_idf]
        vecteurs_tfidf.append(vecteur_tfidf)

    return vecteurs_tfidf, noms_fichiers, list(scores_idf.keys())


# Exemple d'utilisation
corpus_directory = "/chemin/vers/le/repertoire/corpus"
vecteurs_tfidf, noms_fichiers, vocabulaire = calculer_matrice_tfidf(corpus_directory)

# Afficher les vecteurs TF-IDF (à titre d'exemple)
for i, vecteur_tfidf in enumerate(vecteurs_tfidf):
    print(f"\nVecteur TF-IDF pour le document '{noms_fichiers[i]}':")
    for j, score_tfidf in enumerate(vecteur_tfidf):
        print(f"{vocabulaire[j]}: {score_tfidf}")
