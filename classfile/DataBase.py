import psycopg2


class DataBase:
    conn = psycopg2.connect(dbname='db', user='postgres', password='qwerty', port='5432', host='127.0.0.1')
    cur = conn.cursor()
    data = [
        'users_name.user_name =',
        'users_surname.user_surname =',
        'users_lastname.user_lastname =',
        'users_phone.user_phone =',
        'users_address.user_address ='
    ]

    data_2 = [
        'user_name',
        'surname',
        'lastname',
        'phone',
        'address'
    ]


    data_3 = [
        'users_name',
        'users_surname',
        'users_lastname',
        'users_phone',
        'users_address'
    ]
    data_4 = [
        'user_name',
        'user_surname',
        'user_lastname',
        'user_phone',
        'user_address'
    ]

    @classmethod
    def change_user(cls, user_id: str, user_info: dict):
        cls.cur.execute(f"SELECT * FROM full_info_user WHERE id = {user_id}")
        user = cls.cur.fetchall()[0]
        for i in range(0, len(user_info)):
            if user_info[i] != '':
                cls.cur.execute(f"UPDATE {cls.data_3[i]} SET {cls.data_4[i]}='{user_info[i]}' WHERE id = {user[i+1]}")
                cls.conn.commit()
            

    @classmethod
    def delete_user(cls, user_id):
        cls.cur.execute(f"SELECT * FROM full_info_user WHERE id = {user_id}")
        user = cls.cur.fetchall()[0]
        cls.cur.execute(f"DELETE FROM full_info_user WHERE id = {user_id}")
        cls.conn.commit()
        for i in range(0, len(cls.data_2)):
            cls.cur.execute(f"SELECT * FROM full_info_user WHERE full_info_user.{cls.data_2[i]} = {user[1]}")
            if len(cls.cur.fetchall()) == 0:
                cls.cur.execute(f"DELETE FROM {cls.data_3[i]} WHERE id = {user[i+1]}")
                cls.conn.commit()
        

    @classmethod
    def insert_user(cls, arg: dict, from_form=True):
        user_info = []
        for i in range(0, len (arg)):
            if arg[i] != '':
                cls.cur.execute(f"INSERT INTO {cls.data_3[i]} ({cls.data_4[i]}) VALUES('{arg[i]}')  ON CONFLICT ({cls.data_4[i]}) DO NOTHING")
                cls.conn.commit()
                cls.cur.execute(f"SELECT id FROM {cls.data_3[i]} ORDER BY id DESC")
                user_info.append(cls.cur.fetchall()[0][0])
        if from_form:
            cls.cur.execute(f"INSERT INTO full_info_user (user_name, lastname, surname, address, phone) VALUES({user_info[0]}, {user_info[1]}, {user_info[2]}, {user_info[3]}, {user_info[4]})")
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
    def get_users(cls, delete=False):
        cls.cur.execute(f"""SELECT 
    {('', 'full_info_user.id,')[delete == True]}
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
        count = 0
        for i in range(0, len(users_info)):
            if users_info[i] != '*':
                if count > 0:
                    sql_command += f"AND {cls.data[i]} '{users_info[i]}'"
                else:
                    sql_command += f"{cls.data[i]} '{users_info[i]}'"
                    count += 1


        if count > 0:
            cls.cur.execute(sql_command)
            return cls.cur.fetchall()
        else:
            return cls.get_users()
