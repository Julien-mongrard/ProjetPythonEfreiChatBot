from Fonctions import *


#converti en minuscule et sauvegarde tout les texte dans cleaned
convertir_en_minuscules_et_sauvegarder("speeches","cleaned",".txt")

#reprend les texte du dossier cleaned pour retirer la ponctuation
supprimer_ponctuation_dans_dossier("cleaned","cleaned")

#Calcule le TF de chaque mot dans chaque fichier et le met dans un dictinonaire commun a tout les fichiers
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

#Calcule TF-IDF

corpus_directory = "cleaned"
matrice_tfidf, noms_fichiers, vocabulaire = calculer_matrice_tfidf(corpus_directory)
for i, vecteur_tfidf in enumerate(matrice_tfidf):
    print(f"\nVecteur TF-IDF pour le document '{noms_fichiers[i]}':")
    for j, score_tfidf in enumerate(vecteur_tfidf):
        print(f"{vocabulaire[j]}: {score_tfidf}")

#Trouver les mots non important (TF-IDF = 0 dans tout les documents)
    corpus_directory = "cleaned"
    matrice_tfidf, _ , vocabulaire = calculer_matrice_tfidf(corpus_directory)

    # Afficher les mots les moins importants
    mots_non_importants_liste = mots_non_importants(matrice_tfidf, vocabulaire)
    print("Liste des mots les moins importants:")
    print(mots_non_importants_liste)


#Trouver les mots plus important

corpus_directory = "cleaned"
matrice_tfidf, noms_fichiers, vocabulaire = calculer_matrice_tfidf(corpus_directory)

mots_plus_importants_liste = mot_plus_important(matrice_tfidf, vocabulaire, noms_fichiers)
print("Mot(s) ayant le score TF-IDF le plus élevé dans chaque document:")
for fichier, mot in mots_plus_importants_liste:
    print(f"Document '{fichier}': {mot}")

#recuperer les mots les plus repeter par Chirac
    #recupere le score TF des 2 discour de Chirac
with open("C://Users//mongr//PycharmProjects//pythonProject5//cleaned//Nomination_Chirac1_cleaned.txt", 'r', encoding='utf-8') as fichier:
    contenu = fichier.read()
tf_fichier = TF(contenu)
with open("C://Users//mongr//PycharmProjects//pythonProject5//cleaned//Nomination_Chirac2_cleaned.txt", 'r', encoding='utf-8') as fichier:
    contenu = fichier.read()
tf_fichier = TF(contenu)
    #determine les mots les plus frequent
nb_mot = int(input("Nombre de mots le plus repeté par le président Chirac :"))
mot_plus_frequent=mots_plus_frequents(tf_fichier,nb_mot)
print(f"Les {nb_mot} mots les plus fréquents sont :", mot_plus_frequent)

#nom des president qui on parler de Nation et celui qui la le plus repeté
    # extension = ".txt"

dossier_corpus = ("cleaned")
extension_fichier = ".txt"

# Demander à l'utilisateur de saisir un mot
mot_recherche = input("Entrez le mot à rechercher : ")
mot_recherche = mot_recherche.lower()
print(mot_recherche)
# Appeler la fonction pour trouver le président qui a le plus parlé du mot
president_max, occurrences_max = president_plus_parle_mot(dossier_corpus, extension_fichier, mot_recherche)

print(f"Le président qui a le plus parlé du mot '{mot_recherche}' est {president_max} avec {occurrences_max} occurrences.")

#premier president a parler de Climat
dossier_corpus = ("cleaned")
extension_fichier = ".txt"
mot_recherche="climat"
president_max, occurrences_max = president_plus_parle_mot(dossier_corpus, extension_fichier, mot_recherche)
print(f"Le premier Président a parlé de Climat est {president_max} qui en a parlez {occurrences_max} fois")


#Hormis les mots dits « non importants », quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués.
corpus_directory = "cleaned"
matrices_tfidf_presidents, vocabulaire_global = calculer_matrice_tfidf_presidents(corpus_directory)

# Appeler la fonction pour obtenir les mots prononcés par tous les présidents
mots_par_tous_les_presidents = mots_par_tous_les_presidents(matrices_tfidf_presidents, vocabulaire_global)

# Afficher les résultats
print("Mots prononcés par tous les présidents :", mots_par_tous_les_presidents)