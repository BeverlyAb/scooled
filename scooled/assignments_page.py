# assignments_page.py

import streamlit as st
from structs import PageType as pt
import pandas as pd

class Assignments:

    def __init__(self) -> None:
        self.assignment = st.session_state[pt.assign]

    def display(self):
        st.title(self.assignment)
        if st.sidebar.button('Return to Courses'):
            self.reset_pg(pt.teacher)


    def reset_pg(self, go_to):
        is_bool = lambda x : type(st.session_state[x]) == bool   
        for val in filter(is_bool, st.session_state):
            if val != go_to:
                st.session_state[val] = False
            else:
                st.session_state[val] = True
 
