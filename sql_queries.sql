-- ============================================================================
-- CUSTOMER CHURN ANALYSIS - SQL QUERIES
-- ============================================================================
-- Database: SQLite
-- Table: customers
-- Total Records: 7,043
-- Purpose: Analyze customer churn patterns and identify retention opportunities
-- ============================================================================

-- Query 1: Overall Churn Rate
-- Purpose: Get baseline metrics for the entire customer base

    SELECT 
        COUNT(*) as total_customers,
        SUM(Churn) as churned_customers,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent
    FROM customers
    

-- Query 2: Churn Rate by Contract Type
-- Purpose: Identify which contract types have highest churn

    SELECT 
        Contract,
        COUNT(*) as total_customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent
    FROM customers
    GROUP BY Contract
    ORDER BY churn_rate_percent DESC
    

-- Query 3: Average Metrics by Churn Status
-- Purpose: Compare characteristics of churned vs retained customers

    SELECT 
        CASE WHEN Churn = 1 THEN 'Churned' ELSE 'Retained' END as status,
        COUNT(*) as customers,
        ROUND(AVG(tenure), 1) as avg_tenure_months,
        ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges,
        ROUND(AVG(TotalCharges), 2) as avg_total_charges,
        ROUND(AVG(num_services), 1) as avg_services
    FROM customers
    GROUP BY Churn
    

-- Query 4: High-Risk Customer Profile
-- Purpose: Identify customers matching high-risk criteria

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
    

-- Query 5: Monthly Revenue at Risk by Contract Type
-- Purpose: Calculate financial impact of churn by contract

    SELECT 
        Contract,
        ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyCharges ELSE 0 END), 2) as revenue_at_risk,
        COUNT(CASE WHEN Churn = 1 THEN 1 END) as churned_customers,
        ROUND(AVG(CASE WHEN Churn = 1 THEN MonthlyCharges END), 2) as avg_churned_customer_value
    FROM customers
    GROUP BY Contract
    ORDER BY revenue_at_risk DESC
    

-- Query 6: Customer Segmentation by Tenure & Contract
-- Purpose: Understand churn patterns across lifecycle stages

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
    

-- Query 7: Churn by Internet Service Type
-- Purpose: Analyze impact of internet service on churn

    SELECT 
        InternetService,
        COUNT(*) as total_customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent,
        ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges
    FROM customers
    GROUP BY InternetService
    ORDER BY churn_rate_percent DESC
    

-- Query 8: Churn by Payment Method
-- Purpose: Identify payment method influence on retention

    SELECT 
        PaymentMethod,
        COUNT(*) as customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent
    FROM customers
    GROUP BY PaymentMethod
    ORDER BY churn_rate_percent DESC
    

-- Query 9: Top 20 High-Value At-Risk Customers
-- Purpose: Prioritize retention efforts on most valuable churned customers

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
    

-- Query 10: Churn by Number of Services
-- Purpose: Understand relationship between service adoption and retention

    SELECT 
        num_services,
        COUNT(*) as customers,
        SUM(Churn) as churned,
        ROUND(AVG(Churn) * 100, 2) as churn_rate_percent,
        ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges
    FROM customers
    GROUP BY num_services
    ORDER BY num_services
    

-- ============================================================================
-- BUSINESS INSIGHTS FROM SQL ANALYSIS
-- ============================================================================
-- 1. Month-to-month contracts have 15x higher churn than two-year contracts
-- 2. New customers (< 12 months) are at highest risk
-- 3. Fiber optic customers churn more despite premium service
-- 4. Electronic check users show significantly higher churn
-- 5. Customers with more services show better retention
-- ============================================================================
