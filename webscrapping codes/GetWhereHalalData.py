from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

def scrape_wherehalal():
    # Setup Selenium with Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = "https://www.wherehalal.com/search"
    print(f"Fetching URL: {url}")  # Debug statement
    driver.get(url)
    
    # Open the CSV file in write mode initially to write the header
    csv_file = 'wherehalal_listings.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Address', 'Halal', 'Muslim Owned', 'Food Court', 'Mixed Food Court', 'Type of Food', 'Rating'])
        writer.writeheader()
    
    total_listings = 0
    processed_titles = set()

    while True:
        # Wait for the JavaScript to load content
        time.sleep(5)  # Adjust the sleep time if needed

        # Extract page source and pass to BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Finding all listings on the page
        listings = soup.find_all('div', class_='outlet')
        new_total_listings = len(listings)
        print(f"Number of listings found: {new_total_listings}")  # Debug statement

        if new_total_listings == total_listings:
            print("No new listings found. Ending scrape.")
            break
        
        total_listings = new_total_listings

        # Process and write each listing to the CSV file in real-time
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Address', 'Halal', 'Muslim Owned', 'Food Court', 'Mixed Food Court', 'Type of Food', 'Rating'])
            
            for listing in listings:
                title_element = listing.find('h5', class_='mb-1')
                title = title_element.text.strip() if title_element else 'N/A'
                
                # Skip if this title has already been processed
                if title in processed_titles:
                    continue
                
                processed_titles.add(title)
                
                address = listing.find('p', class_='mb-1 d-none d-md-block')
                categories = listing.find('p', class_='small mb-0')
                rating = listing.find('p', class_='mb-0 mt-1')

                categories_text = categories.text.strip() if categories else ''
                halal = 'Yes' if 'Halal Certified' in categories_text else 'No'
                muslim_owned = 'Yes' if 'Muslim Owned' in categories_text else 'No'
                food_court = 'Yes' if 'Food Court' in categories_text and 'Mixed Food Court' not in categories_text else 'No'
                mixed_food_court = 'Yes' if 'Mixed Food Court' in categories_text else 'No'

                # Filter to include only listings that are Food Court or Mixed Food Court
                if food_court == 'No' and mixed_food_court == 'No':
                    continue

                # Extract the type of food, excluding "Food Court" and "Mixed Food Court"
                type_of_food_list = categories_text.split('·')[2:] if '·' in categories_text else []
                type_of_food_list = [food.strip() for food in type_of_food_list if food.strip() not in ['Food Court', 'Mixed Food Court']]
                type_of_food = ', '.join(type_of_food_list)
                
                writer.writerow({
                    'Title': title,
                    'Address': address.text.strip() if address else 'N/A',
                    'Halal': halal,
                    'Muslim Owned': muslim_owned,
                    'Food Court': food_court,
                    'Mixed Food Court': mixed_food_court,
                    'Type of Food': type_of_food,
                    'Rating': rating.text.strip() if rating else 'N/A'
                })

        # Check for the "Load More" button and click it if it exists
        try:
            load_more_button = driver.find_element(By.ID, "loadMoreButton")
            driver.execute_script("arguments[0].click();", load_more_button)
        except Exception as e:
            print("No more pages to load.")
            break
    
    driver.quit()
    print(f"Data has been written to {csv_file}")

# Example usage
scrape_wherehalal()
