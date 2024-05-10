import mysql.connector

def is_null(username,password):
	if(username==''or password==''):
		return True
	else:
		return False

def is_existed(username, password):
    db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12041111Xx',
            database='account_management'
            )
    cur = db.cursor()
    try:
        sql = "SELECT * FROM user WHERE username = '%s' and password = '%s'" % (username, password)
        cur.execute(sql)
        result = cur.fetchall()
        return len(result) > 0
    except Exception as e:
        print("Error occurred during database operation:", e)
        db.rollback()
        return False
    finally:
        cur.close()
        db.close()

def exist_user(username):
    db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12041111Xx',
            database='account_management'
            )
    cur = db.cursor()
    try:
        sql = "SELECT * FROM user WHERE username = '%s'" % username
        cur.execute(sql)
        result = cur.fetchall()
        return len(result) > 0
    except Exception as e:
        print("Error occurred during database operation:", e)
        return False
    finally:
        cur.close()
        db.close()

