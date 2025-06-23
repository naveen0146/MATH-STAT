import pandas as pd
from sqlalchemy import create_engine

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

# === Step 3: Clean column names ===
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("/", "_")
)

df.rename(columns={"unnamed:_0": "number"}, inplace=True)
print("✅ Cleaned Column Names:")
print(df.columns.tolist())

# === Step 4: Fix structural errors for specific columns ===
cols_to_clean = ['gender', 'customer_type', 'type_of_travel', 'class']

for col in cols_to_clean:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

# === Step 5: Save cleaned data back to MySQL ===
# This will replace the existing table with the cleaned data
df.to_sql('airline_ratings', con=engine, if_exists='replace', index=False)
print("✅ Cleaned data saved back to MySQL table 'airline_ratings'")
# Show total missing values per column
print(df.isnull().sum())

# Or percentage missing per column
print(df.isnull().mean() * 100)


