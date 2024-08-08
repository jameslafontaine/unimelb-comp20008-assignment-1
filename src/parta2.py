import pandas as pd
import argparse
import matplotlib.pyplot as plt

# handle command line input
parser = argparse.ArgumentParser()
parser.add_argument('pngname1', type=str)
parser.add_argument('pngname2', type=str)
args = parser.parse_args()

## 1

# load in the original data set
covid_data = pd.read_csv("owid-covid-data.csv")

# filter down to all the rows containing data from the year 2020
covid2020 = covid_data.loc[covid_data['date'].str.contains('2020')]

# group the data into the 2020 annual data for each location
covid2020 = covid2020.groupby('location', as_index = False).aggregate({'total_cases': max, 'new_cases': lambda x: x.sum(min_count=1), 
                                                                                         'total_deaths': max, 'new_deaths': lambda x: x.sum(min_count=1)})
# calculate the annual case_fatality_rate 
covid2020['case_fatality_rate'] = covid2020['new_deaths'] / covid2020['new_cases']

# plot a scatter plot comparing case fatality rate vs the confirmed new cases in 2020 for each location
plt.scatter(covid2020['new_cases'], covid2020['case_fatality_rate'], s=15)
plt.ylabel("case fatality rate")
plt.xlabel("new cases")
plt.title("Case fatality rate vs Confirmed new COVID-19 cases in 2020")
plt.grid(True)

# save the plot as a png file using the input from the command line
plt.savefig(args.pngname1)

## 2

# impute missing values by replacing them with 0
covid2020.fillna(0, inplace=True)

# plot the same scatter plot but this time using a log scale on the x axis
plt.scatter(covid2020['new_cases'], covid2020['case_fatality_rate'], s=15)
plt.xscale('log')
plt.ylabel("case fatality rate")
plt.xlabel("new cases (log scale)")
plt.title("Case fatality rate vs Confirmed new COVID-19 cases in 2020")
plt.grid(True)  

# save the plot as a png file using the input from the command line
plt.savefig(args.pngname2)