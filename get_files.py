import pandas as pd
import requests
from io import StringIO

# Initialize an empty list to hold all dataframes
dfs = []

# Function to fetch and process CSV data
def fetch_and_process(year, quarter):
    url = f"https://www.ourcommons.ca/ProactiveDisclosure/en/members/{year}/{quarter}/csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        response.encoding = 'utf-8'  # Explicitly set encoding to UTF-8
        raw_text = response.text

        try:
            csv_data = StringIO(raw_text)
            df = pd.read_csv(csv_data)

            # Add year and quarter columns
            df['Year'] = year
            df['Quarter'] = quarter

            # Append the modified dataframe to the list
            dfs.append(df)

            print(f"Successfully fetched and processed data for {year} Q{quarter}")
        except pd.errors.ParserError as e:
            print(f"Failed to parse CSV for {year} Q{quarter}. Error: {e}")
    else:
        print(f"Failed to fetch data for {year} Q{quarter}, Status Code: {response.status_code}")


for year in range(2021, 2024):
    start_quarter = 2 if year == 2021 else 1
    for quarter in range(start_quarter, 5):
        fetch_and_process(year, quarter)

if dfs:
    master_df = pd.concat(dfs, ignore_index=True)
    master_df.to_csv('master_commons.csv', index=False)
    print("Master CSV created: master_commons.csv")
else:
    print("No dataframes to concatenate. Master CSV not created.")
