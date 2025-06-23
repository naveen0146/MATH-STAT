import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import norm

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

# === Step 3: Clean Data ===
features = [
    'age', 'class', 'inflight_wifi_service',
    'seat_comfort', 'cleanliness', 'food_and_drink', 'satisfaction'
]
df = df[features]
df = df.drop_duplicates()

# Handle missing values
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# === Step 4: Segment Age Groups ===
def age_segment(age):
    if age <= 30:
        return 'Young'
    elif 30 < age <= 60:
        return 'Middle-aged'
    else:
        return 'Senior'

df['Age Group'] = df['age'].apply(age_segment)

# === Step 5: Plot Satisfaction by Age Group ===
sns.countplot(data=df, x='Age Group', hue='satisfaction', palette='Set2')
plt.title("Satisfaction Distribution by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Passenger Count")
plt.tight_layout()
plt.show()

# === Step 6: Average Service Ratings by Age Group ===
service_means = df.groupby('Age Group')[['inflight_wifi_service', 'seat_comfort', 'cleanliness', 'food_and_drink']].mean()
print("\U0001F50D Average Service Ratings:\n", service_means)

# === Step 7: Class Preference by Age Group ===
sns.countplot(data=df, x='class', hue='Age Group', palette='pastel')
plt.title("Travel Class Preference by Age Group")
plt.xlabel("Class")
plt.ylabel("Passenger Count")
plt.tight_layout()
plt.show()

# === Step 8: Confidence Intervals for Service Ratings ===
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)
    margin = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return mean, margin

print("\n\U0001F4CF Confidence Intervals (95%) for Service Ratings:")
error_margins = {'inflight_wifi_service': [], 'seat_comfort': [], 'cleanliness': [], 'food_and_drink': []}
for feature in error_margins.keys():
    print(f"\n\u25B6 {feature.upper()}")
    for group in ['Young', 'Middle-aged', 'Senior']:
        group_data = df[df['Age Group'] == group][feature]
        mean, margin = confidence_interval(group_data)
        error_margins[feature].append(margin)
        print(f"{group}: {mean:.2f} ± {margin:.2f}")

# === Step 9: Plot with Confidence Interval (Error Bars) ===
error_df = pd.DataFrame(error_margins, index=['Young', 'Middle-aged', 'Senior'])
ax = service_means.plot(kind='bar', yerr=error_df, capsize=4, figsize=(9,6), legend=True)
plt.title("Average Inflight Service Ratings by Age Group (with 95% Confidence Intervals)")
plt.ylabel("Rating (1–5)")
plt.xlabel("Age Group")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# === Step 10: Point Estimation and Confidence Margin Graph with Labels ===
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
features = ['inflight_wifi_service', 'seat_comfort', 'cleanliness', 'food_and_drink']
colors = ['#3b8bba', '#a0522d', '#228b22', '#8b008b']
age_groups = ['Young', 'Middle-aged', 'Senior']

for ax, feature, color in zip(axes.flatten(), features, colors):
    means = []
    margins = []
    for group in age_groups:
        data = df[df['Age Group'] == group][feature]
        mean, margin = confidence_interval(data)
        means.append(mean)
        margins.append(margin)

    bars = ax.bar(age_groups, means, yerr=margins, capsize=8, color=color, alpha=0.8)
    ax.set_title(f'{feature.replace("_", " ").title()}', fontsize=12)
    ax.set_ylabel("Average Rating (1 to 5)")
    ax.set_xlabel("Age Group")
    ax.set_ylim(0, 5.5)
    ax.axhline(y=np.mean(means), color='gray', linestyle='--', label='Overall Mean')
    ax.legend()

    for bar, mean_val, margin_val in zip(bars, means, margins):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.15,
                f"{mean_val:.2f} ± {margin_val:.2f}", ha='center', fontsize=10)

plt.suptitle("Point Estimates with 95% Confidence Margins", fontsize=16)
plt.tight_layout()
plt.show()

# === Step 11: Hypothesis Test (ANOVA) Summary ===
anova_pvals = []
for feature in features:
    groups_data = [df.loc[df['Age Group'] == g, feature] for g in age_groups]
    _, p_val = stats.f_oneway(*groups_data)
    anova_pvals.append(p_val)

plt.figure(figsize=(8,5))
sns.barplot(x=features, y=anova_pvals, palette='coolwarm')
plt.axhline(0.05, color='red', linestyle='--', label='α = 0.05 (Significance Level)')
plt.title("P-values from ANOVA Tests (Service Ratings by Age Group)")
plt.ylabel("p-value")
plt.xlabel("Feature")
plt.xticks(rotation=15)
plt.legend()
plt.tight_layout()
plt.show()

print("\n🔬 ANOVA Test Results (Does rating differ by age group?)")
for feature in features:
    groups = [df[df['Age Group'] == grp][feature] for grp in age_groups]
    f_stat, p_val = stats.f_oneway(*groups)
    print(f"{feature}: F = {f_stat:.2f}, p = {p_val:.4f}")
    if p_val < 0.05:
        print("  👉 Significant difference among age groups.")
    else:
        print("  👉 No significant difference among age groups.")

# === Step 12: Export Summary ===
summary = df.groupby('Age Group').agg({
    'satisfaction': lambda x: x.value_counts().to_dict(),
    'inflight_wifi_service': 'mean',
    'seat_comfort': 'mean',
    'cleanliness': 'mean',
    'food_and_drink': 'mean'
})
summary.to_csv("age_group_summary.csv")
print("✅ Summary exported to 'age_group_summary.csv'")

# === Step 13: Bayesian Inference ===
print("\n📈 Bayesian Inference: Probability one group rates lower than another")

def bayesian_probability_less(group1, group2, label1, label2, feature):
    mean1, std1, n1 = np.mean(group1), np.std(group1, ddof=1), len(group1)
    mean2, std2, n2 = np.mean(group2), np.std(group2, ddof=1), len(group2)
    samples1 = norm.rvs(loc=mean1, scale=std1 / np.sqrt(n1), size=10000)
    samples2 = norm.rvs(loc=mean2, scale=std2 / np.sqrt(n2), size=10000)
    prob = (samples1 < samples2).mean()
    print(f"▶ {label1} < {label2} in {feature}: P = {prob:.3f}")
    if prob > 0.95:
        print("   ✅ Strong evidence that first group rates lower.\n")
    elif prob > 0.80:
        print("   ⚠️ Moderate evidence that first group rates lower.\n")
    else:
        print("   ❌ Weak or no evidence of difference.\n")

comparisons = [
    ('Young', 'Middle-aged'),
    ('Young', 'Senior'),
    ('Middle-aged', 'Senior')
]

for feature in features:
    print(f"\n--- {feature.upper()} ---")
    for g1, g2 in comparisons:
        group1 = df[df['Age Group'] == g1][feature]
        group2 = df[df['Age Group'] == g2][feature]
        bayesian_probability_less(group1, group2, g1, g2, feature)

