import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

class DiceJobAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.clean_salary()  # Clean salary on init

    def show_data(self, n=5):
        print(self.df.head(n))

    def clean_salary(self):
        # Extract minimum salary using regex
        self.df['MinSalary'] = self.df['Salary'].apply(self.extract_min_salary)

    def extract_min_salary(self, salary_str):
        try:
            # Use regex to extract first numeric part
            match = re.search(r'([\d,]+)', salary_str)
            if match:
                return float(match.group(1).replace(',', ''))
            else:
                return None
        except:
            return None

    def sort_by_salary(self):
        sorted_df = self.df.sort_values(by='MinSalary', ascending=False)
        print(sorted_df[['Job Title', 'Company', 'MinSalary']])
        return sorted_df

    def filter_by_location(self, location):
        filtered_df = self.df[self.df['Location'].str.contains(location, case=False, na=False)]
        print(filtered_df)
        return filtered_df

    def plot_jobs_per_company(self):
        plt.figure(figsize=(12, 6))
        sns.countplot(y=self.df['Company'], order=self.df['Company'].value_counts().index)
        plt.title("Number of Job Postings per Company")
        plt.xlabel("Number of Jobs")
        plt.ylabel("Company")
        plt.show()

    def plot_salary_distribution(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['MinSalary'].dropna(), bins=20, kde=True)
        plt.title("Salary Distribution")
        plt.xlabel("Minimum Salary (USD)")
        plt.ylabel("Frequency")
        plt.show()

    def jobs_posted_recently(self, keyword="days"):
        recent_jobs = self.df[self.df['Posted Date'].str.contains(keyword, case=False, na=False)]
        print(recent_jobs)
        return recent_jobs

# --------- Usage Example ---------

# Create analyzer object from your CSV
analyzer = DiceJobAnalyzer("dice_jobs_boston_full.csv")

# Show first few records
analyzer.show_data()

# Sort by Salary
analyzer.sort_by_salary()

# Filter jobs in Boston
analyzer.filter_by_location("Boston")

# Plot jobs per company
analyzer.plot_jobs_per_company()

# Plot salary distribution
analyzer.plot_salary_distribution()

# Show jobs posted recently (last X days)
analyzer.jobs_posted_recently("days")
