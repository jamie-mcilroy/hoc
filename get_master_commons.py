import pandas as pd
import requests
from io import StringIO

# Initialize an empty list to hold all dataframes
dfs = []

# Function to determine Start Date and End Date based on Year and Quarter
def calculate_dates(row):
    year = row['Year']
    quarter = row['Quarter']

    if quarter == 1:
        return pd.Series([f"{year-1}-04-01", f"{year-1}-06-30"])
    elif quarter == 2:
        return pd.Series([f"{year-1}-07-01", f"{year-1}-09-30"])
    elif quarter == 3:
        return pd.Series([f"{year-1}-10-01", f"{year-1}-12-31"])
    elif quarter == 4:
        return pd.Series([f"{year}-01-01", f"{year}-03-31"])

def reverse_name(name):
    parts = name.split(', ')
    if len(parts) == 2:
        last, first = parts
        return f"{first} {last}"
    else:
        return name  # If the name can't be split into two, return it as is


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

            # Reverse the 'Name' column
            df['Name'] = df['Name'].apply(reverse_name)

            # Add year and quarter columns
            df['Year'] = year
            df['Quarter'] = quarter

            # Add Quarter-Year column
            df['Quarter-Year'] = df['Quarter'].astype(str) + "-" + df['Year'].astype(str)

            # Add Start Date and End Date columns
            df[['Start Date', 'End Date']] = df.apply(calculate_dates, axis=1)

            # Append the modified dataframe to the list
            dfs.append(df)

            print(f"Successfully fetched and processed data for {year} Q{quarter}")
        except pd.errors.ParserError as e:
            print(f"Failed to parse CSV for {year} Q{quarter}. Error: {e}")
    else:
        print(f"Failed to fetch data for {year} Q{quarter}, Status Code: {response.status_code}")

# Loop to fetch and process data for each year and quarter
for year in range(2021, 2024):
    start_quarter = 2 if year == 2021 else 1
    for quarter in range(start_quarter, 5):
        fetch_and_process(year, quarter)

# Combine all the dataframes
if dfs:
    master_df = pd.concat(dfs, ignore_index=True)
    master_df.to_csv('master_commons_index.csv', index=False)
    print("Master CSV created: master_commons_index.csv")
else:
    print("No dataframes to concatenate. Master CSV not created.")
