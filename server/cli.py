# coding: utf8

import os
import sys
import time
import pickle
import sqlite3

base_dir = os.path.abspath(os.path.dirname(__name__))
db_path = os.path.join(base_dir, 'app.db')

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






def start_construktor():
    new_task = {}
    result = ''

    print('''
========= Конструктор новых задач ============
    ''')
    upd_exe = input('Update programm?, Y/n \n >>')
    if result.lower() == 'y':
        new_task['update_exe'] = 1
    else:
        new_task['update_exe'] = 0

    result = input('Add new "id"?, Y/n \n >>')
    if result.lower() == 'y':
        json_id = input('"id": \n >>')
        new_task['json_id'] = json_id
    else:
        new_task['json_id'] = ''


    result = input('Add new "access-token"?, Y/n \n >>')
    if result.lower() == 'y':
        json_access_token = input(
            '"access-token": \n >>')
        new_task['json_access_token'] = json_access_token
    else:
        new_task['json_access_token'] = ''
    
    result = input('Add new "ipv4"?, Y/n \n >>')
    if result.lower() == 'y':
        json_ipv4 = input('"ipv4": \n >>')
        new_task['json_ipv4'] = json_ipv4
    else:
        new_task['json_ipv4'] = ''

    result = input('Add new "check"?, Y/n \n >>')
    if result.lower() == 'y':
        json_check = input('"check": \n >>')
        new_task['json_check'] = 1
    else:
        new_task['json_check'] = 0
    
    print()
    print('=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+')
    print()
    print(f'CREATED NEW TASK : {new_task}')
    print()
    print('=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+')
    print()

    
    db_exec("insert into task (update_exe, json_id, json_access_token, json_ipv4, json_check) values({}, '{}', '{}', '{}', {})".format(
        new_task['update_exe'],
        new_task['json_id'],
        new_task['json_access_token'],
        new_task['json_ipv4'],
        new_task['json_check']
    ), return_result=False)  


def cli():
    

    while True:
        print('''
============ SERVER-MANAGER ==================
    name: server-manager
    ver: 1.0
    autor: dchak09 (davidchak@yandex.ru)
==============================================

    1. Start server

    2. Add new task

    q. Exit

==============================================
        ''')

        result = input('\n >>')
        
        if result.lower() == '1':
            os.startfile("server.exe")
    

        elif result.lower() == '2':
            start_construktor()
            time.sleep(3)
            

        elif result.lower() == 'q':
            sys.exit()

        else:
            print('try again...')


if __name__ == '__main__':
    create_db()
    cli()
