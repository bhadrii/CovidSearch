from setup import tokenize,bigrams

def suggest(query):
    suggestions=[]
    query=tokenize(query)[0]
    for items in bigrams:

        word1=items[0][0]
        word2=items[0][1]
        if query==word1:
            suggestions.append((word2,items[1]))
        
        
    
    return {query:suggestions}


            
