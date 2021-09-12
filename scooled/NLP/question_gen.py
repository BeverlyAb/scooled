import nltk
from pprint import pprint
from Questgen import main

class QuestionGen:
    def __init__(self):
        self.qg = main.QGen()

    def download(self):
        # use command on terminal instead 
       nltk.download('stopwords') # python -m nltk.downloader stopwords 

    def generate(self,payload :dict):
        output = self.qg.predict_mcq(payload)
        return self.q_and_a(output)
    def q_and_a(self,bank : dict):
        answer = bank['questions'][0]['answer']
        opt1 = bank['questions'][0]['options'][0]
        opt2 = bank['questions'][0]['options'][0]
        opt3 = bank['questions'][0]['options'][0]
        opt4 = answer
        note = bank['questions'][0]['context']

        return answer, [opt1,opt2,opt3,opt4],note

if __name__=="__main__":
    test = QuestionGen()
    payload = {
            "input_text": "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team."
    }
    ans, opt_list, note = test.generate(payload)
    print(ans,'\n',opt_list,note,'\n')