import re
import xml.etree.ElementTree as et
import nltk
import math

from numpy import true_divide
import file_io
import sys
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
nltk_test.stem("Stemming") # outputs "stem"




class Indexer:
    def __init__(self, file, title, docs, words):
        self.title = title
        self.docs = docs
        self.words = words
        self.file_io = file_io
        self.corpus = []

        #may not need the next three to be apart of the object
        self.title_dictionary = {}
        
        

        self.docmax = {}
        self.words_to_contain = {} 
        self.word_to_ids_to_amounts = {}
        self.id_to_links = {}
        self.id_to_weights = {}
        self.number_of_documents = 0

        self.parser(file)
        self.relevance()
        self.heavy(self.id_to_links)
        self.pagerank(self.title_dictionary)


        


        #This populates the IDs to text dictionary
        #Param: This function takes in the xml file 
        # and a self(representation of the indexer class)
    def page_func(self, xml):
        root = et.parse(xml).getroot()
        all_pages =  root.findall("page")
        for page in all_pages:
            title = page.find('title').text.strip()
            id = int(page.find('id').text)
            self.title_dictionary[int(id)] = title
            self.number_of_documents += 1

        self.file_io.write_title_file(self.title, self.title_dictionary)
        
    #Checks to see if the value is in a dictionary or not
    #Params: Takes in a dictionary as well as a value. 
    #Returns a boolean based on if the value 
    # is inside the dictionary or not.
    def in_dict(self, dictionary:dict, val):
        for x in dictionary:
            if val == dictionary[x]:
                return True
        return False

#This function takes in multiple strings for the link,
#  title and then an integer for ID
#If the link string is not equal to the 
# title string and both of those strings are
#  inside the dictionary then
#  if the link string is not in id to link dictionary 
# it will be added. 
#Param: takes in the string link title,
#  a string for the title, and an integer for the id

    def can_link(self, link_title: str, title: str, id: int):
        if link_title != title and self.in_dict(self.title_dictionary, link_title):
            if link_title not in self.id_to_links[id]:
                self.id_to_links[id].append(link_title)


#This function addresses stemming and tockenizing 
# the passed in words and titles, 
# while also linking the id to either.
#It then addresses all the special cases
#  for tokenizing and splitting on bars,
#  quotation marks and colons. 
#Param: takes in string for the words, 
# title, and an integer for the ID. 
    def linkage(self, wordies:str, title:str, id:int):
     new_wordies = wordies[2:-2]
     if "|" in new_wordies:
        link_title = new_wordies.split("|")[0]
        corp_word = new_wordies.split("|")[1]
        token_bar = self.tokenize('''\[\[[^\[]+?\]\]|
        [a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+''', corp_word)
        self.can_link(link_title, title, id)

        for x in token_bar:
            self.stem(x, id)
                        

     elif ":" in new_wordies:
        words = new_wordies.split(":")
        separator = ', '
        corp_words = separator.join(words)
        token_col = self.tokenize('''\[\[[^\[]+?\]\]|
        [a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+''', corp_words)
                        
        for x in token_col:
            self.stem(x, id)
        self.can_link(new_wordies, title, id)

     else:
        token_none = self.tokenize('''\[\[[^\[]+?\]\]|
        [a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+''',  new_wordies)
        for x in token_none:
            self.stem(x, id)
        self.can_link(new_wordies, title, id)

    def maxFunc(self, max_dict: dict, id: int, val:int):
        for x in max_dict:
            if x == id:
                if max_dict[x] < val:
                    max_dict[x] = val
              
  #This method stems and removes stop words by making them all
  #  lowercase and checking if the words are in stop words
    #Then if it is not in stop words they will get stemmed
    #Param: Takes in a string for the words and an integer for the ID
  
    def stem(self, wordies: str, id: int):
        new_wordies = wordies.lower()
        if new_wordies not in STOP_WORDS:
            new_word = nltk_test.stem(new_wordies)

            if new_word in self.word_to_ids_to_amounts:
                if id in self.word_to_ids_to_amounts[new_word]:
                    self.word_to_ids_to_amounts[new_word][id] += 1
                    self.maxFunc(self.docmax,
                     id, self.word_to_ids_to_amounts[new_word][id])
                
                else:
                    self.word_to_ids_to_amounts[new_word][id] = 1
                    self.maxFunc(self.docmax, id, 1)
                    self.words_to_contain[new_word] += 1
            else:
                self.word_to_ids_to_amounts[new_word] = {id: 1}
                self.corpus.append(new_word)
                self.maxFunc(self.docmax, id, 1)
                self.words_to_contain[new_word] = 1


     #This function tokenizes the passed in
     #  words using the regex and then 
     # returns the tokenized word. 
    #Param: This function takes in a regex
    #  and a string for the words.         
    def tokenize(self, regex, word:str):
        tokens = re.findall(regex, word)
        return tokens

    #This functions parses all of the text,
    #populating the necessary data structures
    #Param: This takes in an XML file as a string. 
    def parser(self, xml: str):
    #------------------------
        self.page_func(xml)
    #------------------------
        root= et.parse(xml).getroot()
        all_pages = root.findall("page")
        for page in all_pages:

            title = page.find('title').text.strip()
            id = int(page.find('id').text)
            

            self.id_to_links[id] = []
            self.docmax[id] = 0
            text: str = page.find('text').text

            

            tokens = self.tokenize('''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+''', str(title) + ' ' + str(text))
            separator = ', '
            links = self.tokenize('''\[\[[^\[]+?\]\]''', separator.join(tokens))


            
 
            for wordies in tokens:
                if wordies in links:
                    self.linkage(wordies, title, id)
                else:
                    self.stem(wordies,id)


        del self.title
        del root
        del id
        del all_pages
        del self.corpus
    

 


        #This function uses our dictionary to calculate
        #  term frequency and inverse document frequency
        #  and multiples them together to find
        #the relevance of a specific word in a specific document.
    def relevance(self):

        
        for word in self.word_to_ids_to_amounts:
            for id in self.word_to_ids_to_amounts[word]:
        
                value = (self.word_to_ids_to_amounts[word][id]
                /self.docmax[id]) * (math.log(self.number_of_documents
                /self.words_to_contain[word]))
                
                self.word_to_ids_to_amounts[word][id] = value

        #*******-----------------------------------------------------------------------************#
        self.file_io.write_words_file(self.words, self.word_to_ids_to_amounts)
        #*******-----------------------------------------------------------------------************#

        del self.word_to_ids_to_amounts
        del self.words
        
        
        
    #This function calculates the weights 
    # that help set up page rank and uses our 
    # ids to links dictionary.        
#Param: takes in a dictionary     
    def heavy(self, linkings: dict):
        eon = 0.15/self.number_of_documents
        for x in linkings:
            if linkings[x] == []:
                for j in linkings:
                    if x == j:
                        self.id_to_weights[(x,j)] = eon
                    else:
                        weight = eon + ((1 - 0.15)/
                        (self.number_of_documents - 1))
                        self.id_to_weights[(x,j)] = weight 
            else:
                for j in linkings:
                    if x == j:
                        self.id_to_weights[(x,j)] = eon
                    #CHECK IF IT LINKS TO THAT PAGE
                    elif self.title_dictionary[j] in linkings[x]:
                        weight = eon + ((1 - 0.15)/len(linkings[x]))
                        self.id_to_weights[(x,j)] = weight
                    #OTHERWISE IF IT DOESNT LINK TO THAT
                    else:
                        self.id_to_weights[(x,j)] = eon

#This function calculates the distance 
# between the numbers two separate dictionaries
#Param: Takes in two dictionaries. 
    def distance(self, i: dict, j: dict):
        differences = []
        for x in i:
            sub = i[x] - j[x]
            differences.append((sub * sub))
        
        return math.sqrt(sum(differences))

#This method takes in a list of pages and instantiates two different
#  dictionaries to aid in computing the individual page ranks
#Then it cycles through the title dictionary and populates 
# the dictionaries that were just created with values
#After populating those dictionaries we use the distance
#  function on those dictionaries and when it is between a low value
#then we create a copy of one of our dictionaries and set it equal to the other
#This method concludes by iterating through the pages and for each page
#  we set the value to 0 and then for the rprime dictionary 
# we finally compute the pagerank by adding rprime to
#  another id dictionary and our 
    def pagerank(self, pages: list):
        r = {}
        r_prime = {}
        for x in self.title_dictionary:
            r[x] = 0
            r_prime[x] = 1/self.number_of_documents
        
        while self.distance(r_prime, r) > 0.001:
            r = r_prime.copy()

            for j in pages:
                r_prime[j] = 0
                for k in pages:
                    r_prime[j] = r_prime[j] + (self.id_to_weights[(k,j)] * r[k])
          
        
        self.file_io.write_docs_file(self.docs, r_prime)
        

if __name__ == "__main__":
    if len(sys.argv) == 5:
        try:
            Indexer(*sys.argv[1:])
        except FileNotFoundError:
            print('File not found')
    else:
        print("Invalid Argument Input")