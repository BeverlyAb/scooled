# student_status.py
from structs import PageType as pt
from sql_connector import SQLConnector
import streamlit as st

''' Displays # perfect scores and retries per exam given a course'''


class StudentStatus:

    def __init__(self, id: str):
        """Every teacher should have:
        - name
        - course
        - current course (to be used when viewing exam)

        Args:
            id (str): name or email of teacher
        """        
        self.sql_conn = SQLConnector()
        self.courses = []
        self.course = ""
        self.id = id

    def update_courses(self):
        get_col = ['course']
        table = 'test.teacher'
        from_col = ['id']
        val_from_col = [self.id]
        dtype_from_col = ['str']
        self.sql_conn.get_where_specified(table,get_col,from_col,val_from_col,dtype_from_col)
    
        self.courses = [val[0] for val in st.session_state[pt.submit]]
        

    def display(self):
        st.title("s'CoolEd")
        course = st.sidebar.selectbox("Courses", options=self.courses)

    def run(id):
        s_status = StudentStatus(id)
        s_status.update_courses()
        st.write(s_status.display())
