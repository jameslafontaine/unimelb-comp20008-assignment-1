## Part B Task 1

import re
import pandas as pd
import os
import argparse

# handle command line input
parser = argparse.ArgumentParser()
parser.add_argument('csvname', type=str)
args = parser.parse_args()

# set the directory to the cricket folder
current_path = os.chdir('cricket')

# record the names of the all the txt files in the cricket directory
filenames = sorted([filename for filename in os.listdir(current_path) if '.txt' in filename])

# now locate and record document IDs of the txt files using regex
docIDs = []
for file in filenames:
    f = open(file, 'r')
    contents = f.read()
    docIDs.append(re.search(r'[A-Z]{4}-\d{3}[A-Z]?', contents).group(0))
    f.close()
    
# now create the dataframe and save it back into the assignment folder
doc_dataframe = pd.DataFrame({'filename': filenames, 'documentID': docIDs}, columns = ['filename', 'documentID'])
os.chdir('..')
doc_dataframe.to_csv(args.csvname, index=False)

