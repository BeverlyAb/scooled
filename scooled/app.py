# app.py

from Pages.edit_exam import EditExam
import streamlit as st
from structs import PageType as pt
# from teacher_page import Teacher
from assignments_page import Assignments
import pandas as pd
from question_bank import QuestionBank
from multi_page import MultiPage
from Pages.student_status import StudentStatus
from Pages.add_plan import AddPlan
from structs import PageName as pg

if __name__ == "__main__":

    name = 'Bev'
    st.title("s'CoolEd")
    st.sidebar.title(f"Welcome, {name}!")
    # teacher_opt = [pt.add,pt.new,pt.status,pt.edit]
    
    app = MultiPage()
    app.add_page(pg.status,StudentStatus.run)
    app.add_page(pg.lesson,AddPlan.run)
    app.add_page(pg.assignment,EditExam.run)
    app.run(name)

    # sel = st.sidebar.selectbox('What would you like to do?',options=teacher_opt)


    # if sel == teacher_opt[1]:
    #     teacher  = Teacher('Bev',pt.edit_pg,pt.new_pg,pt.teacher,pt.assign,pt.submit,pt.bank)
    #     courses, students, grades, assignment_table = teacher.gen_dummy()
        
    #     course = teacher.display(courses)
    #     assignment = teacher.assignments()
    # elif sel == teacher_opt[2]:
    #     cur_assign = Assignments()
    #     #update vals
    #     cur_assign.update_q_df()
    #     cur_assign.update_note_df()
    #     cur_assign.display()
    # else:
    #     st.write("I'm placeholder!")