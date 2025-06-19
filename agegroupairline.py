import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt

# === Step 1: Connect to MySQL ===
user = 'root'
password = 'Mnaveen%409159'
host = 'localhost'
database = 'Travel'
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# === Step 2: Load data from MySQL ===
query = "SELECT * FROM airline_ratings"
df = pd.read_sql(query, con=engine)
print("Original data shape:", df.shape)

# Select relevant columns
features = [
    'age', 'class', 'inflight_wifi_service',
    'seat_comfort', 'cleanliness','food_and_drink','satisfaction'
]
df = df[features]

# Drop duplicate rows
df = df.drop_duplicates()

# Fill missing numeric values with mean
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# Fill missing categorical values with mode
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# STEP 2: Create 3 Age Segments

# Updated function for precise age groups
def age_segment(age):
    if age <= 30:
        return 'Young'
    elif 30 < age <= 60:
        return 'Middle-aged'
    else:
        return 'Senior'

df['age'] = df['age'].apply(age_segment)

# STEP 3: Satisfaction by Age Group
sns.countplot(data=df, x='age', hue='satisfaction', palette='Set2')
plt.title("Satisfaction Distribution by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Passenger Count")
plt.show()

# STEP 4: Service Ratings by Age Group

service_means = df.groupby('age')[['inflight_wifi_service', 'seat_comfort', 'cleanliness','food_and_drink']].mean()
print("🔍 Average Service Ratings:\n", service_means)

service_means.plot(kind='bar', figsize=(8,5))
plt.title("Average Inflight Service Ratings by Age Group")
plt.ylabel("Rating (1–5)")
plt.xticks(rotation=0)
plt.show()

# STEP 5: Class Preference by Age Group
sns.countplot(data=df, x='class', hue='age', palette='pastel')
plt.title("Travel Class Preference by Age Group")
plt.xlabel("Class")
plt.ylabel("Passenger Count")
plt.show()

# STEP 6: Export Summary (Optional)

summary = df.groupby('age').agg({
    'satisfaction': lambda x: x.value_counts().to_dict(),
    'inflight_wifi_service': 'mean',
    'seat_comfort': 'mean',
    'cleanliness': 'mean'
    
})

summary.to_csv("age_group_summary.csv")
print("✅ Summary exported to 'age_group_summary.csv'")
