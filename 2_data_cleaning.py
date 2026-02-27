"""
Customer Churn Analysis - Part 2: Data Cleaning & Preprocessing
This script cleans the data and prepares it for analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """Load the dataset"""
    print("Loading data...")
    df = pd.read_csv('telco_churn.csv')
    print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df

def clean_data(df):
    """Clean and preprocess the data"""
    
    print("="*70)
    print("DATA CLEANING")
    print("="*70)
    
    # 1. Handle TotalCharges (it's a string but should be numeric)
    print("\n1. Fixing TotalCharges column...")
    print(f"   Current type: {df['TotalCharges'].dtype}")
    
    # Convert to numeric (empty strings will become NaN)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Check for missing values after conversion
    missing_charges = df['TotalCharges'].isnull().sum()
    print(f"   Missing values found: {missing_charges}")
    
    if missing_charges > 0:
        # Fill missing TotalCharges with 0 (these are likely new customers)
        df['TotalCharges'] = df['TotalCharges'].fillna(0)
        print(f"   Filled {missing_charges} missing values with 0")
    
    print(f"   New type: {df['TotalCharges'].dtype}")
    
    # 2. Convert binary categorical variables to numeric
    print("\n2. Converting binary variables to numeric...")
    binary_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 
                   'PaperlessBilling', 'Churn']
    
    for col in binary_cols:
        if col in df.columns:
            # Map Yes/No to 1/0, Male/Female to 1/0
            if col == 'gender':
                df[col] = df[col].map({'Male': 1, 'Female': 0})
            else:
                df[col] = df[col].map({'Yes': 1, 'No': 0})
            print(f"   Converted {col}")
    
    # 3. Check for duplicates
    print("\n3. Checking for duplicates...")
    duplicates = df.duplicated().sum()
    print(f"   Duplicate rows: {duplicates}")
    
    if duplicates > 0:
        df.drop_duplicates(inplace=True)
        print(f"   Removed {duplicates} duplicate rows")
    
    # 4. Create new features
    print("\n4. Creating new features...")
    
    # Tenure groups
    df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 72], 
                                 labels=['0-1 year', '1-2 years', '2-4 years', '4+ years'])
    print("   Created tenure_group")
    
    # Average monthly charges per tenure month
    df['avg_monthly_charge'] = df['TotalCharges'] / (df['tenure'] + 1)  # +1 to avoid division by zero
    print("   Created avg_monthly_charge")
    
    # Has multiple services
    service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                    'TechSupport', 'StreamingTV', 'StreamingMovies']
    df['num_services'] = 0
    for col in service_cols:
        if col in df.columns:
            df['num_services'] += (df[col] == 'Yes').astype(int)
    print("   Created num_services")
    
    print("\n" + "="*70)
    print("CLEANED DATA SUMMARY")
    print("="*70)
    print(f"\nFinal shape: {df.shape}")
    print(f"\nData types:\n{df.dtypes.value_counts()}")
    print(f"\nMissing values:\n{df.isnull().sum().sum()} total")
    
    return df

def save_cleaned_data(df):
    """Save the cleaned dataset"""
    output_file = 'telco_churn_cleaned.csv'
    df.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to: {output_file}")
    return output_file

def show_cleaning_results(df):
    """Display before/after comparison"""
    
    print("\n" + "="*70)
    print("CLEANING RESULTS")
    print("="*70)
    
    print("\nNumeric Columns:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"   {len(numeric_cols)} columns: {numeric_cols[:5]}...")
    
    print("\nCategorical Columns:")
    cat_cols = df.select_dtypes(include=['object', 'str']).columns.tolist()
    print(f"   {len(cat_cols)} columns: {cat_cols}")
    
    print("\nNew Features Created:")
    print("   - tenure_group (categorical)")
    print("   - avg_monthly_charge (numeric)")
    print("   - num_services (numeric)")
    
    print("\nSample of cleaned data:")
    print(df[['customerID', 'tenure', 'tenure_group', 'MonthlyCharges', 
              'TotalCharges', 'num_services', 'Churn']].head(10))

if __name__ == "__main__":
    # Load original data
    df = load_data()
    
    # Clean the data
    df_cleaned = clean_data(df)
    
    # Show results
    show_cleaning_results(df_cleaned)
    
    # Save cleaned data
    save_cleaned_data(df_cleaned)
    
    print("\n" + "="*70)
    print("CLEANING COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Review the cleaned data")
    print("2. Run 3_eda_analysis.py for exploratory data analysis")
