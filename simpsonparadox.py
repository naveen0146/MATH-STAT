import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_path = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
df = pd.read_csv(file_path)

# Check your categorical columns
cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
print("Categorical columns:", cat_cols)

# Pick two categorical variables to group by (adjust these to your data)
if len(cat_cols) >= 2:
    g1, g2 = cat_cols[:2]  # for example, "Gender" and "Class"

    # Group by both categories and calculate mean Age and Flight Distance
    grouped_age = df.groupby([g1, g2])["Age"].mean().unstack()
    grouped_distance = df.groupby([g1, g2])["Flight Distance"].mean().unstack()

    # Overall mean by second category only
    overall_age = df.groupby(g2)["Age"].mean()
    overall_distance = df.groupby(g2)["Flight Distance"].mean()

    # Plot Age grouped means
    ax1 = grouped_age.plot(kind='bar', figsize=(10, 6), rot=45)
    ax1.set_ylabel("Mean Age")
    ax1.set_title(f"Mean Age by {g1} & {g2}")
    ax1.legend(title=g1)
    plt.tight_layout()
    plt.show()

    # Overall Age by one category
    overall_age.plot(kind='bar', color='orange', alpha=0.7, figsize=(6,4), rot=45)
    plt.ylabel("Mean Age")
    plt.title(f"Overall Mean Age by {g2}")
    plt.tight_layout()
    plt.show()

    # Plot Flight Distance grouped means
    ax2 = grouped_distance.plot(kind='bar', figsize=(10, 6), rot=45)
    ax2.set_ylabel("Mean Flight Distance")
    ax2.set_title(f"Mean Flight Distance by {g1} & {g2}")
    ax2.legend(title=g1)
    plt.tight_layout()
    plt.show()

    # Overall Flight Distance by one category
    overall_distance.plot(kind='bar', color='orange', alpha=0.7, figsize=(6,4), rot=45)
    plt.ylabel("Mean Flight Distance")
    plt.title(f"Overall Mean Flight Distance by {g2}")
    plt.tight_layout()
    plt.show()

else:
    print("Not enough categorical columns for grouping.")
