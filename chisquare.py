import pandas as pd
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv(r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv")

# Choose two categorical columns
col1 = 'Class'   # example
col2 = 'satisfaction'  # example

# Create a contingency table
#The contingency table will count how often each combination occurs
contingency_table = pd.crosstab(df[col1], df[col2])

# Run the chi-square test
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Print the results
print("Chi-Square Statistic:", chi2)
print("Degrees of Freedom:", dof)
print("P-value:", p)

# Conclusion
if p < 0.05:
    print("✅ There is a significant relationship between", col1, "and", col2)
else:
    print("❌ There is no significant relationship between", col1, "and", col2)
# Visualize the contingency table
contingency = pd.crosstab(df['Class'], df['satisfaction'])

plt.figure(figsize=(6,4))
sns.heatmap(contingency, annot=True, cmap="YlGnBu")
plt.title("Class vs Satisfaction – Passenger Counts")
plt.xlabel("Satisfaction")
plt.ylabel("Class")
plt.tight_layout()
plt.show()
