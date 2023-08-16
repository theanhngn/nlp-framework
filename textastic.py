"""
Core framework class for NLP Comparative Analysis
Nathan Brito, Kelly Chen, Anh Nguyen, Tung Giang
DS3500 / A Reusable Extensible Framework for Natural Language Processing
Homework 3
Date Created: 2/15/2023 / Date Last Updated: 2/27/2023
"""
from nltk.corpus import stopwords
from collections import defaultdict
from parser import text_parse, text_clean
from sankey import make_sankey
from exception import ParserException
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from afinn import Afinn


class Textastic:
    def __init__(self):
        # manage data about the different texts that
        # we register with the framework
        self.text_data = defaultdict(dict)
        self.stop_words = set()
        self.file_contents = {}

    def load_text(self, filename, label=None):
        """
        Register a document with the framework
        :param filename: (str) Name of the file
        :param label: (str) Label of the file contents
        """
        # Check if user did not input a label
        # if so, make label the file name
        if label is None:
            label = filename

        # Open file
        with open(filename, "r", encoding='utf8', errors="ignore") as f:
            # Read and get contents and save into file_contents dict
            contents = f.read()
            self.file_contents[label] = text_parse(contents)
            
            # Save word count into text data dict
            self.text_data["word_count"][label] = len(self.file_contents[label].split())

            # Save afinn sentiment score into text data dict
            afinn = Afinn()
            self.text_data["sentiment_score"][label] = afinn.score(self.file_contents[label])


    def load_stop_words(self, stopfile=""):
        """
        Loads the stop words
        :param stopfile: Name of the file with the list of stop words
        """
        # inititalize stop_words set in class as stopwords from nltk.corpus
        self.stop_words = set(stopwords.words("english"))
        
        # Check if user inputted a stopfile 
        if stopfile != "":
            # Open stopfile
            with open(stopfile, "r") as stop_f:
                # Read words from stopfile and insert to the stop_words set
                stop_f_words = stop_f.read()
                stop_f_words = text_parse(stop_f_words)
                stop_f_words = set(stop_f_words.split())
                self.stop_words.update(stop_f_words)

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Creates a Sankey diagram for either word_list that the user chooses OR top k words for each file combined
        :param word_list: (list) List of words included the Sankey diagram
        :param k: (int) Number of top words per file
        """
        
        # Initialize an empty dataframe for word count 
        word_count_df = pd.DataFrame()
        
        # Loop through each label and their text 
        for label, text in self.file_contents.items():
            # initalize text and split into a list 
            text = text_clean(text).split()
            
            # Find the word count and make the word count into a pandas series
            word_count_series = pd.Series(text).value_counts()
            
            # Insert word_count_series into count_df and reset index 
            count_df = word_count_series.to_frame()
            count_df = count_df.reset_index()
            
            # Name columns for word and count 
            count_df.columns = ['word', 'count']
            
            # Create a new column for the label that the words came form 
            count_df = count_df.assign(label=label)
            
            # Concatenate count_df into word_count_df 
            word_count_df = pd.concat([word_count_df, count_df])
        
        # Reassign order of columns 
        word_count_df = word_count_df[["label", "word", "count"]]
        
        # Exclude words that in the stop_words set 
        word_count_df = word_count_df[~word_count_df["word"].isin(self.stop_words)]
        
        # Convert all values in word column into a string
        word_count_df['word'] = word_count_df["word"].astype(str)

        # Initialize word_sankey from function make_sankey 
        word_sankey = make_sankey(df=word_count_df,
                                  src="label",
                                  targ="word",
                                  vals="count",
                                  word_list=word_list,
                                  k=k)
        # Display word_sankey
        word_sankey.show()

    def wordcloud(self):
        """
        Takes a dictionary and subplots with word clouds for each key-value pair.
        """
        # Initialize the subplots 
        fig, axs = plt.subplots(1, len(self.file_contents), figsize=(20, 10))
        
        for i, (key, value) in enumerate(self.file_contents.items()):
            # Join all the values of the current key into a single string
            text = ''.join(value)

            # Create the wordcloud for the current key-value pair
            wc = WordCloud(stopwords=self.stop_words, background_color='white').generate(text)

            # Add the wordcloud to the subplot
            axs[i].imshow(wc, interpolation='bilinear')
            axs[i].set_title(key)
            axs[i].axis('off')
        # Show wordclouds 
        plt.show()

    def sentiment_bar(self):
        """
        Creates and shows a bar chart showing the sentiment score for each text
        """
        # Create a dataframe for the sentiment score of each text
        df_scores = pd.DataFrame(self.text_data["sentiment_score"].items(), columns=["label", "sentiment_score"])
        
        # Sort scores by descending order 
        df_scores.sort_values("sentiment_score", ascending=False, inplace=True)
        
        # Create and show plotly.express bar chart
        sentiment_bar = px.bar(data_frame=df_scores, x="label", y="sentiment_score", title="Sentiment Score by Text")
        sentiment_bar.show()
