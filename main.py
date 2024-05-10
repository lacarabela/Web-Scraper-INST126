import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the web page
url = 'https://en.wikipedia.org/wiki/2022%E2%80%9323_FC_Barcelona_season#La_Liga'

# Send a request to the web page
response = requests.get(url)
data = response.text

# parse the HTML
soup = BeautifulSoup(data, 'html.parser')

# Find the correct table based on the header "La Liga" which is an h3 element
la_liga_header = soup.find('span', {'id': 'La_Liga'}).parent

# Find the "Matches" table, which is the fourth h4 element after "La Liga"
matches_header = la_liga_header
for _ in range(4):
    matches_header = matches_header.find_next('h4')

# Find the table element
matches_table = matches_header.find_next('table')

# Check if the table is found
if matches_table:
    print("Table found.")
else:
    print("Table not found.")

# Extract the table data
matches = []
for row in matches_table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) > 5: 
        date = cols[0].get_text(strip=True)
        # Identify home and away teams
        home = cols[1].get_text(strip=True)
        away = cols[2].get_text(strip=True)
        score = cols[3].get_text(strip=True)
        if 'Barcelona' in home:
            opponent = away
            venue = 'home'
        else:
            opponent = home
            venue = 'away'
        matches.append([date,opponent, venue, score])

# Create a DataFrame
df = pd.DataFrame(matches, columns = ['Date', 'Opponent', 'Venue', 'Score'])

# save the DataFrame to a CSV file
df.to_csv('fc_barcelona_matches.csv', index=False)