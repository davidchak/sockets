# coding: utf8

#########################################################
#
#   Название: client
#   Автор: dchk09 (davidchak@yandex.ru)
#   Версия: 1.0
#   Дата разработки: 22.10.2018
#
#########################################################


import sys
import os
import pickle
import time
import sqlite3
from random import randint
from string import ascii_lowercase
from socket import *
import json
from pathlib import Path
from dbase import db_exec

base_dir = os.path.abspath(os.path.dirname(__name__))
db_path = os.path.join(base_dir, 'client.db')


######################### НАСТРОЙКИ ##########################
#
# адрес сервера
server_ip = '127.0.0.1'
#
# порт сервера
server_port = 8251
#
# интервал запроса обновлений, в секундах
time_interval = 5
#
# ссылка на папку с программой
json_file_path = os.path.join(base_dir, 'prog', 'Import.json')
#
###############################################################


def db_exec(new_query, return_result=True):

    con = sqlite3.connect(db_path)

    with con:
        cur = con.cursor()
        try:
            cur.execute(new_query)
            if return_result == True:
                result = cur.fetchall()
                return result
            cur.commit()
        except sqlite3.DatabaseError as err:
            return err


def generate_client_id(id_len=20):
    clinet_id = ''
    for i in range(id_len):
        clinet_id += ascii_lowercase[randint(0, 25)]
    return clinet_id


def create_db():
    if not os.path.exists(db_path):
        db_exec("CREATE TABLE 'client' ('client_id'	TEXT)")
        db_exec("CREATE TABLE 'task' ('task_id'	INTEGER)")
        db_exec("INSERT INTO task(task_id) VALUES(1)")
        new_cid = generate_client_id()
        db_exec(f"insert into client(client_id) values('{new_cid}')")


def get_client_data():
    c_data = {}
    c_data['client_id'] = db_exec('select * from client')[0][0]
    c_data['task_id'] = db_exec('select * from task')[0][0]
    return c_data


def edit_json_file(json_path, s_task):
    path = Path(json_path)
    try:
        data = json.loads(path.read_text())
        if s_task['json_id'] != '':
            data['id'] = s_task['json_id']
        
        if s_task['json_access_token'] != '':
            data['api']['access-token'] = s_task['json_id']

        if s_task['json_ipv4'] != '':
            data['api']['ipv4'] = s_task['json_ipv4']
 
        data['api']['check'] = s_task['json_ipv4']

        path.write_text(json.dumps(data))

    except Error as json_err:
        print(json_err)



def start_client(sec):

    while True:  

        client = socket(AF_INET, SOCK_STREAM)
        
        try:
            client.connect((server_ip, server_port))
            c_data = get_client_data()
            client.send(pickle.dumps(c_data))
            s_data = client.recv(1024)
            try:
                data = pickle.loads(s_data)
                # парсим ответ сервера
                c_task_id = db_exec('select task_id from task')[0][0]

                # если есть новое задание, выполняем
                if data['task_id'] != c_task_id:
                    print(f'Новое задание {data}')
                    edit_json_file(json_file_path, data)
                    db_exec(f"update task set task_id = {data['task_id']}")
                else:
                    print('Новых заданий нет')

            except EOFError:
                pass

        except ConnectionRefusedError as err:
            print(err)
            

        except ConnectionResetError as err:
            print(err)

        finally:
            client.close()

        time.sleep(sec)

        
if __name__ == '__main__':
    create_db()
    start_client(time_interval)
