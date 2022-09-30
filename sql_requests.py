from distutils.log import error
from logging import exception
import psycopg2
from db_connect import *



def new_user(chat_id, last_name, first_name, phone, nick_name):
    try:
        conn, cursor = connect_to_base()
        cursor.execute("""INSERT INTO users (chat_id, lastname, firstname, phone, nickname, date_create) VALUES(%s, %s, %s, %s, %s, CURRENT_DATE)""", (chat_id, last_name, first_name, phone,nick_name))
        conn.commit()
        close_connection(conn, cursor)
        print('user added') 
        return 1
    except: 
        conn, cursor = connect_to_base()
        cursor.execute("UPDATE users SET phone=%s, lastname=%s, firstname=%s, nickname=%s where chat_id=%s", 
        (phone, last_name, first_name, nick_name, chat_id))
        conn.commit()
        close_connection(conn, cursor)
        print('overwrite user')
        return 0

def change_salary(chat_id, salary):
    conn, cursor = connect_to_base()
    try:
        cursor.execute("UPDATE users SET salary=%s WHERE chat_id=%s",
        (salary, chat_id))
        conn.commit()
        close_connection(conn, cursor)
        return 1
    except:
        return 0

def enter_hours(chat_id, hours):
    conn, cursor = connect_to_base()
    cursor.execute("SELECT * FROM hours WHERE chat_id =%s AND date = CURRENT_DATE", (chat_id,))
    date_select = cursor.fetchall()
    print(date_select)

    if(len(date_select)== 0):
        conn, cursor = connect_to_base()
        cursor.execute("INSERT INTO hours (chat_id, date, hours) VALUES (%s, CURRENT_DATE, %s)",
        (chat_id, hours))
        conn.commit()
        close_connection(conn, cursor)

        return 1
    else:
        conn, cursor = connect_to_base()
        cursor.execute("UPDATE hours SET hours=%s where chat_id=%s AND date=CURRENT_DATE",
        (hours, chat_id))
        conn.commit()
        close_connection(conn, cursor)

        return 0

def choose_interval(chat_id, current_date, date):
    conn, cursor = connect_to_base()
    cursor.execute("SELECT * FROM hours WHERE chat_id = %s AND date BETWEEN %s AND %s AND paid = false", (chat_id, date, current_date))
    result = cursor.fetchall()
    close_connection(conn,cursor)
    if result != None:
        return result
    else: 
        return 0

def user_salary(chat_id):
    conn, cursor = connect_to_base()
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
    result = cursor.fetchall()
    close_connection(conn,cursor)
    if result[0][6] != None:
        return result[0][6]
    else:
        return 0

def exist_check(chat_id):
    conn, cursor = connect_to_base()
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
    result = cursor.fetchall()
    close_connection(conn,cursor)
    if(len(result) == 0):
        return 0
    else:
        return 1

def check_admin(chat_id):
    admin_id = 420159893
    if chat_id == admin_id:
        return 1
    else:
        return 0

def users_list():
    conn, cursor = connect_to_base()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    close_connection(conn,cursor)
    return result

def paid_salary(chat_id, date, current_date):
    conn, cursor = connect_to_base()
    cursor.execute("UPDATE hours SET paid=true WHERE chat_id=%s AND date BETWEEN %s AND %s", 
    (chat_id, date, current_date))
    conn.commit()
    close_connection(conn, cursor)
    return 1
