"""
Nathan Brito, Kelly Chen, Anh Nguyen, Tung Giang
DS3500 / A Reusable Extensible Framework for Natural Language Processing
Homework 3
Date Created: 2/15/2023 / Date Last Updated: 2/26/2023
"""

from textastic import Textastic


def main():
    # initialize frameworks
    tt = Textastic()

    # register some text files
    tt.load_text(filename="boston_25_mbta.txt", label="Boston 25 MBTA")
    tt.load_text(filename="boston_com_mbta.txt", label="Boston.com MBTA")
    tt.load_text(filename="boston_globe_mbta.txt", label="Boston Globe MBTA")
    tt.load_text(filename="WBUR_mbta.txt", label="WBUR MBTA")
    tt.load_text(filename="wcvb_mbta.txt", label="WCVB MBTA")

    # Load stop words
    tt.load_stop_words(stopfile="stopwords.txt")

    # Show visualizations
    
    # Display wordclouds
    tt.wordcloud()
    
    # Show Sankey diagram of the top 5 words for each file 
    tt.wordcount_sankey(k=5)
    
    # Show a Sankey diagram of specific words
    tt.wordcount_sankey(word_list=["mbta", "boston", "blue", "red", "green", "orange", "line", "silver", "train"])
    
    # Show sentiment bar chart
    tt.sentiment_bar()

# Run main
if __name__ == '__main__':
    main()
