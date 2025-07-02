import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture

# Load your data
file_path = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
df = pd.read_csv(file_path)

# Check your column names if needed
print(df.columns.tolist())

# If "Inflight Wifi Service" or any feature is categorical, convert it to numeric as needed
# For example, if 'Inflight Wifi Service' has strings like 'Excellent', 'Good', map them to numbers:
# mapping = {"Excellent": 3, "Good": 2, "Poor": 1}
# df["Inflight Wifi Service Numeric"] = df["Inflight Wifi Service"].map(mapping)
# Then use "Inflight Wifi Service Numeric" instead in features below

# Define features for GMM clustering (must be numeric)
x_ax, y_ax ="Age","Flight Distance"  

# Prepare data - drop NA
X_gmm = df[[x_ax, y_ax]].dropna()

# Scale features
scaler = StandardScaler()
X_gmm_scaled = scaler.fit_transform(X_gmm)

# Fit Gaussian Mixture Model with 3 components (adjust as needed)
gmm = GaussianMixture(n_components=3, random_state=42)
labels_gmm = gmm.fit_predict(X_gmm_scaled)

# Plot results
plt.figure()
plt.scatter(X_gmm[x_ax], X_gmm[y_ax], c=labels_gmm, cmap="coolwarm", edgecolor='k')
plt.xlabel(x_ax)
plt.ylabel(y_ax)
plt.title(f"GMM Clustering: {x_ax} vs. {y_ax}")
plt.show()
