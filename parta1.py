import pandas as pd
import argparse

# create the dataframe
covid_data = pd.read_csv("owid-covid-data.csv")

## 1

# first filter down to all the rows containing data from the year 2020
covid2020 = covid_data.loc[covid_data['date'].str.contains('2020')]

# now filter down to the columns that contain location, date, total_cases, new_cases, total_deaths and new_deaths
covid2020 = covid2020.loc[:,['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

# replace the date column with a month column
covid2020['date'] = covid2020['date'].str[5:7]
covid2020.columns = ['location', 'month', 'total_cases', 'new_cases', 'total_deaths','new_deaths']

# aggregate the values by month and location, making sure not to impute missing values when summing
monthlycovid2020 = covid2020.groupby(['location', 'month'], as_index = False).aggregate({'total_cases': max, 'new_cases': lambda x: x.sum(min_count=1), 'total_deaths': max, 'new_deaths':lambda x: x.sum(min_count=1)})

## 2

# add case_fatality_rate to the dataframe just after the month column, this is defined as the number of deaths per confirmed case in a given period
monthlycovid2020['case_fatality_rate'] = monthlycovid2020['total_deaths'] / monthlycovid2020['total_cases']

# reorder the columns to the order specified
cols = list(monthlycovid2020.columns)
monthlycovid2020 = monthlycovid2020[cols[0:2] + [cols[-1]] + cols[2:6]]

# print the first 5 rows of the dataframe to standard output
print(monthlycovid2020.head())

# save the dataframe as a csv file using the input from the command line and exclude the dataframe index
parser = argparse.ArgumentParser()
parser.add_argument('csvname', type=str)
args = parser.parse_args()
monthlycovid2020.to_csv(args.csvname, index=False)