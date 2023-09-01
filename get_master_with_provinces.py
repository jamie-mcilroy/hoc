import pandas as pd

# Define mapping of province names to abbreviations
province_to_abbreviation = {
    'Alberta': 'AB',
    'British Columbia': 'BC',
    'Manitoba': 'MB',
    'New Brunswick': 'NB',
    'Newfoundland and Labrador': 'NL',
    'Nova Scotia': 'NS',
    'Ontario': 'ON',
    'Prince Edward Island': 'PE',
    'Quebec': 'QC',
    'Saskatchewan': 'SK',
    'Yukon': 'YT',
    'Northwest Territories': 'NT',
    'Nunavut': 'NU'
}

# Read master_commons_index.csv into a DataFrame
master_df = pd.read_csv('master_commons_index.csv')

# Read constituencies.csv into a DataFrame
constituencies_df = pd.read_csv('constituencies.csv')

# Merge the two DataFrames based on the 'Constituency' and 'ConstituencyName' columns
merged_df = pd.merge(master_df, constituencies_df, left_on='Constituency', right_on='ConstituencyName', how='left')

# Drop the 'ConstituencyName' column as it's redundant
merged_df.drop('ConstituencyName', axis=1, inplace=True)

# Create the new column based on the province abbreviation
merged_df['ISO3166-2'] = merged_df['ConstituencyProvinceTerritoryName'].map(province_to_abbreviation).fillna('')
merged_df['ISO3166-2'] = 'CA-' + merged_df['ISO3166-2']

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('master_commons_index_with_provinces_and_ISO.csv', index=False)

print("Merged CSV created: master_commons_index_with_provinces_and_ISO.csv")
