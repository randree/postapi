#!/usr/bin/python3
import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self):
        # create a database connection
        self.create_connection("history.db")

        sql_create_history_table = """ CREATE TABLE IF NOT EXISTS history (
                                            id INTEGER PRIMARY KEY,
                                            url text UNIQUE,
                                            param1 text NULL,
                                            param2 text NULL,
                                            param3 text NULL,
                                            cookie1 text NULL,
                                            cookie2 text NULL
                                        ); """

        if self.conn is not None:
            # create tables if not exists
            self.create_table(sql_create_history_table)
        else:
            print("Error! cannot create the database connection.")


    def create_connection(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def write(self, url, param1, param2, param3, cookie1, cookie2):
        if url != "":
            try:
                c = self.conn.cursor()
                c.execute("INSERT OR REPLACE INTO history(url, param1, param2, param3, cookie1, cookie2) VALUES (?,?,?,?,?,?)", (url, param1, param2, param3, cookie1, cookie2))
                self.conn.commit()
                c.close()
            except Error as e:
                print(e)

    def readParams(self, url):
        try:
            self.conn.row_factory = sqlite3.Row
            cur = self.conn.cursor()
            row = cur.execute("SELECT * FROM history WHERE url = ?", (url,)).fetchone()
            # print(row['url'])
            return row
        except Error as e:
            print(e)  


    def readUrls(self):
        list = []
        try:
            cur = self.conn.cursor()
            for row in cur.execute("SELECT * FROM history ORDER BY id DESC LIMIT 20"):
                list.append(row[1])
            cur.close()
        except Error as e:
            print(e)           
        
        return list