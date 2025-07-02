# -------------------------------------------------------------
# 0. Setup
# -------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
from scipy.cluster.hierarchy import linkage, dendrogram

# -------------------------------------------------------------
# 1. Load your data
# -------------------------------------------------------------
file_path = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
df = pd.read_csv(file_path)

print("Shape:", df.shape)
print(df.head())

# -------------------------------------------------------------
# 2. Quick data-type scan
# -------------------------------------------------------------
num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

print("\nNumeric columns:", num_cols)
print("Categorical columns:", cat_cols)

# -------------------------------------------------------------
# 3. Core features for clustering  (EDIT as you like)
# -------------------------------------------------------------
# Choose a compact numeric subset that makes sense for travel behaviour
core_features = [
    "Age",
    "Flight Distance",
    "Departure Delay",
    "Arrival Delay",
    "Inflight Wifi Service",
    "Satisfaction"
]  # TODO: adjust to real column names

core_features = [c for c in core_features if c in df.columns]
print("\nClustering on:", core_features)

X = df[core_features].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# For 2-D plots we’ll use the first two numeric columns
x_axis, y_axis = core_features[:2]

# -------------------------------------------------------------
# 3a. K-Means
# -------------------------------------------------------------
kmeans = KMeans(n_clusters=2, random_state=42)
labels_km = kmeans.fit_predict(X_scaled)

plt.figure()
plt.scatter(X[x_axis], X[y_axis], c=labels_km, cmap="viridis")
plt.xlabel(x_axis); plt.ylabel(y_axis)
plt.title("K-Means Clusters")
plt.show()

# -------------------------------------------------------------
# 3b. Hierarchical
# -------------------------------------------------------------
linked = linkage(X_scaled, method="ward")
plt.figure(figsize=(8,4))
dendrogram(linked, truncate_mode="lastp", p=15)
plt.title("Hierarchical-Clustering Dendrogram")
plt.xlabel("Cluster size"); plt.ylabel("Distance")
plt.show()

# -------------------------------------------------------------
# 3c. DBSCAN
# -------------------------------------------------------------
dbscan = DBSCAN(eps=0.9, min_samples=6)        # tweak eps/min_samples
labels_db = dbscan.fit_predict(X_scaled)

plt.figure()
plt.scatter(X[x_axis], X[y_axis], c=labels_db, cmap="plasma")
plt.xlabel(x_axis); plt.ylabel(y_axis)
plt.title("DBSCAN (clusters & outliers)")
plt.show()

# -------------------------------------------------------------
# 3d. Gaussian Mixture Model  (GMM)
# -------------------------------------------------------------
gmm = GaussianMixture(n_components=3, random_state=42)
labels_gmm = gmm.fit_predict(X_scaled)

plt.figure()
plt.scatter(X[x_axis], X[y_axis], c=labels_gmm, cmap="coolwarm")
plt.xlabel(x_axis); plt.ylabel(y_axis)
plt.title("GMM Soft Clusters")
plt.show()

# -------------------------------------------------------------
# 4. Simple correlations
# -------------------------------------------------------------
print("\nCorrelation matrix (numeric):")
print(df[num_cols].corr().round(2))

# -------------------------------------------------------------
# 5. Association / Dependency quick checks
# -------------------------------------------------------------
if len(cat_cols) >= 2:
    a, b = cat_cols[:2]
    print(f"\nAssociation table ({a} vs. {b}):")
    print(pd.crosstab(df[a], df[b], normalize="index").round(2))

if len(num_cols) >= 2:
    u, v = num_cols[:2]
    plt.figure()
    plt.scatter(df[u], df[v], alpha=0.3)
    plt.xlabel(u); plt.ylabel(v)
    plt.title(f"Dependency scatter: {u} vs {v}")
    plt.show()

# -------------------------------------------------------------
# 6. Simpson’s Paradox demo (needs ≥2 cats + 1 numeric metric)
# -------------------------------------------------------------
if len(cat_cols) >= 2 and "Satisfaction" in df.columns:
    g1, g2 = cat_cols[:2]          # e.g. Flight_Type, Class
    metric = "Satisfaction"        # or any numeric outcome

    grouped = df.groupby([g1, g2])[metric].mean().reset_index()
    overall = df.groupby(g2)[metric].mean().reset_index()

    plt.figure()
    for name, sub in grouped.groupby(g1):
        plt.bar(sub[g2] + f" ({name})", sub[metric])
    plt.ylabel(metric); plt.title(f"{metric} by {g1} & {g2}")
    plt.xticks(rotation=45)
    plt.show()

    plt.figure()
    plt.bar(overall[g2], overall[metric])
    plt.ylabel(metric); plt.title(f"Overall {metric} by {g2} (Simpson’s check)")
    plt.show()
