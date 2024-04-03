import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Acceuil import OpenCartMonitorApp
import mysql.connector

class LoginPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Page de Connexion")
        self.geometry("300x200")
        self.iconbitmap("cartico.ico")
        self.configure(bg="#333741")  # Définir la couleur de fond

        ttk.Label(self, text="Veuillez vous connecter", font=("Arial", 8), background="#333741", foreground="white").pack(pady=5)  # Changer la couleur du texte

        self.parent = parent

        self.username_label = ttk.Label(self, text="Nom d'utilisateur:", background="#333741", foreground="white")  # Changer la couleur de fond et du texte
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self, background="white")  # Changer la couleur de fond de l'entrée
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self, text="Mot de passe:", background="#333741", foreground="white")  # Changer la couleur de fond et du texte
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*", background="white")  # Changer la couleur de fond de l'entrée
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self, text="Se Connecter", command=self.login, style="Custom.TButton")  # Utiliser un style personnalisé pour le bouton
        self.login_button.pack(pady=10)

        # Définir le style personnalisé pour le bouton
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", background="blue", foreground="black")  # Changer la couleur de fond et du texte

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Connexion à la base de données MySQL
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="test"
            )

            cursor = connection.cursor()
            query = "SELECT * FROM utilisateur WHERE email = %s AND mot_de_passe = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Connexion Réussie", "Connexion réussie!")
                self.destroy()  # Ferme la fenêtre de connexion
                app = OpenCartMonitorApp(self.parent)  # Affiche l'application principale
            else:
                messagebox.showerror("Erreur de Connexion", "Nom d'utilisateur ou mot de passe incorrect!")

            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            messagebox.showerror("Erreur de Connexion", f"Erreur lors de la connexion à la base de données: {error}")

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()
