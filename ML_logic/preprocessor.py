import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
import re
from nltk import download
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
download('stopwords')
download('punkt')
download('wordnet')
download('omw-1.4')
#general function to preprocess
def body(text):
    """
    Obtain body of book obtained with Gutendex
    """
    result = re.findall(r'\*\*\* START OF .+ \*\*\*(.*?)\*\*\* END OF .+ \*\*\*', text, flags=re.DOTALL)
    if result:
        body = result[0].strip()
    else:
        body="No match found."
    return body
# function to clean body obtained
def clean_body(body, strip=True, lower=False, rem_num=False, rem_punct=False,
    token=False, stop_words=False, lemm=False):
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
    # CLEAN BODY
    # Removing whitespaces
    if strip == True:
        body = body.strip()
    # Lowercasing
    if lower == True:
        body = body.lower()
    # Removing numbers
    if rem_num == True:
        body = ''.join(char for char in body if not char.isdigit())
    # Removing punctuation
    if rem_punct == True:
        for punctuation in string.punctuation:
            body = body.replace(punctuation, '')
    # Tokenizing
    if token == True:
        tokenized_body = word_tokenize(body)
    # stop word removal
    if stop_words == True:
        stop_words_en = set(stopwords.words('english'))
        stop_words_fr = set(stopwords.words('french'))
        sw_body=[]
        if token==True :
            sw_body = [w for w in tokenized_body if w not in stop_words_en
                                 and w not in stop_words_fr]
    # Lemmatizing
    if lemm == True:
        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(word) for word in tokenized_body]
        lemm_body = " ".join(lemmatized)
    if stop_words == True:
        return sw_body
    elif lemm == True:
        return lemm_body
    elif token == True:
        return tokenized_body
    else:
        return body
