# coding: utf8

import sys
import pickle
import time
from random import randint
from string import ascii_lowercase
from socket import *
from config import server_ip, server_port, time_interval
from dbase import db_exec



def generate_client_id(id_len=20):
    clinet_id = ''
    for i in range(id_len):
        clinet_id += ascii_lowercase[randint(0, 25)]
    return clinet_id


def get_client_data():
    c_data = {}
    c_data['client_id'] = db_exec('select * from client')
    c_data['task_id'] = db_exec('select * from task')
    return c_data


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
                print(data)
            except EOFError:
                data = {}


            
        except ConnectionRefusedError as err:
            print(f'Ошибка соединения: {err}')

        finally:
            client.close()
        
        time.sleep(sec)


def check_client_id():
    cid = db_exec('select client_id from client')
    if not cid:
        db_exec(f'insert into client(client_id) values({generate_client_id()})')

        
if __name__ == '__main__':
    check_client_id()
    start_client(time_interval)
