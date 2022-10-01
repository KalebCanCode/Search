Kaleb Slater Newman & Korey Sam 

Instructions for use, describing how a user would interact with your program:
    In the beginning, run index.py in the format of index.py <XML file> <titleFile> <docsFile> <wordsfile> and then run the querier
    with the format of query.py --pagerank <titleFile> <docsFile> <wordsfile>, with "--pagerank" being optional
    if the uses --pagerank, pagerank will be taken into account for the top web pages.
    The user can then input words and get back the top 10 results until they enter “:quit.”

Description of how the pieces of your program fit together
    Given an xml file and three other text files, a user runs the indexer on that collection of xmls.
    These files are scored agaisnt each other with relevance (for specific words) and pagerank.

    The __init__ runs parser(), relevance(), heavy() --the weight function --, and pagerank()

    After this the querier is run, we run our repl() and parses the input, we use our score() method to return the 10 most relevant pages


No failure to execute any features and no additional features added. 

description of how you tested your program, and ALL of your system tests
For the functions that make up the indexer and querier, we unit tested them, primarily hand calculating their results and then those functions to be the same as the hand calculations. 

***** ------------     SYSTEM TESTS SYSTEM TESTS SYSTEM TESTS    SYSTEM TESTS ----------------******

index.py wiki/MedWiki a b c
query.py --pagerank a b c

Text:  baseball
returns:
Ohio
February 2
Oakland Athletics
Kenesaw Mountain Landis
Miami Marlins
Netherlands
Minor league baseball
Kansas
Pennsylvania
Fantasy sport

Text:  search

Netherlands
New Amsterdam
Pope
Empress Jit?
Empress Suiko
Pennsylvania
George Berkeley
Hinduism
History of the Netherlands
North Pole

Text:  ioehfqfhuhfu search  
Netherlands
New Amsterdam
Pope
Empress Jit?
Empress Suiko
Pennsylvania
George Berkeley
Hinduism
History of the Netherlands
North Pole

Text:  qfodhuouou 
No Results Found

Text:  a
No Results Found

Text:  Kaleb 
No Results Found

#THESE RESULTS DO NOT TAKE INTO ACCOUNT PAGERANK
query.py  a b c

Text:  baseball
Oakland Athletics
Minor league baseball
Miami Marlins
Fantasy sport
Kenesaw Mountain Landis
Out
October 30
January 7
Hub
February 2

Text:    ggggggg baseball
Oakland Athletics
Minor league baseball
Miami Marlins
Fantasy sport
Kenesaw Mountain Landis
Out
October 30
January 7
Hub
February 2

Text:  fggougvcbb
No Results Found

index.py wiki/MedWiki a b c
query.py a b c

Text:  war enter
List of wartime cross-dressers
War
Philosophy of war
Effects of war
Progressive war
War referendum
War profiteering
War porn
Bavarian War (1459?1463)
Military history

Text:  war porn
War porn
Philosophy of war
List of wartime cross-dressers
Effects of war
Progressive war
War referendum
War profiteering
War
Bavarian War (1459?1463)
Military history
