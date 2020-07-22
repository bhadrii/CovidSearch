# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:07:14 2020

@author: bhadr
"""

import json
read_file=open("cw_data.json",encoding="utf8")
data=json.load(read_file)
#%%
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
histogram=dict() 
for codes in flattened:
    digest = flattened[codes]["digest"].split()
    headline=flattened[codes]["headline"].split()
    combined=digest+headline
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    
    for word in combined:
        for x in word: 
            if x in punctuations: 
                word = word.replace(x, "")
        word=word.lower()
        if word not in histogram:
            histogram[word]={codes}
        else:
            histogram[word].add(codes)
            
#%%
import nltk
from nltk.corpus import stopwords
common=stopwords.words('english')
for words in common:
    histogram.pop(words,None)

#%%
for words in histogram:
    histogram[words]=list(histogram[words])

#%%
with open("sample.json", "w") as outfile:  
    json.dump(histogram, outfile)
