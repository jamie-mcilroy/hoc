import csv
import mps
import get_cabinet

# Function to create a dictionary from 338ForMpsDetailed.csv
def create_mp_dictionary(file_path):
    mp_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            mp_name = row[1].strip()  # Name is in the second column
            mp_url = row[0].strip()  # URL is in the first column
            mp_dict[mp_name] = mp_url
    return mp_dict

# Function to read names from ministers.csv and categorize them into lists
def categorize_ministers(ministers_file, mp_dict):
    gain_list = []
    hold_list = []
    toss_up_list = []

    with open(ministers_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            full_name = f"{row[2].strip()} {row[3].strip()}"  # Combining first and last names
            url = mp_dict.get(full_name)
            if url:
                standing = get_cabinet.extract_text_from_url(url)
                if 'gain' in standing.lower():
                    gain_list.append(full_name)
                elif 'hold' in standing.lower():
                    hold_list.append(full_name)
                elif 'toss up' in standing.lower():
                    toss_up_list.append(full_name)

    return gain_list, hold_list, toss_up_list
def create_html_table(gain_list, hold_list, toss_up_list, output_file):
    # Sorting the lists alphabetically
    gain_list.sort()
    hold_list.sort()
    toss_up_list.sort()

    # HTML structure with escaped curly braces
    html_content = """
    <html>
    <head>
        <title>MP Categorization</title>
        <style>
            table, th, td {{
                border: 1px solid black;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 5px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>Gain</th>
                <th>Hold</th>
                <th>Toss Up</th>
            </tr>
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Converting lists to HTML list items
    gain_html = "<ul>" + "".join(f"<li>{name}</li>" for name in gain_list) + "</ul>"
    hold_html = "<ul>" + "".join(f"<li>{name}</li>" for name in hold_list) + "</ul>"
    toss_up_html = "<ul>" + "".join(f"<li>{name}</li>" for name in toss_up_list) + "</ul>"

    # Formatting the HTML content
    html_content = html_content.format(gain_html, hold_html, toss_up_html)

    # Writing to the output file
    with open(output_file, 'w') as file:
        file.write(html_content)
    print(f"HTML file '{output_file}' created successfully.")

# Path to the files
ministers_file = 'ministers.csv'
mps_file = '338ForMpsDetailed.csv'

# Create MP dictionary
mp_dict = create_mp_dictionary(mps_file)

# Categorize ministers
gain_list, hold_list, toss_up_list = categorize_ministers(ministers_file, mp_dict)

create_html_table(gain_list, hold_list, toss_up_list, 'mp_categorization.html')

# Print the lists
print("Gain:", gain_list)
print("Hold:", hold_list)
print("Toss Up:", toss_up_list)
