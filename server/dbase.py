# coding: utf8

import sqlite3
from config import db_path


def db_exec(new_query):

    con = sqlite3.connect(db_path)

    with con:
        cur = con.cursor()
        try:
            cur.execute(new_query)
            result = cur.fetchall()
            return result[0]
        except sqlite3.DatabaseError as err:
            return err


