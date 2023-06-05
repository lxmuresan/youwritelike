import numpy as np
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer

import string
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

#obtain only body
def body(text):

    #split text - start : '*** START OF'
    beg=re.findall(r"\*\*\* START OF .+ \*\*\*", text)
    start = text.index(beg[0])

    #split text - end : '*** END OF'
    ending=re.findall(r"\*\*\* END OF .+ \*\*\*", text)
    end = text.index(ending[0])

    #extract only corpus of book
    corp=book[start:end]

    return corp


#general function to preprocess
def clean_body(corp, strip=True, lower=True, rem_num=True, rem_punct=True,
    token=True, lemm=True, stop_words=True):
    """
    strip : removes all the whitespaces at the beginning and the end of a string
    lower : lowercases every word
    rem_num : removes numbers
    rem_punct : removes punctuation
    token : tokenizes
    lemm : lemmatizes
    rem_stop_word : once tokenized, the function removes common stop words
    stop_words : remove stopwords from english AND french stopword lexicons
    """

    # Removing whitespaces
    if strip == True:
        corp = corp.strip()

    # Lowercasing
    if lower == True:
        corp = corp.lower()

    # Removing numbers
    if rem_num == True:
        corp = ''.join(char for char in corp if not char.isdigit())

    # Removing punctuation
    if rem_punct == True:
        for punctuation in string.punctuation:
            corp = corp.replace(punctuation, '')

    # Tokenizing
    if token == True:
        tokenized_corp = word_tokenize(corp)

    # Lemmatizing
    if lemm == True:
        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(word) for word in tokenized_corp]
        lemmed_corp = " ".join(lemmatized)

    # stop word removal
    if stop_words == True:
        stop_words_en = set(stopwords.words('english'))
        stop_words_fr = set(stopwords.words('french'))
        clean_corp=[]
        if lemm==True :
            clean_corp = [w for w in lemmed_corp if w not in stop_words_en
                                 and w not in stop_words_fr]
        else:
            clean_corp = [w for w in tokenized_corp if w not in stop_words_en
                                 and w not in stop_words_fr]


    return clean_corp

def preproc(clean_corp):
    pass #scale/vectorize/embed
