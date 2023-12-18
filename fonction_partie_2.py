# Fichier les fonctions demander dans la partie 2 :
# Projet Efrei ChatBot Partie 2
# Maelle Chollet / Julien Mongrard
# Receuille toute les fonctiond demander dans la partie 2
from fonction_partie_1 import *



#fonction qui mets en minuscule / rere
def Tokenisation(question):
    question = question.lower()
    question = supprimer_ponctuation(question)
    question = question.split()
    return (question)


def mot_question_dans_corpus(liste, corpus_path):
    mot_question_dans_Discour = []
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                contenu = f.read()
                for mot in liste:
                    if mot in contenu:
                        mot_question_dans_Discour.append(mot)
    mot_question_dans_Discour = list(set(mot_question_dans_Discour))

    return (mot_question_dans_Discour)


def vecteur_question(liste, corpus_path):
    # recupere tout les mots du Corpus_path
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
                    mots_corpus.update(document.split())
    mots_corpus = list(mots_corpus)
    tf_question = [0] * len(mots_corpus)
    cpt = 0
    for mot in mots_corpus:
        tf_question[cpt] = liste.count(mot)
        cpt += 1
    scores_idf_question = IDF(corpus_path)
    vecteur_tfidf_question = []

    idf_question = [0] * len(mots_corpus)
    for i in range(len(mots_corpus)):
        if tf_question[i] != 0:
            temp = str(mots_corpus[i])
            idf_question[i] = scores_idf_question[temp]
        vecteur_tfidf_question.append(idf_question[i] * tf_question[i])
    return tf_question, vecteur_tfidf_question, mots_corpus


def produit_scalaire(vecteur1, vecteur2):
    return sum(x * y for x, y in zip(vecteur1, vecteur2))


def norme_vecteur(vecteur):
    return math.sqrt(sum(x ** 2 for x in vecteur))


def similarite_cosinus(vecteur1, vecteur2):
    produit = produit_scalaire(vecteur1, vecteur2)
    norme1 = norme_vecteur(vecteur1)
    norme2 = norme_vecteur(vecteur2)

    if norme1 == 0 or norme2 == 0:
        return 0  # Évite la division par zéro

    return produit / (norme1 * norme2)


def document_le_plus_pertinent(matrice_tfidf_corpus, vecteur_tfidf_question, noms_fichiers):
    scores_similarite = []

    # Calcule la similarité cosinus  vecteur question / chaque vecteur du corpus
    for i, vecteur_tfidf_corpus in enumerate(matrice_tfidf_corpus):
        sim = similarite_cosinus(vecteur_tfidf_question, vecteur_tfidf_corpus)
        scores_similarite.append((noms_fichiers[i], sim))

    # Trouve le document qui a la plus grande similarité
    document_pertinent = max(scores_similarite, key=lambda x: x[1])

    return document_pertinent[0]


def mot_le_plus_important(question, corpus_path="cleaned"):
    vecteur_tfidf_question = vecteur_question(question, corpus_path)[1]

    # Trouve l'index du mot qui a le score TF-IDF le plus élevé de la question
    index_max_tfidf = max(range(len(vecteur_tfidf_question)), key=lambda i: vecteur_tfidf_question[i])
    mots_corpus = vecteur_question([], corpus_path)[2]
    mot_plus_important_question = mots_corpus[index_max_tfidf]

    return mot_plus_important_question


def extraire_phrase_autour_occurrence(nom_document_pertinent, mot_occurrence,question):
    nom_document_pertinent = nom_document_pertinent[:-12] + ".txt"
    chemin_document_pertinent = os.path.join("speeches", nom_document_pertinent)

    # Lis le contenu du document pertinent
    with open(chemin_document_pertinent, 'r', encoding='utf-8') as fichier:
        contenu_document_pertinent = fichier.read()

    # Trouve la première occurrence du mot dans le document
    index_occurrence = contenu_document_pertinent.find(mot_occurrence)



    # Extrait la phrase autour de cette occurrence
    debut_phrase = contenu_document_pertinent.rfind('.', 0, index_occurrence) + 1
    fin_phrase = contenu_document_pertinent.find('.', index_occurrence)+1

    phrase_contenant_mot = contenu_document_pertinent[debut_phrase:fin_phrase]

    # Dictionnaire associant des formes de questions à des modèles de réponses
    question_starters = {
        "comment": "Après analyse,",
        "pourquoi": "Car,",
        "peux": "Oui, bien sûr!"}

    # Vérifie si la question a une correspondance dans le dictionnaire
    if question[0] in question_starters:
        phrase_contenant_mot = question_starters[question[0]]+phrase_contenant_mot.strip()


    return phrase_contenant_mot


