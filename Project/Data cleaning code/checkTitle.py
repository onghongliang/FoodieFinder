import pandas as pd
import os
import re

# Define the dataset file name and path
dataset_folder = 'datasets'
#dataset_file = 'halal.csv'
dataset_file = 'veganRestaurant.csv'
dataset_path = os.path.join(dataset_folder, dataset_file)

# Print a message indicating the reading of the dataset
print(f"Reading the dataset: {dataset_path}")

# Load your dataset
df = pd.read_csv(dataset_path)

# Function to check if a string contains weird characters except '@', ',', or '.'
def contains_weird_characters(s):
    return bool(re.search(r'[^a-zA-Z0-9 @,.\'\-()/&$+!]', s))

# Apply the function to the 'restaurant_name' column and filter rows
weird_character_names = df[df['Title'].apply(contains_weird_characters)]

# Check if there are any rows with weird characters except '@', ',', or '.'
if not weird_character_names.empty:
    num_weird_characters = len(weird_character_names)
    print(f"Number of lines found: {num_weird_characters}")

    print("Rows with weird characters:")
    print(weird_character_names)
else:
    print("All restaurant names contain only alphanumeric characters, '@', ',', or '.'.")
