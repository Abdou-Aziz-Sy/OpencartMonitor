import tkinter as tk
from tkinter import ttk

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
        options = ["People Online", "Total Orders", "Total Sales"]
        style = ttk.Style()
        style.configure("Menu.TButton", background="#333741", foreground="#333741")

        for option in options:
            button = ttk.Button(self.menu_frame, text=option, command=lambda o=option: self.show_functionality(o), style="Menu.TButton")
            button.pack(fill="x", padx=10, pady=2)
            ttk.Separator(self.menu_frame, orient='horizontal').pack(side="top", fill="x", pady=0, padx=5)

    def show_functionality(self, option):
        self.functionality_label.config(text=f"Affichage des {option}")
        if option == "People Online":
            online_users = self.get_online_users()
            self.display_results(online_users)
        elif option == "Total Orders":
            total_orders = self.get_total_orders()
            self.display_results(total_orders)
        elif option == "Total Sales":
            total_sales = self.get_total_sales()
            self.display_results(total_sales)

    def get_online_users(self):
        return {"online_users": 50}

    def get_total_orders(self):
        return {"total_orders": 1000}

    def get_total_sales(self):
        return {"total_sales": "$50000"}

    def display_results(self, data):
        result_text = ""
        for key, value in data.items():
            
            result_text += f"{key}: {value}\n"
        result_label = tk.Label(self.content_frame, text=result_text, bg="white", font=("Arial", 12))
        result_label.pack(pady=10)