import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load dataset
df = pd.read_csv("spotify_with_recommendations.csv")

# Step 2: Select features for clustering
features = ['ms_played', 'hour', 'platform', 'reason_start', 'reason_end', 'time_of_day']
df_clustering = df[features].copy()

# Step 3: One-hot encode categorical features
df_clustering = pd.get_dummies(df_clustering, columns=['platform', 'reason_start', 'reason_end', 'time_of_day'])

# Step 4: Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clustering)

# Step 5: Elbow Method to visualize inertia
inertia = []
K = range(1, 11)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K, inertia, 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.title('Elbow Method for Optimal k')
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 6: Silhouette Score for evaluation
print("\n🔍 Silhouette Scores:")
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    print(f"➡️ k = {k}, Silhouette Score = {score:.4f}")

# Step 7: Final KMeans clustering with best k = 10
best_k = 10
final_kmeans = KMeans(n_clusters=best_k, random_state=42)
df['cluster'] = final_kmeans.fit_predict(X_scaled)

# Step 8: Save to new CSV
df.to_csv("spotify_clustered.csv", index=False)
print("✅ Final clustering done with k = 10 and saved as 'spotify_clustered.csv'")

# Optional: Visualize cluster distribution
plt.figure(figsize=(8, 5))
sns.countplot(x='cluster', data=df, palette='Set2')
plt.title("Cluster Distribution of Spotify Users")
plt.xlabel("Cluster Label")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.show()
