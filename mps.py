import csv

def normalize_apostrophe(s):
    return s.replace("’", "'")  # Replace curly apostrophes with straight ones

def create_mp_dictionary(file_path):
    mp_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            mp_name = normalize_apostrophe(row[1].strip())  # Normalize name
            mp_url = row[0].strip()
            mp_dict[mp_name] = mp_url
    return mp_dict

mp_dict = create_mp_dictionary('338ForMpsDetailed.csv')

def getUrl(name):
    normalized_name = normalize_apostrophe(name)  # Normalize input name
    return mp_dict.get(normalized_name, "No URL found")
