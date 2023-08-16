"""
sankey.py: A reusable library for sankey visualizations
Nathan Brito, Kelly Chen, Anh Nguyen, Tung Giang
DS3500 / A Reusable Extensible Framework for Natural Language Processing
Homework 3
Date Created: 2/15/2023 / Date Last Updated: 2/27/2023
"""


import plotly.graph_objects as go


def filter_top_words(df, k):
    """
    Filters the k most common words in each text 
    :param df: (int) this is what parameter 1 is
    :param k: (int) Number of common words
    :return: (df) An edited dataframe that includes the top k common words in each text 
    """
    # Create top_words_set 
    top_words_set = set()
    
    # Create a list of labels 
    labels_list = list(df["label"])
    
    # Go through each label/text and extract the top k words for each text and update top_words_set
    for label in labels_list:
        df_temp = df[df["label"] == label]
        df_temp = df_temp.sort_values("count", ascending=False)[:k]
        word_set = set(df_temp["word"])
        top_words_set.update(word_set)
        
    # Extract words that are in top_words_set
    df = df[df["word"].isin(top_words_set)]
    return df


def _code_mapping(df, src, targ):
  """
  Map the labels with the codes
  :param df (DataFrame): The dataframe
  :param src: (df) The source nodes of the Sankey diagram
  :param targ: (df) The target nodes of the Sankey diagram
  :return: The DataFrame (df) and the labels 
  """
  # Get distinct labels
  labels = sorted(list(set(list(df[src]) + list(df[targ]))))

  # Get integer codes
  codes = list(range(len(labels)))

  # Create label to code mapping
  lc_map = dict(zip(labels, codes))

  # Substitute names for codes in dataframe
  df = df.replace({src: lc_map, targ: lc_map})

  return df, labels


def make_sankey(df, src, targ, vals, word_list, k, **kwargs):
    """ Create a sankey diagram linking src values to
    target values with thickness vals
    Args:
        df (pd.DataFrame): Unfiltered artist_df dataframe
        columns (list): List of columns for the Sankey diagram
        vals (None/str): Name of the column where the values are for the Sankey diagram (str)
    """
    # Check if user called a word_list
    if word_list == None:
        # Look for top k words for each file 
        df = filter_top_words(df=df, k=k)
        
    # Else look for words from word_list
    else:
        df = df[df["word"].isin(word_list)]

    # Replace source and target values with int values in df_sankey and get labels for df_sankey
    df_sankey, labels = _code_mapping(df=df, src=src, targ=targ)

    # Check if values is valid
    if vals:
        vals = df_sankey.loc[:, vals]
    else:
        vals = [1] * len(df_sankey)

    # Initialize link, pad, and node for Sankey diagram
    link = {
        "source": df_sankey[src],
        "target": df_sankey[targ],
        "value": vals
    }
    pad = kwargs.get("pad", 50)
    node = {"label": labels, "pad": pad}

    # Initialize and return Sankey diagram
    sk = go.Sankey(valueformat=".0f", link=link, node=node)
    fig = go.Figure(sk)
    return fig
