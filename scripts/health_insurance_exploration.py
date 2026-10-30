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