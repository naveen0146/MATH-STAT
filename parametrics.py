import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import chi2_contingency

# -------------------------------
# 1. Generate Synthetic Dataset
# -------------------------------
np.random.seed(42)

# Satisfaction scores
business_sat = np.random.normal(loc=8,   scale=1.0, size=30)
economy_sat  = np.random.normal(loc=6.5, scale=1.5, size=30)

# NEW: Passenger ages (Business skew older than Economy)
business_age = np.random.normal(loc=45, scale=8,  size=30)
economy_age  = np.random.normal(loc=35, scale=10, size=30)

# Assemble DataFrame
df = pd.DataFrame({
    'Class'       : ['Business']*30 + ['Economy']*30,
    'Satisfaction': np.concatenate([business_sat, economy_sat]),
    'Age'         : np.concatenate([business_age,  economy_age])
})

# -------------------------------
# 2. PARAMETRIC TESTS
# -------------------------------
# 2a. Independent t-test on Satisfaction
t_sat, p_sat = stats.ttest_ind(df[df.Class=='Business'].Satisfaction,
                               df[df.Class=='Economy'].Satisfaction)

# 2b. Independent t-test on Age
t_age, p_age = stats.ttest_ind(df[df.Class=='Business'].Age,
                               df[df.Class=='Economy'].Age)

# 2c. Pearson correlation (Age ↔ Satisfaction)
r_pearson, p_pears = stats.pearsonr(df.Age, df.Satisfaction)

print(f"T-test (Parametric) — Satisfaction:\t t = {t_sat:5.2f}, p = {p_sat:.3f}")
print(f"T-test (Parametric) — Age:        \t t = {t_age:5.2f}, p = {p_age:.3f}")
print(f"Pearson r (Parametric) Age↔Sat:   \t r = {r_pearson:.3f}, p = {p_pears:.3f}")

# -------------------------------
# 3. NON-PARAMETRIC TESTS
# -------------------------------
# 3a. Mann-Whitney U on Satisfaction
u_sat, p_u_sat = stats.mannwhitneyu(df[df.Class=='Business'].Satisfaction,
                                   df[df.Class=='Economy'].Satisfaction,
                                   alternative='two-sided')

# 3b. Mann-Whitney U on Age
u_age, p_u_age = stats.mannwhitneyu(df[df.Class=='Business'].Age,
                                   df[df.Class=='Economy'].Age,
                                   alternative='two-sided')

# 3c. Spearman correlation (Age ↔ Satisfaction)
rho_spear, p_spear = stats.spearmanr(df.Age, df.Satisfaction)

# 3d. Chi-square on categorical Satisfaction (≥7 = Yes / <7 = No)
df['SatisfiedCat'] = np.where(df.Satisfaction >= 7, 'Yes', 'No')
cont = pd.crosstab(df.Class, df.SatisfiedCat)
chi2, p_chi, dof, exp = chi2_contingency(cont)

print(f"Mann-Whitney U (Non-Param) Sat:\t U = {u_sat:.0f}, p = {p_u_sat:.3f}")
print(f"Mann-Whitney U (Non-Param) Age:\t U = {u_age:.0f}, p = {p_u_age:.3f}")
print(f"Spearman ρ (Non-Param) Age↔Sat:\t ρ = {rho_spear:.3f}, p = {p_spear:.3f}")
print(f"Chi-square (Non-Param): χ² = {chi2:.2f}, p = {p_chi:.3f}")

# -------------------------------
# 4. VISUALISATIONS
# -------------------------------
sns.set_style('whitegrid')

# Box + Violin for Satisfaction
fig, ax = plt.subplots(1, 2, figsize=(12,4))
sns.boxplot(x='Class', y='Satisfaction', data=df, ax=ax[0])
ax[0].set_title('Boxplot • Satisfaction by Class')
sns.violinplot(x='Class', y='Satisfaction', data=df, ax=ax[1])
ax[1].set_title('Violin • Satisfaction by Class')
plt.show()

# Histogram of Age by class
plt.figure(figsize=(6,4))
sns.histplot(data=df, x='Age', hue='Class', bins=10, kde=True)
plt.title('Histogram • Age Distribution by Class')
plt.show()

# Scatter & regression line Age vs Satisfaction
plt.figure(figsize=(6,4))
sns.regplot(x='Age', y='Satisfaction', data=df, scatter_kws={'alpha':0.7})
plt.title('Scatter • Age vs Satisfaction (with OLS line)')
plt.show()

# Bar plot for categorical satisfaction
plt.figure(figsize=(6,4))
sns.countplot(x='Class', hue='SatisfiedCat', data=df)
plt.title('Bar • Satisfied (Yes/No) by Class')
plt.show()
