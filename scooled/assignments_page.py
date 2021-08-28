# assignments_page.py

import streamlit as st
from structs import PageType as pt
import pandas as pd
from sql_connector import SQLConnector
import re

class Assignments:

    def __init__(self) -> None:
        self.assignment = st.session_state[pt.assign]
        # if st.session_state[pt.submit] not in st.session_state:
        #     st.session_state[pt.submit] = False
        self.sql_con = SQLConnector()
        self.table = 'assignments'
        

    def display(self):
        st.sidebar.title('Menu')
        course = self.assignment.columns[0]
        st.title(course)
        st.write(self.load_from_db(course))
        if st.sidebar.button('Return to Courses'):
            self.reset_pg(pt.teacher)

    def load_from_db(self, course):
        self.sql_con.get_where_specified(table=self.table,get_cols=['*'],from_col='course_name',val_from_col=course)
        st.write(self.sql_con.get(table=self.table,col=['*']))
        st.write(self.sql_con.query('SHOW COLUMNS FROM test.assignments'))
    
    def create_new_pg(self):
        st.sidebar.title('Menu')
        exam_name = self.assignment.columns[0]
        st.title(exam_name)
        set_ques_len = 4
        set_ans_len = 3
        
        ques_bank = self.get_bank_from_forms(exam_name,set_ques_len,set_ans_len)

        if st.button('Submit'):
            self.write_to_db(ques_bank,exam_name)               # add to db
            self.reset_forms()                                  # clear forms
            # self.reset_pg(pt.teacher)                           # go back to teacher pg
        if st.sidebar.button('Return to Courses'):
            self.reset_forms()                                  # clear forms
            self.reset_pg(pt.teacher)                           # go back to teacher pg

    def write_to_db(self, ques_bank,exam_name):
        to_cols = ["assign_name", "course_name","q1", "q1_op_1","q1_op_2", "q1_op_3",
	            "q1_ans","q2","q2_op_1","q2_op_2","q2_op_3","q2_ans","q3","q3_op_1",
                "q3_op_2","q3_op_3","q3_ans","q4","q4_op_1","q4_op_2","q4_op_3","q4_ans"]
        course_name = str(exam_name.split(sep='_')[0])
        to_vals = [exam_name,course_name]

        for key, vals in ques_bank.items():
            to_vals.append(key)
            for ans, options in vals.items():
                for opt in options:
                    to_vals.append(opt)
                to_vals.append(str(ans))

        if self.sql_con.insert(table=self.table,to_cols=to_cols,to_vals=to_vals) == None:
             st.success(f'Your assignment, {exam_name}, was saved!')
           
        # st.write(self.sql_con.get(table='assignments',col=None))

    def get_bank_from_forms(self,exam_name,set_ques_len,set_ans_len):
        ques_bank = {} # { exam_question : { answer index : options } }
        for i in range(set_ques_len):
            with st.form(exam_name+'_Form_'+str(i)):
                question = exam_name+'_'+str(i)+','
                question += st.text_input(label="Question "+str(i+1),)
                options = []
                col0,col1,col2 = st.columns(set_ans_len)
                col_arr = [col0, col1,col2]
                for ind,col in enumerate(col_arr):
                        with col:
                            options.append(st.text_input(label='Option '+str(ind+1),key = str(i)+str(ind)))

                ans = st.selectbox(label='Correct option:',options=range(1,set_ans_len+1),key=exam_name+'ans'+str(i))
                st.form_submit_button('OK')
            ques_bank[question] = {int(ans)-1 : options}
            options = []
        return ques_bank

    def reset_forms(self):
        non_form_states = [pt.teacher,pt.edit_pg,pt.new_pg,pt.submit,pt.assign]
        for val in filter(lambda x: x not in non_form_states, st.session_state):
            del st.session_state[val] 

    def reset_pg(self, go_to):
        is_bool = lambda x : type(st.session_state[x]) == bool   
        for val in filter(is_bool, st.session_state):
            if val != go_to:
                st.session_state[val] = False
            else:
                st.session_state[val] = True
 
