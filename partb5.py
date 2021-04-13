## Part B Task 5
import re
import pandas as pd
import nltk
import os
import argparse
import math

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
completeStemList = []
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
        # add all the stems of words in all matched document to a list
        for word in stemList:
            if word not in completeStemList:
                completeStemList.append(word)
                
# create a dataframe to track term frequency of each word with all stemmed words in matched documents and docIDs as columns
term_freq = pd.DataFrame(completeStemList, columns=['words'])

# create a series with words as indices to track the doc_freq of each term and thus calculate the idf of each term
doc_freq = pd.Series(0, completeStemList)

for ID in matchIDs:
    term_freq[ID] = 0
    preprocessed = preprocess(docIDs.loc[docIDs['documentID'] == ID, 'filename'].item())
    
    wordList = nltk.word_tokenize(preprocessed)
    
    # create a list of stem words for every word in the document
    stemList = [porterStemmer.stem(word) for word in wordList]
    
    # record the unique stem term frequencies for this matched document
    for word in stemList:
        term_freq.loc[term_freq['words'] == word, ID] += 1
    
    # add 1 to the doc_freq for each unique stem if it appears in this document
    for word in completeStemList:
        if word in stemList:
            doc_freq.loc[word] += 1
        
# now use the doc_freq of each term to calculate the IDF of each term
IDF = pd.Series(0, completeStemList)
for word in completeStemList:
    IDF.loc[word] = math.log((1+len(matchIDs))/(1 + doc_freq.loc[word])) + 1

# now calculate the TF-IDF of each term in each matched document
TF_IDF = pd.DataFrame(completeStemList, columns=['words'])
for ID in matchIDs:
    TF_IDF[ID] = 0
    TF_IDF[ID] = (term_freq.loc[:, ID] * list(IDF.values)) 
        
    # now normalise each TF-IDF
    TF_IDF[ID] = TF_IDF[ID] / math.sqrt(sum(list(TF_IDF[ID] * TF_IDF[ID])))

# calculate the dot product of the TF-IDF and the normalised query vector (the keywords)
cos_sim = pd.DataFrame(matchIDs, columns = ['documentID'])
cos_sim['score'] = 0
for ID in matchIDs:
    dot_product = 0
    for keyword in keywords:
        dot_product += TF_IDF.loc[TF_IDF['words'] == porterStemmer.stem(keyword), ID].item() * (1/math.sqrt(len(keywords)))
        
    cos_sim.loc[cos_sim['documentID'] == ID, 'score'] = round(dot_product, 4)

# print the results
print(cos_sim.to_string(index=False))

# return to the parent directory
os.chdir('..')
