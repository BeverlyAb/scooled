from structs import PageType as pt
import psycopg2
import streamlit as st
import os
import pandas as pd



class SQLConnector():
    def __init__(self):
        # I am the only one using this at this point 
        self.conn = psycopg2.connect(database = os.environ["db"],user = os.environ["user"] ,host = os.environ["hostname"] ,password = os.environ["password"], port = os.environ["port"])  
        # self.cur.execute("USE test;")

    def __del__(self):
        del self.conn

    def connect(self):
        self.conn = psycopg2.connect(database = os.environ["db"],user = os.environ["user"] ,host = os.environ["hostname"] ,password = os.environ["password"], port = os.environ["port"])  
        

    def query(self, command : str):
        self.connect()

        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(command)
                    st.session_state[pt.submit] = cur.fetchall()
                except Exception as e:
                    st.write(e)
                    cur.close()
                    return e
        self.conn.close()

    def get_where_specified(self,table : str, get_cols : list, from_col : str, val_from_col : str ):
        '''get certain col(s) based on certain col value'''
        

        # self.cur = self.conn.cursor()
        # table = 'test.' + table
        # self.cur.execute(f"SELECT {','.join(get_cols)} FROM {table} WHERE {from_col} = ('{val_from_col}');")
        # out = pd.Series()   
        # out = [val for val in self.cur]
        # self.cur.close()

        # return out
        table = 'test.' + table
        query = f"SELECT {','.join(get_cols)} FROM {table} WHERE {from_col} in ('{val_from_col}');"
        st.write(query)
        self.query(query)

    def get(self,table : str, col : list):
        '''get everything or just one col - calling from SQL is faster than me structuring them up into DF'''
        self.connect()
        table = 'test.' + table     
        self.cur = self.conn.cursor()
        
        self.cur.execute(f"SELECT {','.join(col)} FROM {table};")
        out = pd.DataFrame()   
        out = [val for val in self.cur]
        
        self.cur.close()
        self.conn.close()
        return out


    def insert(self, table : str, to_cols : list, to_vals : list):
        table = 'test.' + table
        to_cols = ", ".join(to_cols)
        to_vals = ["'" + val + "'" for val in to_vals]
        to_vals = ", ".join(to_vals)
        query = f"INSERT INTO {table} ({to_cols}) VALUES ({to_vals});"
        self.query(query)

# if __name__ == "__main__":
    # sql_con = SQLConnector()
    # get_cols = ['teacher','student']
    # table = 'courses'
    # from_col = 'name'
    # val_from_col = 'ENGLISH_0'
    # out= sql_con.get_where_specified(table,get_cols,from_col,val_from_col)
    # # out = sql_con.get(table,None)
    # # st.write(out)

    # to_cols = ['name','teacher','student']
    # to_vals = ['MATH_0','Erly','STUDENT_0']
    # sql_con.insert(table,to_cols,to_vals)
    # st.write(sql_con.get(table,['*']))

# st.write(cur.execute("SHOW TABLES"))

# st.stop()