import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# URL of the page to scrape
url = 'https://fbref.com/en/squads/206d90db/2022-2023/Barcelona-Stats#all_matchlogs'

# Fetch the page
response = requests.get(url)
response.raise_for_status()  # This will raise an exception for HTTP errors

# Parse the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table by ID
table = soup.find('table', id='matchlogs_for')

# Extract the rows from the table
rows = table.find_all('tr')

# Create a list to hold all match data
matches = []

# Iterate over rows and collect data
for row in rows:
    # Include th for the first column (date) and td for the rest
    cols = row.find_all(['th', 'td'])
    if cols:
        match_data = {
            'date': cols[0].text.strip(),
            'start_time': cols[1].text.strip(),
            'comp': cols[2].text.strip(),
            'round': cols[3].text.strip(),
            'day_of_week': cols[4].text.strip(),
            'venue': cols[5].text.strip(),
            'result': cols[6].text.strip(),
            'goals_for': cols[7].text.strip(),
            'goals_against': cols[8].text.strip(),
            'opponent': cols[9].text.strip(),
            'xg_for': cols[10].text.strip(),
            'xg_against': cols[11].text.strip(),
            'possession': cols[12].text.strip(),
            'attendance': cols[13].text.strip(),
            'captain': cols[14].text.strip(),
            'formation': cols[15].text.strip(),
            'referee': cols[16].text.strip(),
            'notes': cols[17].text.strip() if len(cols) > 17 else ''
        }
        matches.append(match_data)

df = pd.DataFrame(matches)
df = df.drop(df.index[0]) # Removes the header row from the dataframe

print(df)

# Convert date to datetime and xG values to numeric
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['xg_for'] = pd.to_numeric(df['xg_for'], errors='coerce')
df['xg_against'] = pd.to_numeric(df['xg_against'], errors='coerce')

# Plot xG for and xG against over time
plt.figure(figsize=(14, 7))
plt.plot(df['date'], df['xg_for'], label='xG For', marker='o')
plt.plot(df['date'], df['xg_against'], label='xG Against', marker='o', color='red')
plt.title('Expected Goals For and Against Over Time')
plt.xlabel('Date')
plt.ylabel('Expected Goals')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Showing insights on the collected data

# Derive insights based on xG performances
# Group by opponent and calculate average xG for and xG against
grouped_data = df.groupby('opponent').agg({'xg_for': 'mean', 'xg_against': 'mean'}).reset_index()

# Finding worst Barca Offensive performance on average xG
poor_offensive_performance = grouped_data.loc[grouped_data['xg_for'].idxmin()]
# Finding worst Barca Defensive performance on average xG
poor_defensive_performance = grouped_data.loc[grouped_data['xg_against'].idxmax()]
# Finding best Barca Offensive performance on average xG
best_offensive_performance = grouped_data.loc[grouped_data['xg_for'].idxmax()]
# Finding best Barca Defensive performance on average xG
best_defensive_performance = grouped_data.loc[grouped_data['xg_against'].idxmin()]

# Print the insights on xG based barca performance
print('Worst Barca Offensive performance on average xG:')
print(poor_offensive_performance)
print()
print('Worst Barca Defensive performance on average xG:')
print(poor_defensive_performance)
print()
print('Best Barca Offensive performance on average xG:')
print(best_offensive_performance)
print()
print('Best Barca Defensive performance on average xG:')
print(best_defensive_performance)
print()

# Derive insights based on who the referee is and their results
# Group by referee and result
referee_results = df.groupby(['referee', 'result']).size().unstack(fill_value=0)

# Visualization
fig, ax = plt.subplots(figsize=(12, 8))
referee_results[['W', 'D', 'L']].plot(kind='bar', stacked=True, ax=ax)
ax.set_title('Results by Referee')
ax.set_xlabel('Referee')
ax.set_ylabel('Number of Matches')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Calculate the total matches officiated by each referee
referee_results['Total'] = referee_results.sum(axis=1)

# Calculate the percentage of W, D, L for each referee
referee_results['%W'] = referee_results['W'] / referee_results['Total'] * 100
referee_results['%D'] = referee_results['D'] / referee_results['Total'] * 100
referee_results['%L'] = referee_results['L'] / referee_results['Total'] * 100

# Identifying the referee with the highest win, draw, and loss percentage
max_win_referee = referee_results['%W'].idxmax()
max_draw_referee = referee_results['%D'].idxmax()
max_loss_referee = referee_results['%L'].idxmax()

# Print the results
print(f"Referee most associated with wins: {max_win_referee} with {referee_results.loc[max_win_referee, '%W']:.2f}% wins")
print()
print(f"Referee most associated with draws: {max_draw_referee} with {referee_results.loc[max_draw_referee, '%D']:.2f}% draws")
print()
print(f"Referee most associated with losses: {max_loss_referee} with {referee_results.loc[max_loss_referee, '%L']:.2f}% losses")
print()
print(f"I dont like {max_loss_referee}. He is a bad referee.")
print()

# Derive insights based on their goals for and against
df['goals_for'] = pd.to_numeric(df['goals_for'], errors='coerce')
df['goals_against'] = pd.to_numeric(df['goals_against'], errors='coerce')

# Calculate average goals for and against
average_goals_for = df['goals_for'].mean()
average_goals_against = df['goals_against'].mean()

print(f"Average Goals For: {average_goals_for:.2f}")
print(f"Average Goals Against: {average_goals_against:.2f}")

# Identify matches with the highest and lowest goals for and against
max_goals_for_match = df.loc[df['goals_for'].idxmax()]
min_goals_for_match = df.loc[df['goals_for'].idxmin()]
max_goals_against_match = df.loc[df['goals_against'].idxmax()]
min_goals_against_match = df.loc[df['goals_against'].idxmin()]

print("\nMatch with the highest goals for:")
print(max_goals_for_match)
print("\nMatch with the lowest goals for:")
print(min_goals_for_match)
print("\nMatch with the highest goals against:")
print(max_goals_against_match)
print("\nMatch with the lowest goals against:")
print(min_goals_against_match)

# Visualization
plt.figure(figsize=(14, 7))
# Plot goals for
plt.subplot(2, 1, 1)
plt.plot(df['date'], df['goals_for'], marker='o', linestyle='-')
plt.title('Goals For Over the Season')
plt.xlabel('Date')
plt.ylabel('Goals For')
# Plot goals against
plt.subplot(2, 1, 2)
plt.plot(df['date'], df['goals_against'], marker='o', linestyle='-', color='r')
plt.title('Goals Against Over the Season')
plt.xlabel('Date')
plt.ylabel('Goals Against')
plt.tight_layout()
plt.show()

# Calculate the difference between actual goals and xG
df['goals_vs_xg'] = df['goals_for'] - df['xg_for']
df['goals_against_vs_xg'] = df['goals_against'] - df['xg_against']

# Calculate average goals vs xG
average_goals_vs_xg = df['goals_vs_xg'].mean()
average_goals_against_vs_xg = df['goals_against_vs_xg'].mean()

print(f"Average Goals For vs xG: {average_goals_vs_xg:.2f}")
print(f"Average Goals Against vs xG: {average_goals_against_vs_xg:.2f}")

# Identify matches with significant over/underperformance
significant_overperforming_matches = df[df['goals_vs_xg'] > 1]
significant_underperforming_matches = df[df['goals_vs_xg'] < -1]

print("\nMatches where Barcelona significantly overperformed:")
print(significant_overperforming_matches[['date', 'opponent', 'goals_for', 'xg_for', 'goals_vs_xg']])

print("\nMatches where Barcelona significantly underperformed:")
print(significant_underperforming_matches[['date', 'opponent', 'goals_for', 'xg_for', 'goals_vs_xg']])

# Visualization
plt.figure(figsize=(14, 7))
# Plot actual goals vs xG
plt.plot(df['date'], df['goals_for'], marker='o', linestyle='-', label='Goals For')
plt.plot(df['date'], df['xg_for'], marker='o', linestyle='--', label='xG For')
plt.title('Goals For vs xG Over the Season')
plt.xlabel('Date')
plt.ylabel('Goals')
plt.legend()
plt.tight_layout()
plt.show()
plt.figure(figsize=(14, 7))
# Plot goals against vs xG
plt.plot(df['date'], df['goals_against'], marker='o', linestyle='-', color='r', label='Goals Against')
plt.plot(df['date'], df['xg_against'], marker='o', linestyle='--', color='orange', label='xG Against')
plt.title('Goals Against vs xG Against Over the Season')
plt.xlabel('Date')
plt.ylabel('Goals')
plt.legend()
plt.tight_layout()
plt.show()