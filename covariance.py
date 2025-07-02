import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------
# 1. Load and clean your dataset
# ---------------------------------------
file_path = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
df = pd.read_csv(file_path)

# ---------------------------------------
# 2. Filter to just 'Age' and 'Flight Distance'
# ---------------------------------------
X = df[["Age", "Flight Distance"]].dropna()

# ---------------------------------------
# 3. Compute Covariance and Correlation
# ---------------------------------------
cov_value = X.cov().iloc[0, 1]  # Covariance between Age and Flight Distance
corr_value = X.corr().iloc[0, 1]  # Pearson correlation coefficient

print(f"Covariance (Age vs Flight Distance): {cov_value:.2f}")
print(f"Correlation (Age vs Flight Distance): {corr_value:.2f}")

# ---------------------------------------
# 4. Visualize
# ---------------------------------------
plt.figure(figsize=(6, 5))
sns.scatterplot(data=X, x="Age", y="Flight Distance", alpha=0.6)
plt.title(f"Age vs. Flight Distance\nCov: {cov_value:.2f}, Corr: {corr_value:.2f}")
plt.xlabel("Passenger Age")
plt.ylabel("Flight Distance")
plt.grid(True)
plt.show()
