
import nltk
from nltk.stem import PorterStemmer
#create an object of class PorterStemmer
porter = PorterStemmer()
SETUP_PATH="masterdata.json"
CUTOFF_FREQ=5
URL='https://covidwire.firebaseio.com/corpus.json'


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


