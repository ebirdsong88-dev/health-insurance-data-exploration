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