import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load Dataset
df = pd.read_csv("spotify_history1.csv")  # Use cleaned dataset if available

# Step 2: Convert 'ts' to datetime and extract useful features
df['ts'] = pd.to_datetime(df['ts'], errors='coerce')
df['date'] = df['ts'].dt.date
df['time'] = df['ts'].dt.time
df['hour'] = df['ts'].dt.hour

# Categorize time of day
def label_time_of_day(hour):
    if 5 <= hour <= 11:
        return 'Morning'
    elif 12 <= hour <= 16:
        return 'Afternoon'
    elif 17 <= hour <= 20:
        return 'Evening'
    elif 21 <= hour <= 23:
        return 'Night'
    else:
        return 'Late Night'

df['time_of_day'] = df['hour'].apply(label_time_of_day)

# Drop original ts
df.drop(columns='ts', inplace=True)

# Step 3: Randomly sample 5000 rows
df = df.sample(n=5000, random_state=42).reset_index(drop=True)

# Step 4: Create text_features column
df['text_features'] = df['track_name'].astype(str) + " " + df['artist_name'].astype(str)

# Step 5: TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['text_features'])

# Step 6: Compute Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 7: Recommendation logic
def get_recommendation_indices(idx, cosine_sim=cosine_sim, top_n=10):
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # Skip itself
    return [i[0] for i in sim_scores]

# Step 8: Add recommended tracks for each row
recommended_track_list = []
for idx in range(len(df)):
    indices = get_recommendation_indices(idx)
    tracks = df.iloc[indices]['track_name'].tolist()
    recommended_track_list.append(", ".join(tracks))

df['recommended_tracks'] = recommended_track_list

# Step 9: Save updated table
df.to_csv("spotify_with_recommendations.csv", index=False)
print("✅ Data saved to 'spotify_with_recommendations.csv'")

# Step 10: Visualize time-of-day usage
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='time_of_day', order=['Late Night', 'Morning', 'Afternoon', 'Evening', 'Night'], palette='viridis')
plt.title("🔊 Spotify Usage by Time of Day")
plt.xlabel("Time of Day")
plt.ylabel("Number of Tracks Played")
plt.tight_layout()
plt.show()

# Optional: Hour-wise usage
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='hour', palette='magma')
plt.title("⏰ Spotify Plays by Hour of the Day")
plt.xlabel("Hour (0-23)")
plt.ylabel("Number of Tracks Played")
plt.tight_layout()
plt.show()
