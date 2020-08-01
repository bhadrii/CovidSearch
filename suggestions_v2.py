import json
from config import tokenize,CUTOFF_FREQ,SETUP_PATH

read_file=open(SETUP_PATH,encoding="utf8")
unigrams,bigrams=json.load(read_file)['suggest_data']


def starts(word,string):
    if len(string)>len(word):
        return False
    for i in range(len(string)):        
        if word[i]!=string[i]:
            return False
    return True


def autocomplete(string):
    string=string.lower()
    output=dict()
    for item in unigrams:
        word=item[0]
        if starts(word,string) and item[1] > CUTOFF_FREQ:
            (query,suggestions)=suggest(word)
            output[query]=suggestions
            
    return output
    

def suggest(query):
    
    suggestions=[]
    query=tokenize(query)[0]
    
    for items in bigrams:

        word1=items[0][0]
        word2=items[0][1]
        if query==word1 and items[1]>CUTOFF_FREQ:
            suggestions.append((word2,items[1]))
        
        
    
    return (query,suggestions)


            
