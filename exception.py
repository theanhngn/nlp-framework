"""
Nathan Brito, Kelly Chen, Anh Nguyen, Tung Giang
DS3500 / A Reusable Extensible Framework for Natural Language Processing
Homework 3
Date Created: 2/15/2023 / Date Last Updated: 2/27/2023
"""

class Exception(Exception):
  """
    A class that inherits the Exception class
    
    Attributes:
        message: explanation of the errors
  """
  def __init__(self, message):
    self.message = message
    super().__init__("File is not found or read")
    

def ParserException(filename):
  """
    Anticipate possible errors to the file
    :param filename: (string) Name of the file
    :return: Errors (if any)
  """
  try:
    with open(filename, 'r') as f:
        contents = f.read()  
    return contents
    
  except Exception as e:
      raise Exception(filename, str(e))
      return None
  
