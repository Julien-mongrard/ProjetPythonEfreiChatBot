import tkinter as tk
from tkinter import messagebox

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Principal")

        # Créer le menu
        self.menu = tk.Menu(root)

        # Options du menu
        options = [
            ("Option 1", self.option_1),
            ("Option 2", self.option_2),
            ("Option 3", self.option_3),
            ("Option 4", self.option_4),
            ("Option 5", self.option_5),
            ("Option 6", self.option_6)
        ]

        # Ajouter les options au menu
        for option_text, option_command in options:
            self.add_menu_option(option_text, option_command)

        # Configurer le menu
        root.config(menu=self.menu)

    def add_menu_option(self, option_text, option_command):
        menu_option = tk.Menu(self.menu, tearoff=0)
        menu_option.add_command(label=option_text, command=option_command)
        self.menu.add_cascade(label=f"Menu {option_text}", menu=menu_option)

    def option_1(self):
        self.show_message("Option 1")

    def option_2(self):
        self.show_message("Option 2")

    def option_3(self):
        self.show_message("Option 3")

    def option_4(self):
        self.show_message("Option 4")

    def option_5(self):
        self.show_message("Option 5")

    def option_6(self):
        self.show_message("Option 6")

    def show_message(self, option_text):
        messagebox.showinfo("Option Sélectionnée", f"Vous avez choisi {option_text}")

def main():
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

# Appeler la fonction principale pour démarrer l'application
main()