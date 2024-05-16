import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    return response.text

def parse_data(html):
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
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
    return df

def process_data(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['xg_for'] = pd.to_numeric(df['xg_for'], errors='coerce')
    df['xg_against'] = pd.to_numeric(df['xg_against'], errors='coerce')
    df['goals_for'] = pd.to_numeric(df['goals_for'], errors='coerce')
    df['goals_against'] = pd.to_numeric(df['goals_against'], errors='coerce')
    return df

def calculate_goal_averages(df):
    # Calculate average goals for and against
    average_goals_for = df['goals_for'].mean()
    average_goals_against = df['goals_against'].mean()
    return average_goals_for, average_goals_against

def find_extreme_matches(df):
    # Identify matches with the highest and lowest goals for and against
    max_goals_for_match = df.loc[df['goals_for'].idxmax()]
    min_goals_for_match = df.loc[df['goals_for'].idxmin()]
    max_goals_against_match = df.loc[df['goals_against'].idxmax()]
    min_goals_against_match = df.loc[df['goals_against'].idxmin()]
    return max_goals_for_match, min_goals_for_match, max_goals_against_match, min_goals_against_match

def plot_goals_over_time(df):
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

def calculate_xg_differences(df):
    # Calculate the difference between goals and xG
    df['goals_vs_xg'] = df['goals_for'] - df['xg_for']
    df['goals_against_vs_xg'] = df['goals_against'] - df['xg_against']
    # Calculate the average difference between goals and xG
    average_goals_vs_xg = df['goals_vs_xg'].mean()
    average_goals_against_vs_xg = df['goals_against_vs_xg'].mean()
    return average_goals_vs_xg, average_goals_against_vs_xg

def calculate_goals_vs_xg(df):
    # Identify matches with significant over/underperformance
    significant_overperforming_matches = df[df['goals_vs_xg'] > 1]
    significant_underperforming_matches = df[df['goals_vs_xg'] < -1]
    return significant_overperforming_matches, significant_underperforming_matches

def plot_goals_vs_xg(df):
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

def plot_xg_for_and_against(df):
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

def referee_impact(df):
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
    print(f"Referee most associated with draws: {max_draw_referee} with {referee_results.loc[max_draw_referee, '%D']:.2f}% draws")
    print(f"Referee most associated with losses: {max_loss_referee} with {referee_results.loc[max_loss_referee, '%L']:.2f}% losses")
    print(f"I dont like {max_loss_referee}. He is a bad referee.")

def main():
    # URL of the page to scrape
    url = 'https://fbref.com/en/squads/206d90db/2022-2023/Barcelona-Stats#all_matchlogs'
    html = fetch_data(url)
    df = parse_data(html)
    df = process_data(df)

    average_goals_for, average_goals_against = calculate_goal_averages(df)
    print(f"Average Goals For: {average_goals_for:.2f}")
    print(f"Average Goals Against: {average_goals_against:.2f}")
    
    max_goals_for_match, min_goals_for_match, max_goals_against_match, min_goals_against_match = find_extreme_matches(df)
    print("\nMatch with the highest goals for:")
    print(max_goals_for_match)
    print("\nMatch with the lowest goals for:")
    print(min_goals_for_match)
    print("\nMatch with the highest goals against:")
    print(max_goals_against_match)
    print("\nMatch with the lowest goals against:")
    print(min_goals_against_match)
    
    plot_goals_over_time(df)
    plot_xg_for_and_against(df)
    
    average_goals_vs_xg, average_goals_against_vs_xg = calculate_xg_differences(df)
    print(f"Average Goals For vs xG: {average_goals_vs_xg:.2f}")
    print(f"Average Goals Against vs xG: {average_goals_against_vs_xg:.2f}")
    
    significant_overperforming_matches, significant_underperforming_matches = calculate_goals_vs_xg(df)
    print("\nMatches where Barcelona significantly overperformed:")
    print(significant_overperforming_matches[['date', 'opponent', 'goals_for', 'xg_for', 'goals_vs_xg']])
    print("\nMatches where Barcelona significantly underperformed:")
    print(significant_underperforming_matches[['date', 'opponent', 'goals_for', 'xg_for', 'goals_vs_xg']])
    
    plot_goals_vs_xg(df)
    referee_impact(df)

main()

