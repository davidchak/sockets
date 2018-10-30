# coding: utf8

import os
import sys
import sqlite3
import socket
import pickle
import time
from datetime import datetime
from pathlib import Path
import json


version = '1.3'
base_dir = os.path.abspath(os.path.dirname(__name__))
db_path = os.path.join(base_dir, 'app.db')
json_config_filepath = os.path.join(base_dir, 'config.json')
script_info = f'''
    ===========================================
        name: SERVER
        ver: {version}
        autor: dchak09 (davidchak@yandex.ru)
    ===========================================
    '''


# создаем config.json при старте
def create_config_on_start():
    config = {
        "server_ip" : "0.0.0.0",
        "server_port" : 8251,
        "update_path" : "C:\\temp\\s_prog"
    }

    config_json = os.path.join(base_dir, 'config.json')
    if not os.path.exists(config_json):
        with open(config_json, 'w', encoding="utf-8") as file:
            file.write(json.dumps(config))


# получаем конфигурацию из файла config.json
def get_config_from_json_file(json_config_file):
    if os.path.exists(json_config_file):
        path = Path(json_config_file)
        try:
            app_config = json.loads(path.read_text())
            return app_config
        except Exception as json_err:
            print("ERROR: сan't open CONFIG.JSON")
    else:
        print('ERROR: broken config.json')


# запись\ чтение из базы данных
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

# получаем дату и время
def get_time():
    now = datetime.now()
    return (f'{now.day}-{now.month}-{now.year} {now.hour}:{now.minute}:{now.second}')


# создание базы банных
def create_db():
    if not os.path.exists(db_path):
        db_exec("CREATE TABLE 'clients' ('client_id' TEXT, 'task_id' INTEGER)")
        db_exec('''CREATE TABLE 'task' (
            'task_id'	INTEGER PRIMARY KEY AUTOINCREMENT,
            'update_exe'	INTEGER,
            'update_json'	INTEGER
        )''')
        db_exec("INSERT INTO 'task' ('update_exe','update_json') VALUES (0, 0)")


# читаем новый файл import.json
def read_json_file(json_file):
    if os.path.exists(json_file):
        path = Path(json_file)
        try:
            data = json.loads(path.read_text())
            return data
        except Exception as json_err:
            print('ERROR: broken config.json')


# запускаем сервер
def start_server():

    print(script_info)

    # получаем конфигурационные данные
    app_config = get_config_from_json_file(json_config_filepath)

    # проверяем базу данных если, если ее нет создаем
    create_db()

    # устанавливаем параметры сервера
    server_ip = app_config['server_ip']
    server_port = app_config['server_port']
    update_path = app_config['update_path']
    
    # проверка на наличие переменных окружения в файле
    if update_path[0] == '%':
        env_path = update_path[0][1:-1]
        update_path = os.environ[env_path]

    # пути к файлам обновлений
    json_filepath = os.path.join(update_path, 'Import.json')
    exe_filepath = os.path.join(update_path, 'btex.exe')

    # инициализируем сервер
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(50)
    
    # запускаем "вечный" обработчик
    while True:

        conn, addr = server.accept()

        try:          
            print()
            print()
            # принимаем
            dt = get_time()
            print(f'{dt} connection: ', addr)
            c_bin_data = conn.recv(1024)
            c_data = pickle.loads(c_bin_data)
            print('client < ', c_data)


            s_last_task_id = db_exec("select seq from sqlite_sequence where sqlite_sequence.name='task'")[0][0]
            res = db_exec(f"select * from task where task.task_id = {s_last_task_id}")[0]
            s_task = {}
            s_task['task_id'] = res[0]
            s_task['update_exe'] = res[1]
            s_task['update_json'] = res[2]

            if c_data['task_id'] > s_last_task_id or c_data['task_id'] < s_last_task_id:
                
                if c_data['q'] == 'get_new_tasks':
                    s_data = {}
                    s_data['server_name'] = 'server'
                    s_data['r'] = 'ok'
                    s_data['tasks'] = s_task
                    print('server > ', s_data)
                    conn.send(pickle.dumps(s_data))

                elif c_data['q'] == 'get_new_json':
                    s_data = {}
                    s_data['server_name'] = 'server'
                    s_data['r'] = 'ok'
                    s_data['json_file'] = read_json_file(json_filepath)
                    print('server > ', s_data)
                    conn.send(pickle.dumps(s_data))
                
                elif c_data['q'] == 'get_new_exe':
                    s_data = {}
                    s_data['server_name'] = 'server'
                    s_data['r'] = 'ok'
                    with open(exe_filepath, 'rb') as exe_file:
                        data = exe_file.read()
                    s_data['data_len'] = len(data)
                    print('server > ', s_data)
                    conn.send(pickle.dumps(s_data))
                    print('server > ', 'отправляю exe-файл')
                    conn.sendall(data)

            else:
                s_data = {}
                s_data['server_name'] = 'server'
                s_data['r'] = 'no_new_tasks'
                print('server > ', s_data)
                conn.send(pickle.dumps(s_data))

        except Exception as err:
            print('Error :', err)

        finally:
            conn.close()



if __name__ == '__main__':
    create_config_on_start()
    start_server()
  
