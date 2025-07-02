import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# Load your data
file_path = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
df = pd.read_csv(file_path)

# Define the feature pair for DBSCAN
x_ax, y_ax ="Inflight wifi service","Age"

# Prepare data: select columns and drop missing values
X_db = df[[x_ax, y_ax]].dropna()

# Scale features
scaler = StandardScaler()
X_db_scaled = scaler.fit_transform(X_db)

# Run DBSCAN clustering
dbscan = DBSCAN(eps=0.9, min_samples=6)  # You can tweak eps and min_samples
labels_db = dbscan.fit_predict(X_db_scaled)

# Plot clusters (noise points labeled as -1)
plt.figure()
plt.scatter(X_db[x_ax], X_db[y_ax], c=labels_db, cmap="plasma", edgecolor='k')
plt.xlabel(x_ax)
plt.ylabel(y_ax)
plt.title(f"DBSCAN Clustering: {x_ax} vs. {y_ax}")
plt.show()
