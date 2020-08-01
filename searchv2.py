# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 13:09:24 2020

@author: bhadr
"""


from config import stemtokenize,SETUP_PATH
import json
read_file=open(SETUP_PATH,encoding="utf8")
file_words,file_idfs=json.load(read_file)['search_data']

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
    
#FILE_MATCHES=15 --> Currently we return all files that match the keywords. Can filter articles i


def search(query):
    query = set(stemtokenize(query))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs)
    return filenames

