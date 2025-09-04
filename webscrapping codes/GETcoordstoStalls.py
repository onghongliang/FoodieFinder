
import pandas as pd
import requests

# Load the dataset
dataset_path = 'veganRestaurant.csv'  
df = pd.read_csv(dataset_path)

# Ensure the postal code column name matches your dataset
address_list = list(df['Postal_Code'])

def get_coordinates(address):
    try:
        req = requests.get(f'https://www.onemap.gov.sg/api/common/elastic/search?searchVal={address}&returnGeom=Y&getAddrDetails=Y&pageNum=1')
        results_dict = req.json()
        if len(results_dict['results']) > 0:
            return results_dict['results'][0]['LATITUDE'], results_dict['results'][0]['LONGITUDE']
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching coordinates for {address}: {e}")
        return None, None

coordinates_list = []
count = 0
failed_count = 0

for address in address_list:
    latitude, longitude = get_coordinates(address)
    if latitude and longitude:
        print(f'Extracting {count + 1} out of {len(address_list)} addresses')
        coordinates_list.append((latitude, longitude))
    else:
        print(f'Failed to extract {count + 1} out of {len(address_list)} addresses')
        failed_count += 1
        coordinates_list.append((None, None))
    count += 1

print('Total Number of Addresses With No Coordinates', failed_count)

# Create a DataFrame with the coordinates
df_coordinates = pd.DataFrame(coordinates_list, columns=['Latitude', 'Longitude'])

# Join the coordinates with the original DataFrame
df_combined = df.join(df_coordinates)

# Save the updated DataFrame to a new CSV file
df_combined.to_csv('/mnt/data/halalandmuslimowneddataset1(coords)_updated.csv', index=False)
