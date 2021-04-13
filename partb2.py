# Part B Task 2

import re
import os
import argparse

# handle command line input
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
args = parser.parse_args()
    
if '/' in args.filename:
    # remove 'cricket/' from the command line input to get the exact file name
    docname = args.filename[8:]
elif 'cricket' in args.filename:
    # remove 'cricket' from the command line input to get the exact file name
    docname = args.filename[7:]
else:
    # we will assume that the file name has been directly input
    docname = args.filename
    
# go into the cricket folder if necessary 
if 'cricket' in os.listdir():
    os.chdir('cricket')
    
# function which performs the preprocessing
def preprocess(docname):
    # open and load the specified document for preprocessing
    f = open(docname, 'r')
    contents = f.read()
    f.close()
  
    # Remove all non-alphabetic characters except for spacing such as whitespaces, tabs and newlines
    contents = re.sub(r'[^A-Za-z\s]', '', contents)
    
    # Convert all spacing characters such as tabs and newlines to whitespace and ensure that only one whitespace character exists between each word
    contents = re.sub(r'[\s]+', ' ', contents)

    # Change all uppercase characters to lowercase
    contents = contents.lower()

    return contents

# print the preprocessing results to the standard output and change the directory back to the parent directory
print(preprocess(docname))
os.chdir('..')