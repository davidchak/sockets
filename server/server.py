# coding: utf8

import socket
import pickle
from config import server_ip, server_port
from dbase import db_exec


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(50) 

while True:
    
    connection, address = server.accept()
    print('Новый запрос от адресата: ', address)
    
    while True:

        # получаем от клиента
        b_data = connection.recv(1024)
        try:
            data = pickle.loads(b_data)
            print(data)
        except EOFError:
            data = {}
        
        if not data: 
            break
        
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
