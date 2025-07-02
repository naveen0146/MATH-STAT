# kmeans_clustering_manual_scaling.py
#
# Cluster airline passengers with K-Means AFTER scaling
# each feature manually to mean = 0 and std = 1.
# -----------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# -------------------------------------------------------------
# 1. Load Data
# -------------------------------------------------------------
file_path = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
df = pd.read_csv(file_path)

print(f"✅ Data Loaded. Shape: {df.shape}")
print(df.head(2))

# -------------------------------------------------------------
# 2. Select Features for K-Means
# -------------------------------------------------------------
features = [
    "Age",
    "Flight Distance",
]

# keep only those that actually exist in the file
features = [f for f in features if f in df.columns]
data = df[features].dropna()          # remove rows with missing values

print(f"\n🧪 Using Features: {features}")
print("Remaining rows after dropping NA:", data.shape[0])

# -------------------------------------------------------------
# 3. Scale the data MANUALLY (mean = 0, std = 1)
# -------------------------------------------------------------
means = data.mean()                   # μ for every column
stds  = data.std(ddof=0)              # σ for every column (population std)

scaled_data = (data - means) / stds   # X_scaled = (X − μ) / σ

# Quick sanity check
print("\n📐 Manual Scaling Check:")
print("  Means (≈0):")
print(scaled_data.mean().round(4))
print("  Std Devs (≈1):")
print(scaled_data.std(ddof=0).round(4))

# -------------------------------------------------------------
# 4. Apply K-Means Clustering
# -------------------------------------------------------------
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
labels = kmeans.fit_predict(scaled_data)

# Append cluster labels to the *unscaled* data if you want to
data_with_labels = data.copy()
data_with_labels["Cluster"] = labels

# -------------------------------------------------------------
# 5. Visualize Clusters (first two features)
# -------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(
    data_with_labels[features[0]],
    data_with_labels[features[1]],
    c=data_with_labels["Cluster"],
    cmap="viridis",
    alpha=0.6,
)
plt.xlabel(features[0])
plt.ylabel(features[1])
plt.title("K-Means Clustering of Airline Passengers")
plt.colorbar(label="Cluster")
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------------------------------------
# 6. Output Cluster Summary
# -------------------------------------------------------------
print("\n📊 Cluster sizes:")
print(data_with_labels["Cluster"].value_counts().sort_index())

# Optional: Save results
# data_with_labels.to_csv("kmeans_clustered_airline_data_manual_scaling.csv", index=False)
