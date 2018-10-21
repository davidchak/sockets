# coding: utf8

import sqlite3
from config import db_path


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
            



