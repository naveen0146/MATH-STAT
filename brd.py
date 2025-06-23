import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your sorted dataset
df = pd.read_csv("airline_sorted_by_age_distance.csv")

# If Gender is numeric (0 and 1), map it back to categories for clarity
# Uncomment below if your Gender column is numeric
# df['Gender'] = df['Gender'].map({0: 'Female', 1: 'Male'})

# 1. Descriptive statistics for numeric columns
print("Descriptive statistics:")
print(df.describe())

# 2. Check satisfaction counts
print("\nSatisfaction Value Counts:")
print(df['satisfaction'].value_counts())

# 3. Correlation heatmap to see relations between variables
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between Variables")
plt.show()

# 4. Satisfaction by Travel Class
plt.figure(figsize=(8, 5))
sns.countplot(x='Class', hue='satisfaction', data=df)
plt.title("Satisfaction Count by Travel Class")
plt.xlabel("Travel Class")
plt.ylabel("Number of Passengers")
plt.legend(title='Satisfaction Level')
plt.show()

# 5. Satisfaction by Type of Travel
plt.figure(figsize=(8, 5))
sns.countplot(x='Type of Travel', hue='satisfaction', data=df)
plt.title("Satisfaction Count by Type of Travel")
plt.xlabel("Type of Travel")
plt.ylabel("Number of Passengers")
plt.legend(title='Satisfaction Level')
plt.show()

# 6. Flight Distance Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['Flight Distance'], bins=30, kde=True)
plt.title("Distribution of Flight Distance (in kilometers)")
plt.xlabel("Flight Distance (km)")
plt.ylabel("Number of Flights")
plt.show()

# 7. Satisfaction by Gender
plt.figure(figsize=(8, 5))
sns.countplot(x='Gender', hue='satisfaction', data=df)
plt.title("Satisfaction Count by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Passengers")
plt.legend(title='Satisfaction Level')
plt.show()

# Optional: Print unique values of Gender
print("\nUnique values in Gender column:", df['Gender'].unique())
