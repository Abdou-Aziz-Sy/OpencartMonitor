import tkinter as tk
from tkinter import ttk
import pymysql
from collections import defaultdict
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Analytique du site")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.plot = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack()

        self.get_client_data()
        self.plot_bar_chart()

    def get_client_data(self):
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='',
                                         db='opencart',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute("SELECT DATE_FORMAT(date_added, '%Y-%m') AS month, COUNT(customer_id) AS num_clients FROM oc_customer GROUP BY month")
                self.client_data = cursor.fetchall()
        except Exception as e:
            print("Erreur lors de la récupération des données clients:", e)
            self.client_data = None
        finally:
            connection.close()

    def plot_bar_chart(self):
        if self.client_data:
            months = defaultdict(int)
            for row in self.client_data:
                months[row['month']] = row['num_clients']

            month_labels = list(months.keys())
            num_clients = list(months.values())

            self.plot.bar(month_labels, num_clients)
            self.plot.set_xlabel('Mois')
            self.plot.set_ylabel('Nombre de clients')
            self.plot.set_title('Nombre de clients par mois')

            self.canvas.draw()
        else:
            tk.messagebox.showerror("Erreur", "Impossible de récupérer les données clients.")

