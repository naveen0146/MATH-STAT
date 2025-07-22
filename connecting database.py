from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import mysql.connector

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target URL
url = "https://www.dice.com/jobs?location=Boston%2C+MA%2C+USA&q=data+scientist"
driver.get(url)
time.sleep(5)

# Scroll to bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Collect job links
job_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="job-search-job-detail-link"]')

data = []

# Scrape each job
for link in job_links:
    job_title = link.text
    job_url = link.get_attribute("href")

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(job_url)
    time.sleep(3)

    try:
        salary = driver.find_element(By.XPATH, '//span[contains(@id, "payChip")]').text
    except:
        salary = 'N/A'

    try:
        location = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="location"]').text
    except:
        location = 'N/A'

    try:
        company = driver.find_element(By.CSS_SELECTOR, 'a[data-cy="companyNameLink"]').text
    except:
        company = 'N/A'

    try:
        posted_date = driver.find_element(By.CSS_SELECTOR, 'span#timeAgo').text
    except:
        posted_date = 'N/A'

    data.append({
        "Job Title": job_title,
        "Company": company,
        "Location": location,
        "Salary": salary,
        "Posted Date": posted_date,
        "Job URL": job_url
    })

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Convert to DataFrame and save CSV
df = pd.DataFrame(data)
df.to_csv("dice_jobs_boston23.csv", index=False, encoding='utf-8-sig')
print("✅ CSV file saved.")

# -------- MYSQL PART STARTS HERE --------
# MySQL DB config
mysql_config = {
    "host": "localhost",
    "user": "root",         # 🔁 Replace with your MySQL username
    "password": "Mnaveen@9159", # 🔁 Replace with your MySQL password
    "database": "datadice"   # 🔁 Replace with your MySQL DB name
}

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()
print("✅ Connected to MySQL")

# Drop and recreate the table
cursor.execute("DROP TABLE IF EXISTS dice_jobs")
cursor.execute("""
    CREATE TABLE dice_jobs (
        job_title TEXT,
        company TEXT,
        location TEXT,
        salary TEXT,
        posted_date TEXT,
        job_url TEXT
    )
""")

# Insert data into MySQL
for row in data:
    cursor.execute("""
        INSERT INTO dice_jobs (job_title, company, location, salary, posted_date, job_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row["Job Title"], row["Company"], row["Location"],
        row["Salary"], row["Posted Date"], row["Job URL"]
    ))

conn.commit()
cursor.close()
conn.close()
print("✅ Data saved to MySQL database!")

# Close browser
driver.quit()
print("✅ Scraping complete. Browser closed.")

