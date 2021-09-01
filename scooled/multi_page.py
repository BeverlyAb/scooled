# multi_page.py

# referenced from https://github.com/prakharrathi25/data-storyteller/blob/main/multipage.py
import streamlit as st
class MultiPage: 

    def __init__(self) -> None:
        self.pages = []
    def add_page(self, title, func) -> None: 

        self.pages.append(
            {
                "title": title, 
                "function": func
            }
        )

    def run(self,id):
        page = st.sidebar.selectbox(f'What would you like to do?',
            self.pages, 
            format_func=lambda page: page['title']
        )

        # run the app function 
        page['function'](id)