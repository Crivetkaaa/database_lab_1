import psycopg2


class DataBase:
    conn = psycopg2.connect(dbname='db', user='postgres', password='qwerty', port='5432', host='127.0.0.1')
    cur = conn.cursor()

    @classmethod
    def insert_user(cls, *arg):
        cls.cur.execute(f"INSERT INTO users_name (user_name) VALUES('{arg[0]}')")
        cls.conn.commit()
        cls.cur.execute("SELECT id FROM users_name ORDER BY id DESC")
        user_name_id = cls.cur.fetchall()[0][0]

        cls.cur.execute(f"INSERT INTO users_surname (user_surname) VALUES('{arg[1]}')")
        cls.conn.commit()
        cls.cur.execute("SELECT id FROM users_surname ORDER BY id DESC")
        user_surname_id = cls.cur.fetchall()[0][0]

        cls.cur.execute(f"INSERT INTO users_lastname (user_lastname) VALUES('{arg[2]}')")
        cls.conn.commit()
        cls.cur.execute("SELECT id FROM users_lastname ORDER BY id DESC")
        user_lastname_id = cls.cur.fetchall()[0][0]

        cls.cur.execute(f"INSERT INTO users_phone (user_phone) VALUES('{arg[3]}')")
        cls.conn.commit()
        cls.cur.execute("SELECT id FROM users_phone ORDER BY id DESC")
        user_phone_id = cls.cur.fetchall()[0][0]

        cls.cur.execute(f"INSERT INTO users_address (user_address) VALUES('{arg[4]}')")
        cls.conn.commit()
        cls.cur.execute("SELECT id FROM users_address ORDER BY id DESC")
        user_address_id = cls.cur.fetchall()[0][0]

        cls.cur.execute(f"INSERT INTO full_info_user (user_name, lastname, surname, address, phone) VALUES({user_name_id}, {user_lastname_id}, {user_surname_id}, {user_address_id}, {user_phone_id})")
        cls.conn.commit()
        
        
