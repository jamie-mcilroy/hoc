import csv

# Function to process and write to a new CSV file
def process_and_write_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            url = row[0]
            name_info = row[1].split(' (', 1)  # Split at the first occurrence of ' ('
            name = name_info[0].strip()
            info = f"({name_info[1]}" if len(name_info) > 1 else ""  # Add the opening bracket back if it was split
            writer.writerow([url, name, info])

# File paths
input_csv = '338ForMps.csv'
output_csv = '338ForMpsDetailed.csv'

# Process and write to the new CSV file
process_and_write_csv(input_csv, output_csv)

print(f"Processed data has been written to {output_csv}")
