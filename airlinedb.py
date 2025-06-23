import pandas as pd
from sqlalchemy import create_engine

# Read CSV file
df = pd.read_csv("airline_passenger_satisfaction.csv")

# Create SQLAlchemy engine
engine = create_engine("mysql+mysqlconnector://root:Mnaveen%409159@localhost/Travel")

# Write to MySQL (replace if exists)
df.to_sql(name='airline_ratings', con=engine, if_exists='replace', index=False)

print("CSV data uploaded successfully to MySQL!")
