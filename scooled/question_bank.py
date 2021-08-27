# question_bank.py

import streamlit as st
class QuestionBank:

    def __init__(self, bank):
        self.bank = {}

    def get_bank(self):
        return self.bank 
    
    def update_bank(self, assign : dict):
        st.write(assign.keys()[0])
        self.bank[assign.keys()[0]] = assign

