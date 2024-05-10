import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    cols = row.find_all('td')
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

# Output or process the scraped data
print(matches)