"""
Customer Churn Analysis - Part 5: SQL Analysis
This demonstrates SQL skills by querying the data using SQLite
"""

import pandas as pd
import sqlite3
import os

def create_database():
    """Create SQLite database and load data"""
    
    print("="*70)
    print("CREATING SQL DATABASE")
    print("="*70)
    
    # Load cleaned data
    df = pd.read_csv('telco_churn_cleaned.csv')
    
    # Create SQLite database
    conn = sqlite3.connect('churn_analysis.db')
    
    # Load data into SQL table
    df.to_sql('customers', conn, if_exists='replace', index=False)
    
    print(f"\nCreated database: churn_analysis.db")
    print(f"Table 'customers' created with {len(df)} records")
    print(f"Columns: {len(df.columns)}")
    
    # Show table schema
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(customers)")
    schema = cursor.fetchall()
    
    print("\nTable Schema:")
    print("-" * 70)
    for col in schema[:10]:  # Show first 10 columns
        print(f"  {col[1]:<20} {col[2]}")
    print(f"  ... and {len(schema) - 10} more columns")
    
    conn.close()

def run_sql_queries():
    """Run various SQL queries for analysis"""
    
    print("\n" + "="*70)
    print("SQL QUERY ANALYSIS")
    print("="*70)
    
    conn = sqlite3.connect('churn_analysis.db')
    
    # Query 1: Overall churn rate
    print("\n1. OVERALL CHURN RATE")
    print("-" * 70)
    query1 = """
    SELECT 
        COUNT(*) as total_customers,
        SUM(Churn) as churned_customers,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent
    FROM customers
    """
    result1 = pd.read_sql_query(query1, conn)
    print(result1.to_string(index=False))
    
    # Query 2: Churn by contract type
    print("\n\n2. CHURN RATE BY CONTRACT TYPE")
    print("-" * 70)
    query2 = """
    SELECT 
        Contract,
        COUNT(*) as total_customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent
    FROM customers
    GROUP BY Contract
    ORDER BY churn_rate_percent DESC
    """
    result2 = pd.read_sql_query(query2, conn)
    print(result2.to_string(index=False))
    
    # Query 3: Average metrics by churn status
    print("\n\n3. AVERAGE METRICS BY CHURN STATUS")
    print("-" * 70)
    query3 = """
    SELECT 
        CASE WHEN Churn = 1 THEN 'Churned' ELSE 'Retained' END as status,
        COUNT(*) as customers,
        ROUND(AVG(tenure), 1) as avg_tenure_months,
        ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges,
        ROUND(AVG(TotalCharges), 2) as avg_total_charges,
        ROUND(AVG(num_services), 1) as avg_services
    FROM customers
    GROUP BY Churn
    """
    result3 = pd.read_sql_query(query3, conn)
    print(result3.to_string(index=False))
    
    # Query 4: High-risk customer profile
    print("\n\n4. HIGH-RISK CUSTOMER PROFILE")
    print("-" * 70)
    print("(Month-to-month contract + tenure < 12 months + high charges)")
    query4 = """
    SELECT 
        COUNT(*) as high_risk_count,
        ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charge,
        ROUND(AVG(tenure), 1) as avg_tenure,
        SUM(Churn) as actually_churned,
        ROUND(AVG(Churn) * 100, 2) as actual_churn_rate
    FROM customers
    WHERE Contract = 'Month-to-month'
        AND tenure < 12
        AND MonthlyCharges > 70
    """
    result4 = pd.read_sql_query(query4, conn)
    print(result4.to_string(index=False))
    print("\nInsight: These customers should be prioritized for retention!")
    
    # Query 5: Revenue at risk by contract type
    print("\n\n5. MONTHLY REVENUE AT RISK BY CONTRACT TYPE")
    print("-" * 70)
    query5 = """
    SELECT 
        Contract,
        ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyCharges ELSE 0 END), 2) as revenue_at_risk,
        COUNT(CASE WHEN Churn = 1 THEN 1 END) as churned_customers,
        ROUND(AVG(CASE WHEN Churn = 1 THEN MonthlyCharges END), 2) as avg_churned_customer_value
    FROM customers
    GROUP BY Contract
    ORDER BY revenue_at_risk DESC
    """
    result5 = pd.read_sql_query(query5, conn)
    print(result5.to_string(index=False))
    
    # Query 6: Customer segmentation
    print("\n\n6. CUSTOMER SEGMENTS BY TENURE & CONTRACT")
    print("-" * 70)
    query6 = """
    SELECT 
        CASE 
            WHEN tenure < 12 THEN 'New (0-12 months)'
            WHEN tenure < 24 THEN 'Medium (12-24 months)'
            WHEN tenure < 48 THEN 'Established (24-48 months)'
            ELSE 'Long-term (48+ months)'
        END as tenure_segment,
        Contract,
        COUNT(*) as customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent
    FROM customers
    GROUP BY tenure_segment, Contract
    ORDER BY churn_rate_percent DESC
    LIMIT 10
    """
    result6 = pd.read_sql_query(query6, conn)
    print(result6.to_string(index=False))
    
    # Query 7: Internet service analysis
    print("\n\n7. CHURN BY INTERNET SERVICE TYPE")
    print("-" * 70)
    query7 = """
    SELECT 
        InternetService,
        COUNT(*) as total_customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent,
        ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges
    FROM customers
    GROUP BY InternetService
    ORDER BY churn_rate_percent DESC
    """
    result7 = pd.read_sql_query(query7, conn)
    print(result7.to_string(index=False))
    
    # Query 8: Payment method impact
    print("\n\n8. CHURN BY PAYMENT METHOD")
    print("-" * 70)
    query8 = """
    SELECT 
        PaymentMethod,
        COUNT(*) as customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent
    FROM customers
    GROUP BY PaymentMethod
    ORDER BY churn_rate_percent DESC
    """
    result8 = pd.read_sql_query(query8, conn)
    print(result8.to_string(index=False))
    
    # Query 9: Top 20 customers to target
    print("\n\n9. TOP 20 HIGH-VALUE AT-RISK CUSTOMERS")
    print("-" * 70)
    query9 = """
    SELECT 
        customerID,
        Contract,
        tenure,
        ROUND(MonthlyCharges, 2) as monthly_charges,
        ROUND(TotalCharges, 2) as total_charges,
        InternetService,
        PaymentMethod,
        num_services
    FROM customers
    WHERE Churn = 1
    ORDER BY TotalCharges DESC
    LIMIT 20
    """
    result9 = pd.read_sql_query(query9, conn)
    print(result9.to_string(index=False))
    
    # Query 10: Service adoption analysis
    print("\n\n10. CHURN BY NUMBER OF SERVICES")
    print("-" * 70)
    query10 = """
    SELECT 
        num_services,
        COUNT(*) as customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent,
        ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges
    FROM customers
    GROUP BY num_services
    ORDER BY num_services
    """
    result10 = pd.read_sql_query(query10, conn)
    print(result10.to_string(index=False))
    
    conn.close()
    
    # Save all queries to a SQL file
    print("\n" + "="*70)
    print("SAVING SQL QUERIES TO FILE")
    print("="*70)
    
    sql_file_content = f"""-- ============================================================================
-- CUSTOMER CHURN ANALYSIS - SQL QUERIES
-- ============================================================================
-- Database: SQLite
-- Table: customers
-- Total Records: 7,043
-- Purpose: Analyze customer churn patterns and identify retention opportunities
-- ============================================================================

-- Query 1: Overall Churn Rate
-- Purpose: Get baseline metrics for the entire customer base
{query1}

-- Query 2: Churn Rate by Contract Type
-- Purpose: Identify which contract types have highest churn
{query2}

-- Query 3: Average Metrics by Churn Status
-- Purpose: Compare characteristics of churned vs retained customers
{query3}

-- Query 4: High-Risk Customer Profile
-- Purpose: Identify customers matching high-risk criteria
{query4}

-- Query 5: Monthly Revenue at Risk by Contract Type
-- Purpose: Calculate financial impact of churn by contract
{query5}

-- Query 6: Customer Segmentation by Tenure & Contract
-- Purpose: Understand churn patterns across lifecycle stages
{query6}

-- Query 7: Churn by Internet Service Type
-- Purpose: Analyze impact of internet service on churn
{query7}

-- Query 8: Churn by Payment Method
-- Purpose: Identify payment method influence on retention
{query8}

-- Query 9: Top 20 High-Value At-Risk Customers
-- Purpose: Prioritize retention efforts on most valuable churned customers
{query9}

-- Query 10: Churn by Number of Services
-- Purpose: Understand relationship between service adoption and retention
{query10}

-- ============================================================================
-- BUSINESS INSIGHTS FROM SQL ANALYSIS
-- ============================================================================
-- 1. Month-to-month contracts have 15x higher churn than two-year contracts
-- 2. New customers (< 12 months) are at highest risk
-- 3. Fiber optic customers churn more despite premium service
-- 4. Electronic check users show significantly higher churn
-- 5. Customers with more services show better retention
-- ============================================================================
"""
    
    with open('sql_queries.sql', 'w') as f:
        f.write(sql_file_content)
    
    print("\nSaved: sql_queries.sql")
    print("   This file contains all queries for future reference")

def generate_sql_insights():
    """Generate key insights from SQL analysis"""
    
    print("\n" + "="*70)
    print("KEY SQL INSIGHTS")
    print("="*70)
    
    conn = sqlite3.connect('churn_analysis.db')
    
    # Calculate key metrics
    total_customers = pd.read_sql_query("SELECT COUNT(*) as count FROM customers", conn).iloc[0]['count']
    churned = pd.read_sql_query("SELECT SUM(Churn) as count FROM customers", conn).iloc[0]['count']
    churn_rate = (churned / total_customers) * 100
    
    total_revenue = pd.read_sql_query("SELECT SUM(MonthlyCharges) as revenue FROM customers", conn).iloc[0]['revenue']
    revenue_at_risk = pd.read_sql_query("SELECT SUM(MonthlyCharges) as revenue FROM customers WHERE Churn = 1", conn).iloc[0]['revenue']
    
    print(f"""
    OVERALL METRICS:
    -------------------
    Total Customers: {total_customers:,}
    Churned Customers: {churned:,}
    Churn Rate: {churn_rate:.2f}%
    
    REVENUE IMPACT:
    ------------------
    Total Monthly Revenue: ${total_revenue:,.2f}
    Revenue at Risk: ${revenue_at_risk:,.2f}
    % Revenue at Risk: {(revenue_at_risk/total_revenue)*100:.2f}%
    Annual Revenue at Risk: ${revenue_at_risk * 12:,.2f}
    
    TOP ACTIONABLE INSIGHTS:
    ---------------------------
    1. Month-to-month contracts are the biggest risk
       -> Implement contract upgrade incentives
    
    2. First 12 months are critical
       -> Enhanced onboarding and early engagement programs
    
    3. Electronic check users churn 2x more
       -> Payment method migration campaign
    
    4. High monthly charges correlate with churn
       -> Value perception analysis and pricing review
    
    5. Service bundling reduces churn
       -> Promote multi-service packages
    """)
    
    conn.close()

if __name__ == "__main__":
    # Create database
    create_database()
    
    # Run SQL queries
    run_sql_queries()
    
    # Generate insights
    generate_sql_insights()
    
    print("\n" + "="*70)
    print("SQL ANALYSIS COMPLETE!")
    print("="*70)
    print("\nFiles created:")
    print("  - churn_analysis.db - SQLite database with customer data")
    print("  - sql_queries.sql - All SQL queries for portfolio")
    print("\nYou can now:")
    print("  1. Open the database with any SQLite client")
    print("  2. Run queries directly in DB Browser for SQLite")
    print("  3. Share sql_queries.sql to show your SQL skills")
    print("  4. Include database in your GitHub repository")
    print("\nNext step: Create Power BI dashboard using this database!")
