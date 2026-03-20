import sqlite3
import pandas as pd
from datetime import datetime
class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)

    def query(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def execute(self, sql: str, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
    def executemany(self, sql : str, params=()):
        cur =self.conn.cursor()
        cur.executemany(sql,params)
        self.conn.commit()
    def read_xls(self, file_path:str,sheet_name:str):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    def read_csv(self,file_path:str):
        df =pd.read_csv(file_path)
        return df
        



    def close(self):
        self.conn.close()
