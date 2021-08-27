import psycopg2
import streamlit as st
import os


class SQLConnector():
    def __init__(self):
        # I am the only one using this at this point 
        self.conn = psycopg2.connect(database = os.environ["db"],user = os.environ["user"] ,host = os.environ["hostname"] ,password = os.environ["password"], port = os.environ["port"])
        self.cur = self.conn.cursor()
        self.cur.execute("USE test;")

    def __del__(self):
        del self.conn
        del self.cur

    def get(self,table : str, get_cols : list, from_col : str, val_from_col : str ):
        table = 'test.' + table
        self.cur.execute(f"SELECT {','.join(get_cols)} FROM {table} WHERE {from_col} in ('{val_from_col}');")
        for i in self.cur:
            st.write("HI",i)


if __name__ == "__main__":
    sql_con = SQLConnector()
    get_cols = ['teacher','student']
    table = 'courses'
    from_col = 'name'
    val_from_col = 'ENGLISH_0'
    sql_con.get(table,get_cols,from_col,val_from_col)
# st.write(cur.execute("SHOW TABLES"))

# st.stop()
