import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from fonctions import get_active_transactions_count, block_transactions, get_connected_users_count

class OpenCartMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenCart Monitoring Interface")
        self.root.geometry("800x600")
        self.root.iconbitmap("cartico.ico")

        self.menu_frame = tk.Frame(root, bg="#333741", width=150)
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.menu_frame.pack_propagate(False)
        ttk.Label(self.menu_frame, text="    Dashboard", background="#333741", foreground="white",font=("Arial", 14, "bold")).pack(side="top", fill="x", pady=10, anchor="center")

        ttk.Separator(self.menu_frame, orient='horizontal').pack(side="top", fill="x", pady=5)

        self.content_frame = tk.Frame(root, bg="white", padx=20, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.functionality_label = tk.Label(self.content_frame, text="Sélectionnez une option dans le menu", bg="white", font=("Arial", 14))
        self.functionality_label.pack(pady=10)

        self.create_vertical_menu()

    def create_vertical_menu(self):
        options = ["People Online", "Total Orders", "Active Transactions", ]
        style = ttk.Style()
        style.configure("Menu.TButton", background="#333741", foreground="#333741")

        for option in options:
            button = ttk.Button(self.menu_frame, text=option, command=lambda o=option: self.show_functionality(o), style="Menu.TButton")
            button.pack(fill="x", padx=10, pady=2)
            ttk.Separator(self.menu_frame, orient='horizontal').pack(side="top", fill="x", pady=0, padx=5)

    def show_functionality(self, option):
        self.functionality_label.config(text=f"Affichage des {option}")
        if option == "People Online":
            self.show_people_online()
        elif option == "Total Orders":
            total_orders = self.get_total_orders()
            self.display_results(total_orders)
        elif option == "Active Transactions":
            active_transactions = self.get_active_transactions()
            self.display_results(active_transactions)
      
    def show_people_online(self):
        count = get_connected_users_count()
        if count is not None:
            result_text = f"Nombre d'utilisateurs en ligne : {count}"
            result_label = tk.Label(self.content_frame, text=result_text, bg="white", font=("Arial", 12))
            result_label.pack(pady=10)
        else:
            messagebox.showerror("Erreur", "Impossible de récupérer le nombre d'utilisateurs en ligne.")

    def get_total_orders(self):
        total_orders = {"total_orders": 1000}  # Placeholder for demonstration purposes
        return total_orders

    def get_active_transactions(self):
        active_transactions_count = get_active_transactions_count()
        if active_transactions_count is not None:
            return {"active_transactions_count": active_transactions_count}
        else:
            return {"active_transactions_count": "Erreur lors de la récupération des transactions en cours"}



    def display_results(self, data):
        result_text = ""
        for key, value in data.items():
            result_text += f"{key}: {value}\n"
        result_label = tk.Label(self.content_frame, text=result_text, bg="white", font=("Arial", 12))
        result_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenCartMonitorApp(root)
    root.mainloop()
