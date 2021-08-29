# teacher_page.py

import streamlit as st
import pandas as pd
import random 
import itertools
from structs import PageType as pt
from question_bank import QuestionBank
from sql_connector import SQLConnector


class Teacher:
    
    def __init__(self, name : str, edit_pg : st.session_state, new_pg : st.session_state, teacher : st.session_state, assign : st.session_state, submit : st.session_state, bank : st.session_state) -> None:
    #, df : pd.DataFrame) 

        self.name = name
        # self.df = df
        if edit_pg not in st.session_state:
            st.session_state[edit_pg] = False
        if new_pg not in st.session_state:
            st.session_state[new_pg] = False
        if teacher not in st.session_state:
            st.session_state[teacher] = True
        if assign not in st.session_state:
            st.session_state[assign] = None
        if submit not in st.session_state:    
            st.session_state[pt.submit] = False
        if bank not in st.session_state:
            st.session_state[pt.bank] = QuestionBank()

        self.sql_con = SQLConnector()
        self.course = ""

    def display(self, courses)->None:
        st.title("s'CoolEd")
        st.sidebar.title(f"{self.name}'s Subjects")
        self.course = st.sidebar.selectbox(label='Subjects',options=courses)
        st.write(f'{self.course} Assignments')
        return self.course

    def get_courses(self,assign):
        df = pd.DataFrame([["","","","",""]] , columns = ["Assignment","Description","# of Perfect Scores","# of Retries","Time of Last Retry"])
        get_cols = ['assign_name','topic','num_full_grade','retries','time']
        from_col=['assign_name']
        dtype_from_col=['str']
        table = 'test.general_course'
        self.sql_con.query(f"SELECT COUNT(DISTINCT assign_name) FROM test.general_course WHERE (assign_name) LIKE'{assign.split('_')[0]}%';")
        exam_len = st.session_state[pt.submit][0][0] 
        val_from_col = []
        for i in range(exam_len):
            val_from_col.append(assign+"_"+str(i))
        val_from_col = [val_from_col]
    
        for i in range(exam_len):
            self.sql_con.get_where_specified(table=table,get_cols=get_cols,from_col=from_col,val_from_col=[val_from_col[0][i]],dtype_from_col=dtype_from_col)
            if st.session_state[pt.submit] != None and len(st.session_state[pt.submit]) > 0:
                q = st.session_state[pt.submit][0]
                q = [val for val in q]
                df.loc[i] = q 
        return df

    def assignments(self,course,assignment_table)->None:
        # course_display = assignment_table.filter([course,course+'_description'], axis=1)]
        # keep track of the assignment description in case user want to edit
        df = self.get_courses(self.course)
        st.write(df)
        assignments = df['Assignment']#assignment_table[course
        assignment = st.selectbox(label='Assignment',options=assignments)
      
        col0, col1 = st.columns(2)
        with col0:
            if st.button(label='View '+ assignment,key='view'):
                # desc = pd.Series(course_display[course+'_description'][int(assignment.split(sep='_')[1])],name=assignment)
                st.session_state[pt.assign] = assignment
                self.edit_assign()#course_display[course+'_description'][int(assignment.split(sep='_')[1])])

        with col1:
            if st.button(label='Add new assignment',key='new'):
                # create a new assignment name
                # next_num = len(course_display)
                # assignment = assignment.replace(assignment.split(sep='_')[1],"")+str(next_num)
                # desc = pd.Series([0],name=assignment)
                # st.session_state[pt.assign] = assignment
                self.new_assign()
        
    def edit_assign(self):#,assignment):
        st.session_state[pt.new_pg] = False
        st.session_state[pt.teacher] = False
        st.session_state[pt.edit_pg] = True
        st.session_state[pt.submit] = False

    def new_assign(self):
        st.session_state[pt.edit_pg] = False
        st.session_state[pt.teacher] = False
        st.session_state[pt.submit] = False
        st.session_state[pt.new_pg] = True


    def gen_dummy(self):
        courses = ['Math','Biology','English','Art']
        students = [str(name) for name in range(100)]
        grades = [grade for grade in map(lambda x: random.randrange(0,101),range(len(students)*len(courses)))]
        assignments = [assignment[0]+'_'+str(assignment[1]) for assignment in itertools.product(courses,range(10))]
        
        assignment_table = pd.DataFrame()
        for i in range(len(courses)):
            assign_name_series = pd.Series([table for table in assignments[i*10:(i+1)*10]],name=courses[i])
            assign_desc_series = pd.Series(['Description for '+table for table in assign_name_series],name=courses[i]+"_description")
            assignment_table = assignment_table.append([assign_name_series,assign_desc_series])
        assignment_table = assignment_table.transpose()
        return courses, students, grades, assignment_table

# if __name__ == '__main__':
#     # Dummy data for now. Need to create Entity Relationship Diagram later
#     teacher  = Teacher('Bev')
#     courses, students, grades, assignment_table = teacher.gen_dummy()
#     course = teacher.display(courses,assignment_table)
#     teacher.assignments(course,assignment_table)
