# Part B Task 2

import re
import os
import sys
import argparse

# handle command line input
parser = argparse.ArgumentParser()
parser.add_argument('docname', type=str)
args = parser.parse_args()

# remove 'cricket' from the command line input to get the exact file name
docname = args.docname[7:]

# go into the cricket folder and open and load the specified document for preprocessing
os.chdir('cricket')
f = open(docname, 'r')
contents = f.read()
f.close()

# function which performs the preprocessing
def preprocess(contents):
    
    # Remove all non-alphabetic characters except for spacing such as whitespaces, tabs and newlines
    contents = re.sub(r'[^A-Za-z\s]', '', contents)
    
    # Convert all spacing characters such as tabs and newlines to whitespace and ensure that only one whitespace character exists between each word
    contents = re.sub(r'[\s]+', ' ', contents)

    # Change all uppercase characters to lowercase
    contents = contents.lower()

    return contents

# print the preprocessing results to the standard output and change the directory back to the parent directory
print(preprocess(contents))
os.chdir('..')