# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 22:41:25 2020

@author: bhadr
"""
path="mast.json"
CUTOFF_FREQ=5
URL='https://covidwire.firebaseio.com/corpus.json'
from urllib.request import urlretrieve
out=urlretrieve(URL, path)