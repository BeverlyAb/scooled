# app.py

import streamlit as st
from structs import PageType as pt
from teacher_page import Teacher
from assignments_page import Assignments
import pandas as pd
from question_bank import QuestionBank

if __name__ == "__main__":

    # init states
    if pt.teacher not in st.session_state or pt.edit_pg not in st.session_state or pt.new_pg not in st.session_state or pt.assign not in st.session_state or pt.bank not in st.session_state:
        st.session_state[pt.teacher] = True
        st.session_state[pt.edit_pg] = False
        st.session_state[pt.new_pg] = False
        assignment = None
        st.session_state[pt.bank] = QuestionBank()


    # Display Teacher Page
    if st.session_state[pt.teacher]:
    # Dummy data for now. Need to create Entity Relationship Diagram later
        teacher  = Teacher('Bev',pt.edit_pg,pt.new_pg,pt.teacher,pt.assign,pt.submit,pt.bank)
        courses, students, grades, assignment_table = teacher.gen_dummy()
        
        course = teacher.display(courses)
        assignment = teacher.assignments(course,assignment_table)
    # Edit Page
    elif st.session_state[pt.edit_pg]:
        cur_assign = Assignments()
        q_df = cur_assign.get_question()
        note_df = cur_assign.get_notes()
        cur_assign.display(q_df,note_df)

    # New Page
    elif st.session_state[pt.new_pg]:
        new_assign = Assignments()
        new_assign.create_new_pg()

        # Not sure why pt.bank wasn't saved under first call of app main() 
        if pt.bank not in st.session_state:         
            st.session_state[pt.bank] = QuestionBank() 

        if st.session_state[pt.submit] != False:
            exam_name = st.session_state[pt.submit][0]
            assign = st.session_state[pt.submit][1]
            st.session_state[pt.bank].add(exam_name,assign)
  
