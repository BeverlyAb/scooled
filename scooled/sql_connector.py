import psycopg2
import streamlit as st
import os
import pandas as pd


class SQLConnector():
    def __init__(self):
        # I am the only one using this at this point 
        self.conn = psycopg2.connect(database = os.environ["db"],user = os.environ["user"] ,host = os.environ["hostname"] ,password = os.environ["password"], port = os.environ["port"])
        self.cur = self.conn.cursor()
        self.cur.execute("USE test;")

    def __del__(self):
        del self.conn
        del self.cur

    def query(self, command : str):
        self.cur.execute(command)

    def get(self,table : str, get_cols : list, from_col : str, val_from_col : str ):
        '''get certain col(s) based on certain col value'''
        table = 'test.' + table
        self.cur.execute(f"SELECT {','.join(get_cols)} FROM {table} WHERE {from_col} in ('{val_from_col}');")
        
        out = pd.Series()   
        out = [val for val in self.cur]
        return out

    def get(self,table : str ):
        '''get everything'''
        table = 'test.' + table
        self.cur.execute(f"SELECT * FROM {table};")
        
        out = pd.DataFrame()   
        out = [val for val in self.cur]
        return out

if __name__ == "__main__":
    sql_con = SQLConnector()
    get_cols = ['teacher','student']
    table = 'courses'
    from_col = 'name'
    val_from_col = 'ENGLISH_0'
    # out= sql_con.get(table,get_cols,from_col,val_from_col)
    out = sql_con.get(table)
    st.write(out)
# st.write(cur.execute("SHOW TABLES"))

# st.stop()
