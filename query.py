
import sys
import file_io
import re
import nltk
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
nltk_test.stem("Stemming")

def tup_sort(tup: tuple):
        return tup[1]

class Querier:
    def __init__(self):
        self.dict_title = {}
        self.dict_words = {}
        self.dict_docs = {}
        self.page_bool = sys.argv[1]
        self.arg_length = len(sys.argv) - 1


        
            # file_io.read_title_file(sys.argv[2], self.dict_title)
            # file_io.read_docs_file(sys.argv[3], self.dict_docs)
            # file_io.read_words_file(sys.argv[4], self.dict_words)
        
#This function tokenizes, makes all the words lowercase, removes stop words, stems them and adds them to an array list. 
#Param: takes in a string for words. 
    def stem_q(self, wordies: str):
        q_list = []
        tokens = re.findall('''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+''', wordies)
        for new_wordies in tokens:
            new_wordies = new_wordies.lower()
            if new_wordies not in STOP_WORDS:
                new_word = nltk_test.stem(new_wordies)
                q_list.append(new_word)
        
        return q_list


   #The boolean denotes whether to use pagerank or not, given the list of words we calculate the top ten most relevant pages. 
    #Param: Takes in a list of words and a boolean
    def score(self, q_list: list, bool: bool):
        return_docs = {}
        if not bool:

            for x in q_list:
                try:
                    doc_rel = self.dict_words[x]
                    for j in doc_rel:
                        if j in return_docs:
                            return_docs[j] += self.dict_words[x][j]
                        else:
                            return_docs[j] = self.dict_words[x][j]
                except KeyError:
                    q_list = q_list
        else:
            for x in q_list:
                try:
                    doc_rel = self.dict_words[x]
                
                    for j in doc_rel:
                        if j in return_docs:
                            return_docs[j] += self.dict_words[x][j]
                        else:
                            return_docs[j] = self.dict_words[x][j] * self.dict_docs[j]
                except KeyError:
                    q_list = q_list
        

        d_list = list(return_docs.items())
        d_list.sort(reverse=True, key=tup_sort)
        if d_list == []:
            print("No Results Found")
        count = 10
        for x in d_list:
            if count != 0:
                print(self.dict_title[x[0]])
                count -= 1
# This function runs an infinite loop of input text and calls the score and stem functions on the passed in input text. 
#If the text ends up being :quit then it will stop running the loop. 
#Param: takes in the class and a boolean. 
def repl_run(q_class, bool: bool):
    while 1>0:
        repl = input("Text:  ")
        if repl == ":quit":
            break
        else:
            
            q_list = q_class.stem_q(repl)
            q_class.score(q_list, bool)
#This function runs all of the other functions as soon as the querier is initialized. 
#Param: takes in the query class, title, document, and words. 
def main(q_class, tit, doc, words):
    if q_class.arg_length == 4 and q_class.page_bool == '--pagerank':
        file_io.read_title_file(sys.argv[2], tit)
        file_io.read_docs_file(sys.argv[3], doc)
        file_io.read_words_file(sys.argv[4], words)
        repl_run(q_class, True)

    elif q_class.arg_length == 4 and q_class.page_bool != '--pagerank':
        print("Invalid Input for pagerank")
        
    elif q_class.arg_length == 3:
        try:
            file_io.read_title_file(sys.argv[1], tit)
            file_io.read_docs_file(sys.argv[2], doc)
            file_io.read_words_file(sys.argv[3], words)
            repl_run(q_class, False)
        except FileNotFoundError:
            print("File Not Found")
    else:
        
        raise IOError("Invalid Argumant Input")
        


if __name__ == "__main__":
    my_class = Querier()
    main(my_class, my_class.dict_title, my_class.dict_docs, my_class.dict_words)


