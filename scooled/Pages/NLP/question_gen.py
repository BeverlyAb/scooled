import nltk
from Questgen import main
import streamlit as st

class QuestionGen:
    
    def __init__(self):
        self.qg = main.QGen()

    # def download(self):
    #     # use command on terminal instead 
    #    nltk.download('stopwords') # python -m nltk.downloader stopwords 

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
        question = bank['questions'][0]['question_statement'].replace("'","`")
        answer = bank['questions'][0]['answer'].replace("'","`")
        # opt1 = bank['questions'][0]['options'][0].replace("'","`")
        # opt2 = bank['questions'][0]['options'][1].replace("'","`")
        # opt3 = bank['questions'][0]['options'][2].replace("'","`")
        opt_list = [bank['questions'][0]['options'].replace("'","`") for bank['questions'][0]['options'] in bank['questions'][0]['options']]
        note = bank['questions'][0]['context'].replace("'","`")

        return question,answer,opt_list,note

if __name__=="__main__":
    # def run(self):
    test = QuestionGen()
    t = "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team."
    text = "Addition is the summing of parts."
    payload = {
            "input_text": text
    }
    ques, ans, opt_list, note = test.generate(payload)
    print(ques,'\n',ans,'\n',opt_list,note,'\n')