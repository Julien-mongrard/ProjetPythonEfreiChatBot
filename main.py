from Fonctions import *
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

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
for i, vecteur_tfidf in enumerate(matrice_tfidf):
    print(f"\nVecteur TF-IDF pour le document '{noms_fichiers[i]}':")
    for j, score_tfidf in enumerate(vecteur_tfidf):
        print(f"{vocabulaire[j]}: {score_tfidf}")

class MenuApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu Principal")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Menu Principal")
        self.label.pack()

        options = [
            ("Trouver les mots non importants", self.afficher_mots_non_importants),
            ("Trouver les mots plus importants", self.afficher_mots_plus_importants),
            ("Récupérer les mots les plus fréquents pour Chirac", self.recuperer_mots_plus_frequents_chirac),
            ("Premier president a avoir parlez de Climat", self.chercher_premier_president_parler_climat),
            ("Président qui a le plus parlez de", self.chercher_president_plus_parle_mot),
            ("Mots évoqués par tous les présidents", self.afficher_mots_par_tous_les_presidents)
        ]

        for option_text, option_command in options:
            button = tk.Button(self.frame, text=option_text, command=option_command)
            button.pack()

    def afficher_mots_non_importants(self):
        corpus_directory = "cleaned"
        matrice_tfidf, _, vocabulaire = calculer_matrice_tfidf(corpus_directory)
        mots_non_importants_liste = mots_non_importants(matrice_tfidf, vocabulaire)
        messagebox.showinfo("Mots non importants", f"Liste des mots les moins importants:\n{mots_non_importants_liste}")

    def afficher_mots_plus_importants(self):
        corpus_directory = "cleaned"
        matrice_tfidf, noms_fichiers, vocabulaire = calculer_matrice_tfidf(corpus_directory)
        mots_plus_importants_liste = mot_plus_important(matrice_tfidf, vocabulaire, noms_fichiers)
        message = "Mot(s) ayant le score TF-IDF le plus élevé dans chaque document:\n"
        for fichier, mot in mots_plus_importants_liste:
            message += f"Document '{fichier}': {mot}\n"
        messagebox.showinfo("Mots plus importants", message)

    def recuperer_mots_plus_frequents_chirac(self):
        with open("speeches//Nomination_Chirac2.txt", 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        tf_fichier = TF(contenu)
        with open("cleaned//Nomination_Chirac1_cleaned.txt", 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        tf_fichier = TF(contenu)
        with open("cleaned//Nomination_Chirac2_cleaned.txt", 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        tf_fichier = TF(contenu)
        # determine les mots les plus frequent
        nb_mot = simpledialog.askinteger("Nombre de mots", "Entrez le nombre de mots le plus répété par le président Chirac :")
        mot_plus_frequent = mots_plus_frequents(tf_fichier, nb_mot)
        message = f"Les {nb_mot} mots les plus fréquents sont : {mot_plus_frequent}"
        messagebox.showinfo("Mots les plus repetée par Chirac", message)

    def chercher_premier_president_parler_climat(self):
        dossier_corpus = ("cleaned")
        extension_fichier = ".txt"
        mot_recherche = "climat"
        president_max, occurrences_max = president_plus_parle_mot(dossier_corpus, extension_fichier, mot_recherche)
        print(f"Le premier président qui a parlez de  '{mot_recherche}' est {president_max} avec {occurrences_max} occurrences.")
        messagebox.showinfo("Président plus parlé du mot",f"Le premier président qui a parlez de  '{mot_recherche}' est {president_max} avec {occurrences_max} occurrences.")

    def chercher_president_plus_parle_mot(self):
        dossier_corpus = ("cleaned")
        extension_fichier = ".txt"
        # Demander à l'utilisateur de saisir un mot
        mot_recherche = simpledialog.askstring("Recherche de mot", "Entrez le mot à rechercher : ")
        mot_recherche = mot_recherche.lower()
        # Appeler la fonction pour trouver le président qui a le plus parlé du mot
        president_max, occurrences_max = president_plus_parle_mot(dossier_corpus, extension_fichier, mot_recherche)
        if occurrences_max==0:
            messagebox.showinfo("Président plus parlé du mot",
                                f"Aucun président n'a parlé de '{mot_recherche}' car il y a {occurrences_max} occurrence dans tous les discours.")
        else:
            messagebox.showinfo("Président plus parlé du mot",f"Le président qui a le plus parlé du mot '{mot_recherche}' est {president_max} avec {occurrences_max} occurrences.")

    def afficher_mots_par_tous_les_presidents(self):
        corpus_directory = "cleaned"
        matrices_tfidf_presidents, vocabulaire_global = calculer_matrice_tfidf_presidents(corpus_directory)

        # Appeler la fonction pour obtenir les mots prononcés par tous les présidents
        mots_par_tous_les_president = mots_par_tous_les_presidents(matrices_tfidf_presidents, vocabulaire_global)

        # Afficher des informations de débogage
        print("Mots évoqués par tous les présidents :", mots_par_tous_les_president)

        # Concaténer la liste de mots en une seule chaîne
        mots_string = ", ".join(mots_par_tous_les_president)

        # Afficher les mots dans une boîte de dialogue avec un titre approprié
        titre = "Mots par tous les présidents"
        message = f"Mots évoqués par tous les présidents : {mots_string}"
        messagebox.showinfo(titre, message)

def main():
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
