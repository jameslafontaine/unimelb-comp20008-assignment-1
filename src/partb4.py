## Part B Task 4
import re
import pandas as pd
import nltk
import os
import argparse

# set up the Porter Stemmer
from nltk.stem.porter import *
porterStemmer = PorterStemmer()

# handle command line input
parser = argparse.ArgumentParser()
parser.add_argument('keyword1', type=str)
parser.add_argument('keyword2', nargs='?', type=str)
parser.add_argument('keyword3', nargs='?', type=str)
parser.add_argument('keyword4', nargs='?', type=str)
parser.add_argument('keyword5', nargs='?', type=str)
args = parser.parse_args()

keywords = [args.keyword1.lower()]

if args.keyword2:
    keywords.append(args.keyword2.lower())
if args.keyword3:
    keywords.append(args.keyword3.lower())
if args.keyword4:
    keywords.append(args.keyword4.lower())
if args.keyword5:
    keywords.append(args.keyword5.lower())
    
# load in partb1.csv
docIDs = pd.read_csv('partb1.csv')

# go into the cricket folder if necessary 
if 'cricket' in os.listdir():
    os.chdir('cricket')

# preprocessing function
def preprocess(filename):
    # open and load the specified document for preprocessing
    f = open(filename, 'r')
    contents = f.read()
    f.close()
    
    # Remove all non-alphabetic characters except for spacing such as whitespaces, tabs and newlines
    contents = re.sub(r'[^A-Za-z\s]', '', contents)
    
    # Convert all spacing characters such as tabs and newlines to whitespace and ensure that only one whitespace character exists between each word
    contents = re.sub(r'[\s]+', ' ', contents)

    # Change all uppercase characters to lowercase
    contents = contents.lower()

    return contents

# check all the documents for keyword matches
matchIDs = []
for file in docIDs['filename']:
    preprocessed = preprocess(file)
    match = True
    wordList = nltk.word_tokenize(preprocessed)
    
    # create a list of stem words for every word in the document
    stemList = [porterStemmer.stem(word) for word in wordList]
    
    # check if all the keywords are in this document OR there are least inexact stem matches for each keyword in this document
    for keyword in keywords:
        if keyword not in wordList:
            if porterStemmer.stem(keyword) not in stemList:
                match = False
                break
    # if all the keywords were present then add the corresponding document ID to our matched IDs list        
    if match:
        matchIDs.append(docIDs.loc[docIDs['filename'] == file, 'documentID'].item())

# print the matched document IDs
print(matchIDs)
os.chdir('..')