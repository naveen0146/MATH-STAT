import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.decomposition import PCA

# -------------------------------
# 1. Load & Prepare Data
# -------------------------------
df = pd.read_csv("airline_data.csv")

# Drop unnecessary columns
df = df.drop(columns=["Unnamed: 0", "id"], errors="ignore")

# Drop missing values
df = df.dropna()

# Encode target
df["satisfaction"] = df["satisfaction"].replace({
    "satisfied": 1,
    "neutral or dissatisfied": 0
})

# Categorical columns
categorical_cols = ["Gender", "Customer Type", "Type of Travel", "Class"]
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Features and target
X = df_encoded.drop(columns="satisfaction")
y = df_encoded["satisfaction"]

# -------------------------------
# 2. Feature Selection
# -------------------------------
# Mutual Information
mi_scores = mutual_info_classif(X, y, random_state=42)
mi_series = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)
top_mi_features = mi_series.head(10)

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)
rf_scores = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
top_rf_features = rf_scores.head(10)

# RFE
lr_model = LogisticRegression(max_iter=1000, solver='liblinear')
rfe = RFE(lr_model, n_features_to_select=10)
rfe.fit(X, y)
rfe_support = pd.Series(rfe.support_, index=X.columns)
top_rfe_features = rfe_support[rfe_support].index.tolist()

# Summary table
feature_summary = pd.DataFrame({
    "Mutual Info Score": mi_series,
    "RF Importance": rf_scores,
    "Selected by RFE": rfe_support.map({True: "✅", False: ""})
})

# Show top features from all methods
top_combined = feature_summary.loc[
    top_mi_features.index.union(top_rf_features.index).union(top_rfe_features)
].sort_values(by="Mutual Info Score", ascending=False)

print("\nTop Features Selected (Combined):\n")
print(top_combined.head(15))

# -------------------------------
# 3. Visualize Feature Importance
# -------------------------------
top_mi_features.plot(kind='barh', color='skyblue')
plt.title("Top 10 Features by Mutual Information")
plt.xlabel("Mutual Information Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# -------------------------------
# 4. PCA (90% Variance Retention)
# -------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=0.90, random_state=42)
X_pca = pca.fit_transform(X_scaled)

# Plot explained variance
plt.plot(range(1, len(pca.explained_variance_ratio_) + 1),
         pca.explained_variance_ratio_.cumsum(), marker='o')
plt.title("PCA - Cumulative Explained Variance")
plt.xlabel("Number of Components")
plt.ylabel("Cumulative Variance")
plt.grid(True)
plt.tight_layout()
plt.show()

print("Original shape:", X.shape)
print("PCA reduced shape:", X_pca.shape)

# -------------------------------
# 5. Build & Evaluate Models
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression
lr = LogisticRegression(max_iter=1000, solver='liblinear')
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

# Accuracy and report
print("\n--- Logistic Regression ---")
print("Accuracy:", accuracy_score(y_test, lr_preds))
print(classification_report(y_test, lr_preds))

print("\n--- Random Forest ---")
print("Accuracy:", accuracy_score(y_test, rf_preds))
print(classification_report(y_test, rf_preds))
