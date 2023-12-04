import psycopg2


class DataBase:
    conn = psycopg2.connect(dbname='db', user='postgres', password='qwerty', port='5432', host='127.0.0.1')
    cur = conn.cursor()

    @classmethod
    def insert_user(cls, arg: dict):
        arg[0] = arg[0][0:30]
        if arg[0] != '':
            cls.cur.execute(f"INSERT INTO users_name (user_name) VALUES('{arg[0]}')  ON CONFLICT (user_name) DO NOTHING")
            cls.conn.commit()
            cls.cur.execute("SELECT id FROM users_name ORDER BY id DESC")
            user_name_id = cls.cur.fetchall()[0][0]
        
        if arg[1] != '':
            arg[1] = arg[1][0:30]
            cls.cur.execute(f"INSERT INTO users_surname (user_surname) VALUES('{arg[1]}')  ON CONFLICT (user_surname) DO NOTHING")
            cls.conn.commit()
            cls.cur.execute("SELECT id FROM users_surname ORDER BY id DESC")
            user_surname_id = cls.cur.fetchall()[0][0]

        if arg[2] != '':
            arg[2] = arg[2][0:30]
            cls.cur.execute(f"INSERT INTO users_lastname (user_lastname) VALUES('{arg[2]}') ON CONFLICT (user_lastname) DO NOTHING")
            cls.conn.commit()
            cls.cur.execute("SELECT id FROM users_lastname ORDER BY id DESC")
            user_lastname_id = cls.cur.fetchall()[0][0]

        if arg[3] != '':
            arg[3] = arg[3][0:30]
            cls.cur.execute(f"INSERT INTO users_phone (user_phone) VALUES('{arg[3]}') ON CONFLICT (user_phone) DO NOTHING")
            cls.conn.commit()
            cls.cur.execute("SELECT id FROM users_phone ORDER BY id DESC")
            user_phone_id = cls.cur.fetchall()[0][0]
        
        if arg[4] != '':
            arg[4] = arg[4][0:30]
            cls.cur.execute(f"INSERT INTO users_address (user_address) VALUES('{arg[4]}') ON CONFLICT (user_address) DO NOTHING")
            cls.conn.commit()
            cls.cur.execute("SELECT id FROM users_address ORDER BY id DESC")
            user_address_id = cls.cur.fetchall()[0][0]

        cls.cur.execute(f"INSERT INTO full_info_user (user_name, lastname, surname, address, phone) VALUES({user_name_id}, {user_lastname_id}, {user_surname_id}, {user_address_id}, {user_phone_id})")
        cls.conn.commit()
        
    @classmethod
    def get_all_from_table(cls, table_name:str, column_name:str) ->dict:
        cls.cur.execute(f"SELECT {column_name} FROM {table_name}")
        datas = cls.cur.fetchall()
        
        return_dict = ['']
        
        for data in datas:
            return_dict.append(data[0])
        
        return return_dict

    @classmethod
    def get_users(cls):
        cls.cur.execute("""SELECT 
    
    users_name.user_name,
    users_surname.user_surname,
    users_lastname.user_lastname,
	users_phone.user_phone,
    users_address.user_address
    
FROM 
    full_info_user
JOIN 
    users_name ON full_info_user.user_name = users_name.id
JOIN 
    users_surname ON full_info_user.surname = users_surname.id
JOIN 
    users_lastname ON full_info_user.lastname = users_lastname.id
JOIN 
    users_phone ON full_info_user.phone = users_phone.id
JOIN 
    users_address ON full_info_user.address = users_address.id;
""")
        return cls.cur.fetchall()

    @classmethod
    def search(cls, *args):
        users_info = []
        for arg in args:
            if arg == '':
                arg = '*'
                users_info.append(arg)
            else:
                users_info.append(arg)

        sql_command = '''SELECT 
    
    users_name.user_name,
    users_surname.user_surname,
    users_lastname.user_lastname,
	users_phone.user_phone,
    users_address.user_address
    
FROM 
    full_info_user
JOIN 
    users_name ON full_info_user.user_name = users_name.id
JOIN 
    users_surname ON full_info_user.surname = users_surname.id
JOIN 
    users_lastname ON full_info_user.lastname = users_lastname.id
JOIN 
    users_phone ON full_info_user.phone = users_phone.id
JOIN 
    users_address ON full_info_user.address = users_address.id
	
WHERE '''
        data = [
            'users_name.user_name =',
            'users_surname.user_surname =',
            'users_lastname.user_lastname =',
            'users_phone.user_phone =',
            'users_address.user_address ='
        ]
        count = 0
        for i in range(0, len(users_info)):
            if users_info[i] != '*':
                if count > 0:
                    sql_command += f"AND {data[i]} '{users_info[i]}'"
                else:
                    sql_command += f"{data[i]} '{users_info[i]}'"
                    count += 1


        if count > 0:
            cls.cur.execute(sql_command)
            return cls.cur.fetchall()
        else:
            return cls.get_users()
