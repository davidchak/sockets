# coding: utf8

import sys
import pickle
import time
from random import randint
from string import ascii_lowercase
from socket import *
import json
from pathlib import Path
from config import server_ip, server_port, time_interval, json_file_path
from dbase import db_exec


def create_db():
    db_exec("CREATE TABLE 'client' ('client_id'	TEXT)")
    db_exec("CREATE TABLE 'task' ('task_id'	INTEGER)")
    db_exec("INSERT INTO task(task_id) VALUES(0)")


def generate_client_id(id_len=20):
    clinet_id = ''
    for i in range(id_len):
        clinet_id += ascii_lowercase[randint(0, 25)]
    return clinet_id


# def check_client_id():
# 	cid = db_exec('select client_id from client')
# 	print(cid)
# 	if not cid:
# 		db_exec(f'insert into client(client_id) values({generate_client_id()})')



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
                # print(data)
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
                data = {}


            
        except ConnectionRefusedError as err:
            print(f'Ошибка соединения: {err}')

        finally:
            client.close()
        
        time.sleep(sec)





        

        
if __name__ == '__main__':
    create_db()
    check_client_id()
    start_client(time_interval)
