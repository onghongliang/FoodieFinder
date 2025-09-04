import pandas as pd

# Load the CSV file
file_path = 'Datasets\halal.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Function to extract numerical rating and number of reviews
def extract_rating_and_reviews(rating_str):
    if pd.isna(rating_str):
        return pd.Series(["No Rating", "No Reviews"])
    try:
        rating_part, reviews_part = rating_str.split(' (')
        rating = float(rating_part.split('/')[0])
        reviews = int(reviews_part.replace(' reviews)', ''))
        return pd.Series([rating, reviews])
    except Exception as e:
        print(f"Error parsing: {rating_str} - {e}")
        return pd.Series(["No Rating", "No Reviews"])

# Apply the function to the Rating column
df[['Ratings', 'Review']] = df['Rating'].apply(extract_rating_and_reviews)

# Fill in "No Rating" and "No Reviews" for missing values
df['Ratings'] = df['Ratings'].replace({None: "No Rating"})
df['Review'] = df['Review'].replace({None: "No Reviews"})

# Remove the old Rating column
df = df.drop(columns=['Rating'])

# Save the updated dataframe to a new CSV file
df.to_csv('Datasets/halal_with_seperate_ratings_and_reviews.csv', index=False)  # Replace with your desired output file path

# Display the updated dataframe
print(df.head())
