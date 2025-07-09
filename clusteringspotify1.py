import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Step 1: Load the clustered dataset
df = pd.read_csv("spotify_clustered.csv")

# Step 2: View first few clustered rows
print("🎧 Sample Data with Cluster Labels:\n")
print(df[['track_name', 'artist_name', 'ms_played', 'hour', 'platform', 'time_of_day', 'cluster']].head(10))

# Step 3: Cluster summary analysis
print("\n📊 Cluster Summary:\n")
cluster_summary = df.groupby('cluster').agg({
    'ms_played': 'mean',
    'hour': 'mean',
    'platform': lambda x: x.mode()[0],
    'reason_start': lambda x: x.mode()[0],
    'reason_end': lambda x: x.mode()[0],
    'time_of_day': lambda x: x.mode()[0],
    'track_name': 'count'
}).rename(columns={'track_name': 'count'}).reset_index()

print(cluster_summary)

# Step 4: Prepare data for PCA visualization
features = ['ms_played', 'hour', 'platform', 'reason_start', 'reason_end', 'time_of_day']
df_clustering = df[features].copy()

# One-hot encode categorical features
df_clustering = pd.get_dummies(df_clustering, columns=['platform', 'reason_start', 'reason_end', 'time_of_day'])

# Normalize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clustering)

# Step 5: Reduce to 2D with PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Step 6: Visualize Clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['cluster'], palette='tab10')
plt.title("🎧 K-Means Clusters of Spotify Listening Behavior")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(title="Cluster")
plt.tight_layout()
plt.show()

# Step 7: Optional - Save summary
cluster_summary.to_csv("cluster_summary.csv", index=False)
print("\n✅ Cluster summary saved to 'cluster_summary.csv'")
