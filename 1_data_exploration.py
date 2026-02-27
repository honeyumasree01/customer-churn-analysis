"""
Customer Churn Analysis - Part 1: Data Exploration
This script loads and explores the telco customer churn dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
sns.set_style('whitegrid')

def load_data():
    """Load the dataset"""
    print("Loading data...")
    df = pd.read_csv('telco_churn.csv')
    print(f"Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df

def explore_data(df):
    """Perform initial data exploration"""
    
    print("="*70)
    print("DATASET OVERVIEW")
    print("="*70)
    print(f"\nDataset Shape: {df.shape}")
    print(f"Number of Rows: {df.shape[0]}")
    print(f"Number of Columns: {df.shape[1]}")
    
    print("\n" + "="*70)
    print("FIRST 5 ROWS")
    print("="*70)
    print(df.head())
    
    print("\n" + "="*70)
    print("COLUMN INFORMATION")
    print("="*70)
    print(df.info())
    
    print("\n" + "="*70)
    print("MISSING VALUES")
    print("="*70)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Percentage': missing_pct
    })
    print(missing_df[missing_df['Missing Count'] > 0])
    
    if missing_df['Missing Count'].sum() == 0:
        print("No missing values found!")
    
    print("\n" + "="*70)
    print("STATISTICAL SUMMARY")
    print("="*70)
    print(df.describe())
    
    print("\n" + "="*70)
    print("CHURN DISTRIBUTION")
    print("="*70)
    churn_counts = df['Churn'].value_counts()
    print(churn_counts)
    print(f"\nChurn Rate: {(churn_counts['Yes'] / len(df) * 100):.2f}%")
    print(f"Retention Rate: {(churn_counts['No'] / len(df) * 100):.2f}%")
    
    print("\n" + "="*70)
    print("DATA TYPES")
    print("="*70)
    print(df.dtypes)
    
    return df

def create_basic_visualizations(df):
    """Create and display visualizations"""
    
    # Churn distribution pie chart
    plt.figure(figsize=(8, 6))
    churn_counts = df['Churn'].value_counts()
    plt.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', 
            colors=['#2ecc71', '#e74c3c'], startangle=90)
    plt.title('Customer Churn Distribution', fontsize=14, fontweight='bold')
    plt.savefig('churn_distribution.png', dpi=300, bbox_inches='tight')
    print("\nSaved: churn_distribution.png")
    plt.show()  # This will display the plot
    
    # Churn by gender
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='gender', hue='Churn', palette=['#2ecc71', '#e74c3c'])
    plt.title('Churn by Gender', fontsize=14, fontweight='bold')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.savefig('churn_by_gender.png', dpi=300, bbox_inches='tight')
    print("Saved: churn_by_gender.png")
    plt.show()  # This will display the plot

if __name__ == "__main__":
    # Load data
    df = load_data()
    
    # Explore data
    df = explore_data(df)
    
    # Create visualizations
    create_basic_visualizations(df)
    
    print("\n" + "="*70)
    print("EXPLORATION COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Review the output above")
    print("2. Check the generated visualizations")
    print("3. Run 2_data_cleaning.py for data preprocessing")
