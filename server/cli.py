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



def start_construktor():
    new_task = {}
    result = ''

    print('''
========= Конструктор новых задач ============
    ''')
    result = input('Update "btex.exe"?, Y/n \n >>')
    if result.lower() == 'y':
        new_task['update_exe'] = 1
    else:
        new_task['update_exe'] = 0

    result = input('Update "import.json"?, Y/n \n >>')
    if result.lower() == 'y':
        new_task['update_json'] = 1
    else:
        new_task['update_json'] = 0

    
    print()
    print('=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+')
    print()
    print(f'CREATED NEW TASK : {new_task}')
    print()
    print('=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+')
    print()

    
    db_exec("insert into task (update_exe, update_json) values({}, {})".format(
        new_task['update_exe'],
        new_task['update_json']
    ), return_result=False)  


def cli():
    
    os.system('cls')

    while True:
        print('''
============ SERVER-MANAGER ==================
    name: server-manager
    ver: 1.2
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
