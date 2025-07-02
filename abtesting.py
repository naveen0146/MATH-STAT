# -------------------------------------------------------------
# A/B Test – Inflight Wi-Fi Quality vs Passenger Satisfaction
# -------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, chi2_contingency

# Configuration
# -------------------------------------------------------------
FILE_PATH = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
WIFI_COL = "Inflight wifi service"  # Or "Inflight Wifi Service" depending on exact column name
SAT_COL = "satisfaction"             # Or "Satisfaction" depending on exact column name
OUTPUT_PNG_PATH = r"C:\Users\navee\OneDrive\Desktop\myfiles\wifi_satisfaction_bar.png"

# Define mapping for satisfaction
SATISFACTION_MAP = {"neutral or dissatisfied": 0, "satisfied": 1}

# Define color palette for dissatisfied (0) and satisfied (1)
COLOR_PALETTE = {0: "#e76f51", 1: "#2a9d8f"} # Orange for dissatisfied, Green for satisfied

# 1) Load and Prepare Data
# -------------------------------------------------------------
try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Error: The file '{FILE_PATH}' was not found. Please check the path.")
    exit()

# Select relevant columns and drop rows with any missing values in these columns
df = df[[WIFI_COL, SAT_COL]].dropna()

# Recode satisfaction to binary (0 for dissatisfied, 1 for satisfied)
df["satisfaction_bin"] = df[SAT_COL].map(SATISFACTION_MAP)

# Define Wi-Fi groups based on the "Inflight wifi service" score
df["wifi_group"] = np.where(df[WIFI_COL] <= 3,
                            "Low Wi‑Fi (1–3)",
                            "High Wi‑Fi (4–5)")

# Ensure Wi-Fi groups are treated as a categorical type with a specific order for plotting
df["wifi_group"] = pd.Categorical(df["wifi_group"], categories=["Low Wi‑Fi (1–3)", "High Wi‑Fi (4–5)"], ordered=True)


# 2) Perform Statistical Analysis (A/B Test)
# -------------------------------------------------------------

print("-" * 50)
print("A/B Test Results: Wi-Fi Quality vs. Passenger Satisfaction")
print("-" * 50)

# Group data for summary statistics
summary_stats = df.groupby("wifi_group")["satisfaction_bin"].agg(
    count='size',
    mean='mean'
).round(3)

# Print row counts and means
print("Rows  • Low Wi‑Fi:", summary_stats.loc["Low Wi‑Fi (1–3)", "count"],
      "  High Wi‑Fi:", summary_stats.loc["High Wi‑Fi (4–5)", "count"])
print("Mean  • Low Wi‑Fi:", summary_stats.loc["Low Wi‑Fi (1–3)", "mean"],
      "  High Wi‑Fi:", summary_stats.loc["High Wi‑Fi (4–5)", "mean"])

# Split groups for t-test
group_low_wifi = df[df["wifi_group"] == "Low Wi‑Fi (1–3)"]["satisfaction_bin"]
group_high_wifi = df[df["wifi_group"] == "High Wi‑Fi (4–5)"]["satisfaction_bin"]

# Independent t-test (Welch's t-test, as equal_var=False)
t_stat, p_val_t = ttest_ind(group_low_wifi, group_high_wifi, equal_var=False)
print(f"\nT‑test      t = {t_stat:.3f}   p = {p_val_t:.4f}")

# Chi-square test (for association between two categorical variables)
contingency_table = pd.crosstab(df["wifi_group"], df["satisfaction_bin"])
chi2, p_val_chi, _, _ = chi2_contingency(contingency_table)
print(f"Chi‑square χ² = {chi2:.3f}   p = {p_val_chi:.4f}")

print("-" * 50)


# 3) Prepare Data for Plotting
# -------------------------------------------------------------
# Calculate proportions for plotting
# Using crosstab directly and then normalizing
prop_table = (
    pd.crosstab(df["wifi_group"], df["satisfaction_bin"], normalize='index')
    .reset_index()
    .melt(id_vars="wifi_group",
          var_name="satisfaction_bin",
          value_name="proportion")
)

# Convert satisfaction_bin back to boolean or meaningful labels for legend clarity if desired
# prop_table['satisfaction_label'] = prop_table['satisfaction_bin'].map({0: 'Dissatisfied', 1: 'Satisfied'})


# 4) Plotting
# -------------------------------------------------------------
plt.figure(figsize=(8, 6)) # Slightly larger figure for better readability
sns.barplot(data=prop_table,
            x="wifi_group",
            y="proportion",
            hue="satisfaction_bin",
            palette=COLOR_PALETTE, # Use the defined color palette
            errorbar=None) # No error bars for proportions, as we're plotting exact proportions from data

plt.ylabel("Proportion of Passengers", fontsize=12)
plt.xlabel("Inflight Wi-Fi Quality Group", fontsize=12)
plt.title("Passenger Satisfaction by Inflight Wi-Fi Quality", fontsize=14, pad=15)
plt.ylim(0, 1) # Proportions range from 0 to 1

# Custom legend to clearly state 0 and 1
handles, labels = plt.gca().get_legend_handles_labels()
new_labels = ["Dissatisfied (0)", "Satisfied (1)"] # Match the order of your hue (0 then 1)
plt.legend(handles=handles, labels=new_labels, title="Satisfaction", loc="upper right", frameon=True)


plt.grid(axis="y", linestyle="--", alpha=0.6) # Slightly more visible grid
plt.tight_layout() # Adjust layout to prevent labels from overlapping

# Save figure
try:
    plt.savefig(OUTPUT_PNG_PATH, dpi=300, bbox_inches='tight') # bbox_inches='tight' helps prevent clipping
    print(f"\nBar chart saved to: {OUTPUT_PNG_PATH}")
except Exception as e:
    print(f"Error saving plot: {e}")

plt.show()