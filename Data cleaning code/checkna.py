import pandas as pd
import os

# Define the dataset file name and path
dataset_folder = 'datasets'

#dataset_file = 'halal.csv'
#dataset_file = 'veganRestaurant.csv'
dataset_file = 'mrt.csv'

dataset_path = os.path.join(dataset_folder, dataset_file)

# Print a message indicating the reading of the dataset
print(f"Reading the dataset: {dataset_path}")

# Load your dataset
df = pd.read_csv(dataset_path)

# Check for empty fields (NaN values) in the entire dataset
empty_fields = df.isna()

# Check if there are any NaN values in the dataset
if empty_fields.any().any():
    print("The dataset contains empty fields.")
    
    # Find the columns that contain any NaN values
    columns_with_na = empty_fields.any()
    columns_with_na = columns_with_na[columns_with_na].index.tolist()
    print(f"Columns with NaN values: {columns_with_na}")
    
    # Find the rows that contain any NaN values
    rows_with_empty_fields = df[empty_fields.any(axis=1)]
    
    # Print the number of rows with empty fields
    num_rows_with_empty_fields = len(rows_with_empty_fields)
    print(f"Number of rows with empty fields: {num_rows_with_empty_fields}")
    
    # Optionally, print the rows with empty fields
    print("Rows with empty fields:")
    print(rows_with_empty_fields)
else:
    print("The dataset does not contain any empty fields.")
