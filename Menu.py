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
            ("Trouver le président qui a le plus parlé d'un mot", self.chercher_president_plus_parle_mot),
            ("Premier président à parler d'un mot", self.chercher_premier_president_parler_mot),
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
        # Votre code pour récupérer les mots les plus fréquents pour Chirac
        pass

    def chercher_president_plus_parle_mot(self):
        # Votre code pour chercher le président qui a le plus parlé d'un mot
        pass

    def chercher_premier_president_parler_mot(self):
        # Votre code pour chercher le premier président à parler d'un mot
        pass

    def afficher_mots_par_tous_les_presidents(self):
        # Votre code pour afficher les mots évoqués par tous les présidents
        pass

def main():
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()