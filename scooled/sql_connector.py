from streamlit.caching import suppress_cached_st_function_warning
from structs import PageType as pt
import psycopg2
import streamlit as st
import os
import pandas as pd



class SQLConnector():
    def __init__(self):
        # I am the only one using this at this point 
        self.conn = psycopg2.connect(database = os.environ["db"],user = os.environ["user"] ,host = os.environ["hostname"] ,password = os.environ["password"], port = os.environ["port"])  
        # # self.cur.execute("USE test;")
        # if pt.submit not in st.session_state:
        #     st.session_state[pt.submit] = None

    def __del__(self):
        del self.conn

    # @st.cache(hash_funcs={psycopg2.extensions.connection: id},allow_output_mutation=True)
    def connect(self):
        self.conn = psycopg2.connect(database = os.environ["db"],user = os.environ["user"] ,host = os.environ["hostname"] ,password = os.environ["password"], port = os.environ["port"])  
        return self.conn

    # @st.cache(hash_funcs={psycopg2.extensions.connection: id},show_spinner=False)
    def query(self, command : str):
        self.connect()
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(command)
                    if cur.description != None:
                        st.session_state[pt.submit] = cur.fetchall()
                    cur.close()
                except Exception as e:
                    st.write(e)
                    cur.close()
                    return e
        self.conn.close()
        return None
 

    # def write(self, command : str):
    #     self.connect()
    #     with self.conn:
    #         with self.conn.cursor() as cur:
    #             try:
    #                 cur.execute(command)
    #             except Exception as e:
    #                 st.write(e)
    #                 cur.close()
    #                 return e
    #     self.conn.close()
    #     return None
    def update_where_specified(self,table : str, to_col : list,to_val : list, from_col : list, val_from_col : list, dtype_from_col:list):
        """apppends values to existing col based on where

        Args:
            table (str): table name
            to_col (list): col to be updated
            to_val (list): val to be appended
            from_col (list): specified col
            val_from_col (list): specified values
            dtype_from_col (list): data type of from_column data 
        """        
        query = f"UPDATE {table} SET {to_col} =  {to_col} + {to_val}"
        if dtype_from_col[0] == 'int':
            query += f" WHERE {from_col[0]} = {val_from_col[0]}"
        else:
            query += f" WHERE {from_col[0]} = '{val_from_col[0]}'"
        for i in range(1,len(from_col)):
            if dtype_from_col[i] == 'int':
                query += f" AND {from_col[i]} = {val_from_col[i]}"
            else:
                query += f" AND {from_col[i]} = '{val_from_col[i]}'"
        query += ";"
        # st.write(query)
        self.query(query)
        

    def get_where_specified(self,table : str, get_cols : list, from_col : list, val_from_col : list, dtype_from_col:list):
        '''get certain col(s) based on certain col value'''
        query = f"SELECT {','.join(get_cols)} FROM {table}"
        if dtype_from_col[0] == 'int':
            query += f" WHERE {from_col[0]} = {val_from_col[0]}"
        else:
            query += f" WHERE {from_col[0]} = '{val_from_col[0]}'"
        for i in range(1,len(from_col)):
            if dtype_from_col[i] == 'int':
                query += f" AND {from_col[i]} = {val_from_col[i]}"
            else:
                query += f" AND {from_col[i]} = '{val_from_col[i]}'"
        query += ";"
        # st.write(query)
        self.query(query)

    def get_where_like(self,table : str, get_cols : list, from_col : list, val_from_col : list, dtype_from_col:list):
        '''get certain col(s) based on similar col value'''

        query = f"SELECT {','.join(get_cols)} FROM {table}"
        if dtype_from_col[0] == 'int':
            query += f" WHERE {from_col[0]} = {val_from_col[0]}"
        else:
            query += f" WHERE {from_col[0]} LIKE '{val_from_col[0]}%'"
        for i in range(1,len(from_col)):
            if dtype_from_col[i] == 'int':
                query += f" OR {from_col[i]} = {val_from_col[i]}"
            else:
                query += f" OR {from_col[i]} LIKE '{val_from_col[i]}%'"
        query += ";"
        # st.write(query)
        self.query(query)

    # def get(self,table : str, col : list):
    #     '''get everything or just one col - calling from SQL is faster than me structuring them up into DF'''
    #     self.connect()
    #     table = 'test.' + table     
    #     self.cur = self.conn.cursor()
        
    #     self.cur.execute(f"SELECT {','.join(col)} FROM {table};")
    #     out = pd.DataFrame()   
    #     out = [val for val in self.cur]
        
    #     self.cur.close()
    #     self.conn.close()
    #     return out


    def insert(self, table : str, to_cols : list, to_vals : list):
        """inserts to values to existing row and column

        Args:
            table (str): table
            to_cols (list): which columns to store into
            to_vals (list): which values to store

        Returns:
            psycopg2.connect
        """        
        to_cols = ", ".join(to_cols)
        to_vals = ["'" + val + "'" for val in to_vals]
        to_vals = ", ".join(to_vals)
        query = f"INSERT INTO {table} ({to_cols}) VALUES ({to_vals});"
        return self.query(query)

    def upload_bytea(self, table : str, to_cols : list, to_vals : list, file_content):
        """uploads a file with the corr to_cols values

        Args:
            table (str): table
            to_cols (list): which columns to store into
            to_vals (list): which values to store
            file_content (psycopg2.Binary) : file contents

        Returns:
            psycopg2.cursor
        """        
        to_cols = ", ".join(to_cols)
        to_vals = ["'" + val + "'" for val in to_vals]
        to_vals = ", ".join(to_vals)
    
        # insert into test values (1, pg_read_file('/home/xyz')::bytea);
        query = f"INSERT INTO {table} ({to_cols}) VALUES ({to_vals},{file_content}::bytea);"
        return self.query(query)

    def load_bytea(self,table : str, get_cols : list, from_col : list, val_from_col : list, dtype_from_col:list):
        """downloads a file with the corr to_cols values

        Args:
            table (str): table
            get_cols (list): which columns to get
            from_col (list): specified col
            val_from_col (list): specified values
            dtype_from_col (list): data type of from_column data 
        
        Returns:
            psycopg2.cursor
        """ 

        # "SELECT CONVERT_FROM(DECODE(f{file}, 'BASE64'), 'UTF-8') FROM ;"
        query = f"SELECT CONVERT_FROM(DECODE({','.join(get_cols)}, 'BASE64'), 'UTF-8') FROM {table}"
        if dtype_from_col[0] == 'int':
            query += f" WHERE {from_col[0]} = {val_from_col[0]}"
        else:
            query += f" WHERE {from_col[0]} LIKE '{val_from_col[0]}%'"
        for i in range(1,len(from_col)):
            if dtype_from_col[i] == 'str':
                query += f" OR {from_col[i]} LIKE '{val_from_col[i]}%'"
            else:
                query += f" OR {from_col[i]} = {val_from_col[i]}"
        query += ";" 
        st.write(query)
        return self.query(query)
  
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
