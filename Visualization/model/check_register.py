import mysql.connector
from environs import Env   
env = Env()     
env.read_env()

def add_user(username, password):
    db = mysql.connector.connect(
        host=env('HOST'),
        user=env('USER'),
        password=env('PASSWORD'),
        database=env('DATABASE_ACCOUNT')
    )
    
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

