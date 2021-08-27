# teacher_page.py

import streamlit as st
import pandas as pd
import random 
import itertools
from structs import PageType as pt
from question_bank import QuestionBank

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

    def display(self, courses)->None:
        st.title(f"{self.name}'s Courses")
        st.sidebar.title('Menu')
        course = st.sidebar.selectbox(label='Courses',options=courses)
        return course

    def assignments(self,course,assignment_table)->None:
        course_display = assignment_table.filter([course,course+'_description'], axis=1)
        assignments = assignment_table[course]
        st.write(course_display)

        # keep track of the assignment description in case user want to edit
        assignment = st.selectbox(label='Assignment',options=assignments)

        col0, col1 = st.columns(2)
        with col0:
            # description = course+'_description'+ assignment.split(sep='_')[1]
            # assignment_table[course+'_description'][int(assignment.split(sep='_')[1])]
            if st.button(label='Edit '+ assignment,key='edit'):
                desc = pd.Series(course_display[course+'_description'][int(assignment.split(sep='_')[1])],name=assignment)
                st.session_state[pt.assign] = pd.DataFrame(desc)
                self.edit_assign()#course_display[course+'_description'][int(assignment.split(sep='_')[1])])

        with col1:
            if st.button(label='Add new assignment',key='new'):
                # create a new assignment name
                next_num = len(course_display)
                assignment = assignment.replace(assignment.split(sep='_')[1],"")+str(next_num)
                desc = pd.Series([0],name=assignment)
                st.session_state[pt.assign] = pd.DataFrame(desc)
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
