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

corpus_directory = "cleaned"
matrice_tfidf, noms_fichiers, vocabulaire = calculer_matrice_tfidf(corpus_directory)
for i, vecteur_tfidf in enumerate(matrice_tfidf):
    print(f"\nVecteur TF-IDF pour le document '{noms_fichiers[i]}':")
    for j, score_tfidf in enumerate(vecteur_tfidf):
        print(f"{vocabulaire[j]}: {score_tfidf}")

#Trouver les mots non important (TF-IDF = 0 dans tout les document)

corpus_directory = "cleaned"
matrice_tfidf, _, vocabulaire = calculer_matrice_tfidf(corpus_directory)

# Afficher les mots les moins importants
mots_non_importants_liste = mots_non_importants(matrice_tfidf, vocabulaire)
print("Liste des mots les moins importants:")
print(mots_non_importants_liste)
