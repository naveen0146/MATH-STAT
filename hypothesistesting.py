import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
import numpy as np
from scipy import stats

# Load your dataset
df = pd.read_csv(r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv")

# Drop missing values for class and satisfaction
df = df.dropna(subset=['Class', 'satisfaction','Age'])

# Show unique class names
print("Classes in data:", df['Class'].unique())

# Plot satisfaction by class (boxplot)
plt.figure(figsize=(8,6))
sns.boxplot(x='Class', y='satisfaction', data=df)
plt.title('Satisfaction by Class')
plt.show()

# Get scores for each class
#Eco = df[df['Class'] == 'Economy']['satisfaction']
#EcoPlus = df[df['Class'] == 'Eco Plus']['satisfaction']
#Business = df[df['Class'] == 'Business']['satisfaction']

# ANOVA Test (do any class means differ?)
f_stat, p_val = f_oneway(Eco, EcoPlus, Business)
print(f"\nANOVA result: F = {f_stat:.2f}, p = {p_val:.4f}")
if p_val < 0.05:
    print("Result: At least one class is significantly different.")
else:
    print("Result: No significant difference between class satisfaction levels.")

# Function to print 95% confidence interval
def print_confidence_interval(scores, class_name):
    n = len(scores)
    mean = np.mean(scores)
    std_err = stats.sem(scores)
    ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=std_err)
    print(f"{class_name} - Mean: {mean:.2f}, 95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")

# Print confidence intervals for each class
print("\n95% Confidence Intervals:")
print_confidence_interval(Eco, "Economy")
print_confidence_interval(EcoPlus, "Eco Plus")
print_confidence_interval(Business, "Business")
