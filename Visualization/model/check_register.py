import mysql.connector

def add_user(username, password):
    db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12041111Xx',
            database='account_management')
    cur = db.cursor()
    try:
        sql = "INSERT INTO user (username, password) VALUES ('%s', '%s')" % (username, password)
        cur.execute(sql)
        db.commit()
    except Exception as e:
        print("Error occurred during database operation:", e)
        db.rollback()
    finally:
        cur.close()
        db.close()

