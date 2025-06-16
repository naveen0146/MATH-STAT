from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Chrome driver options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target URL - Dice job search page
url = "https://www.dice.com/jobs?location=Boston%2C+MA%2C+USA&q=data+scientist"
driver.get(url)
time.sleep(5)  # wait for page load

# Scroll to bottom to ensure jobs load
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Grab all job listing links on the page
job_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="job-search-job-detail-link"]')

data = []

for link in job_links:
    job_title = link.text
    job_url = link.get_attribute("href")
    
    # Open each job detail page in new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(job_url)
    time.sleep(3)  # wait for page load
    
    # Extract Salary
    try:
        salary = driver.find_element(By.XPATH, '//span[contains(@id, "payChip")]').text
    except:
        salary = 'N/A'
    
    # Extract Location
    try:
        location = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="location"]').text
    except:
        location = 'N/A'
    
    # Extract Company Name
    try:
        company = driver.find_element(By.CSS_SELECTOR, 'a[data-cy="companyNameLink"]').text
    except:
        company = 'N/A'
    
    # Extract Posted Date
    try:
        posted_date = driver.find_element(By.CSS_SELECTOR,'span#timeAgo').text
    except:
        posted_date = 'N/A'
    
    # Save the data
    data.append({
        "Job Title": job_title,
        "Company": company,
        "Location": location,
        "Salary": salary,
        "Posted Date": posted_date,
        "Job URL": job_url
    })
    
    # Close job detail tab and switch back to main tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Save all data to CSV
df = pd.DataFrame(data)
df.to_csv("dice_jobs_boston_full.csv", index=False, encoding='utf-8-sig')

print("✅ Scraping complete! All job details saved to dice_jobs_boston_full.csv")

driver.quit()

