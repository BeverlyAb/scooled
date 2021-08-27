# question_bank.py

import streamlit as st
class QuestionBank:

    def __init__(self):
        self.bank = {}

    def get_bank(self):
        return self.bank 
    
    def add(self, name:str, assign : dict):
        self.bank[name] = assign
