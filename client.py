import pymysql

def lister_clients():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='opencart')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT customer_id, firstname, lastname, email FROM oc_customer")
        clients = cursor.fetchall()
        return clients
    except Exception as e:
        print("Erreur lors de la récupération de la liste des clients:", e)
        return None
    finally:
        connection.close()

def modifier_client(client_id, nouveau_nom, nouveau_prenom, nouvel_email):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='opencart')
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE oc_customer SET firstname = %s, lastname = %s, email = %s WHERE customer_id = %s",
                       (nouveau_prenom, nouveau_nom, nouvel_email, client_id))
        connection.commit()
        print("Informations du client modifiées avec succès.")
    except Exception as e:
        connection.rollback()
        print("Erreur lors de la modification des informations du client:", e)
    finally:
        connection.close()

def supprimer_client(client_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='opencart')
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM oc_customer WHERE customer_id = %s", (client_id,))
        connection.commit()
        print("Client supprimé avec succès.")
    except Exception as e:
        connection.rollback()
        print("Erreur lors de la suppression du client:", e)
    finally:
        connection.close()

# Exemple d'utilisation des fonctions
clients = lister_clients()
if clients:
    print("Liste des clients :")
    for client in clients:
        print(client)

# Modifier un client
modifier_client(1, "NouveauNom", "NouveauPrenom", "nouveau@mail.com")

# Supprimer un client
supprimer_client(2)
