import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# --------------------------------------------
# 1. Load and prepare the data
# --------------------------------------------
df = pd.read_csv("airline_data.csv")

# Drop unnecessary columns
df = df.drop(columns=["Unnamed: 0", "id"], errors="ignore")

# Drop missing values
df = df.dropna()

# Encode the target variable
df["satisfaction"] = df["satisfaction"].replace({
    "satisfied": 1,
    "neutral or dissatisfied": 0
})

# Identify categorical columns
categorical_cols = ["Gender", "Customer Type", "Type of Travel", "Class"]
numerical_cols = df.drop(columns=categorical_cols + ["satisfaction"]).columns.tolist()

# One-hot encode categorical columns
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Split into features and target
X = df_encoded.drop(columns="satisfaction")
y = df_encoded["satisfaction"]

# --------------------------------------------
# 2. Mutual Information
# --------------------------------------------
mi_scores = mutual_info_classif(X, y, random_state=42)
mi_series = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)
top_mi_features = mi_series.head(10)

# --------------------------------------------
# 3. Random Forest Importance
# --------------------------------------------
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)
rf_scores = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
top_rf_features = rf_scores.head(10)

# --------------------------------------------
# 4. RFE (Wrapper Method)
# --------------------------------------------
lr_model = LogisticRegression(max_iter=1000, solver='liblinear')
rfe = RFE(lr_model, n_features_to_select=10)
rfe.fit(X, y)
rfe_support = pd.Series(rfe.support_, index=X.columns)
top_rfe_features = rfe_support[rfe_support].index.tolist()

# --------------------------------------------
# 5. Combine and Print Summary
# --------------------------------------------
feature_summary = pd.DataFrame({
    "Mutual Info Score": mi_series,
    "RF Importance": rf_scores,
    "Selected by RFE": rfe_support.map({True: "✅", False: ""})
})

top_combined = feature_summary.loc[
    top_mi_features.index.union(top_rf_features.index).union(top_rfe_features)
].sort_values(by="Mutual Info Score", ascending=False)

print("\nTop Features Selected (Combined):\n")
print(top_combined.head(15))
