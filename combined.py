from config import stemtokenize,SETUP_PATH,tokenize,CUTOFF_FREQ
import json


def top_files(query, files, idfs,FILE_MATCHES=0):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the top
    'FILE_MATCHES' that match the query if >0 or all the files that 
    match the query if 'FILE_MATCHES' is not passed.
    """
    tfidf=dict()
    for eachfile in files:
        tfidfsum=0
        for word in query:
            tf=files[eachfile].count(word)
            tfidfsum+=tf*idfs[word]
        tfidf[eachfile]=tfidfsum    
    
    ranked = sorted(tfidf.keys(),key=lambda var:-tfidf[var])
    
    
    if FILE_MATCHES!=0:
        return ranked[:FILE_MATCHES]
    else:
        filtered=[]
        for f in ranked:
            if tfidf[f]>0:
                filtered.append(f)
            else:
                break
        return filtered
    


def filesearch(query):
    query = set(stemtokenize(query))
    
    read_file=open(SETUP_PATH,encoding="utf8")
	file_words,file_idfs=json.load(read_file)['search_data']

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs)
    return filenames





def starts(word,string):
    if len(string)>len(word):
        return False
    for i in range(len(string)):        
        if word[i]!=string[i]:
            return False
    return True


def autocomplete(string):
    read_file=open(SETUP_PATH,encoding="utf8")
    unigrams,bigrams=json.load(read_file)['suggest_data']
    string=string.lower()
    output=dict()
    for item in unigrams:
        word=item[0]
        if starts(word,string) and item[1] > CUTOFF_FREQ:
            (query,suggestions)=suggest(word)
            output[query]=suggestions
    print(output)     
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

def search(keyword="keyword",type="suggest/search"):
    if type=="search":
        return filesearch(keyword)
    elif type=="suggest":
        return autocomplete(keyword)