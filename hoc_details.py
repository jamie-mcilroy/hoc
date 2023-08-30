import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# Function to fetch and save the CSV
def fetch_and_save_csv(uuid, category, name, year, quarter):
    csv_url = f'https://www.ourcommons.ca/ProactiveDisclosure/en/members/{category}/{year}/{quarter}/{uuid}/csv'
    csv_response = requests.get(csv_url)
    csv_response.encoding = 'utf-8'  # Explicitly set encoding to UTF-8

    if csv_response.status_code == 200:
        csv_text = csv_response.text.split('\n', 1)[1]  # Skip the first line
        
        # Create folders if they do not exist
        folder_path = f"./{year}/{quarter}/{category}"
        os.makedirs(folder_path, exist_ok=True)

        # Sanitize the name and create the full file path
        safe_name = name.replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_")
        file_name = f"{safe_name}_{year}_{quarter}_{category}.csv"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "wb") as f:
            f.write(csv_text.encode('utf-8'))

        print(f"Successfully downloaded {category} CSV for {name} with UUID: {uuid} in {year}, {quarter}")

    else:
        print(f"Failed to download {category} CSV for {name} with UUID: {uuid} in {year}, {quarter}. URL: {csv_url}")

# Start at Q2 2021
start_year = 2021
start_quarter = 2

# End at Q4 2023
end_year = 2023
end_quarter = 4

# Iterate through the years and quarters
for year in range(start_year, end_year + 1):
    for quarter in range(start_quarter if year == start_year else 1, end_quarter + 1 if year == end_year else 5):
        # Replace the URL with the correct year and quarter
        table_url = f'https://www.ourcommons.ca/ProactiveDisclosure/en/members/{year}/{quarter}'

        response = requests.get(table_url)
        if response.status_code != 200:
            print(f"Failed to fetch data for {year}, {quarter}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr', {'class': 'expenses-main-info'})

        data = []
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
        
        # Download the CSVs
        for _, row in df.iterrows():
            uuid = row['UUID']
            name = row['Name']
            
            if uuid != 'N/A':
                for category in ['travel', 'hospitality', 'contract']:
                    fetch_and_save_csv(uuid, category, name, year, quarter)
