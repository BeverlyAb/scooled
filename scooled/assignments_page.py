# assignments_page.py

from numpy.lib.function_base import append
import streamlit as st
from structs import PageType as pt
import pandas as pd
from sql_connector import SQLConnector
import numpy as np
import itertools

class Assignments:

    def __init__(self) -> None:
        self.assignment = st.session_state[pt.assign]
        # if st.session_state[pt.submit] not in st.session_state:
        #     st.session_state[pt.submit] = False
        self.sql_con = SQLConnector()
        self.table = 'test.question_bank'
        self.set_ques_len = 4
        self.set_opt_len = 3
        

    def display(self):
        st.sidebar.title('Menu')
        assign = self.assignment.columns[0]
        st.title('Assignment Overview')
        st.write(assign)
        st.stop()
        notes, vals = self.split_notes_and_questions(assign)
        assign_name = vals[0]
        if vals != None:
            df = self.group_by_type(vals[2:])
            st.subheader(assign_name)
            st.table(df)

        self.view_notes(notes)
        self.edit_notes(df,assign_name)
        if st.sidebar.button('Back to Courses'):
            self.reset_pg(pt.teacher)

    def get_cols_from_db(self):
                # cols = self.get_cols_from_db()
        # d = {}
        # for val, col in zip(vals, cols):
        #     d[col] = val

        # df=pd.DataFrame(d,index=[0]).transpose()
        # # df.index = np.arange(1, len(df)+1)
        # st.write(df)
        self.sql_con.query(f"SHOW COLUMNS FROM {self.table}")
        cols = st.session_state[pt.submit]
        column_name = [col[0] for col in cols]
        return column_name[:-1] #exclude rowindex

    def view_notes(self,notes : tuple):
        with st.expander(label='Feedback'):
            for note in notes:
                st.write(note)

    def edit_notes(self,df,assign_name):
        if st.checkbox(label='Edit Feedback Notes'):
            with st.form('Note Edit'):   
                q = st.selectbox(label='Edit notes for which question?',options=range(1,self.set_ques_len+1))
                note = st.text_input('Write text or link to a website or image!')
                corr_q = df['Question'][q]
                q = 'q'+str(q)
                if st.form_submit_button('OK'):
                    query = f"UPDATE {self.table} SET Notes = '{note}' WHERE assign_name = '{assign_name}' AND {q} = '{corr_q}';"
                    self.sql_con.query(query)
                    st.success(f"Updated notes for {q}")

    def split_notes_and_questions(self,assign):
        self.load_from_db(assign,['*'])
        if len(st.session_state[pt.submit]) > 0:
            everything = st.session_state[pt.submit][0]

            self.load_from_db(assign,['Notes'])#,'q1','q2','q3','q4'])
            if len(st.session_state[pt.submit]) > 0:
                notes = st.session_state[pt.submit][0]
                q_bank = [val for val in everything if val not in notes]
                return notes, q_bank

            else: 
                return None
        else:
            return None

    def group_by_type(self,vals):
        group_len = self.set_ques_len + 1 # question + ans
        q1 = []
        q2 = []
        q3 = []
        q4 = []
        q_bank = [q1,q2,q3,q4]
        for i in range (len(vals) // group_len):
            q_bank[i].extend(vals[group_len*i:group_len*(i+1)])
        
        df = pd.DataFrame(q_bank)
        df.index = np.arange(1, len(df)+1)
        df.columns = ['Question','Option 1','Option 2','Option 3','Answer']
        return df

    def load_from_db(self, assign, col :list):
        ''' updates st.session_state[pt.submit]'''
        self.sql_con.get_where_specified(table=self.table,get_cols=col,from_col='assign_name',val_from_col=assign)

    
    def create_new_pg(self):
        st.sidebar.title('Menu')
        exam_name = 'Math_1'#self.assignment.columns[0]
        st.title(exam_name)

        
        ques_bank = self.get_bank_from_forms(exam_name,self.set_ques_len,self.set_opt_len)

        if st.button('Submit'):
            self.write_to_db(ques_bank,exam_name)               # add to db
            self.reset_forms()                                  # clear forms
            # self.reset_pg(pt.teacher)                           # go back to teacher pg
        if st.sidebar.button('Return to Courses'):
            self.reset_forms()                                  # clear forms
            self.reset_pg(pt.teacher)                           # go back to teacher pg

    def write_to_db(self, ques_bank : dict,exam_name):
        to_cols = ["assign_name","course_name","question","question_num","answer","opt1","opt2","opt3"]
        course_name = str(exam_name.split(sep='_')[0])

        for i in reversed(range(self.set_ques_len)):
            to_vals = [exam_name,course_name]    
            grouped_val = ques_bank.popitem()
            question = grouped_val[0]
            question_num = str(i+1)
            ans_set = grouped_val[1]
            answer = [ans for ans in ans_set.keys()][0]
            opts = [opt for opt in ans_set.values()][0]
        
        
            to_vals.extend([question,question_num,answer])
            to_vals.extend(opts)
            st.write(to_vals)
            self.sql_con.insert(table=self.table,to_cols=to_cols,to_vals=to_vals)
        else:
            st.success(f'Your assignment, {exam_name}, was saved!')

    def get_bank_from_forms(self,exam_name,set_ques_len,set_ans_len):
        ques_bank = {} # { exam_question : { answer index : options } }
        for i in range(set_ques_len):
            with st.form(exam_name+'_Form_'+str(i)):
                # question = exam_name+'_'+str(i)+','
                question = st.text_input(label="Question "+str(i+1),)
                options = []
                col0,col1,col2 = st.columns(set_ans_len)
                col_arr = [col0, col1,col2]
                for ind,col in enumerate(col_arr):
                        with col:
                            options.append(st.text_input(label='Option '+str(ind+1),key = str(i)+str(ind)))

                ans = st.selectbox(label='Correct answer',options=range(1,set_ans_len+1),key=exam_name+'ans'+str(i))
                ans = options[ans-1]
                st.form_submit_button('OK')
            ques_bank[question] = {ans : options}
            options = []
        return ques_bank

    def reset_forms(self):
        non_form_states = [pt.teacher,pt.edit_pg,pt.new_pg,pt.submit,pt.assign]
        for val in filter(lambda x: x not in non_form_states, st.session_state):
            del st.session_state[val] 

    def reset_pg(self, go_to):
        is_bool = lambda x : type(st.session_state[x]) == bool   
        for val in filter(is_bool, st.session_state):
            if val == go_to:
            #     st.session_state[val] = False
            # else:
                st.session_state[val] = True
        
 
