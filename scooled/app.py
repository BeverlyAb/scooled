# app.py

import streamlit as st
from structs import PageType as pt
from teacher_page import Teacher



if __name__ == "__main__":
    st.session_state[pt.teacher] = True
    st.session_state[pt.edit_pg] = False
    st.session_state[pt.new_pg] = False

    if st.session_state[pt.teacher]:
    # Dummy data for now. Need to create Entity Relationship Diagram later
        teacher  = Teacher('Bev')
        courses, students, grades, assignment_table = teacher.gen_dummy()
        course = teacher.display(courses,assignment_table)
        teacher.assignments(course,assignment_table)
    elif st.session_state[pt.edit_pg]:
        st.write(pt.edit_pg)
    elif st.session_state[pt.new_pg]:
        st.write(pt.new_pg)