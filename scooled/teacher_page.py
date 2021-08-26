# teacher_page.py

import streamlit as st
import pandas as pd
import random 
import itertools
import re

class Teacher:
    
    def __init__(self, name : str)-> None:
    #, df : pd.DataFrame) 

        self.name = name
        # self.df = df

    def display(self, courses, assignment_table)->None:
        st.title("s'cooled")
        st.sidebar.title(f'Welcome, {self.name}')
        course = st.sidebar.selectbox(label='Courses',options=courses)
        self.assignments(course,assignment_table)

    def assignments(self,course,assignment_table)->None:
        assignments = assignment_table[course]   
        st.write(assignments)
        assignment = st.sidebar.selectbox(label='Assignment',options=assignments)
    
        st.write(assignment_table[course+'_description'][int(assignment.split(sep='_')[1])])

#outside of class
def gen_dummy():
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

if __name__ == '__main__':
    # Dummy data for now. Need to create Entity Relationship Diagram later
    courses, students, grades, assignment_table = gen_dummy()
    teacher  = Teacher('Bev')
    teacher.display(courses,assignment_table)

