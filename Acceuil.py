import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from fonctions import get_active_transactions_count, block_transactions, get_connected_users_count

class HomePage(tk.Frame):
    def __init__(self, parent, show_dashboard, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.show_dashboard = show_dashboard
        self.configure(bg="white")

        # Charger l'image et redimensionner
        banner_image = tk.PhotoImage(file="fond.png").subsample(5, 5)  # Réduire de moitié en largeur et en hauteur
        banner_label = tk.Label(self, image=banner_image)
        banner_label.image = banner_image  # Garder une référence à l'image pour éviter qu'elle ne soit supprimée par le garbage collector
        banner_label.pack(pady=10)

        # Texte expliquant l'interface et les options
        welcome_label = tk.Label(self, text="Bienvenue dans l'interface de surveillance d'OpenCart!", bg="white", font=("Arial", 16, "bold"), justify="center")
        welcome_label.pack(pady=20)

        explanation_text = (
            "Cette interface vous permet de surveiller différentes métriques de votre magasin OpenCart.\n\n"
            "Options disponibles :\n"
            "- People Online : Affiche le nombre d'utilisateurs en ligne actuellement.\n"
            "- Total Orders : Affiche le nombre total de commandes en cours.\n"
            "- Cancel Transactions : Permet d'annuler les transactions en cours.\n"
            "- Peoples : Permet de manipuler la liste des clients.\n"
            "- Dashboard : Affiche le tableau de bord complet."
        )

        explanation_label = tk.Label(self, text=explanation_text, bg="white", font=("Arial", 12), justify="left")
        explanation_label.pack(pady=10)
class OpenCartMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenCart Monitoring Interface")
        self.root.geometry("800x600")
        self.root.iconbitmap("cartico.ico")

        self.menu_frame = tk.Frame(root, bg="#333741", width=150)
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.menu_frame.pack_propagate(False)
        ttk.Label(self.menu_frame, text="    Dashboard", background="#333741", foreground="white", font=("Arial", 14, "bold")).pack(side="top", fill="x", pady=10, anchor="center")

        ttk.Separator(self.menu_frame, orient='horizontal').pack(side="top", fill="x", pady=5)

        self.content_frame = tk.Frame(root, bg="white", padx=20, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.home_page = HomePage(self.content_frame, self.show_functionality)
        self.home_page.pack(expand=True, fill="both")

        self.create_vertical_menu()


        # Affichez la page d'accueil au démarrage
        self.create_homepage()

    def create_vertical_menu(self):
        options = [("Dashboard", "dashboard_icon.png"), ("People Online", "online_icon.png"),("Peoples", "peoples.png") ,("Total Orders", "orders_icon.png"), ("Cancel Transactions", "cancel_icon.png")]
        style = ttk.Style()
        style.configure("Menu.TButton", background="#333741", foreground="#333741")

        for option, icon_file in options:
            # Charger l'icône pour cette option
            option_icon = PhotoImage(file=icon_file)
            button = ttk.Button(self.menu_frame, text=option, command=lambda o=option: self.show_functionality(o), style="Menu.TButton", image=option_icon, compound="left")
            button.image = option_icon  # Garantir que l'image est conservée en mémoire
            button.pack(fill="x", padx=10, pady=10)
            ttk.Separator(self.menu_frame, orient='horizontal').pack(side="top", fill="x", pady=0, padx=5)

    def create_homepage(self):
        self.functionality_label = tk.Label(self.content_frame, text="Bienvenue dans l'application de monitoring", bg="white", font=("Arial", 14))
        self.functionality_label.pack(pady=10)

       
        self.homepage = HomePage(self.content_frame, self.show_dashboard)
        self.homepage.pack(fill="both", expand=True)

    def create_dashboard_page(self):
      
        self.show_people_online()
        self.functionality_label = tk.Label(self.content_frame, text="Sélectionnez une option dans le menu", bg="white", font=("Arial", 14))
        self.functionality_label.pack(pady=10)
  

    def show_functionality(self, option):
        self.functionality_label.config(text=f"Affichage des {option}")
        if option == "Dashboard":
            self.create_dashboard_page()
        elif option == "People Online":
            self.show_people_online()
        elif option == "peoples":
            self.get_peoples()
        elif option == "Total Orders":
            total_orders = self.get_total_orders()
            self.display_results(total_orders)
        elif option == "Cancel Transactions":
            self.cancel_transactions()

    def show_people_online(self):
        count = get_connected_users_count()
        if count is not None:
            result_text = f"Nombre d'utilisateurs en ligne : {count}"
            result_label = tk.Label(self.content_frame, text=result_text, bg="white", font=("Arial", 12))
            result_label.pack(pady=10)
        else:
            messagebox.showerror("Erreur", "Impossible de récupérer le nombre d'utilisateurs en ligne.")

    def get_total_orders(self):
        active_transactions_count = get_active_transactions_count()
        if active_transactions_count is not None:
            return {"active_transactions_count": active_transactions_count}
        else:
            return {"active_transactions_count": "Erreur lors de la récupération des transactions en cours"}

    def cancel_transactions(self):
        confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir annuler les transactions en cours?")
        if confirmation:
            block_transactions()
            messagebox.showinfo("Blocage des transactions", "Transactions annulées avec succès.")

    def display_results(self, data):
        result_text = ""
        for key, value in data.items():
            result_text += f"{key}: {value}\n"
        result_label = tk.Label(self.content_frame, text=result_text, bg="white", font=("Arial", 12))
        result_label.pack(pady=10)

    def show_dashboard(self):
        self.create_dashboard_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenCartMonitorApp(root)
    root.mainloop()
