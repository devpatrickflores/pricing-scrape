import json
import difflib
import csv

def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def find_nearest_match(input_string, strings):
    closest_match = difflib.get_close_matches(input_string, strings, n=1)
    if closest_match:
        return closest_match[0]
    else:
        return None

bcf_data = load_json('bcf_rods_listing.json')
ana_data = load_json('ana_rods_listing.json')

bcf_strings = [item['BCF Description'] for item in bcf_data]
ana_strings = [item['ANA Description'] for item in ana_data]

nearest_matches = {}

for bcf_string in bcf_strings:
    nearest_match = find_nearest_match(bcf_string, ana_strings)
    nearest_matches[bcf_string] = nearest_match

# Write the results to a CSV file
with open('nearest_matches.csv', 'w', newline='') as csvfile:
    fieldnames = ['BCF Description', 'ANA Description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for bcf_string, nearest_match in nearest_matches.items():
        writer.writerow({'BCF Description': bcf_string, 'ANA Description': nearest_match})
