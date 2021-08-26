# teacher_page.py

import streamlit as st
import pandas as pd
import random 
import itertools
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
        st.write(assignment_table[course])





if __name__ == '__main__':
    # Dummy data for now. Need to create Entity Relationship Diagram later
    courses = ['Math','Biology','English','Art']
    students = [str(name) for name in range(100)]
    grades = [grade for grade in map(lambda x: random.randrange(0,101),range(len(students)*len(courses)))]
    assignments = [assignment[0]+'_'+str(assignment[1]) for assignment in itertools.product(courses,range(10))]
    
    assignment_table = []
    for i in range(len(courses)):
        assignment_table.append(pd.Series([table for table in assignments[i*10:(i+1)*10]],name=courses[i]))
    assignment_table = pd.DataFrame(assignment_table)
    assignment_table = assignment_table.transpose()
    teacher  = Teacher('Bev')
    teacher.display(courses,assignment_table)

