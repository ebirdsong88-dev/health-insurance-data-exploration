"""
Health Insurance Data Exploration
Univariate/bivariate analysis, descriptive statistics,
and parametric/nonparametric hypothesis testing.
"""

# Import libraries
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from scipy import stats
from itertools import combinations

# Build paths relative to this file so the script runs from any folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "health_insurance.csv"
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Print environment versions
print("Python:", sys.version)
print("pandas:", pd.__version__, "| scipy:", scipy.__version__)

# Load the dataset
df = pd.read_csv(DATA_PATH)
print("Shape:", df.shape)
print(df.head())
df.info()
print("Missing values:\n", df.isnull().sum())

# Check categorical values for inconsistent labels
for col in ["sex", "smoker", "region", "Level"]:
    print(f"\{col} value counts:\n{df[col].value_counts()}")

# Chart settings
sns.set_theme(style="whitegrid")

def save_chart(filename):
    """Save the current chart to the images folder and close it."""
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / filename, dpi=150)
    plt.close()

# Univariate Visualizations

# Charges: histogram shows the shape of the distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["charges"], bins=30, kde=True)
plt.title("Distribution of Insurance Charges")
plt.xlabel("Charges ($)")
plt.ylabel("Number of Customers")
save_chart("univariate_charges.png")

# BMI: histogram shows the shape of the distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["bmi"], bins=30, kde=True)
plt.title("Distribution of BMI")
plt.xlabel("BMI")
plt.ylabel("Number of Customers")
save_chart("univariate_bmi.png")

# Smoker: bar chart of counts in each category
plt.figure(figsize=(6, 5))
sns.countplot(data=df, x="smoker", order=df["smoker"].value_counts().index)
plt.title("Smokers vs. Nonsmokers")
plt.xlabel("Smoker")
plt.ylabel("Number of Customers")
save_chart("univariate_smoker.png")

# Region: bar chart of counts in each category
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="region", order=df["region"].value_counts().index)
plt.title("Customers by Region")
plt.xlabel("Region")
plt.ylabel("Number of Customers")
save_chart("univariate_region.png")

print("\nUnivariate charts saved to:", IMAGES_DIR)

# Bivariate visualizations
# 1. Charges vs. BMI (quantitative vs. quantitative)
#    Scatter plot with a trend line to show the relationship
plt.figure(figsize=(8, 5))
sns.regplot(data=df, x="bmi", y="charges",
            scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
plt.title("Insurance Charges vs. BMI")
plt.xlabel("BMI")
plt.ylabel("Charges ($)")
save_chart("bivariate_charges_bmi.png")

# Correlation coefficient to put a number on the relationship
r = df["bmi"].corr(df["charges"])
print(f"\nCorrelation between BMI and charges: r = {r:.3f}")

# 2. Charges vs. Smoker (quantitative vs. categorical)
#    Box plot compares the distribution of charges for each group
plt.figure(figsize=(6, 5))
sns.boxplot(data=df, x="smoker", y="charges")
plt.title("Insurance Charges by Smoking Status")
plt.xlabel("Smoker")
plt.ylabel("Charges ($)")
save_chart("bivariate_charges_smoker.png")

print("\nCharges by smoking status:")
print(df.groupby("smoker")["charges"].describe().round(2))

# 3. BMI vs. Region (quantitative vs. categorical)
#    Box plot compares the BMI distribution across regions
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="region", y="bmi")
plt.title("BMI by Region")
plt.xlabel("Region")
plt.ylabel("BMI")
save_chart("bivariate_bmi_region.png")

print("\nBMI by region:")
print(df.groupby("region")["bmi"].describe().round(2))

# 4. Smoker vs. Region (categorical vs. categorical)
#    Grouped bar chart shows smoker counts within each region
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="region", hue="smoker")
plt.title("Smoking Status by Region")
plt.xlabel("Region")
plt.ylabel("Number of Customers")
plt.legend(title="Smoker")
save_chart("bivariate_smoker_region.png")

# Percentages make regions of different sizes easier to compare
print("\nSmoking status by region (% of each region):")
print((pd.crosstab(df["region"], df["smoker"], normalize="index") * 100).round(1))

print("\nBivariate charts saved to:", IMAGES_DIR)

# Descriptive Statistics
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Show wide tables in full in the terminal
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "{:,.2f}".format)

# Separate the numeric and categorical columns
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
print("\nNumeric variables:", numeric_cols)
print("Categorical variables:", categorical_cols)

# Quantitative variables
num = df[numeric_cols]
q1 = num.quantile(0.25)
q3 = num.quantile(0.75)

numeric_summary = pd.DataFrame({
    "count": num.count(),
    "mean": num.mean(),
    "median": num.median(),
    "min": num.min(),
    "max": num.max(),
    "range": num.max() - num.min(),
    "variance": num.var(),           # sample variance
    "std_dev": num.std(),            # sample standard deviation
    "10th_pct": num.quantile(0.10),
    "Q1_25th": q1,
    "Q3_75th": q3,
    "90th_pct": num.quantile(0.90),
    "IQR": q3 - q1,
    "skewness": num.skew(),          # helps decide parametric vs. nonparametric
}).round(2)

print("\nDescriptive statistics - quantitative variables:")
print(numeric_summary)
numeric_summary.to_csv(REPORTS_DIR / "descriptive_stats_numeric.csv")

# Qualitative variables
freq_tables = []
for col in categorical_cols:
    counts = df[col].value_counts().rename_axis("category")
    percents = (df[col].value_counts(normalize=True) * 100).rename_axis("category")

    table = pd.DataFrame({"count": counts, "percent": percents.round(2)})
    print(f"\nFrequency table - {col}:")
    print(table)

    # Add the variable name so all tables can be stacked into one file
    table = table.reset_index()
    table.insert(0, "variable", col)
    freq_tables.append(table)

categorical_summary = pd.concat(freq_tables, ignore_index=True)
categorical_summary.to_csv(REPORTS_DIR / "descriptive_stats_categorical.csv", index=False)

print("\nDescriptive statistics saved to:", REPORTS_DIR)

# Parametric test - one-way ANOVA (BMI across regions)
# Research question: Does average BMI differ across the four regions?
# H0: Mean BMI is the same in all four regions.
# H1: Mean BMI differs in at least one region.
ALPHA = 0.50

print("\n" + "=" * 60)
print("PART II: ONE-WAY ANOVA - BMI BY REGION")
print("=" * 60)
print("Research question: Does average BMI differ across the four regions?")
print("H0: Mean BMI is equal across all regions.")
print("H1: Mean BMI differs in at least one region.")
print(f"Significance level: alpha = {ALPHA}")

# Split BMI into one group per region
regions = sorted(df["region"].unique())
bmi_groups = [df.loc[df["region"] == r, "bmi"] for r in regions]

# Group summary
bmi_summary = df.groupby("region")["bmi"].agg(["count", "mean", "std", "var"])
print("\nBMI summary by region:")
print(bmi_summary)

# --- Assumption 1: Normality within each group (Shapiro-Wilk) ---
# H0 for Shapiro-Wilk: the group's data is normally distributed
print("\nAssumption check 1 - Normality (Shapiro-Wilk):")
for region, group in zip(regions, bmi_groups):
    w_stat, p_norm = stats.shapiro(group)
    verdict = "normal" if p_norm > ALPHA else "departs from normal"
    print(f"  {region:<10} W = {w_stat:.4f}, p = {p_norm:.4f} -> {verdict}")

# Q-Q plots: points close to the line indicate approximately normal data
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, region, group in zip(axes.flat, regions, bmi_groups):
    stats.probplot(group, dist="norm", plot=ax)
    ax.set_title(f"Q-Q Plot of BMI: {region}")
save_chart("anova_qq_plots_bmi_region.png")

# --- Assumption 2: Equal variances across groups (Levene's test) ---
# H0 for Levene: all groups have equal variances
lev_stat, lev_p = stats.levene(*bmi_groups)
equal_var = bool(lev_p > ALPHA)
print("\nAssumption check 2 - Equal variances (Levene's test):")
print(f"  W = {lev_stat:.4f}, p = {lev_p:.4f} -> "
      f"{'equal variances' if equal_var else 'variances are NOT equal'}")

# --- Run the ANOVA ---
# Classic ANOVA assumes equal variances; Welch's ANOVA does not.
# Levene's result decides which version is reported.
f_stat, anova_p = stats.f_oneway(*bmi_groups, equal_var=equal_var)
test_name = "Classic one-way ANOVA" if equal_var else "Welch's one-way ANOVA"

# Degrees of freedom
k = len(regions)
df_between = k - 1
if equal_var:
    df_within = len(df) - k
else:
    # Welch's ANOVA adjusts the denominator degrees of freedom
    # for unequal variances (Welch, 1951)
    weights = np.array([len(g) / g.var() for g in bmi_groups])
    w_total = weights.sum()
    sizes = np.array([len(g) for g in bmi_groups])
    adj = (((1 - weights / w_total) ** 2) / (sizes - 1)).sum()
    df_within = (k ** 2 - 1) / (3 * adj)

# Effect size: eta squared = between-group variation / total variation
grand_mean = df["bmi"].mean()
ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in bmi_groups)
ss_total = ((df["bmi"] - grand_mean) ** 2).sum()
eta_squared = ss_between / ss_total

print(f"\n{test_name} results:")
print(f"  F statistic = {f_stat:.4f}")
print(f"  p-value     = {anova_p:.4e}")
print(f"  df between  = {df_between}, df within = {df_within:.2f}")
print(f"  Eta squared = {eta_squared:.4f} "
      f"({eta_squared * 100:.1f}% of BMI variation explained by region)")

if anova_p < ALPHA:
    print(f"  Decision: p < {ALPHA}, so REJECT H0. Mean BMI differs across regions.")
else:
    print(f"  Decision: p >= {ALPHA}, so FAIL TO REJECT H0. No evidence mean BMI differs.")

# --- Post-hoc: which pairs of regions differ? ---
# Pairwise Welch t-tests with a Bonferroni correction
# (multiplies each p-value by the number of comparisons to limit false positives)
pairs = list(combinations(regions, 2))
posthoc_rows = []
for r1, r2 in pairs:
    g1 = df.loc[df["region"] == r1, "bmi"]
    g2 = df.loc[df["region"] == r2, "bmi"]
    t_stat, p_raw = stats.ttest_ind(g1, g2, equal_var=False)
    p_adj = min(p_raw * len(pairs), 1.0)
    posthoc_rows.append({
        "group_1": r1,
        "group_2": r2,
        "mean_difference": g1.mean() - g2.mean(),
        "t_statistic": t_stat,
        "p_value_bonferroni": p_adj,
        "significant": p_adj < ALPHA,
    })

posthoc = pd.DataFrame(posthoc_rows)
print("\nPost-hoc comparisons (Welch t-tests, Bonferroni-adjusted):")
print(posthoc.to_string(index=False, formatters={"p_value_bonferroni": "{:.4e}".format}))

# Save results for the README/report
anova_results = pd.DataFrame([{
    "test": test_name,
    "levene_p": lev_p,
    "f_statistic": f_stat,
    "p_value": anova_p,
    "eta_squared": eta_squared,
    "decision": "Reject H0" if anova_p < ALPHA else "Fail to reject H0",
}])
anova_results.to_csv(REPORTS_DIR / "anova_bmi_region_results.csv", index=False)
posthoc.to_csv(REPORTS_DIR / "anova_bmi_region_posthoc.csv", index=False)
print("\nANOVA results saved to:", REPORTS_DIR)