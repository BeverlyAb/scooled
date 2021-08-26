# assignments_page.py

import streamlit as st
from structs import PageType as pt

class Assignments:

    def __init__(self) -> None:
        self.assignment = st.session_state[pt.assign]

    def display(self):
        st.title(self.assignment)