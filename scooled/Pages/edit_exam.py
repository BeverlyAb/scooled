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
        self.ques_len = 4
        self.ans_len = 3

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
        self.courses = [val[0] for val in sorted(set(st.session_state[pt.submit]))]

    def update_exam(self,course):
        """updates exam choices based on course selected

        Args:
            course (str): 
        """        
        get_col = ['assign_name']
        table = 'test.question_bank'
        from_col = ['course_name']
        val_from_col = [course]
        dtype_from_col = ['str']
        self.sql_con.get_where_specified(
            table, get_col, from_col, val_from_col, dtype_from_col)
        self.exams = [val[0] for val in sorted(st.session_state[pt.submit])]

    @st.cache(hash_funcs={psycopg2.extensions.connection: id}, show_spinner=False)
    def get_exam_details(self, exam,course):
        """gets exam details

        Args:
            exam (str): 
            course (str): 

        Returns:
            pd.DataFrame: 
        """        
        get_cols = ['question_num','question','answer','opt1','opt2','opt3']
        from_col = ['assign_name','course_name']
        dtype_from_col = ['str','str']
        table = 'test.question_bank'

        val_from_col = [exam,course]
        self.sql_con.get_where_specified(table=table, get_cols=get_cols, from_col=from_col,
                                    val_from_col=val_from_col, dtype_from_col=dtype_from_col)
        full = st.session_state[pt.submit]
        df = pd.DataFrame(list(full), columns=[
                          "Number", "Question", "Answer", "Option 1", "Option 2", "Option 3"])
        df = df.set_index('Number')
        return df.sort_values(by=['Number'])

    @st.cache(hash_funcs={psycopg2.extensions.connection: id}, show_spinner=False)
    def get_feedback(self, exam):
        """gets student feedback

        Args:
            exam (str)): 

        Returns:
            pd.DataFrame: feedback
        """        
        get_cols = ['question_num','student','feedback']
        from_col = ['assign_name']
        dtype_from_col = ['str']
        table = 'test.student_feedback'

        val_from_col = [exam]
        self.sql_con.get_where_specified(table=table, get_cols=get_cols, from_col=from_col,
                                    val_from_col=val_from_col, dtype_from_col=dtype_from_col)
        full = st.session_state[pt.submit]
        df = pd.DataFrame(list(full), columns=["Number", "Student", "Feedback Per Question"])
        df = df.set_index('Number')
        return df.sort_values(by=['Number'])

    @st.cache(hash_funcs={psycopg2.extensions.connection: id}, show_spinner=False)
    def get_notes(self, exam):
        """gets notes based on exam

        Args:
            exam (str)): 

        Returns:
            pd.DataFrame:
        """        
        get_cols = ['question_num','note']
        from_col = ['assign_name']
        dtype_from_col = ['str']
        table = 'test.question_bank'

        val_from_col = [exam]
        self.sql_con.get_where_specified(table=table, get_cols=get_cols, from_col=from_col,
                                    val_from_col=val_from_col, dtype_from_col=dtype_from_col)
        full = st.session_state[pt.submit]
        df = pd.DataFrame(list(full), columns=["Number", "Note Per Question"])
        df = df.set_index('Number')
        return df.sort_values(by=['Number'])

    def display(self):
        """displays pg
        """        
        course = st.sidebar.selectbox("Courses", options=self.courses)
        self.update_exam(course)
        exam = st.sidebar.selectbox('Exams',options=self.exams)
        
        if exam != None:
            st.subheader(exam)
        else:
            st.subheader('No assignment available')
            st.stop()
        with st.expander('Questions'):
            st.table(self.get_exam_details(exam,course))
        with st.expander('Notes'):
            st.table(self.get_notes(exam))
        with st.expander('Student Feedback'):
            st.table(self.get_feedback(exam))


    def run(id):
        """runs page

        Args:
            id (str): teacher's name or email
        """        
        exam = EditExam(id)
        exam.update_courses()
        exam.display()
