import pymysql

def get_connected_users_count():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='opencartdb',)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM oc_session WHERE session_id != ''")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print("Erreur lors de la récupération du nombre d'utilisateurs connectés:", e)
        return None
    finally:
        connection.close()
# Fonction pour récupérer le nombre de transactions en cours
def get_active_transactions_count():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='opencartdb')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM oc_order WHERE order_status_id IN (0, 7)")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print("Erreur lors de la récupération du nombre de transactions en cours:", e)
        return None
    finally:
        connection.close()

# Fonction pour bloquer les transactions/ventes
def block_transactions():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='opencartdb')
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE oc_order SET order_status_id = 0 WHERE order_status_id IN (2, 3, 5)")
        connection.commit()
        print("Transactions bloquées avec succès.")
    except Exception as e:
        connection.rollback()
        print("Erreur lors du blocage des transactions:", e)
    finally:
        connection.close()


