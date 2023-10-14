# Env variables
import os
from dotenv import load_dotenv

import mysql.connector as mysql

# Load env variables secrets
load_dotenv()

db = mysql.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD')
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Basement3DPrinters;")
cursor.execute("USE Basement3DPrinters")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS SlackActivity(
    user_id varchar(32),
    activity_type varchar(32),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP)"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS FileCache(
    user_id varchar(32),
    file_id varchar(32))"""
)

def record_activity(user_id, activity_type):
    query = "INSERT INTO SlackActivity (user_id, activity_type) VALUES (%s, %s)"
    value = (user_id, activity_type)
    cursor.execute(query, value)

    db.commit()

def delete_file_cache(user_id):
    try:
        cursor.execute(f"SELECT * FROM FileCache WHERE user_id='{user_id}' LIMIT 1;")
        file_id = cursor.fetchone()[1]
    
        cursor.execute(f"DELETE FROM FileCache WHERE user_id='{user_id}'")
        db.commit()

    except:
        file_id = None

    return file_id

def add_file_cache(user_id, file_id):
    query = "INSERT INTO FileCache (user_id, file_id) VALUES (%s, %s)"
    value = (user_id, file_id)
    cursor.execute(query, value)
    
    db.commit()

if __name__ == "__main__":
    #record_activity('f', 'help')

    # query = "INSERT INTO FileCache (user_id, file_id) VALUES (%s, %s)"
    # value = ("1", "fsdf")
    # cursor.execute(query, value)
    # db.commit()


    # delete_file_cache(1)

    query = f"SELECT * FROM FileCache WHERE user_id={3}"
    cursor.execute(query)

    entry = cursor.fetchone()

    print(entry[1])
