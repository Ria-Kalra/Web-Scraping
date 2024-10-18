<h1> TASK 1 Scrape any sample website using beautifulsoup or selenium or playwright </h1> 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Initialize the Chrome WebDriver using WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Specify the URL to scrape
url = 'https://quotes.toscrape.com/'
driver.get(url)

# Wait for the page to load completely
time.sleep(3)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the driver after extraction
driver.quit()

# Print the page title to verify the extraction
print(soup.title.text)
