import sqlite3
import re


class Database:

        
    def start():
        conn = sqlite3.connect('first_db.db', check_same_thread=False)
        curs = conn.cursor()

        curs.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INT NOT  NULL PRIMARY KEY,
            weather INT,
            news INT,
            cripto INT
            ) """)
        conn.commit()

    def user_check(user_id):
        conn = sqlite3.connect('first_db.db', check_same_thread=False)
        curs = conn.cursor()

        curs.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
        return re.sub("[^0-9]", "", str(curs.fetchone()))

    def add_new_id(user_id):
        conn = sqlite3.connect('first_db.db', check_same_thread=False)
        curs = conn.cursor()

        curs.execute(f"INSERT INTO users (user_id, weather, news, cripto) VALUES ({user_id},'1','1','1')")
        conn.commit()

    def service_check(user_id):
        conn = sqlite3.connect('first_db.db', check_same_thread=False)
        curs = conn.cursor()

        curs.execute(f"SELECT weather, news, cripto FROM users WHERE user_id = {user_id}")
        return re.sub("[^0-9]", "", str(curs.fetchone()))
        
    def any_update(user_id, serv, one_null):
        conn = sqlite3.connect('first_db.db', check_same_thread=False)
        curs = conn.cursor()

        curs.execute(f" UPDATE users SET {serv} = {one_null} WHERE user_id = {user_id}")
        conn.commit()
