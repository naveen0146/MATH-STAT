import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load your data
file_path = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
df = pd.read_csv(file_path)

# Define the feature pair for K-Means
x_ax, y_ax = "Age", "Flight Distance"

# Prepare data: select columns and drop missing values
X_km = df[[x_ax, y_ax]].dropna()

# Scale features
scaler = StandardScaler()
X_km_scaled = scaler.fit_transform(X_km)

# Fit K-Means with 2 clusters (adjust n_clusters as needed)
kmeans = KMeans(n_clusters=2, random_state=42)
labels_km = kmeans.fit_predict(X_km_scaled)

# Plot clusters
plt.figure()
plt.scatter(X_km[x_ax], X_km[y_ax], c=labels_km, cmap="viridis")
plt.xlabel(x_ax)
plt.ylabel(y_ax)
plt.title(f"K-Means Clustering: {x_ax} vs. {y_ax}")
plt.show()
