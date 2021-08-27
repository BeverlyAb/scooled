# app.py

import streamlit as st
from structs import PageType as pt
from teacher_page import Teacher
from assignments_page import Assignments
import pandas as pd
from question_bank import QuestionBank

if __name__ == "__main__":
    qbank = QuestionBank()

    # init states
    if pt.teacher not in st.session_state or pt.edit_pg not in st.session_state or pt.new_pg not in st.session_state or pt.assign not in st.session_state:
        st.session_state[pt.teacher] = True
        st.session_state[pt.edit_pg] = False
        st.session_state[pt.new_pg] = False
        assignment = None

    # Display Teacher Page
    if st.session_state[pt.teacher]:
    # Dummy data for now. Need to create Entity Relationship Diagram later
        teacher  = Teacher('Bev',pt.edit_pg,pt.new_pg,pt.teacher,pt.assign,pt.submit)
        courses, students, grades, assignment_table = teacher.gen_dummy()
        course = teacher.display(courses)
        assignment = teacher.assignments(course,assignment_table)

        st.write(qbank.get_bank())

    # Edit Page
    elif st.session_state[pt.edit_pg]:
        cur_assign = Assignments()
        cur_assign.display()

    # New Page
    elif st.session_state[pt.new_pg]:
        new_assign = Assignments()

        if new_assign.create_new_pg() != None:
            exam_name, questions = new_assign.create_new_pg()
            qbank.add(st.session_state[pt.submit])