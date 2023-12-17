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

print("Entrez votre question : ")
question = input()
question = Tokenisation(question)
print(question)
question1 = mot_question_dans_corpus(question,"cleaned")
print(question1)


def vecteur_question(liste, corpus_path):
    #recupere tout les mots du Corpus_path
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
                    mots_corpus.update(document.split())
    mots_corpus = list(mots_corpus)
    print(mots_corpus)
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

print(vecteur_question(question,"cleaned"))