import tkinter as tk
from PageConnexion import LoginPage
from Acceuil import OpenCartMonitorApp

if __name__ == "__main__":
    root = tk.Tk()

    #Affiche la page de connexion

    login_page = LoginPage(root)

    root.mainloop()
