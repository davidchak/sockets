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
        b_data = connection.recv(1024)
        try:
            data = pickle.loads(b_data)
        except EOFError:
            data = {}
        
        if not data: 
            break

        s_data = {}
        cid = data['client_id']
        cid_db = db_exec(f"select name from clients where name = '{cid}'")
        if not cid_db:
            db_exec(f"insert into clients(name) values ('{cid}')")


        connection.send(b'otvet')

    connection.close()
