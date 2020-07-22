# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 22:37:42 2020

@author: bhadr
"""

import json
read_file=open("cw_data.json",encoding="utf8")
data=json.load(read_file)
flattened=dict()
for region in data:
    for date in data[region]:
        for codes in data[region][date]:
            flattened[codes]=dict()
            flattened[codes]["id"]=data[region][date][codes]["hash"]
            flattened[codes]["time"]=data[region][date][codes]["time"]
            flattened[codes]["src"]=data[region][date][codes]["src"]
            flattened[codes]["region"]=data[region][date][codes]["region"]
            flattened[codes]["time"]=data[region][date][codes]["time"]
            flattened[codes]["domain"]=data[region][date][codes]["domain"]
            flattened[codes]["digest"]=data[region][date][codes]["digests"]["English"]["digest"]
            flattened[codes]["headline"]=data[region][date][codes]["digests"]["English"]["headline"]

#%%
import nltk
import math
FILE_MATCHES = 1
SENTENCE_MATCHES = 1
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer

#create an object of class PorterStemmer
porter = PorterStemmer()
lancaster=LancasterStemmer()

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens=[]
    sentence=nltk.tokenize.word_tokenize(document)

    for word in sentence:
        lowered=word.lower()
        for letter in word:
            if not letter.isalnum():
                lowered=lowered.replace(letter,"")
        if lowered not in nltk.corpus.stopwords.words("english") and lowered != '':
            tokens.append(porter.stem(lowered))
    return tokens
    raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    for filename in documents:
        words.update(documents[filename])
    # Calculate IDFs
    idfs = dict()
    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf
    return idfs
    
    raise NotImplementedError


def top_files(query, files, idfs):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf=dict()
    for eachfile in files:
        tfidfsum=0
        for word in query:
            tf=files[eachfile].count(word)
            tfidfsum+=tf*idfs[word]
        tfidf[eachfile]=tfidfsum    
    
    ranked = sorted(tfidf.keys(),key=lambda var:-tfidf[var])
    filtered=[]
    for f in ranked:
        if tfidf[f]>0:
            filtered.append(f)
    return filtered
    raise NotImplementedError



#%%

file_words = {
        codes: tokenize(flattened[codes]["digest"]+flattened[codes]["headline"])
        for codes in flattened
    }
file_idfs = compute_idfs(file_words)


#%%

import time
import sys

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

for i in range(10):
    query = set(tokenize(input("Query: ")))
    tic = time.perf_counter()
    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs)
    toc = time.perf_counter()
    print ("query = ",query ,f"Time Taken ={toc - tic:0.4f} seconds")
    print (filenames)

sys.stdout = orig_stdout
f.close()

