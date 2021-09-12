import nltk
from Questgen import main
import streamlit as st

class QuestionGen:
    def __init__(self):
        self.qg = main.QGen()

    def download(self):
        # use command on terminal instead 
       nltk.download('stopwords') # python -m nltk.downloader stopwords 

    def generate(self,payload :dict):
        """Runs NLP model and returns dict of questions, answer, option, and context

        Args:
            payload (dict): [description]

        Returns:
            output: list
        """        
        output = self.qg.predict_mcq(payload)
        return self.q_and_a(output)
    
    def q_and_a(self,bank : dict):
        """splits bank into question, answer, opts, and note

        Args:
            bank (dict): 

        Returns:
            list: 
        """       
        question = bank['questions'][0]['question_statement'] 
        answer = bank['questions'][0]['answer']
        opt1 = bank['questions'][0]['options'][0]
        opt2 = bank['questions'][0]['options'][0]
        opt3 = bank['questions'][0]['options'][0]
        opt4 = answer
        note = bank['questions'][0]['context']

        return question,answer, [opt1,opt2,opt3,opt4],note

if __name__=="__main__":
    # def run(self):
    test = QuestionGen()
    payload = {
            "input_text": "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team."
    }
    ques, ans, opt_list, note = test.generate(payload)
    st.write(ques,'\n',ans,'\n',opt_list,note,'\n')