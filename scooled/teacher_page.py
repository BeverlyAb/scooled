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

    def display(self, courses)->None:
        st.title("s'cooled")
        st.sidebar.title(f'Welcome, {self.name}')
        st.sidebar.selectbox(label='Courses',options=courses)


    def assignments(self,course,students)->None:
        st.write(students)




if __name__ == '__main__':
    # Dummy data for now. Need to create Entity Relationship Diagram later
    courses = ['Math','Biology','English','Art']
    students = [str(name) for name in range(100)]
    grades = [grade for grade in map(lambda x: random.randrange(0,101),range(len(students)*len(courses)))]
    assignments = [assignment[0]+'_'+str(assignment[1]) for assignment in itertools.product(courses,range(10))]
    assignment_table = [table for table in itertools.product([courses[0]],assignments[0:10])]
    st.write(assignment_table)
    teacher  = Teacher('Bev')
    teacher.display(courses)

