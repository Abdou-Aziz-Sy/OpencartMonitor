import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

class GestionProduits:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des produits")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Liste des produits")
        self.label.grid(row=0, column=0, columnspan=5)

        self.tableau_produits = ttk.Treeview(self.frame, columns=("ID", "Nom", "Prix", "Quantité", "Actions"), show="headings", selectmode="browse")
        self.tableau_produits.heading("ID", text="ID")
        self.tableau_produits.heading("Nom", text="Nom")
        self.tableau_produits.heading("Prix", text="Prix")
        self.tableau_produits.heading("Quantité", text="Quantité")
        self.tableau_produits.heading("Actions", text="Actions")
        self.tableau_produits.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        self.btn_actualiser = tk.Button(self.frame, text="Actualiser", command=self.actualiser_produits)
        self.btn_actualiser.grid(row=2, column=0, pady=5)

        self.btn_ajouter = tk.Button(self.frame, text="Ajouter", command=self.ajouter_produit)
        self.btn_ajouter.grid(row=2, column=1, pady=5)

        self.btn_modifier = tk.Button(self.frame, text="Modifier", command=self.modifier_produit)
        self.btn_modifier.grid(row=2, column=2, pady=5)

        self.btn_supprimer = tk.Button(self.frame, text="Supprimer", command=self.supprimer_produit)
        self.btn_supprimer.grid(row=2, column=3, pady=5)

        self.actualiser_produits()

    def actualiser_produits(self):
        for child in self.tableau_produits.get_children():
            self.tableau_produits.delete(child)

        produits = self.lister_produits()
        if produits:
            for produit in produits:
                self.tableau_produits.insert("", "end", values=(produit['product_id'], produit['model'], produit['price'], produit['quantity'], ""))
    
    def lister_produits(self):
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='',
                                         db='opencart',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM oc_product")
                return cursor.fetchall()
        except Exception as e:
            print("Erreur lors de la récupération de la liste des produits:", e)
            return None
        finally:
            connection.close()

    def ajouter_produit(self):
        ajouter_window = tk.Toplevel(self.root)
        ajouter_window.title("Ajouter un produit")

        label_nom = tk.Label(ajouter_window, text="Nom du produit :")
        label_nom.grid(row=0, column=0, padx=5, pady=5)
        entry_nom = tk.Entry(ajouter_window)
        entry_nom.grid(row=0, column=1, padx=5, pady=5)

        label_prix = tk.Label(ajouter_window, text="Prix du produit :")
        label_prix.grid(row=1, column=0, padx=5, pady=5)
        entry_prix = tk.Entry(ajouter_window)
        entry_prix.grid(row=1, column=1, padx=5, pady=5)

        label_quantite = tk.Label(ajouter_window, text="Quantité du produit :")
        label_quantite.grid(row=2, column=0, padx=5, pady=5)
        entry_quantite = tk.Entry(ajouter_window)
        entry_quantite.grid(row=2, column=1, padx=5, pady=5)

        btn_valider = tk.Button(ajouter_window, text="Valider", command=lambda: self.valider_ajout(ajouter_window, entry_nom.get(), entry_prix.get(), entry_quantite.get()))
        btn_valider.grid(row=3, column=0, columnspan=2, pady=5)

    def valider_ajout(self, window, nom, prix, quantite):
        if nom and prix and quantite:
            try:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             db='opencart')
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO oc_product (model, price, quantity) VALUES (%s, %s, %s)",
                                   (nom, prix, quantite))
                    connection.commit()
            except Exception as e:
                print("Erreur lors de l'ajout du produit:", e)
                connection.rollback()
            finally:
                connection.close()
            self.actualiser_produits()
            messagebox.showinfo("Succès", "Produit ajouté avec succès.")
            window.destroy()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

    def modifier_produit(self):
        selected_item = self.tableau_produits.focus()
        if selected_item:
            produit_id = self.tableau_produits.item(selected_item, 'values')[0]
            modifier_window = tk.Toplevel(self.root)
            modifier_window.title("Modifier un produit")

            label_nom = tk.Label(modifier_window, text="Nouveau nom du produit :")
            label_nom.grid(row=0, column=0, padx=5, pady=5)
            entry_nom = tk.Entry(modifier_window)
            entry_nom.grid(row=0, column=1, padx=5, pady=5)

            label_prix = tk.Label(modifier_window, text="Nouveau prix du produit :")
            label_prix.grid(row=1, column=0, padx=5, pady=5)
            entry_prix = tk.Entry(modifier_window)
            entry_prix.grid(row=1, column=1, padx=5, pady=5)

            label_quantite = tk.Label(modifier_window, text="Nouvelle quantité du produit :")
            label_quantite.grid(row=2, column=0, padx=5, pady=5)
            entry_quantite = tk.Entry(modifier_window)
            entry_quantite.grid(row=2, column=1, padx=5, pady=5)

            btn_valider = tk.Button(modifier_window, text="Valider", command=lambda: self.valider_modification(modifier_window, produit_id, entry_nom.get(), entry_prix.get(), entry_quantite.get()))
            btn_valider.grid(row=3, column=0, columnspan=2, pady=5)
        else:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un produit à modifier.")

    def valider_modification(self, window, produit_id, nom, prix, quantite):
        if nom and prix and quantite:
            try:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             db='opencart')
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE oc_product SET model = %s, price = %s, quantity = %s WHERE product_id = %s",
                                   (nom, prix, quantite, produit_id))
                    connection.commit()
            except Exception as e:
                print("Erreur lors de la modification du produit:", e)
                connection.rollback()
            finally:
                connection.close()
            self.actualiser_produits()
            messagebox.showinfo("Succès", "Produit modifié avec succès.")
            window.destroy()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

    def supprimer_produit(self):
        selected_item = self.tableau_produits.focus()
        if selected_item:
            produit_id = self.tableau_produits.item(selected_item, 'values')[0]
            if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce produit ?"):
                try:
                    connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='',
                                                 db='opencart')
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM oc_product WHERE product_id = %s", (produit_id,))
                        connection.commit()
                except Exception as e:
                    print("Erreur lors de la suppression du produit:", e)
                    connection.rollback()
                finally:
                    connection.close()
                self.actualiser_produits()
                messagebox.showinfo("Succès", "Produit supprimé avec succès.")
        else:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un produit.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionProduits(root)
    root.mainloop()
