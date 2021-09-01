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
        self.lessons = []

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

    def create_form(self, course):
        """allows user to type input and save as file
        """
        with st.form('Create Form'):
            lesson = st.text_input(label="Title")
            content = st.text_area("Write away!")
            if st.form_submit_button('Save'):
                if lesson != "" and content != "":
                    table = 'test.teacher'
                    to_cols = ['lesson_plan', 'id', 'course', 'lesson_title']
                    to_vals = [str(content), self.id, course, lesson]
                    self.sql_con.insert(table, to_cols, to_vals)
                    st.success(f'Successfully created {lesson}')
                else:
                    st.error('Title and lesson cannot be empty.')

    def upload(self, course):
        """uploads files to db
        """
        with st.form('Upload Form'):
            file = st.file_uploader(label='File', accept_multiple_files=False)
            if st.form_submit_button('Upload'):
                if file != None:
                    table = 'test.teacher'
                    to_cols = ['lesson_plan', 'id', 'course']
                    contents = str(psycopg2.Binary(file.getbuffer()))
                    to_vals = [contents, self.id, course]
                    self.sql_con.upload(
                        table=table, to_cols=to_cols, to_vals=to_vals)
                    st.success(f'Successfully uploaded {file.name}')
                else:
                    st.error('No file uploaded')

    def update_lesson(self,course):
        """updates exam choices based on course selected

        Args:
            course (str): 
        """        
        get_col = ['lesson_title']
        table = 'test.teacher'
        from_col = ['course']
        val_from_col = [course]
        dtype_from_col = ['str']
        self.sql_con.get_where_specified(
            table, get_col, from_col, val_from_col, dtype_from_col)
        self.lessons = [val[0] for val in filter(lambda x : x[0] != None,st.session_state[pt.submit])]


    @st.cache(hash_funcs={psycopg2.extensions.connection: id}, show_spinner=False)
    def get_lesson_plans(self, course, title):
        """displays lesson plans and enables caching

        Args:
            course (str): retrieves lessons depending on course

        Returns:
            pd.DataFrame: lessons
        """

        get_cols = ['lesson_plan']
        from_col = ['course', 'id','lesson_title']
        dtype_from_col = ['str', 'str','str']
        table = 'test.teacher'

        val_from_col = [course, self.id,title]
        self.sql_con.get_where_like(table=table, get_cols=get_cols, from_col=from_col,
                                    val_from_col=val_from_col, dtype_from_col=dtype_from_col)
        full = st.session_state[pt.submit]
        df = pd.DataFrame(list(full), columns=["Lesson Plan"])
        return df

    def display(self):
        """displays pg
        """        
        course = st.sidebar.selectbox("Courses", options=self.courses)
        self.update_lesson(course)
        lesson = st.sidebar.selectbox('Lessons',options=self.lessons)
        
        if len(self.lessons) > 0:
            st.subheader(lesson)
            with st.expander('View Lesson Plans'):
                st.table(self.get_lesson_plans(course,lesson))

            with st.expander('Create'):
                self.create_form(course)

        # with st.expander('Upload'):
        #     self.upload(course)
        else:

            st.subheader(f"No {course} lesson yet. Let's create one!")
            with st.expander('Create'):
                self.create_form(course)


    def run(id):
        """runs page

        Args:
            id (str): teacher's name or email
        """
        plan = AddPlan(id)
        plan.update_courses()
        plan.display()
