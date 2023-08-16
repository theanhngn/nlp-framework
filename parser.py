"""
Nathan Brito, Kelly Chen, Anh Nguyen, Tung Giang
DS3500 / A Reusable Extensible Framework for Natural Language Processing
Homework 3
Date Created: 2/15/2023 / Date Last Updated: 2/27/2023
"""

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stopwords_list = set(stopwords.words("english"))
punctuations = """!()-![]{};:,+'",<>./?@#$%^&*_~Â""" # List of punctuation to remove

def text_parse(textfile):
    """
    Breaks down and cleans the whitespace of the text 
    :param textfile: (str) Name of the text file
    :return: parsedReview (str): A broken down version of the text 
    """
    # split the review into words
    splitReview = textfile.split()
    # take the stubborn punctuations out
    parsedReview = " ".join([word.translate(str.maketrans('', '', punctuations)) + " " for word in splitReview])

    return parsedReview

def text_clean(textfile):
    """
    Excludes stop words and lower cases each character from the text in textfile
    :param textfile: (str) Name of the text file
    :return: clean_review (str) A cleaned version of the text
    """
    # Create a list of clean words
    clean_words = []
    
    # Split text
    splitReview = textfile.split()
    
    # Check if each word is a word and not in the stopwords_list
    for w in splitReview:
        if w.isalpha() and w not in stopwords_list:
            clean_words.append(w.lower())
            
    # Join each word as a string seperated by space 
    clean_review = " ".join(clean_words)

    return clean_review
