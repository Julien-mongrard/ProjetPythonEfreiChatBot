import string
import os
import re
import math
from collections import Counter

from Fonctions import *


#converti en minuscule et sauvegarde tout les texte dans cleaned
convertir_en_minuscules_et_sauvegarder("speeches","cleaned",".txt")

#reprend les texte du dossier cleaned pour retirer la ponctuation
supprimer_ponctuation_dans_dossier("cleaned","cleaned")


#Calcule le TF de chaque mot dans chaque fichier et le met dans un dictinonaire
fichiers_dossier = lister_fichiers("cleaned", ".txt")
tf_total = {}
for nom_fichier in fichiers_dossier:
    chemin_fichier = os.path.join("cleaned", nom_fichier + ".txt")
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    tf_fichier = TF(contenu)
    for mot, occurrences in tf_fichier.items():
        if mot in tf_total:
            tf_total[mot] += occurrences
        else:
            tf_total[mot] = occurrences
print(tf_total)

#Calcule l'IDF
idf = IDF("cleaned")
print(IDF)

#Calcule TF-IDF



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

# Exemple d'utilisation
corpus_directory = "cleaned"
matrice_tfidf, noms_fichiers, vocabulaire = calculer_matrice_tfidf(corpus_directory)

# Afficher la matrice TF-IDF (à titre d'exemple)
for i, vecteur_tfidf in enumerate(matrice_tfidf):
    print(f"\nVecteur TF-IDF pour le document '{noms_fichiers[i]}':")
    for j, score_tfidf in enumerate(vecteur_tfidf):
        print(f"{vocabulaire[j]}: {score_tfidf}")