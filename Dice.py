import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Set your correct chromedriver path
driver_path = r"C:\Users\navee\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load job search results
url = "https://www.dice.com/jobs?location=Boston%2C+MA%2C+USA&q=data+analyst&latitude=42.3555076&longitude=-71.0565364&countryCode=US&locationPrecision=City&adminDistrictCode=MA"
driver.get(url)
time.sleep(5)

# Get job cards
job_cards = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="job-search-job-detail-link"]')
print(f"Found {len(job_cards)} job cards\n")

# Extract job links
job_links = []
for job in job_cards:
    link = job.get_attribute('href')
    if link and link not in job_links:
        job_links.append(link)

# Prepare CSV file
csv_file = open('dice_jobs.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['Index', 'Title', 'Company', 'Location', 'Salary', 'Description', 'Link'])

# Visit each job page to extract full details
for i, link in enumerate(job_links, start=1):
    print(f"\n{i}. Visiting: {link}")
    driver.get(link)
    time.sleep(3)

    try:
        title = driver.find_element(By.TAG_NAME, 'h1').text.strip()
    except:
        title = "N/A"

    try:
        company = driver.find_element(By.CSS_SELECTOR, 'a[data-cy="companyNameLink"]').text.strip()
    except:
        company = "N/A"

    # Updated Location extraction using correct selector you provided:
    try:
        location = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="location"]').text.strip()
    except:
        location = "N/A"

    # Updated Salary extraction using XPath for dynamic ID:
    try:
        salary = driver.find_element(By.XPATH, '//span[starts-with(@id, "payChip:")]').text.strip()
    except:
        salary = "N/A"

    try:
        description = driver.find_element(By.CSS_SELECTOR, 'div[data-cy="jobDescription"]').text.strip()
    except:
        description = "N/A"

    # Save row to CSV
    writer.writerow([i, title, company, location, salary, description, link])

    # Print for terminal visibility
    print(f"Index: {i}")
    print(f"Title: {title}")
    print(f"Company: {company}")
    print(f"Location: {location}")
    print(f"Salary: {salary}")
    print("-" * 80)

csv_file.close()
driver.quit()

print("\n✅ All job details saved to 'dice_jobs.csv'")
