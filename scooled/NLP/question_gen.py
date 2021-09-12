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
        pprint(output)


if __name__=="__main__":
    test = QuestionGen()
    payload = {
            "input_text": "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
    }
    test.generate(payload)