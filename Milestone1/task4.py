from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options (optional)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start maximized (optional)
# chrome_options.add_argument("--headless")  # Uncomment this for headless mode (optional)

# Set up the Chrome WebDriver using WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the main page
base_url = 'https://directory.wigan.gov.uk/kb5/wigan/fsd/results.page?healthchannel=6&sr='
total_records = 287
records_per_page = 10  # Adjust if necessary
total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

# Initialize a list to store records
all_records = []

# Loop through each page
for page in range(total_pages):
    start_record = page * records_per_page
    url = f"{base_url}{start_record}"
    driver.get(url)

    # Allow time for the page to load
    time.sleep(2)  # Adjust as needed

    # Find all relevant records on the page
    records = driver.find_elements(By.CLASS_NAME, 'fsd-result')  # Adjust class name as necessary
    
    for record in records:
        title = record.find_element(By.TAG_NAME, 'h2').text.strip()  # Adjust tag as needed
        description = record.find_element(By.TAG_NAME, 'p').text.strip()  # Adjust tag as needed
        link = record.find_element(By.TAG_NAME, 'a').get_attribute('href')  # Adjust tag as needed

        # Store the record
        all_records.append({
            'title': title,
            'description': description,
            'link': link
        })

    print(f"Page {page + 1}/{total_pages} scraped successfully.")

# Close the driver
driver.quit()

# Print all records
for record in all_records:
    print(record)
