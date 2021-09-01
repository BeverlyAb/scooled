# student_status.py
from structs import PageType as pt
from sql_connector import SQLConnector
import streamlit as st
import pandas as pd
import psycopg2

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
        self.sql_con = SQLConnector()
        self.courses = []
        self.course = ""
        self.id = id

    def update_courses(self):
        get_col = ['course']
        table = 'test.teacher'
        from_col = ['id']
        val_from_col = [self.id]
        dtype_from_col = ['str']
        self.sql_con.get_where_specified(table,get_col,from_col,val_from_col,dtype_from_col)
        self.courses = [val[0] for val in sorted(st.session_state[pt.submit])]
    

    @st.cache(hash_funcs={psycopg2.extensions.connection: id},show_spinner=False)
    def get_student_status(self,course):
        df = pd.DataFrame([["","","","",""]] , columns = ["Assignment","Description","# of Perfect Scores","# of Retries","Time of Last Retry"])
        get_cols = ['assign_name','topic','num_full_grade','retries','time']
        from_col=['assign_name']
        dtype_from_col=['str']
        table = 'test.general_course'
        self.sql_con.query(f"SELECT COUNT(DISTINCT assign_name) FROM test.general_course WHERE (assign_name) LIKE '{course.split('_')[0]}%';")
        exam_len = 4
        val_from_col = []
        for i in range(exam_len):
            val_from_col.append(course+"_"+str(i))
        val_from_col = [val_from_col]
    
        for i in range(exam_len):
            self.sql_con.get_where_specified(table=table,get_cols=get_cols,from_col=from_col,val_from_col=[val_from_col[0][i]],dtype_from_col=dtype_from_col)
            if st.session_state[pt.submit] != None and len(st.session_state[pt.submit]) > 0:
                q = st.session_state[pt.submit][0]
                q = [val for val in q]
                df.loc[i] = q 
        return df

    def display(self):
        course = st.sidebar.selectbox("Courses", options=self.courses)   
        st.write(self.get_student_status(course)) 

    def run(id):
        s_status = StudentStatus(id)
        s_status.update_courses()
        s_status.display()
