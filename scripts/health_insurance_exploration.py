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