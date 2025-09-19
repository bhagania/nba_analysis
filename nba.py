
'''Performing Analysis using data for NBA Leagues and extract meaningful insights'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Using absolute path below to read the csv file
csv_list = ['/Users/chetanbhagania/PythonProjects/my_project/NBA_Sports_Analysis/nba_data_csv_files/Games.csv',
            '/Users/chetanbhagania/PythonProjects/my_project/NBA_Sports_Analysis/nba_data_csv_files/LeagueSchedule24_25.csv',
            '/Users/chetanbhagania/PythonProjects/my_project/NBA_Sports_Analysis/nba_data_csv_files/Players.csv',
            '/Users/chetanbhagania/PythonProjects/my_project/NBA_Sports_Analysis/nba_data_csv_files/PlayerStatistics.csv',
            '/Users/chetanbhagania/PythonProjects/my_project/NBA_Sports_Analysis/nba_data_csv_files/TeamHistories.csv',
            '/Users/chetanbhagania/PythonProjects/my_project/NBA_Sports_Analysis/nba_data_csv_files/TeamStatistics.csv']

# Creating a function to read all the files in list above


def csv_read(x):
    for csv in csv_list:
        df = pd.read_csv(csv_list[x])
        return df


# Checking any fo the missing values. .sum() at the end gives total of NULL values
csv_read(0).isnull().sum()

# ==============================================================================================
'''Starting off with Simple analysis (EDA) like:
1. How many matches were played?
2. How many venues the matched we played at? And where did most matches occur?
3. Which teams played?'''
# ==============================================================================================

# ==============================================================================================
# How many matches were played?
# ==============================================================================================
# Checking the columns from each file
csv_read(0).columns

# For total matches played in
csv_read(0).shape[0]
# Coversion of date to Datetime stamp
df['gameDate'] = pd.to_datetime(csv_read(0).gameDate)

min_year = df['gameDate'].min()
max_year = df['gameDate'].max()

'''Total games played between 1946 and 2025 were 71,829'''

# ==============================================================================================
# How many venues the matched we played at? And where did most matches occur?
# ==============================================================================================
venues = csv_read(0).hometeamCity.unique()
venues_count = csv_read(0).hometeamCity.value_counts()
venues_count.head(5)

'''Top 5 citis for matches were L.A., Boston, New York, Philly and Detroit'''

# ==============================================================================================
# Which teams played?
# ==============================================================================================
home_team = csv_read(0).hometeamName.unique()
away_team = csv_read(0).awayteamName.unique()

'''Particular Players Performance Analysis/ Player Statistics (Lebron James)'''

# Below is how you filter and return all columns for specific one you want...
df_players = csv_read(3)
df_lj = df_players[(df_players['firstName'].str.lower() ==
                    'lebron') & (df_players['lastName'].str.lower() == 'james')]

# Turning gameDate to datetime stamp
df_lj['gameDate'] = pd.to_datetime(csv_read(3).gameDate)

df_lj['gameDate'].min()  # 2003
df_lj['gameDate'].max()  # 2025
df_lj.value_counts('playerteamName')

# Most Games played in Cleveland Caveliers: 1071, Lakers: 526 and Heat: 412
df_lj.value_counts('playerteamName')
df_lj['threePointersMade'].unique()

len(df_lj[df_lj['threePointersMade'] == 1])

# ==============================================================================================
# Yearly Perfoming Analysis on field basket success rate (fired/ atempted * 100)
# ==============================================================================================
df_baskets = df_lj.groupby(df_lj['gameDate'].dt.year)[
    ['fieldGoalsAttempted', 'fieldGoalsMade']].sum()
df_baskets['success_ratio'] = (
    df_baskets['fieldGoalsMade']/df_baskets['fieldGoalsAttempted']) * 100

# Plotting Success Ratio over the years using below:
plt.figure(figsize=(10, 6))
plt.plot(df_baskets.index, df_baskets['success_ratio'], marker='o')
plt.title("LeBron's Field Goal Success Ratio Over Time")
plt.xlabel("Year")
plt.ylabel("Success Ratio (%)")
plt.grid(True)
plt.show()

'''Insight 1: Lebron's Peak performance was in years 2013 and 2017 with success rate of more than 54%
   Insight 2: Lebron showed a sharp increate in his performance from 2003 to 2013
   Insight 3: In the past 5 Years, Lebron's Success Rate for attempted baskets has been above 50%'''

df_points = df_lj[['points', 'threePointersMade', 'freeThrowsMade']]

# 1 point shots = free throws
df_points['one_points'] = df_points['freeThrowsMade']

# 3 point shots = 3 * number of 3-pointers made
df_points['three_points'] = df_points['threePointersMade'] * 3

# 2 point shots = total points - (1pt + 3pt contributions)
df_points['two_points'] = (
    df_points['points'] - (df_points['one_points'] + df_points['three_points'])
)

# DataFrame of points and Breakdowns
df_pts_total = df_points[[
    'points', 'one_points', 'two_points', 'three_points']]

# Pie chart showing breakdowns of the scores by 1, 2 and 3  pointers

totals = df_pts_total[['one_points',
                       'two_points', 'three_points']].sum()

plt.figure(figsize=(6, 6))
plt.pie(
    totals,
    labels=totals.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.title("Scoring Breakdown (1pt vs 2pt vs 3pt)")
plt.show()

'''Insight 4: Lebron is a good 'small forward' who has scored more than 50 % 2s in his whole career'''

# Below is the analysis of teams over past 15 years.

df_wins = csv_read(0)
df_wins['gameDate'] = pd.to_datetime(df_wins.gameDate)
df_team_wins = csv_read(0)[[
    'gameDate',
    'hometeamName',
    'hometeamId',
    'awayteamName',
    'awayteamId',
    'winner'
]]

# Check for winning team and return the name:

df_team_wins['winner_team'] = np.where(
    df_team_wins['winner'] == df_team_wins['hometeamId'],
    df_team_wins['hometeamName'], df_team_wins['awayteamName'])
df_team_wins['gameDate'] = pd.to_datetime(df_team_wins['gameDate'])
df_team_wins['year'] = df_team_wins['gameDate'].dt.year
win_counts = df_team_wins.groupby(
    ['year', 'winner_team']).size().reset_index(name='wins')
# From year 2003 to 2025... Finding the 'Win' frequency over the past 23 years'

win_counts_filt = win_counts.loc[win_counts.groupby(
    'year')['wins'].idxmax()].reset_index(drop=True)

# Plot to find frequent winning top team over the years
# %%
df_2015_2025 = win_counts_filt[(win_counts_filt['year'] >= 2015)]

plt.figure(figsize=(12, 6))
bars = plt.bar(df_2015_2025['year'], df_2015_2025['wins'])

# Add team names inside bars
for bar, team in zip(bars, df_2015_2025['winner_team']):
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height()/2,
        team,
        ha='center', va='center',
        fontsize=8, color='white', fontweight='bold'
    )

plt.xlabel("Year")
plt.ylabel("Win Frequency")
plt.title("Most Winning Team (2015–2025)")
plt.show()

# END
