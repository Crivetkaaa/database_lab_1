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

    @staticmethod
    def generate_sql_command(delete=False, where=False):
        sql_command = f"""SELECT 
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
    users_address ON full_info_user.address = users_address.id
{('', 'WHERE ')[where == True]}
"""
        return sql_command

    @staticmethod
    def generate_dict(users: dict):
        user_name_id = []
        user_surname_id = []
        user_lastname_id = []
        user_phone_id = []
        user_address_id = []
        
        for  user in users:
            user_name_id.append(user[1])
            user_surname_id.append(user[2])
            user_lastname_id.append(user[3])
            user_phone_id.append(user[4])
            user_address_id.append(user[5])
        
        return (user_name_id, user_surname_id, user_lastname_id, user_phone_id, user_address_id)        

    @classmethod
    def clear_database(cls):
        cls.cur.execute("SELECT * FROM full_info_user")
        users = cls.cur.fetchall()
        users_info =cls.generate_dict(users)
        for user in users:
            for i in range(0, len(users_info)):
                    if user[i+1] not in users_info[i]:
                        cls.cur.execute(f"DELETE FROM {cls.data_3[i]} WHERE id = {user[i+1]}")
                        cls.conn.commit()

    @classmethod
    def change_user(cls, user_id: str, user_info: dict):
        cls.cur.execute(f"SELECT * FROM full_info_user WHERE id = {user_id}")
        user = cls.cur.fetchall()[0]
        
        for i in range(0, len(user)-1):
            cls.cur.execute(f"SELECT * FROM full_info_user WHERE {cls.data_2[i]} = {user[i+1]}")
            lenght = len(cls.cur.fetchall())
        
            if lenght == 1:
                if user_info[i] != '':
                    cls.cur.execute(f"SELECT * FROM public.{cls.data_3[i]} WHERE {cls.data_4[i]} = '{user_info[i]}'")
                    info = cls.cur.fetchall()
                    lenght_2 = len(info)
                    if lenght_2 == 0:
                        cls.cur.execute(f"UPDATE public.{cls.data_3[i]} SET {cls.data_4[i]} = '{user_info[i]}' WHERE id = {user[i+1]}")
                    else:
                        cls.cur.execute(f"UPDATE public.full_info_user SET {cls.data_2[i]} = {info[0][0]} WHERE id = {user[0]}")
                    cls.conn.commit()

            else:
                if user_info[i] != '':
                    cls.cur.execute(f"INSERT INTO {cls.data_3[i]} ({cls.data_4[i]}) VALUES('{user_info[i]}')  ON CONFLICT ({cls.data_4[i]}) DO NOTHING")
                    cls.conn.commit()
                    cls.cur.execute(f"SELECT id FROM {cls.data_3[i]} WHERE {cls.data_4[i]} = '{user_info[i]}'")
                    user_info_id = cls.cur.fetchall()[0][0]
                    cls.cur.execute(f"UPDATE public.full_info_user SET {cls.data_2[i]} = '{user_info_id}' WHERE id = {user[0]}")
                    cls.conn.commit()
        cls.clear_database()

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
        sql_command = cls.generate_sql_command(delete)
        cls.cur.execute(sql_command)
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

        sql_command = cls.generate_sql_command(where=True)
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
