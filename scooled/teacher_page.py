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
    
    assign_names = lambda course_name, i: course_name[0] + str(i)

    assignments = [assignment[0]+'_'+str(assignment[1]) for assignment in itertools.product(courses,range(10))]
    st.write(assignments)
    
    teacher  = Teacher('Bev')
    teacher.display(courses)

