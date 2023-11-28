import requests
from lxml import html
import csv

# Headers to mimic a regular web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to extract text from a URL
def extract_text_from_url(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        xpath = '/html/body/main/center/div[1]/svg/text'
        elements = tree.xpath(xpath)
        if elements:
            return elements[0].text_content().strip()
        else:
            return "No text found at the specified XPath."
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

# Read URLs and names from CSV and process each

# Read URLs and names from CSV and process each
#with open('338ForMps.csv', newline='') as csvfile:
#    reader = csv.reader(csvfile)
#    for row in reader:
#        url, name = row
#        extracted_text = extract_text_from_url(url)
#        print(f"{name}: {extracted_text}")

# Optionally, you could store the results in a list or another CSV file.
