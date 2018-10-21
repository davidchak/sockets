# coding: utf8

import sys
import subprocess
import pickle
from dbase import db_exec


def start_construktor():
    new_task = {}
    result = ''

    print('''
========= Конструктор новых задач ============
    ''')
    upd_exe = input('Требуется обновление файла программы?, Y/n \n')
    if result.lower() == 'y':
        new_task['upd_exe'] = True

    result = input('Установить новый "id"?, Y/n \n')
    if result.lower() == 'y':
        json_id = input('Введите новый параметр "id": \n')
        new_task['json_id'] = json_id

    result = input('Установить новый "access-token"?, Y/n \n')
    if result.lower() == 'y':
        json_access_token = input('Введите новый параметр "access-token": \n')
        new_task['json_access_token'] = json_access_token
    
    result = input('Установить новый "ipv4"?, Y/n \n')
    if result.lower() == 'y':
        json_ipv4 = input('Введите новый параметр "ipv4": \n')
        new_task['json_ipv4'] = json_ipv4

    result = input('Установить новый "check"?, Y/n \n')
    if result.lower() == 'y':
        json_check = input('Введите новый параметр "check": \n')
        new_task['json_check'] = json_check
    

    print(f'Новая задача: {new_task}')

    p_new_task = pickle.dumps(new_task)

    db_exec(f'insert into task(new_task) values("{p_new_task}")')

    print('''
==============================================
    ''')

    


def cli():
    

    while True:
        print('''
============ Сервер-менеджер =================

    1. Запустить сервер

    2. Конструктор новых задач

    q. Выход

==============================================
        ''')

        result = input('Введите команду: \n')
        
        if result.lower() == '1':
            code = subprocess.call(["python.exe", "server.py"])

        elif result.lower() == '2':
            start_construktor()

        elif result.lower() == 'q':
            sys.exit()

        else:
            print('Команда не распознана')
            continue






if __name__ == '__main__':
    cli()
