# coding: utf8

import os
import sys
import subprocess
import time
import pickle
import sqlite3 as db
from dbase import db_exec


# TODO: Проверить запуск сервера на windows


def start_construktor():
    new_task = {}
    result = ''

    print('''
========= Конструктор новых задач ============
    ''')
    upd_exe = input('Требуется обновление файла программы?, Y/n \n >>')
    if result.lower() == 'y':
        new_task['update_exe'] = 1
    else:
        new_task['update_exe'] = 0

    result = input('Установить новый "id"?, Y/n \n >>')
    if result.lower() == 'y':
        json_id = input('Введите новый параметр "id": \n >>')
        new_task['json_id'] = json_id
    else:
        new_task['json_id'] = ''


    result = input('Установить новый "access-token"?, Y/n \n >>')
    if result.lower() == 'y':
        json_access_token = input(
            'Введите новый параметр "access-token": \n >>')
        new_task['json_access_token'] = json_access_token
    else:
        new_task['json_access_token'] = ''
    
    result = input('Установить новый "ipv4"?, Y/n \n >>')
    if result.lower() == 'y':
        json_ipv4 = input('Введите новый параметр "ipv4": \n >>')
        new_task['json_ipv4'] = json_ipv4
    else:
        new_task['json_ipv4'] = ''

    result = input('Установить новый "check"?, Y/n \n >>')
    if result.lower() == 'y':
        json_check = input('Введите новый параметр "check": \n >>')
        new_task['json_check'] = 1
    else:
        new_task['json_check'] = 0
    
    print()
    print('=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+')
    print()
    print(f'НОВАЯ ЗАДАЧА: {new_task}')
    print()
    print('=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+')
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
============ Сервер-менеджер =================

    1. Запустить сервер

    2. Конструктор новых задач

    q. Выход

==============================================
        ''')

        result = input('Введите команду: \n >>')
        
        if result.lower() == '1':
            os.startfile("server.py")
    

        elif result.lower() == '2':
            start_construktor()
            time.sleep(3)
            

        elif result.lower() == 'q':
            sys.exit()

        else:
            print('Команда не распознана')
            continue


if __name__ == '__main__':
    cli()
