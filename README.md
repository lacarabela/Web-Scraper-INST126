# Web Scraper (INST126 Final Project)
## Project Overview
This program fetches and processes soccer match data from a specified URL, performs various analyses, and generates visualizations. The primary goal is to analyze the performance of FC Barcelona in the 2022-2023 season, providing insights such as average goals scored, goals conceded, and the impact of referees on match outcomes. The proposal for this project was approved via email by Dr. Jackson.
## How to Run the Program
### Prerequisites
1. **Python:** Ensure you have Python installed on your machine. You can download it from python.org.
2. **Required Libraries:** Install the following Python libraries:
      - **requests**
      - **beautifulsoup4**
      - **pandas**
      - **matplotlib**

You can install these libraries using pip:
```
pip install requests beautifulsoup4 pandas matplotlib
```
## Running the Program
1. Clone or download the repository containing the **main.py** file.
2. Open a terminal or command prompt.
3. Navigate to the directory where **main.py** is located.
4. Run the program using the following command:
```
python main.py
```
The program will execute and print various analytical results to the console. Additionally, it will generate several plots and display them.
## Program Details
### Fetching Data
The program fetches data from the following URL:
```
url = 'https://fbref.com/en/squads/206d90db/2022-2023/Barcelona-Stats#all_matchlogs'
```
### Parsing Data
The HTML content of the page is parsed using BeautifulSoup, and match data is extracted from a table with the ID **matchlogs_for**. The data is then stored in a Pandas DataFrame.
### Processing Data
The data is cleaned and processed to ensure proper formatting. The processing includes:
- Converting date strings to datetime objects.
- Converting numerical data to appropriate data types.
- Handling missing or malformed data.
### Analysis Performed
The program performs the following analyses:
1. **Average Goals Calculation:** Computes the average goals scored and conceded per match.
2. **Extreme Matches Identification:** Finds matches with the highest and lowest goals scored and conceded.
3. **xG Analysis:** Calculates the differences between actual goals and expected goals (xG) and identifies significant overperforming and underperforming matches.
4. **Referee Impact Analysis:** Analyzes the impact of referees on match outcomes, identifying referees associated with the highest percentage of wins, draws, and losses.
### Visualizations
The program generates the following plots:
1. **Goals Over Time:** A line plot showing goals scored and conceded over time.
2. **xG For and Against:** A scatter plot comparing actual goals to expected goals.
3. **Goals vs xG:** A scatter plot highlighting significant overperforming and underperforming matches.
## Credits
- **BeautifulSoup:** Used for parsing HTML content.
- **Pandas:** Used for data manipulation and analysis.
- **Matplotlib:** Used for generating visualizations.
- **My classmate Mary Nguyen:** For her insights and help in reviewing the code.
## Acknowledgment
- Data sourced from FBRef.
