"""
Customer Churn Analysis - Part 3: Exploratory Data Analysis
This script performs detailed analysis and creates visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_palette("husl")
plt.style.use('seaborn-v0_8-darkgrid')

def load_cleaned_data():
    """Load the cleaned dataset"""
    print("Loading cleaned data...")
    df = pd.read_csv('telco_churn_cleaned.csv')
    print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df

def analyze_churn_by_demographics(df):
    """Analyze churn by demographic factors"""
    
    print("="*70)
    print("CHURN ANALYSIS BY DEMOGRAPHICS")
    print("="*70)
    
    # Churn by gender
    print("\nChurn by Gender:")
    gender_churn = pd.crosstab(df['gender'], df['Churn'], normalize='index') * 100
    print(gender_churn)
    
    # Churn by SeniorCitizen
    print("\nChurn by Senior Citizen Status:")
    senior_churn = pd.crosstab(df['SeniorCitizen'], df['Churn'], normalize='index') * 100
    print(senior_churn)
    
    # Churn by Partner
    print("\nChurn by Partner Status:")
    partner_churn = pd.crosstab(df['Partner'], df['Churn'], normalize='index') * 100
    print(partner_churn)
    
    # Churn by Dependents
    print("\nChurn by Dependents:")
    dependents_churn = pd.crosstab(df['Dependents'], df['Churn'], normalize='index') * 100
    print(dependents_churn)

def analyze_churn_by_services(df):
    """Analyze churn by service usage"""
    
    print("\n" + "="*70)
    print("CHURN ANALYSIS BY SERVICES")
    print("="*70)
    
    service_cols = ['PhoneService', 'MultipleLines', 'InternetService', 
                    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                    'TechSupport', 'StreamingTV', 'StreamingMovies']
    
    for col in service_cols:
        if col in df.columns:
            print(f"\nChurn by {col}:")
            churn_rate = pd.crosstab(df[col], df['Churn'], normalize='index') * 100
            print(churn_rate)

def analyze_churn_by_contract(df):
    """Analyze churn by contract and payment details"""
    
    print("\n" + "="*70)
    print("CHURN ANALYSIS BY CONTRACT TYPE")
    print("="*70)
    
    # Contract type
    print("\nChurn by Contract Type:")
    contract_churn = pd.crosstab(df['Contract'], df['Churn'], normalize='index') * 100
    print(contract_churn)
    
    # Payment method
    print("\nChurn by Payment Method:")
    payment_churn = pd.crosstab(df['PaymentMethod'], df['Churn'], normalize='index') * 100
    print(payment_churn)
    
    # Paperless billing
    print("\nChurn by Paperless Billing:")
    paperless_churn = pd.crosstab(df['PaperlessBilling'], df['Churn'], normalize='index') * 100
    print(paperless_churn)

def create_visualizations(df):
    """Create comprehensive visualizations"""
    
    print("\n" + "="*70)
    print("CREATING VISUALIZATIONS")
    print("="*70)
    
    # 1. Churn by Tenure
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    df[df['Churn']==1]['tenure'].hist(bins=30, alpha=0.7, label='Churned', color='red')
    df[df['Churn']==0]['tenure'].hist(bins=30, alpha=0.7, label='Retained', color='green')
    plt.xlabel('Tenure (months)')
    plt.ylabel('Number of Customers')
    plt.title('Tenure Distribution by Churn Status')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    tenure_churn = df.groupby('tenure')['Churn'].mean() * 100
    plt.plot(tenure_churn.index, tenure_churn.values, marker='o', markersize=3)
    plt.xlabel('Tenure (months)')
    plt.ylabel('Churn Rate (%)')
    plt.title('Churn Rate by Tenure')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('churn_by_tenure.png', dpi=300, bbox_inches='tight')
    print("Saved: churn_by_tenure.png")
    plt.show()
    
    # 2. Churn by Contract Type
    plt.figure(figsize=(10, 6))
    contract_data = df.groupby('Contract')['Churn'].agg(['sum', 'count'])
    contract_data['churn_rate'] = (contract_data['sum'] / contract_data['count']) * 100
    
    bars = plt.bar(contract_data.index, contract_data['churn_rate'], 
                   color=['#e74c3c', '#f39c12', '#2ecc71'])
    plt.xlabel('Contract Type')
    plt.ylabel('Churn Rate (%)')
    plt.title('Churn Rate by Contract Type', fontweight='bold', fontsize=14)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.savefig('churn_by_contract.png', dpi=300, bbox_inches='tight')
    print("Saved: churn_by_contract.png")
    plt.show()
    
    # 3. Churn by Monthly Charges
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    df[df['Churn']==1]['MonthlyCharges'].hist(bins=30, alpha=0.7, label='Churned', color='red')
    df[df['Churn']==0]['MonthlyCharges'].hist(bins=30, alpha=0.7, label='Retained', color='green')
    plt.xlabel('Monthly Charges ($)')
    plt.ylabel('Number of Customers')
    plt.title('Monthly Charges Distribution by Churn')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    df.boxplot(column='MonthlyCharges', by='Churn', figsize=(8, 6))
    plt.xlabel('Churn (0=No, 1=Yes)')
    plt.ylabel('Monthly Charges ($)')
    plt.title('Monthly Charges by Churn Status')
    plt.suptitle('')  # Remove default title
    
    plt.tight_layout()
    plt.savefig('churn_by_monthly_charges.png', dpi=300, bbox_inches='tight')
    print("Saved: churn_by_monthly_charges.png")
    plt.show()
    
    # 4. Churn by Internet Service Type
    plt.figure(figsize=(10, 6))
    internet_data = pd.crosstab(df['InternetService'], df['Churn'], normalize='index') * 100
    internet_data.plot(kind='bar', stacked=False, color=['#2ecc71', '#e74c3c'])
    plt.xlabel('Internet Service Type')
    plt.ylabel('Percentage (%)')
    plt.title('Churn Rate by Internet Service Type', fontweight='bold', fontsize=14)
    plt.legend(['Retained', 'Churned'])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('churn_by_internet_service.png', dpi=300, bbox_inches='tight')
    print("Saved: churn_by_internet_service.png")
    plt.show()
    
    # 5. Churn by Payment Method
    plt.figure(figsize=(12, 6))
    payment_data = pd.crosstab(df['PaymentMethod'], df['Churn'], normalize='index') * 100
    payment_data[1].sort_values(ascending=False).plot(kind='barh', color='#e74c3c')
    plt.xlabel('Churn Rate (%)')
    plt.ylabel('Payment Method')
    plt.title('Churn Rate by Payment Method', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig('churn_by_payment_method.png', dpi=300, bbox_inches='tight')
    print("Saved: churn_by_payment_method.png")
    plt.show()
    
    # 6. Correlation Heatmap
    plt.figure(figsize=(14, 10))
    
    # Select numeric columns
    numeric_cols = ['SeniorCitizen', 'Partner', 'Dependents', 'tenure', 
                    'PhoneService', 'PaperlessBilling', 'MonthlyCharges', 
                    'TotalCharges', 'num_services', 'Churn']
    
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1)
    plt.title('Correlation Heatmap of Key Features', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("Saved: correlation_heatmap.png")
    plt.show()
    
    # 7. Number of Services vs Churn
    plt.figure(figsize=(10, 6))
    services_churn = df.groupby('num_services')['Churn'].mean() * 100
    plt.bar(services_churn.index, services_churn.values, color='#3498db')
    plt.xlabel('Number of Services')
    plt.ylabel('Churn Rate (%)')
    plt.title('Churn Rate by Number of Services', fontweight='bold', fontsize=14)
    plt.xticks(range(int(df['num_services'].min()), int(df['num_services'].max())+1))
    
    for i, v in enumerate(services_churn.values):
        plt.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('churn_by_num_services.png', dpi=300, bbox_inches='tight')
    print("Saved: churn_by_num_services.png")
    plt.show()

def generate_insights(df):
    """Generate key insights from the analysis"""
    
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)
    
    # 1. Overall churn rate
    churn_rate = df['Churn'].mean() * 100
    print(f"\n1. Overall Churn Rate: {churn_rate:.2f}%")
    
    # 2. Contract type impact
    contract_churn = df.groupby('Contract')['Churn'].mean() * 100
    print(f"\n2. Churn by Contract Type:")
    for contract, rate in contract_churn.items():
        print(f"   - {contract}: {rate:.2f}%")
    
    # 3. Tenure impact
    avg_tenure_churned = df[df['Churn']==1]['tenure'].mean()
    avg_tenure_retained = df[df['Churn']==0]['tenure'].mean()
    print(f"\n3. Average Tenure:")
    print(f"   - Churned customers: {avg_tenure_churned:.1f} months")
    print(f"   - Retained customers: {avg_tenure_retained:.1f} months")
    
    # 4. Monthly charges impact
    avg_charges_churned = df[df['Churn']==1]['MonthlyCharges'].mean()
    avg_charges_retained = df[df['Churn']==0]['MonthlyCharges'].mean()
    print(f"\n4. Average Monthly Charges:")
    print(f"   - Churned customers: ${avg_charges_churned:.2f}")
    print(f"   - Retained customers: ${avg_charges_retained:.2f}")
    
    # 5. Internet service impact
    internet_churn = df.groupby('InternetService')['Churn'].mean() * 100
    print(f"\n5. Churn by Internet Service:")
    for service, rate in internet_churn.items():
        print(f"   - {service}: {rate:.2f}%")
    
    # 6. Services impact
    avg_services_churned = df[df['Churn']==1]['num_services'].mean()
    avg_services_retained = df[df['Churn']==0]['num_services'].mean()
    print(f"\n6. Average Number of Services:")
    print(f"   - Churned customers: {avg_services_churned:.2f}")
    print(f"   - Retained customers: {avg_services_retained:.2f}")
    
    print("\n" + "="*70)
    print("TOP CHURN RISK FACTORS")
    print("="*70)
    print("\n1. Month-to-month contracts (highest churn)")
    print("2. Fiber optic internet service")
    print("3. Electronic check payment method")
    print("4. No online security or tech support")
    print("5. Short tenure (< 6 months)")
    print("6. Higher monthly charges")

if __name__ == "__main__":
    # Load cleaned data
    df = load_cleaned_data()
    
    # Perform analyses
    analyze_churn_by_demographics(df)
    analyze_churn_by_services(df)
    analyze_churn_by_contract(df)
    
    # Create visualizations
    create_visualizations(df)
    
    # Generate insights
    generate_insights(df)
    
    print("\n" + "="*70)
    print("EDA COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Review all the visualizations created")
    print("2. Run 4_modeling.py to build the predictive model")
