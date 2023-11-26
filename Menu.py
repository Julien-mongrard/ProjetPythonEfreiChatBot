import tkinter as tk
from tkinter import messagebox
from Fonctions import *


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
        with open("C://Users//mongr//PycharmProjects//pythonProject5//speeches//Nomination_Chirac2.txt", 'r',encoding='utf-8') as fichier:
            contenu = fichier.read()
        tf_fichier = TF(contenu)
        with open("C://Users//mongr//PycharmProjects//pythonProject5//cleaned//Nomination_Chirac1_cleaned.txt", 'r',encoding='utf-8') as fichier:
            contenu = fichier.read()
        tf_fichier = TF(contenu)
        with open("C://Users//mongr//PycharmProjects//pythonProject5//cleaned//Nomination_Chirac2_cleaned.txt", 'r',encoding='utf-8') as fichier:
            contenu = fichier.read()
        tf_fichier = TF(contenu)
        # determine les mots les plus frequent
        nb_mot = int(input("Nombre de mots le plus repeté par le président Chirac :"))
        mot_plus_frequent = mots_plus_frequents(tf_fichier, nb_mot)
        message = f"Les {nb_mot} mots les plus fréquents sont :", mot_plus_frequent
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
        mot_recherche = input("Entrez le mot à rechercher : ")
        mot_recherche = mot_recherche.lower()
        # Appeler la fonction pour trouver le président qui a le plus parlé du mot
        president_max, occurrences_max = president_plus_parle_mot(dossier_corpus, extension_fichier, mot_recherche)
        messagebox.showinfo("Président plus parlé du mot",f"Le président qui a le plus parlé du mot '{mot_recherche}' est {president_max} avec {occurrences_max} occurrences.")

    def afficher_mots_par_tous_les_presidents(self):
        # Votre code pour afficher les mots évoqués par tous les présidents
        pass

def main():
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()