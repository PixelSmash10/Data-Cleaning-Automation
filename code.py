# PROJECT 1 - DATA CLEANING AUTOMATION SYSTEM

import pandas as pd
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ---------------- SELECT CSV FILE ----------------

downloads = os.path.join(os.path.expanduser("~"), "Downloads")

root = Tk()
root.withdraw()

file_path = askopenfilename(
    initialdir=downloads,
    title="Select CSV File",
    filetypes=[("CSV Files", "*.csv")]
)

if file_path:
    int1 = pd.read_csv(file_path)
    print("Selected File:", file_path)
else:
    print("No file selected.")
    exit()

# ---------------- DATASET PREVIEW ----------------

print("\n========== ORIGINAL DATASET ==========")
print(int1.head())

print("\n========== DATASET INFORMATION ==========")
print(int1.info())

print("\nShape:", int1.shape)

print("\nMissing Values:")
print(int1.isnull().sum())

print("\nDuplicate Rows:", int1.duplicated().sum())

# ---------------- BEFORE CLEANING ----------------

original_rows = len(int1)
original_columns = len(int1.columns)
original_missing = int1.isnull().sum().sum()
original_duplicates = int1.duplicated().sum()

# ---------------- REMOVE DUPLICATES ----------------

int1.drop_duplicates(inplace=True)

# ---------------- HANDLE MISSING VALUES ----------------

num_cols = int1.select_dtypes(include=np.number).columns

for col in num_cols:
    int1[col] = int1[col].fillna(int1[col].mean())

cat_cols = int1.select_dtypes(include='object').columns

for col in cat_cols:
    int1[col] = int1[col].fillna(int1[col].mode()[0])

# ---------------- CLEAN TEXT ----------------

for col in cat_cols:
    int1[col] = int1[col].str.strip()

for col in cat_cols:
    int1[col] = int1[col].str.lower()

# ---------------- REMOVE EMPTY ROWS ----------------

int1.dropna(how='all', inplace=True)

# ---------------- REMOVE OUTLIERS ----------------

for col in num_cols:

    Q1 = int1[col].quantile(0.25)
    Q3 = int1[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    int1 = int1[(int1[col] >= lower) & (int1[col] <= upper)]

# ---------------- AFTER CLEANING ----------------

final_rows = len(int1)
final_columns = len(int1.columns)
final_missing = int1.isnull().sum().sum()
final_duplicates = int1.duplicated().sum()

rows_removed = original_rows - final_rows
duplicates_removed = original_duplicates - final_duplicates

# ---------------- SAVE CLEANED FILE ----------------

filename = os.path.basename(file_path)
name = os.path.splitext(filename)[0]

output_file = name + "_Cleaned.csv"

int1.to_csv(output_file, index=False)

# ---------------- RESULTS ----------------

print("\nDataset Cleaned Successfully!")

print("\n========== BEFORE vs AFTER ==========")

print(f"Rows              : {original_rows} --> {final_rows}")
print(f"Columns           : {original_columns} --> {final_columns}")
print(f"Missing Values    : {original_missing} --> {final_missing}")
print(f"Duplicate Rows    : {original_duplicates} --> {final_duplicates}")
print(f"Rows Removed      : {rows_removed}")
print(f"Duplicates Removed: {duplicates_removed}")

print("=====================================")

print(f"\nCleaned File Saved As : {output_file}")