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
        st.title(self.assignment.columns[0])
        set_ques_len = 4
        set_ans_len = 3
        for i in range(set_ques_len):
            if st.checkbox(label="Multiple choice",key=str(i)):
                st.text_input(label="Question "+str(i+1))
                for j in range(set_ans_len):
                    st.text_input(label='Option '+str(j+1))
                st.selectbox(label='Correct option:',options=range(1,set_ans_len+1))
            else:
                st.text_input(label="Question "+str(i+1))

        if st.sidebar.button('Return to Courses'):
            self.reset_pg(pt.teacher)


    def reset_pg(self, go_to):
        is_bool = lambda x : type(st.session_state[x]) == bool   
        for val in filter(is_bool, st.session_state):
            if val != go_to:
                st.session_state[val] = False
            else:
                st.session_state[val] = True
 
