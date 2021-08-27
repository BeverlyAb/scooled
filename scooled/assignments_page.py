# assignments_page.py

import streamlit as st
from structs import PageType as pt
import pandas as pd

class Assignments:

    def __init__(self) -> None:
        self.assignment = st.session_state[pt.assign]
        # if st.session_state[pt.submit] not in st.session_state:
        #     st.session_state[pt.submit] = False

    def display(self):
        st.sidebar.title('Menu')
        st.title(self.assignment.columns[0])

        if st.sidebar.button('Return to Courses'):
            self.reset_pg(pt.teacher)

    def create_new_pg(self):
        st.sidebar.title('Menu')
        exam_name = self.assignment.columns[0]
        st.title(exam_name)
        set_ques_len = 4
        set_ans_len = 3
        for i in range(set_ques_len):
            with st.form(exam_name+'Form'+str(i)):
                st.text_input(label="Question "+str(i+1))
                col0,col1,col2 = st.columns(set_ans_len)
                col_arr = [col0, col1,col2]
                for ind,col in enumerate(col_arr):
                        with col:
                            st.text_input(label='Option '+str(i+1),key = str(i)+str(ind))

                st.selectbox(label='Correct option:',options=range(1,set_ans_len+1),key=exam_name+'ans'+str(i))
                st.form_submit_button('Done')
        if st.sidebar.button('Return to Courses'):
            self.reset_pg(pt.teacher)


    def reset_pg(self, go_to):
        is_bool = lambda x : type(st.session_state[x]) == bool   
        for val in filter(is_bool, st.session_state):
            if val != go_to:
                st.session_state[val] = False
            else:
                st.session_state[val] = True
 
