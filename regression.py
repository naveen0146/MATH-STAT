import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_curve, auc

# Configuration
FILE_PATH = r"C:\Users\navee\OneDrive\Desktop\myfiles\airline_data.csv"
WIFI_COL = "Inflight wifi service"
SAT_COL = "satisfaction"
SATISFACTION_MAP = {"neutral or dissatisfied": 0, "satisfied": 1}

# 1) Load and Prepare Data (same as before)
try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Error: The file '{FILE_PATH}' was not found. Please check the path.")
    exit()

# Select relevant columns and drop rows with any missing values
df = df[[WIFI_COL, SAT_COL]].dropna()

# Recode satisfaction to binary (0 for dissatisfied, 1 for satisfied)
df["satisfaction_bin"] = df[SAT_COL].map(SATISFACTION_MAP)

# For linear regression, we'll use the original numerical Wi-Fi score directly
# Ensure 'Inflight wifi service' is treated as a numerical feature if it's not already
# It's usually 1-5 scale, so it's already numerical.

# Define X (features) and y (target)
X = df[[WIFI_COL]]  # Independent variable (Wi-Fi service score)
y = df["satisfaction_bin"] # Dependent variable (binary satisfaction)

print(f"\n--- Running Models on {len(df)} data points ---")
print(f"Independent Variable: '{WIFI_COL}' (numerical scale)")
print(f"Dependent Variable: 'satisfaction_bin' (0=Dissatisfied, 1=Satisfied)\n")


# --- Option 1: Linear Regression (Linear Probability Model - LPM) ---
print("--- Linear Regression (Linear Probability Model - LPM) ---")

# Using statsmodels for a detailed summary output
X_sm = sm.add_constant(X) # Add a constant (intercept) to the independent variables
lpm_model = sm.OLS(y, X_sm)
lpm_results = lpm_model.fit()

print(lpm_results.summary())

# Interpretation for LPM:
print("\nLPM Interpretation Notes:")
print(" - The coefficient for 'Inflight wifi service' indicates the change in the probability of satisfaction for a one-unit increase in Wi-Fi service.")
print(" - R-squared (Adj. R-squared) tells you the proportion of variance in satisfaction explained by Wi-Fi service.")
print(" - Remember the limitations: predicted values can be <0 or >1, heteroscedasticity, non-normal residuals.")
print("-" * 60)

# --- Option 2: Logistic Regression (Recommended for Binary Target) ---
print("\n--- Logistic Regression ---")

# Using statsmodels for a detailed summary output
# This uses the GLM (Generalized Linear Model) framework for logistic regression
logit_model = sm.Logit(y, X_sm) # X_sm already has the constant
logit_results = logit_model.fit()

print(logit_results.summary())

# Interpretation for Logistic Regression:
print("\nLogistic Regression Interpretation Notes:")
print(" - The coefficients are log-odds. For example, exp(coef) is the odds ratio.")
print(" - A positive coefficient for 'Inflight wifi service' means higher Wi-Fi scores are associated with higher odds of satisfaction.")
print(" - Pseudo R-squared metrics (e.g., McFadden's R-squared) are provided, as standard R-squared is not applicable.")
print(" - This model directly estimates probabilities between 0 and 1, making it more suitable for binary outcomes.")
print("-" * 60)


# --- Visualizing the Models (Optional but helpful) ---
plt.figure(figsize=(10, 6))

# Plot actual data points (jittered for visibility)
sns.scatterplot(x=df[WIFI_COL], y=df["satisfaction_bin"], alpha=0.1, color='gray',
                label='Actual Data (Jittered for density)')

# Plot LPM regression line
wifi_range = np.linspace(X[WIFI_COL].min(), X[WIFI_COL].max(), 100).reshape(-1, 1)
wifi_range_sm = sm.add_constant(wifi_range)
lpm_predictions = lpm_results.predict(wifi_range_sm)
plt.plot(wifi_range, lpm_predictions, color='red', linestyle='--', label='Linear Probability Model')

# Plot Logistic Regression sigmoid curve
logit_predictions_log_odds = logit_results.predict(wifi_range_sm)
plt.plot(wifi_range, logit_predictions_log_odds, color='blue', label='Logistic Regression (Probability)')


plt.title('Satisfaction Probability vs. Inflight Wi-Fi Service')
plt.xlabel(WIFI_COL)
plt.ylabel('Probability of Satisfaction (1)')
plt.ylim(-0.1, 1.1) # Extend y-limits slightly to show LPM boundary issues
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

print("\nVisual comparison of LPM vs. Logistic Regression curve:")
print(" - Notice how the red dashed line (LPM) can go below 0 and above 1.")
print(" - The blue line (Logistic Regression) correctly stays between 0 and 1, representing probabilities.")
print("This highlights why Logistic Regression is generally preferred for binary outcomes.")