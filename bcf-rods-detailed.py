import os
import pandas as pd

# Define the path to the JSON file
json_file_path = 'bcf_rods_detailed.json'

# Check if the JSON file exists
if os.path.exists(json_file_path):
    # Load JSON file into pandas DataFrame
    df = pd.read_json(json_file_path)

    # Convert DataFrame to CSV
    df.to_csv('bcf_rods_detailed.csv', index=False)
else:
    print(f"The file '{json_file_path}' does not exist.")
