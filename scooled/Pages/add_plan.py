# add_plan.py
import streamlit as st
from structs import PageType as pt
from sql_connector import SQLConnector
import streamlit as st
import pandas as pd
import psycopg2
import os

'''Saves file, image or text input'''

class AddPlan():

    def __init__(self, id: str):
            """Every teacher should have:
            - name
            - course

            Args:
                id (str): name or email of teacher
            """
            self.sql_con = SQLConnector()
            self.courses = []
            self.id = id

    def update_courses(self):
        """updates the course according to the teacher
        """
        get_col = ['course']
        table = 'test.teacher'
        from_col = ['id']
        val_from_col = [self.id]
        dtype_from_col = ['str']
        self.sql_con.get_where_specified(
            table, get_col, from_col, val_from_col, dtype_from_col)
        self.courses = [val[0] for val in sorted(st.session_state[pt.submit])]

    

    @st.cache(hash_funcs={psycopg2.extensions.connection: id}, show_spinner=False)
    def get_student_status(self, course):
        """displays student statuses and enables caching

        Args:
            course (str): retrieves status depending on course

        Returns:
            pd.DataFrame: student statuses
        """        
        
        get_cols = ['assign_name', 'topic',
                    'num_full_grade', 'retries', 'time']
        from_col = ['assign_name']
        dtype_from_col = ['str']
        table = 'test.general_course'

        val_from_col = [course]
        self.sql_con.get_where_like(table=table, get_cols=get_cols, from_col=from_col,
                                    val_from_col=val_from_col, dtype_from_col=dtype_from_col)
        full = st.session_state[pt.submit]
        df = pd.DataFrame(list(full), columns=[
                            "Assignment", "Description", "# of Perfect Scores", "# of Retries", "Time of Last Retry"])
        
        return df.sort_values(by=['Assignment'])
    
    def create_form(self,course):
        """allows user to type input and save as file
        """         
        with st.form('Create Form'):
            lesson = st.text_input(label="Title")
            content = st.text_area("Write away!")
            if st.form_submit_button('Save'):
                if lesson != "" and content != "":
                    table = 'test.teacher'
                    to_cols = ['lesson_plan','id','course']
                    to_vals = [str(content),self.id,course]
                    self.sql_con.insert(table,to_cols,to_vals)
                    st.success(f'Successfully created {lesson}')
                else:
                    st.error('Title and lesson cannot be empty.')

    def upload(self,course):
        """uploads files to db
        """        
        with st.form('Upload Form'):
            file = st.file_uploader(label='File',accept_multiple_files=False)
            if st.form_submit_button('Upload'):
                if file != None:
                    table = 'test.teacher'
                    to_cols = ['lesson_plan','id','course']
                    contents = str(psycopg2.Binary(file.getbuffer()))
                    to_vals = [contents,self.id,course]
                    self.sql_con.upload(table=table,to_cols=to_cols,to_vals=to_vals)
                    st.success(f'Successfully uploaded {file.name}')
                else:
                    st.error('No file uploaded')
    
    def get_lesson_plans(self,course):
        st.write("Hello")

    def display(self):
        """display student status
        """        
        course = st.sidebar.selectbox("Courses", options=self.courses)
        st.subheader(f'{course} Lesson Plans')
        
        with st.expander('View Lesson Plans'):
            self.get_lesson_plans(course)

        with st.expander('Create'):
            self.create_form(course)
        
        with st.expander('Upload'):
            self.upload(course)

    def run(id):
        """runs page

        Args:
            id (str): teacher's name or email
        """        
        plan = AddPlan(id)
        plan.update_courses()
        plan.display()
