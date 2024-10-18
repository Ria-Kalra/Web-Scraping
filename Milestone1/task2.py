from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Set up the Chrome WebDriver using WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the main page with state links
base_url = 'https://publiclibraries.com/state/'

# Navigate to the base URL
driver.get(base_url)
time.sleep(3)  # Wait for the page to load

# Parse the main page to get state URLs
soup = BeautifulSoup(driver.page_source, 'html.parser')
state_links = soup.find_all('a', href=True)

# Filter out state links
state_urls = {link.text.strip(): link['href'] for link in state_links if '/state/' in link['href']}

# Directory to store CSV files
output_directory = 'LibraryDataByState'
os.makedirs(output_directory, exist_ok=True)

# Loop through each state URL and extract library data
for state_name, state_url in state_urls.items():
    print(f"Scraping data for: {state_name}")
    driver.get(state_url)
    time.sleep(3)  # Wait for the page to load

    # Parse the state page with BeautifulSoup
    state_soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = state_soup.find('table')

    # Extract data from the table
    libraries = []
    if table:
        rows = table.find_all('tr')
        headers = [header.text.strip() for header in rows[0].find_all('th')]

        for row in rows[1:]:
            data = [cell.text.strip() for cell in row.find_all('td')]
            libraries.append(data)

        # Create a DataFrame and save it to a CSV file
        df = pd.DataFrame(libraries, columns=headers)
        csv_filename = os.path.join(output_directory, f"{state_name.replace(' ', '_')}_libraries.csv")
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to: {csv_filename}")

# Close the browser once done
driver.quit()
print("Scraping complete!")
