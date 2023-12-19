# Fichier les fonctions demander dans la partie 1 :
# Projet Efrei ChatBot Partie 1
# Maelle Chollet / Julien Mongrard
# Receuille toute les fonctiond demander dans la partie 1

import string
import os
import math
from collections import Counter

#Liste tous les fichiers d'un dossier, prend en paramètre un dossier, et une forme de fichier (par exemple .txt ici) et renvoie une liste
def lister_fichiers(dossier, extension):
    """Trouver le nom des fichiers présent dans le dossier et ayant à la même extension"""
    noms_fichiers = []
    # Parcourt fichiers dans le dossier
    for nom_fichier in os.listdir(dossier):
        # Vérification extension du fichier
        if nom_fichier.endswith(extension):
            # Ajout du fichier dans la liste
            noms_fichiers.append(os.path.splitext(nom_fichier)[0])
    return noms_fichiers

#Extrait le nom du president sur le titre d'un fichier, renvoie un tableau
def extraire_nom(nom_fichier):
    """Extraie du nom du président à partir du nom du fichier"""
    # Enlève 'Nomination'
    nom_president = nom_fichier.split('_')[1]
    # Vérification pas de chiffre dérrière le nom du président
    if nom_president[-1] == '1' or nom_president[-1] == '2':
        # Enlève le numéro
        nom_president = nom_president[:-1]
    return nom_president

#associe le nom d'un president a son prenom, prend en parametre une variable et sort une chaine de caractere
def associer_nom_prenom(nom_president):
    """Associe le nom d'un président à son prénom"""
    str(nom_president)
    dictionnaire_nomprenom_president = {"Chirac": "Jacques", "Giscard dEstaing": "Valéry", "Mitterrand": "François",
                                        "Hollande": "François", "Macron": "Emmanuel", "Sarkozy": "Nicolas"}
    return (dictionnaire_nomprenom_president[nom_president])

#affiche la liste des nom des president du dossier a l'aide des noms des fichiers, prend rien en entrée et resort un tableau
def nom_president():
    """Afficher la liste des noms des présidents"""
    fichier = lister_fichiers("speeches", ".txt")
    liste_president = []
    # Parcourt tous les fichiers dans le dossiers speeches
    for i in range(len(fichier)):
        # Ajoute à la liste le nom du président
        liste_president.append(extraire_nom(fichier[i]))
    # Enlève les doublons
    liste_president = list(set(liste_president))
    return list(liste_president)

#Convertie en minuscule tout les fichiers d'un dossier et renvoie un nouveau dossier crée avec les meme fichier mais tout en minuscule
def convertir_en_minuscules_et_sauvegarder(dossier_entree, dossier_sortie, extension=".txt"):
    """Converti tous le texte d'un dossier en minuscule"""
    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # Liste les fichiers dans le dossier d'entrée
    fichiers_entree = lister_fichiers(dossier_entree, extension)

    # Boucle pour traiter chaque fichier
    for fichier_entree in fichiers_entree:
        chemin_fichier_entree = os.path.join(dossier_entree, fichier_entree + extension)

        # Lit le contenu du fichier
        with open(chemin_fichier_entree, 'r', encoding='utf-8') as file:
            contenu = file.read()

        # Convertit en minuscules
        contenu_minuscules = contenu.lower()

        # Crée le chemin du fichier de sortie dans le dossier "cleaned"
        chemin_fichier_sortie = os.path.join(dossier_sortie, fichier_entree + "_cleaned" + extension)

        # Écrit le contenu converti en minuscules dans le fichier de sortie
        with open(chemin_fichier_sortie, 'w', encoding='utf-8') as file:
            file.write(contenu_minuscules)


#Supprime toute la ponctuation d'une chaine de caractere et renvoie une chaine de caractere
def supprimer_ponctuation(contenu):
    """Enlève toute la ponctuation d'un texte"""
    # Remplace les caractères spéciaux
    contenu = contenu.replace("'", " ")
    contenu = contenu.replace("-", " ")
    # Supprime les autres caractères
    for char in string.punctuation:
        contenu = contenu.replace(char, "")
    return contenu

#Parcour un dossier et tout ses ficher pour suprimmer toute la ponctuation a l'aide de la fonction supprimer_ponctuation, elle renvoie le dossier
def supprimer_ponctuation_dans_dossier(dossier_entree, dossier_sortie):
    """Enlève la ponctuation dans un fichier"""
    # Vérifie que le dossier de sortie existe
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # Liste les fichiers dans le dossier d'entrée
    fichiers_entree = os.listdir(dossier_entree)

    # Boucle pour traiter chaque fichier
    for fichier_entree in fichiers_entree:
        # Trouve le chemin complet du fichier d'entrée
        chemin_fichier_entree = os.path.join(dossier_entree, fichier_entree)

        # Trouve le chemin complet du fichier de sortie
        chemin_fichier_sortie = os.path.join(dossier_sortie, fichier_entree)

        # Lit le contenu du fichier d'entrée
        with open(chemin_fichier_entree, 'r', encoding='utf-8') as f:
            contenu = f.read()

        # Applique la fonction pour supprimer la ponctuation
        contenu_sans_ponctuation = supprimer_ponctuation(contenu)

        # Écrit le contenu sans ponctuation dans le fichier de sortie
        with open(chemin_fichier_sortie, 'w', encoding='utf-8') as f:
            f.write(contenu_sans_ponctuation)

#Calcule le TF d'une chaine de caracetere et renvoie un dictionnaire
def TF(texte):
    """Compte le nombre d'occurrences de chaque mot d'un texte"""
    # Crée une liste contenant chaque mot d'un texte
    liste = texte.split()
    occurrences = {}
    # Boucle pour parcourir chaque mot du texte/ de la liste
    for mot in liste:
        # Vérifie que le mot est dans le dictionnaire
        if mot in occurrences:
            # Ajoute 1 à la valeur pour le mot
            occurrences[mot] += 1
        else:
            # Ajoute le mot au dico et valeur=1
            occurrences[mot] = 1
    return (occurrences)

#Calcule de IDF d'un dossier, et renvoie un dictionnaire
def IDF(corpus_path):
    """Mesure l'importance des mots dans le texte"""
    documents_contenant_mot = Counter()
    # Compteur total de documents dans le corpus
    total_documents = 0

    # Parcourt les fichiers dans le répertoire
    for root, dirs, files in os.walk(corpus_path):
        # Boucle qui parcours les fichiers
        for file in files:
            # Ignore les fichiers qui commence par .
            if not file.startswith('.'):
                # Chemin complet du fichier
                filepath = os.path.join(root, file)
                # Incrémente le compteur de documents
                total_documents += 1
                # Lit le contenu du fichier
                with open(filepath, 'r', encoding='utf-8') as f:
                    # Trouve les mots uniques dans le fichier
                    mots_uniques = set(f.read().split())
                    # Mise à jour du compteur de documents_contenant_mot
                    documents_contenant_mot.update(mots_uniques)
    # Calcule le score IDF pour chaque mot
    scores_idf = {mot: math.log10(total_documents / (documents_contenant_mot[mot])) for mot in documents_contenant_mot}

    return scores_idf

#Calcule la Matrice TF-IDF d'un dossier et renvoie la matrice en tableau 2D, le nom des fichier en liste, tout les mots du dissier
def calculer_matrice_tfidf(corpus_path):
    """Calcul de la matrice TF-IDF (détermine mots-clé)"""
    scores_idf = IDF(corpus_path)
    # recupere tout les mots du Corpus_path
    documents = []
    noms_fichiers = []
    mots_corpus = set()  # Utiliser un ensemble pour stocker uniques mots dans le corpus

    # Parcourt les fichiers du répertoire
    for root, dirs, files in os.walk(corpus_path):
        # Parcourt les fichiers
        for file in files:
            if not file.startswith('.'):
                filepath = os.path.join(root, file)
                noms_fichiers.append(file)
                # Lit le contenu du fichier
                with open(filepath, 'r', encoding='utf-8') as f:
                    document = f.read()
                    documents.append(document)
                    mots_corpus.update(document.split())

    # Convertir l'ensemble de mots_corpus en une liste triée
    mots_corpus = list(mots_corpus)
    matrice_tfidf = []

    for document in documents:
        vecteur_tfidf = [0] * len(mots_corpus)  # Initialiser le vecteur à 0 pour chaque document
        # Compter la fréquence des mots dans le document
        tf_document = Counter(document.split())
        # Boucle qui parcourt chaque mot et sa valeur
        for j, mot in enumerate(mots_corpus):
            # Calculer le TD-IDF de chaque mot dans le document
            tf = tf_document.get(mot, 0) / len(document.split())
            tfidf = tf * scores_idf.get(mot, 0)
            vecteur_tfidf[j] = tfidf
        matrice_tfidf.append(vecteur_tfidf)

    return matrice_tfidf, noms_fichiers, mots_corpus

#Revoie les nom non important( TF-IDF =0) prend en parametre la matrice_tfidf un tableau 2D et la liste de tout les mots dans le dossier, renvoie une liste
def mots_non_importants(matrice_tfidf, vocabulaire):
    """Repère les mots qui ne sont pas importants"""
    mots_non_importants = []

    for j, mot in enumerate(vocabulaire):
        # Vérifie que le TF-IDF est toujours égal à zéro dans tous les fichiers
        if all(matrice_tfidf[i][j] == 0 for i in range(len(matrice_tfidf))):
            mots_non_importants.append(mot)

    return mots_non_importants

#Trouve le mot qui est le plus important dans la question (TF-IDF le plus important), entrée la question et le lien du dossier, renvoie une variable
def mot_plus_important(matrice_tfidf, vocabulaire, noms_fichiers):
    """Repère les mots les plus importants des fichiers"""
    mots_plus_importants = []

    for i, fichier in enumerate(noms_fichiers):
        # Trouve l'index du mot ayant le score TF-IDF le plus élevé dans le document
        index_max_tfidf = max(range(len(vocabulaire)), key=lambda j: matrice_tfidf[i][j])
        mots_plus_importants.append((fichier, vocabulaire[index_max_tfidf]))

    return mots_plus_importants

#Trouve les mots avec le TF le plus elevée du dossier 
def mots_plus_frequents(occurrences, nombre_mots=1):
    """Repère les mots les plus utilisé"""
    mots_tries = sorted(occurrences.items(), key=lambda item: item[1], reverse=True)
    mots_plus_frequents = mots_tries[:nombre_mots]
    return mots_plus_frequents


#Trouve le président qui parle le plus d'un mot donné par l'utilisateur, prend en entrée le dossier, l'extension du dossier (.txt) et le mot recherché, sort le président qui a le plus répété le terme et combien de fois il l'a répété.
def president_plus_parle_mot(dossier, extension, mot_recherche):
    """Trouve le président qui a dit le plus de fois un mots"""
    # Liste des fichiers dans le dossier avec l'extension spécifiée
    fichiers = lister_fichiers(dossier, extension)

    occurrences_par_president = {}

    # Parcourt chaque fichier et calcule les occurrences du mot
    for fichier in fichiers:
        # Trouve le chemin complet du fichier
        chemin_fichier = os.path.join(dossier, f"{fichier}{extension}")
        # Lit le fichier
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu_fichier = f.read()
            occurrences = TF(contenu_fichier)
            nom_president = extraire_nom(fichier)

            # Met à jour le dictionnaire des occurrences par président
            if nom_president in occurrences_par_president:
                occurrences_par_president[nom_president] += occurrences.get(mot_recherche, 0)
            else:
                occurrences_par_president[nom_president] = occurrences.get(mot_recherche, 0)

    # Trouve le président qui a le plus parlé du mot
    president_max_occurrences = max(occurrences_par_president, key=occurrences_par_president.get)
    nombre_occurrences_max = occurrences_par_president[president_max_occurrences]

    return president_max_occurrences, nombre_occurrences_max

