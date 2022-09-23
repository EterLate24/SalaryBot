from distutils.log import error
from logging import exception
import psycopg2
from db_connect import *

def new_user(chat_id, last_name, first_name, phone, nick_name):
    conn, cursor = connect_to_base()
    try:    # если запись есть, то выкидывает ошибку(или обновляет существующую запись)
        query = "INSERT INTO users(chat_id, lastname, firstname, phone, nickname, date_create) " \
                  "VALUES(%s, %s, %s, %s, %s, CURRENT_DATE)"
        cursor.execute(query, (chat_id, last_name, first_name, phone, nick_name))
        # close_connection(conn, cursor)
        print('user added')
        return 1





    except:     # ловит ошибку и обновляет запись в таблицу
        # command = "UPDATE _tblTelegramBotUser SET chat_id='%s', " \
        #           "lastname=%s, firstname=%s, nickname=%s where phone_number=%s"
        # cursor.execute(command, (chat_id, last_name, first_name, nick_name, phone_number))
        # close_connection(conn, cursor)
        print('gg')
        close_connection(conn, cursor)
        return 0