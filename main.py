# Programme Principale:
# Projet Efrei ChatBot
# Maelle Chollet / Julien Mongrard


from fonction_partie_1 import *
from fonction_partie_2 import *


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


#Calcule l'IDF
idf = IDF("cleaned")

#Calcule TF-IDF

corpus_directory = "cleaned"
matrice_tfidf, noms_fichiers, vocabulaire = calculer_matrice_tfidf(corpus_directory)
print("matrice Brute avec N lignes et M colonnes, où N = nombre de documents dans le corpus (8 dans notre cas) et M = nombre de mots dans le corpus (1681 dans notre cas).:")
print(matrice_tfidf)
print(("matice plus detailler"))
for i, vecteur_tfidf in enumerate(matrice_tfidf):
    print(f"\nVecteur TF-IDF pour le document '{noms_fichiers[i]}':")
    for j, score_tfidf in enumerate(vecteur_tfidf):
        print(f"{vocabulaire[j]}: {score_tfidf}")




# Main séparée en fonction pour directement choisir la fonction voulue dans le menu
def afficher_mots_non_importants():
    corpus_directory = "cleaned"
    matrice_tfidf, _, vocabulaire = calculer_matrice_tfidf(corpus_directory)
    mots_non_importants_liste = mots_non_importants(matrice_tfidf, vocabulaire)
    print(f"Liste des mots les moins importants:\n{mots_non_importants_liste}")

def afficher_mots_plus_importants():
    corpus_directory = "cleaned"
    matrice_tfidf, noms_fichiers, vocabulaire = calculer_matrice_tfidf(corpus_directory)
    mots_plus_importants_liste = mot_plus_important(matrice_tfidf, vocabulaire, noms_fichiers)
    message = "Mot(s) ayant le score TF-IDF le plus élevé dans chaque document:\n"
    for fichier, mot in mots_plus_importants_liste:
        message += f"Document '{fichier}': {mot}\n"
    print("Mots plus importants", message)

def recuperer_mots_plus_frequents_chirac():
    #recupre tout les mots des 2 discourt de chirac
    with open("cleaned//Nomination_Chirac1_cleaned.txt", 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    tf_fichier = TF(contenu)
    with open("cleaned//Nomination_Chirac2_cleaned.txt", 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    tf_fichier = TF(contenu)
    #retire les mots nom important de la liste de tout les mots dit par chirac
    matrice_tfidf, _, vocabulaire = calculer_matrice_tfidf(corpus_directory)
    mots_non_importants_liste = mots_non_importants(matrice_tfidf, vocabulaire)
    for i in range(len(mots_non_importants_liste)):
        if mots_non_importants_liste[i] in tf_fichier:
            del tf_fichier[mots_non_importants_liste[i]]

    # determine les mots les plus frequent dit par chirac sans les mots non importants
    print("Entrez le nombre de mots le plus répété par le président Chirac :")

    #entrez securisez pour evitez les valeur autre que des entier
    secu = "faux"
    while secu != "vrai":
        nb_mot = input()
        if nb_mot.isdigit():        #.isdigit() verifie si la valeur est un entier
            nb_mot = int(nb_mot)
            secu = "vrai"
        else:
            print("entrez un entier")
    mot_plus_frequent = mots_plus_frequents(tf_fichier, nb_mot)
    message = f"Les {nb_mot} mots les plus fréquents sont : {mot_plus_frequent}"
    print("Mots les plus repetée par Chirac", message)


def chercher_premier_president_parler_climat():
    dossier_corpus = ("cleaned")
    extension_fichier = ".txt"
    mot_recherche = "climat"
    president_max, occurrences_max = president_plus_parle_mot(dossier_corpus, extension_fichier, mot_recherche)
    print(f"Le premier président qui a parlez de  '{mot_recherche}' est {president_max} avec {occurrences_max} occurrences.")

def chercher_president_plus_parle_mot():
    dossier_corpus = ("cleaned")
    extension_fichier = ".txt"
    # Demander à l'utilisateur de saisir un mot
    print("Recherche de mot, entrez le mot à rechercher : ")
    mot_recherche = input()
    mot_recherche = mot_recherche.lower()
    # Appeler la fonction pour trouver le président qui a le plus parlé du mot
    president_max, occurrences_max = president_plus_parle_mot(dossier_corpus, extension_fichier, mot_recherche)
    if occurrences_max==0:
        print(f"Aucun président n'a parlé de '{mot_recherche}' car il y a {occurrences_max} occurrence dans tous les discours.")
    else:
        print(f"Le président qui a le plus parlé du mot '{mot_recherche}' est {president_max} avec {occurrences_max} occurrences.")

def chatbot(question):
    # Recupere la question et la retire la ponctuation et les majuscules
    question = Tokenisation(question)
    question1 = mot_question_dans_corpus(question, "cleaned")

    # traite la question en trouvant le mots le plus important
    matrice_tfidf_corpus, noms_fichiers_corpus, _ = calculer_matrice_tfidf("cleaned")
    tf_question, vecteur_tfidf_question, mots_corpus = vecteur_question(question1, "cleaned")
    document_pertinent = document_le_plus_pertinent(matrice_tfidf_corpus, vecteur_tfidf_question,
                                                    noms_fichiers_corpus)
    mot_plus_important_question = mot_le_plus_important(question1, "cleaned")
    if mot_plus_important_question == "comment":
        mot_plus_important_question = "climat"
    phrase_contenant_mot = extraire_phrase_autour_occurrence(document_pertinent, mot_plus_important_question,
                                                             question)

    # Affiche les resultats
    print(f"Document pertinent retourné :'{document_pertinent}'\n"
          f" Mot ayant le TF-IDF le plus élevé :{mot_plus_important_question}\n"
          f" La réponse générée : {phrase_contenant_mot}")



menu = "-1"
while menu != "0":
    print("=============================================== MENU PRINCIPALE ================================================")

    print(" 1 : Menu Fonctionnalités partie 1")
    print(" 2 : TchatBot")
    print(" 0 : Quitter le programme")

    print("Choisissez menu :")
    menu = input()

    fonctionnalite = "-1"
    if menu == "1":
        while fonctionnalite != "0":
            print("=========================================== MENU Fonctionnalités ===========================================")
            print("1 : Trouver les mots non importants\n"
                  "2 : Trouver les mots plus importants\n"
                  "3 : Récupérer les mots les plus fréquents pour Chirac\n"
                  "4 : Premier president a avoir parlez de Climat\n"
                  "5 : Président qui a le plus parlez de\n"
                  "0 : retour")
            print("Choisissez une fonctionnalité:")
            fonctionnalite = input()

            if fonctionnalite == "1":
                afficher_mots_non_importants()

            if fonctionnalite == "2":
                afficher_mots_plus_importants()

            if fonctionnalite == "3":
                recuperer_mots_plus_frequents_chirac()

            if fonctionnalite == "4":
                chercher_premier_president_parler_climat()

            if fonctionnalite == "5":
                chercher_president_plus_parle_mot()
    question = "-1"
    if menu == "2":
        while question != "0":
            print("================================================ TCHATBOT ================================================")
            print("entrez votre question ou faites 0 pour revenir en arriere")
            question = input()
            if question != "0":
                chatbot(question)