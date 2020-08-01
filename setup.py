# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 14:17:43 2020

@author: bhadr
"""
import math
import nltk
import json
from nltk.util import ngrams
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
#create an object of class PorterStemmer
porter = PorterStemmer()

def stemtokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords WITH STEMMING.
    """
    tokens=[]
    sentence=nltk.tokenize.word_tokenize(document)

    for word in sentence:
        lowered=word.lower()
        for letter in word:
            if not letter.isalnum():
                lowered=lowered.replace(letter,"")
        if lowered not in nltk.corpus.stopwords.words("english") and lowered != '' and not lowered.isnumeric():
            tokens.append(porter.stem(lowered))
    return tokens

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords WITH STEMMING.
    """
    tokens=[]
    sentence=nltk.tokenize.word_tokenize(document)

    for word in sentence:
        lowered=word.lower()
        for letter in word:
            if not letter.isalnum():
                lowered=lowered.replace(letter,"")
        if lowered not in nltk.corpus.stopwords.words("english") and lowered != '' and not lowered.isnumeric():
            tokens.append(lowered)
    return tokens


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
def setup(path="cw_data.json"):
    
    flattened=dict()
    read_file=open(path,encoding="utf8")
    data=json.load(read_file)
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
    file_words = {
                    codes: stemtokenize(flattened[codes]["digest"]+flattened[codes]["headline"])
                    for codes in flattened
                    }
    file_idfs = compute_idfs(file_words)
    return flattened,file_words,file_idfs
flattened,file_words,file_idfs=setup()

def freq_tables():
    bigram_freq=FreqDist()
    unigram_freq=FreqDist()
    for codes in flattened:
        for token in tokenize(flattened[codes]["digest"]+flattened[codes]["headline"]):
            unigram_freq[token] += 1 
        
        for one, two in ngrams(tokenize(flattened[codes]["digest"]+flattened[codes]["headline"]), 2):
            bigram_freq[(one,two)] += 1
    bigrams=[i for i in bigram_freq.items()]
    bigrams.sort(key=lambda x: -x[1])
    return unigram_freq,bigrams
unigram_freq,bigrams=freq_tables()

