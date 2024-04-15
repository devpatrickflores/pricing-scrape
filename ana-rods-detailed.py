import json
import pandas as pd
import re

def load_json_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def extract_columns(data):
    columns = {}
    for entry in data:
        title = entry['Title']
        for key, value in entry.items():
            if key != 'Title':
                if title not in columns:
                    columns[title] = {}
                columns[title][key] = value
    return columns

def combine_titles(data):
    titles = [entry['Title'] for entry in data]
    return ' '.join(titles)

def remove_special_characters(text):
    # Remove special characters except for letters, numbers, and spaces
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def export_to_csv(df, filename):
    df.to_csv(filename)

if __name__ == "__main__":
    # Load JSON data
    data = load_json_data('ana_rods_detailed.json')

    # Extract columns based on the "Title" field
    columns = extract_columns(data)

    # Convert to DataFrame
    df = pd.DataFrame(columns).T

    # Clean column names
    df.columns = df.columns.map(remove_special_characters)

    # Export DataFrame to CSV
    csv_filename = 'ana_rods_detailed.csv'
    export_to_csv(df, csv_filename)

    # Output combined title and CSV filename
    combined_title = combine_titles(data)
    print("Combined Title:", combined_title)
    print("Cleaned CSV file exported successfully:", csv_filename)
