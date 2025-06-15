from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Setup ChromeDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # optional
chrome_options.add_argument("--start-maximized")

driver_path = r"C:\Users\navee\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open URL
url = "https://www.dice.com/jobs?location=Boston%2C+MA%2C+USA&q=data+analyst&latitude=42.3555076&longitude=-71.0565364&countryCode=US&locationPrecision=City&adminDistrictCode=MA"
driver.get(url)
time.sleep(5)  # wait for JavaScript to load

# Get job cards by test id
job_cards = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="job-search-job-detail-link"]')
print(f"Found {len(job_cards)} job cards\n")

for job in job_cards:
    title = job.text.strip()
    link = job.get_attribute('href')
    print(f"Title: {title}")
    print(f"Link: {link}")
    print("-" * 50)

driver.quit()
