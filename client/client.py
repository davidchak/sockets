# coding: utf8

import sys
import os
import pickle
import time
import sqlite3
from shutil import copyfile
from datetime import datetime
from random import randint
import subprocess
from string import ascii_lowercase
from socket import *
import json
from pathlib import Path


version = '1.3'
base_dir = os.path.abspath(os.path.dirname(__name__))
db_path = os.path.join(base_dir, 'client.db')
json_config_filepath = os.path.join(base_dir, 'config.json')
temp_path = os.path.join(base_dir, 'temp_path')
script_info = f'''
    ===========================================
        name: CLIENT
        ver: {version}
        autor: dchak09 (davidchak@yandex.ru)
    ===========================================
    '''

# создаем config.json при старте
def create_config_on_start():
    config = {
        "server_ip" : "127.0.0.1", 
        "server_port" : 8251,
        "time_interval" : 5,
        "prog_path": "c:\\temp"
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
            print(json_err)
    else:
        print('broken config.json')


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
            cur.commit()
        except sqlite3.DatabaseError as err:
            return err


# генератор id клиента
def generate_client_id(id_len=20):
    clinet_id = ''
    for i in range(id_len):
        clinet_id += ascii_lowercase[randint(0, 25)]
    return clinet_id


# создание базы банных
def create_db():
    if not os.path.exists(db_path):
        db_exec("CREATE TABLE 'client' ('client_id'	TEXT)")
        db_exec("CREATE TABLE 'task' ('task_id'	INTEGER)")
        db_exec("INSERT INTO task(task_id) VALUES(1)")
        new_cid = generate_client_id()
        db_exec(f"insert into client(client_id) values('{new_cid}')")


# редактируем файл Import.json
def edit_json_file(json_path, s_task):
    path = Path(json_path)
    try:
        data = json.loads(path.read_text())
        data = s_task
        path.write_text(json.dumps(data))

    except Exception as json_err:
        print('ERROR: broken config.json')


# получаем дату и время
def get_time():
    now = datetime.now()
    return (f'{now.day}-{now.month}-{now.year} {now.hour}:{now.minute}:{now.second}')


# заменяет файл новым и завершает работу
def update_file(old_exe_path, temp_path):
    
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    new = os.path.join(temp_path, 'btex.exe')
    old = old_exe_path

    print("client > stop process btex.exe")

    try:
        os.remove(old)
    except Exception as err:
        cmd = ['powershell.exe', '(Get-Process btex).id']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        proc_info = p.communicate()
        pid = proc_info[0].decode()[:-2]
        print(pid)
        os.kill(pid, 0)
        os.remove(old)

    print("client > copy new file btex.exe")
    copyfile(new, old)
    print("client > start btex.exe")
    subprocess.call(old)
    os.remove(new)
    

# составляем запрос
def query(msg, server_ip, server_port):

    print()
    print()

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((server_ip, server_port))

    print(get_time(), ' client')

    # отправляем
    data = {}
    data['task_id'] = db_exec('select * from task')[0][0]
    data['q'] = msg
    print('client > ', data)
    bin_data = pickle.dumps(data)
    client.send(bin_data)

    # принимаем
    while True:
        s_bin_data = client.recv(1024)
        
        if not s_bin_data:
            break

        s_data = pickle.loads(s_bin_data)
        
        print('server < ', s_data)

        return s_data
    
    client.close()


# запускаем все в работу
def start_client():

    print(script_info)

    # получаем настройки из файла config.json
    app_config = get_config_from_json_file(json_config_filepath)

    # объявляем переменные
    server_ip = app_config['server_ip']
    server_port = app_config['server_port']
    time_interval = app_config['time_interval']
    prog_path = app_config['prog_path']
    temp_path = os.path.join(os.environ['appdata'], 'client')

    # проверяем папку временных файлов, если ее нет - создаем
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    # проверка на наличие переменных окружения в файле
    if prog_path[0] == '%':
        s_path = prog_path.split('\\')
        prog_path = os.environ[s_path[0][1:-1]]
        for i in s_path:
            if i != 0:
                prog_path = os.path.join(prog_path, i)
    
    json_file_path = os.path.join(prog_path, 'Import.json')
    exe_file_path = os.path.join(prog_path, 'btex.exe')


    client_id = db_exec('select * from client')[0][0]
    
    c_data = {}
    c_data['client_id'] = client_id

    # запускаем "вечный" цикл
    while True:  
        
        try:
            # Запрашиваем задания
            resp = query('get_new_tasks', server_ip, server_port)
            
            if resp['r'] != 'no_new_tasks':
                
                # запрашиваем json    
                if resp['tasks']['update_json'] == 1:  
                    resp_1 = query('get_new_json', server_ip, server_port)
                    print('отладка 1' , resp)
                    edit_json_file(json_file_path, resp_1['json_file'])
                
                # запрашиваем exe     
                if resp['tasks']['update_exe'] == 1:
                    
                    print()
                    print()

                    client = socket(AF_INET, SOCK_STREAM)
                    client.connect((server_ip, server_port))

                    print(get_time(), ' client')

                    # отправляем
                    data = {}
                    s_data = {}
                    data['task_id'] = db_exec('select * from task')[0][0]
                    data['q'] = 'get_new_exe'
                    print('client > ', data)
                    bin_data = pickle.dumps(data)
                    client.send(bin_data)

                    # получаем
                    s_bin_data = client.recv(1024)
                    s_data = pickle.loads(s_bin_data)
                    print('server < ', s_data)
                        
                    size = int(s_data['data_len'])
                    
                    exe = b''
                    
                    # получаем файл
                    while size > len(exe):
                        
                        s_data_2 = client.recv(1024)

                        if not s_data_2: 
                            break

                        exe += s_data_2

                    with open(os.path.join(temp_path, 'btex.exe'), 'wb') as exe_file:
                        exe_file.write(exe)
                    
                    client.close()

                    update_file(exe_file_path, temp_path)
                    
                
                db_exec(f"update task set task_id = {resp['tasks']['task_id']}")

            else:
                print('client > wait new tasks...')
    
        except Exception as err:
            print(get_time(), 'waiting ...')
            
        time.sleep(time_interval)
        
        
if __name__ == '__main__':
    create_db()
    create_config_on_start()
    start_client()
