# coding: utf8

import os
import sqlite3
import socket
import pickle
import time
from pathlib import Path
import json


base_dir = os.path.abspath(os.path.dirname(__name__))
db_path = os.path.join(base_dir, 'app.db')
json_config_filepath = os.path.join(base_dir, 'config.json')


def get_config_from_json_file(json_config_file):
    if os.path.exists(json_config_file):
        path = Path(json_config_file)
        try:
            app_config = json.loads(path.read_text())
            return app_config
        except Error as json_err:
            print(json_err)
    else:
        print('broken config.json')


def db_exec(new_query, return_result=True):

    con = sqlite3.connect(db_path)

    with con:
        cur = con.cursor()
        try:
            cur.execute(new_query)
            if return_result == True:
                result = cur.fetchall()
                return result
        except sqlite3.DatabaseError as err:
            return err


def create_db():
    if not os.path.exists(db_path):
        db_exec("CREATE TABLE 'clients' ('name' TEXT)")
        db_exec('''CREATE TABLE 'task' (
            'task_id'	INTEGER PRIMARY KEY AUTOINCREMENT,
            'update_exe'	INTEGER,
            'json_id'	TEXT,
            'json_access_token'	TEXT,
            'json_ipv4'	TEXT,
            'json_check'	INTEGER
        )''')
        db_exec("INSERT INTO 'task' ('update_exe','json_id', 'json_access_token', 'json_ipv4', 'json_check') VALUES (0, '', '', '', 0)")


def start_server():

    app_config = get_config_from_json_file(json_config_filepath)

    server_ip = app_config['server_ip']
    server_port = app_config['server_port']
    update_path = app_config['update_path']

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(50)

    create_db()

    print('''
    ===========================================
        name: server
        ver: 1.0
        autor: dchak09 (davidchak@yandex.ru)
    ===========================================
    ''')
    
    while True:
        
        connection, address = server.accept()
        print('New request: ', address)
        
        # получаем от клиента
        try:
            b_data = connection.recv(1024)
            data = pickle.loads(b_data)
        except EOFError:
            data = {}
        
        if not data: 
            continue
        
        # список для отправки на клиента
        s_data = {}

        # выбираем из данныx клиентский ид если его нет на сервере, пишем в базу
        cid = data['client_id']
        cid_db = db_exec(f"select name from clients where name = '{cid}'")
        if not cid_db:
            db_exec(f"insert into clients(name) values ('{cid}')")

        # извлекаем последнее выполненое на клиенте задание
        last_client_task_id = data['task_id']
        last_server_task_id = db_exec("select seq from sqlite_sequence where sqlite_sequence.name='task'")

        # если задание старее чем на сервере, формируем и отправляем клиенту

        if last_client_task_id < last_server_task_id[0][0]:
            new_client_task = db_exec(
                f'select * from task where task_id = {last_server_task_id[0][0]}'
            )
            
            data = {
                'task_id': new_client_task[0][0],
                'update_exe': new_client_task[0][1],
                'json_id': new_client_task[0][2],
                'json_access_token': new_client_task[0][3],
                'json_ipv4': new_client_task[0][4],
                'json_check': new_client_task[0][5],
            }
        else:
            data = {
                'task_id': last_client_task_id,
                'update_exe': 0,
                'json_id': '',
                'json_access_token': '',
                'json_ipv4': '',
                'json_check': 0,
            }
        connection.send(pickle.dumps(data))

    connection.close()


if __name__ == '__main__':
    start_server()
    time.sleep(20)
