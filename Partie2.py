from Fonctions import *
def Tokenisation(question):
    question = question.lower()
    question = supprimer_ponctuation(question)
    question = question.split()
    return (question)


def mot_question_dans_corpus(liste,corpus_path):
    mot_question_dans_Discour=[]
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                contenu = f.read()
                for mot in liste:
                    if mot in contenu:
                        mot_question_dans_Discour.append(mot)
    mot_question_dans_Discour = list(set(mot_question_dans_Discour))

    return(mot_question_dans_Discour)

def vecteur_question(liste, corpus_path):
    #recupere tout les mots du Corpus_path
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
    cpt=0
    for mot in mots_corpus:
        tf_question[cpt]=liste.count(mot)
        cpt+=1
    scores_idf_question = IDF(corpus_path)
    vecteur_tfidf_question=[]

    idf_question =[0]*len(mots_corpus)
    for i in range(len(mots_corpus)):
        if tf_question[i] != 0:
            temp = str(mots_corpus[i])
            idf_question[i] = scores_idf_question[temp]
        vecteur_tfidf_question.append(idf_question[i]*tf_question[i])
    return (tf_question, vecteur_tfidf_question)

def produit_scalaire(vecteur1, vecteur2):
    return sum(x * y for x, y in zip(vecteur1, vecteur2))

def norme_vecteur(vecteur):
    return math.sqrt(sum(x ** 2 for x in vecteur))

def similarite_cosinus(vecteur1, vecteur2):
    produit = produit_scalaire(vecteur1, vecteur2)
    norme1 = norme_vecteur(vecteur1)
    norme2 = norme_vecteur(vecteur2)

    if norme1 == 0 or norme2 == 0:
        return 0  # Éviter une division par zéro

    return produit / (norme1 * norme2)

def document_le_plus_pertinent(matrice_tfidf_corpus, vecteur_tfidf_question, noms_fichiers):
    scores_similarite = []

    # Calculer la similarité cosinus  vecteur question / chaque vecteur du corpus
    for i, vecteur_tfidf_corpus in enumerate(matrice_tfidf_corpus):
        sim = similarite_cosinus(vecteur_tfidf_question, vecteur_tfidf_corpus)
        scores_similarite.append((noms_fichiers[i], sim))

    # Trouver le document qui a la plus grande similarité
    document_pertinent = max(scores_similarite, key=lambda x: x[1])

    return document_pertinent[0]

print("Entrez votre question : ")
question = input()
question = Tokenisation(question)
print(question)
question1 = mot_question_dans_corpus(question,"cleaned")
print(question1)

print(vecteur_question(question,"cleaned"))

matrice_tfidf_corpus, noms_fichiers_corpus, _ = calculer_matrice_tfidf("cleaned")
tf_question, vecteur_tfidf_question = vecteur_question(question, "cleaned")
document_pertinent = document_le_plus_pertinent(matrice_tfidf_corpus, vecteur_tfidf_question, noms_fichiers_corpus)
print(document_pertinent)