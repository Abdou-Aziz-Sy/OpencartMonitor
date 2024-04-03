import pymysql

def connection_db():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='opencartdb',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        print("Erreur lors de la connexion à la base de données:", e)
        return None

def get_connected_users_count():
    connection = connection_db()
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

def get_active_transactions_count():
    connection = connection_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM oc_order WHERE order_status_id IN (2, 3, 5)")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print("Erreur lors de la récupération du nombre de transactions en cours:", e)
        return None
    finally:
        connection.close()

def block_transactions():
    connection = connection_db()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE oc_order SET order_status_id = 0")
        connection.commit()
        print("Transactions bloquées avec succès.")
    except Exception as e:
        connection.rollback()
        print("Erreur lors du blocage des transactions:", e)
    finally:
        connection.close()

