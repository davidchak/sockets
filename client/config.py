# coding: utf8

import os

server_ip = '0.0.0.0'
server_port = 8246
time_interval = 5
base_dir = os.path.abspath(os.path.dirname(__name__))
db_path = os.path.join(base_dir, 'client.db')