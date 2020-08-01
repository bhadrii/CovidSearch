# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 14:17:43 2020

@author: bhadr
"""
from config import SETUP_PATH,stemtokenize,tokenize,URL
from urllib.request import urlretrieve

import math
import json
from ntk.util import ngrams
from ntk.probability import FreqDist

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
def setup(path="corpus.json"):
    download=urlretrieve(URL, path)
    flattened=dict()
    read_file=open(path,encoding="utf8")
    data=json.load(read_file)
    for region in data:
        for date in data[region]:
            for codes in data:
                flattened[codes]=dict()
                #flattened[codes]["id"]=data[region][date][codes]["hash"]
                flattened[codes]["digest"]=data[codes]["digest"]
                flattened[codes]["headline"]=data[codes]["headline"]
    file_words = {
                    codes: stemtokenize(flattened[codes]["digest"]+flattened[codes]["headline"])
                    for codes in flattened
                    }
    file_idfs = compute_idfs(file_words)
    return flattened,file_words,file_idfs



def freq_tables():
    bigram_freq=FreqDist()
    unigram_freq=FreqDist()
    for codes in flattened:
        for token in tokenize(flattened[codes]["digest"]+flattened[codes]["headline"]):
            unigram_freq[token] += 1 
        
        for one, two in ngrams(tokenize(flattened[codes]["digest"]+flattened[codes]["headline"]), 2):
            bigram_freq[(one,two)] += 1
    #Sorting the frequency distribution tables
    unigrams=[i for i in unigram_freq.items()]
    unigrams.sort(key=lambda x: -x[1])
    bigrams=[i for i in bigram_freq.items()]
    bigrams.sort(key=lambda x: -x[1])
    return unigrams,bigrams

flattened,file_words,file_idfs=setup()
unigrams,bigrams=freq_tables()
masterdata={'search_data':(file_words,file_idfs),'suggest_data':(unigrams,bigrams)}

json_object = json.dumps(masterdata) 
  
# Writing to sample.json 
with open(SETUP_PATH, "w") as outfile: 
    outfile.write(json_object)
