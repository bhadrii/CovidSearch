# CovidSearch
Config.py has the variables for frequency, path for storing the json, download URL and common helper functions for the other files. 

Setup.py takes care of the intial setting up consisting of:
1) Flattening the data
2) Cleaning the data
3) Calculating Idf for each keyword
4) Storing the bigram frequencies

search.py takes queries as arguments and returns a list of article codes best chosen for them.
In[4]: search("vaccine")
Out[4]: ['3R5w', '4n45', 'HtyW', 'ENkE', 'D5r9',...]

suggestions.py takes a query as arguments and returns a Dictionary of AUTO-COMPLETED QUERIES mapped to the suggestion words along with their weights.
In[5]: autocomplete("vaccine")
Out[5]: 
{'vaccine': [('candidates', 7),
  ('developed', 6),
  ('candidate', 5),
  ('covid19', 5),
  ('development', 4),
  ('alliance', 4),
  ('first', 4),
  ('manufacturer', 3),..}
