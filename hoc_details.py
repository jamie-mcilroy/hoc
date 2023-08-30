import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# Initialize an empty list to hold the logs
logs = []

# Function to fetch and save CSVs
def fetch_and_save_csv(uuid, category, name, riding, party, master_df):
    csv_url = f'https://www.ourcommons.ca/ProactiveDisclosure/en/members/{category}/{year}/{quarter}/{uuid}/csv'
    csv_response = requests.get(csv_url)

    if csv_response.status_code == 200:
        csv_response.encoding = 'utf-8'
        csv_text = csv_response.text
        csv_data = StringIO(csv_text)
        csv_df = pd.read_csv(csv_data)

        # Append additional columns
        csv_df['Name'] = name
        csv_df['Party'] = party
        csv_df['Riding'] = riding
        csv_df['Year'] = year
        csv_df['Quarter'] = quarter

        # Append this DataFrame to the master DataFrame
        master_df = pd.concat([master_df, csv_df], ignore_index=True)
        return master_df
    else:
        logs.append(f"Failed for {name} with URL: {csv_url}")
        return master_df

# Iterate over the range of years and quarters
for year in range(2021, 2024):
    for quarter in range(1, 5):
        # Skip Q1 2021 to start from Q2 2021
        if year == 2021 and quarter == 1:
            continue

        # Initialize an empty list to hold the rows and master DataFrames for each category
        data = []
        travel_master_df = pd.DataFrame()
        hospitality_master_df = pd.DataFrame()
        contract_master_df = pd.DataFrame()

        # Define the URL for the table page
        table_url = f'https://www.ourcommons.ca/ProactiveDisclosure/en/members/{year}/{quarter}'
        
        # Fetch and parse the main table
        response = requests.get(table_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr', {'class': 'expenses-main-info'})

            # Collect the main table data
            columns = ['Name', 'Riding', 'Party', 'Salary', 'Travel', 'Hospitality', 'Contracts', 'UUID']
            for row in rows:
                row_data = [td.text.strip() for td in row.find_all('td')]
                a_tag = row.find_all('td')[4].find('a', href=True)
                if a_tag:
                    href = a_tag['href']
                    uuid = href.split('/')[-1]
                    row_data.append(uuid)
                else:
                    row_data.append('N/A')
                data.append(row_data)

            df = pd.DataFrame(data, columns=columns)

            for _, row in df.iterrows():
                uuid = row['UUID']
                name = row['Name']
                riding = row['Riding']
                party = row['Party']

                if uuid != 'N/A':
                    travel_master_df = fetch_and_save_csv(uuid, 'travel', name, riding, party, travel_master_df)
                    hospitality_master_df = fetch_and_save_csv(uuid, 'hospitality', name, riding, party, hospitality_master_df)
                    contract_master_df = fetch_and_save_csv(uuid, 'contract', name, riding, party, contract_master_df)

            # Save the master DataFrames to CSV
            travel_master_df.to_csv(f"{year}_Q{quarter}_travel.csv", index=False, encoding='utf-8')
            hospitality_master_df.to_csv(f"{year}_Q{quarter}_hospitality.csv", index=False, encoding='utf-8')
            contract_master_df.to_csv(f"{year}_Q{quarter}_contract.csv", index=False, encoding='utf-8')

            # Log the failures, if any
            with open(f"{year}_Q{quarter}_log.txt", 'w') as log_file:
                for log in logs:
                    log_file.write(log + '\n')
        else:
            print(f"Failed to fetch the main table for {year} Q{quarter}")
