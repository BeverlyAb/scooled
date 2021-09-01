# edit_exam.py
from structs import PageType as pt
from sql_connector import SQLConnector
import streamlit as st
import pandas as pd
import psycopg2

''' - Displays questions, feedback, notes on a single assignment
    - Enables editting notes
'''

class EditExam:

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
        self.exam = ""
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

    def update_exam(self,course):
        get_col = ['assign_name']
        table = 'test.question_bank'
        from_col = ['course_name']
        val_from_col = [course]
        dtype_from_col = ['str']
        self.sql_con.get_where_specified(
            table, get_col, from_col, val_from_col, dtype_from_col)
        self.exams = [val[0] for val in sorted(st.session_state[pt.submit])]

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
        return df

    def display(self):
        """display student status
        """        
        course = st.sidebar.selectbox("Courses", options=self.courses)
        self.update_exam(course)
        exam = st.sidebar.selectbox('Exams',options=self.exams)
        # st.write(self.get_student_status(course))

    def run(id):
        """runs page

        Args:
            id (str): teacher's name or email
        """        
        exam = EditExam(id)
        exam.update_courses()
        exam.display()
