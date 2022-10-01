import pytest
import file_io
from index import *

#Given test for releveance, check the relevance for the words in documents
def test_frequency():
    index_2 = Indexer("wiki/test_tf_idf.xml", 'a', 'b', 'c')
    map = {}
    file_io.read_words_file('c', map)
    #CHANGE TO SMALL DISTANCE BETWEEN THE NUMBERS
    assert map['dog'][1] - 0.4054 < 0.001

    for x in map['page']:
        assert map['page'][x] == 0.0
    
    assert map['ate'][2] - 1.0986 < 0.001
    assert map['chees'][3] - 0.405465 < 0.0001

#THE NEXT TEST ARE TESTING THE CORRECTNESS OF THE 
#GIVEN PAGERANK EXAMPLES
def test_pagerank():
    indexxx = Indexer("wiki/PageRankExample1.xml", 'a', 'b', 'c')
    pr = {}
    file_io.read_docs_file('b', pr)
    assert pr[1] == 0.4326427188659158
    assert pr[2] == 0.23402394780075067
    assert (pr[3] - 0.3333) < 0.01 

#THE NEXT TEST ARE TESTING THE CORRECTNESS OF THE 
#GIVEN PAGERANK EXAMPLES

def test_pagerank_2():
    indexxx = Indexer("wiki/PageRankExample2.xml", 'a', 'b', 'c')
    pr = {}
    file_io.read_docs_file('b', pr)
    assert (pr[1]- 0.2018) < 0.001
    assert (pr[2]- 0.0375) < 0.001
    assert (pr[3]- 0.3740) < 0.001
    assert (pr[4]- 0.3867) < 0.001
    
#THE NEXT TEST ARE TESTING THE CORRECTNESS OF THE 
#GIVEN PAGERANK EXAMPLES
def test_pagerank_3():
    indexxx = Indexer("wiki/PageRankExample3.xml", 'a', 'b', 'c')
    pr = {}
    file_io.read_docs_file('b', pr)
    assert (pr[1]- 0.0524) < 0.001
    assert (pr[2]- 0.0524) < 0.001
    assert (pr[3]- 0.4476) < 0.001
    assert (pr[4]- 0.4476) < 0.001

#THE NEXT TEST ARE TESTING THE CORRECTNESS OF THE 
#GIVEN PAGERANK EXAMPLES
def test_pagerank_4():
    indexxx = Indexer("wiki/PageRankExample4.xml", 'a', 'b', 'c')
    pr = {}
    file_io.read_docs_file('b', pr)
    #CHANGE TO SMALL DISTANCE BETWEEN THE NUMBERS
    assert (pr[1]- 0.0375) < 0.001
    assert (pr[2]- 0.0375) < 0.001
    assert (pr[3]- 0.4625) < 0.001
    assert (pr[4]- 0.4625) < 0.001

#These test the special cases of pagerank
def test_pagerank_special_cases_yo():

    #Pages have no links
    indexxx = Indexer("pagerankspecial.xml", 'a', 'b', 'c')
    pr = {}
    file_io.read_docs_file('b', pr)
    assert pr[1] == pr[2] == pr[3]

    #Pages 1 and 3 both link to pages outside the corpus
    #nothing is liking to those pages
    indexxx = Indexer("pagerankspecial2.xml", 'a', 'b', 'c')
    pr_2 = {}
    file_io.read_docs_file('b', pr_2)
    assert pr_2[1] == pr_2[3]

    #Page 1 links to page 2 12 times!
    #Page 2 links to page 1 once :((
    #But, multiple links to the same page 
    # are treated as one, so the pagerank
    # should be the same    
 
    indexxx = Indexer("pagerankspecial3.xml", 'a', 'b', 'c')
    pr_3 = {}
    file_io.read_docs_file('b', pr_3)

    assert pr_3[1] == pr_3[2]


#This tests our in_dict method,
# which sees if a value is in a dictionary
def test_dict():
    indexxx = Indexer("wiki/SmallWiki.xml", 'a', 'b', 'c')
    dict = {1:"Hey", 2:"Bro"}
    
    assert indexxx.in_dict(dict, "Bro") == True
    
#This tests our distance function
#calculates euclidean distance
def test_distance():
    i = Indexer("QuantumWiki.xml", 'a', 'b', 'c')
    first_dictionary= {1: 2, 2: 3, 3: 0, 4: 3}
    second_dictionary= {1: 3,2: 3,3: -5, 4: 8}

    assert i.distance(first_dictionary, second_dictionary) - 7.14 < 0.01

#This tests the creation of our weights
def test_weights():
    index = Indexer("LinkWiki.xml", 'a', 'b', 'c')

    index.heavy(index.id_to_links)



    assert index.id_to_weights[(3,1)] - 0.455 < 0.01
    assert index.id_to_weights[(2,1)] - 0.2425 < 0.01
    assert index.id_to_weights[(2,2)] == .15/5

#This also, tests the functionality of our relevance
#includes the special cases
def test_relevance():
    h = Indexer("relWiki.xml", 'a', 'b', 'c')
    relevance_amount = {}
    file_io.read_words_file('c', relevance_amount)
    assert relevance_amount['charl'][1]- 0.45814 < 0.001
    assert relevance_amount['charl'][1] - 0.9162 < 0.001
    #make sure that idf works, dog is in every doc, so 
    #log(n/ni) == 0
    for x in relevance_amount['dog']:
        assert relevance_amount['dog'][x] == 0
    assert relevance_amount['thank'][3] - 1.6094  < 0.001
    assert relevance_amount['violet'][2] - 1.6094379124341003 < 0.001



def test_stem():
    #This test wiki contains the word "continuing" 5 times in page one
    #and 1 time in page 2
    #This wiki contains the word spans once in each page
    #This wiki contains the word a 3 times in each page
    #the word "the" is in the last page

    #THIS TEST IS MEANT TO TEST THE STEMMING FUNCTION BY 
    #LOOKING THROUGH THE RELEVANCE DICTIONARY
    h = Indexer("stemwiki.xml", 'a', 'b', 'c')
    rel = {}
    file_io.read_words_file('c', rel)

    def has_key(dic: dict, val):
        if val in dic:
            return True
        else:
            return False



    assert has_key(rel, 'continu') == True
    assert has_key(rel, 'a') == False
    assert has_key(rel, 'span') == True
    assert has_key(rel, 'the') == False

    for x in rel['span']:
        assert rel['span'][x] == 0

    
#THIS TEST TESTS THE ACCURACY OF THE TITLE DICTIONARY
def test_title():
    
    h = Indexer("stemwiki.xml", 'a', 'b', 'c')
    tit = {}
    file_io.read_title_file('a', tit)

    assert tit[0] == 'I am a lover of the CS'
    assert tit[1] == 'Teen Titans is my favorite show'
    assert tit[2] == 'Rats'
    assert tit[3] == 'Boring Company'




