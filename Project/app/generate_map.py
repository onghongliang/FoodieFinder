import folium
import pandas as pd
import json

# Load the datasets
halal_file_path = 'Datasets/halal.csv'
mrt_file_path = 'Datasets/mrt.csv'
vegan_file_path = 'Datasets/veganRestaurant.csv'

# Read CSV files with specified encoding
halal_data = pd.read_csv(halal_file_path, encoding='latin1')
mrt_data = pd.read_csv(mrt_file_path, encoding='latin1')
vegan_data = pd.read_csv(vegan_file_path, encoding='latin1')

# Initialize the map centered around Singapore
map_center = [1.3521, 103.8198]
mymap = folium.Map(location=map_center, zoom_start=12)

# Add markers for halal locations
for idx, row in halal_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"<strong>{row['Title']}</strong><br>{row['Address']}<br>{row['Type of Food']}<br>{row['Rating']}",
        tooltip=row['Title'],
        icon=folium.Icon(color='blue', icon='cutlery', prefix='fa')  # Blue markers for halal locations
    ).add_to(mymap)

# Add markers for MRT stations
for idx, row in mrt_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"<strong>{row['STN_NAME']}</strong><br>{row['STN_NO']}",
        tooltip=row['STN_NAME'],
        icon=folium.Icon(color='red', icon='train', prefix='fa')  # Red markers for MRT stations
    ).add_to(mymap)

# Add markers for vegan restaurants
for idx, row in vegan_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"<strong>{row['Title']}</strong><br>{row['Address']}<br>{row['Type of Food']}<br>{row['Rating']}",
        tooltip=row['Title'],
        icon=folium.Icon(color='green', icon='leaf', prefix='fa')  # Green markers for vegan restaurants
    ).add_to(mymap)

# Save the map as an HTML file
mymap.save('app/static/map.html')

# Convert the datasets to JSON
halal_json = halal_data.to_json(orient='records')
mrt_json = mrt_data.to_json(orient='records')
vegan_json = vegan_data.to_json(orient='records')

# Save the JSON files
with open('app/static/halal.json', 'w') as f:
    f.write(halal_json)

with open('app/static/mrt.json', 'w') as f:
    f.write(mrt_json)

with open('app/static/vegan.json', 'w') as f:
    f.write(vegan_json)
