import xml.etree.ElementTree as ET
import csv
import requests

# Fetch XML data from URL
response = requests.get('https://www.ourcommons.ca/Members/en/search/XML')
if response.status_code == 200:
    root = ET.fromstring(response.content)
    
    # Open a file for writing
    with open("constituencies.csv", "w", newline='') as csvfile:
        fieldnames = ['ConstituencyName', 'ConstituencyProvinceTerritoryName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through each 'MemberOfParliament' element in the XML
        for member in root.findall('MemberOfParliament'):
            constituency_name = member.find('ConstituencyName').text if member.find('ConstituencyName') is not None else ''
            province_territory_name = member.find('ConstituencyProvinceTerritoryName').text if member.find('ConstituencyProvinceTerritoryName') is not None else ''
            
            writer.writerow({'ConstituencyName': constituency_name, 'ConstituencyProvinceTerritoryName': province_territory_name})

    print("CSV file has been created!")
else:
    print(f"Failed to fetch XML data. Status Code: {response.status_code}")
