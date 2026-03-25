<h1 style="font-size: 2em;">Customer Churn Prediction & Analysis</h1>

This project analyzes customer churn for a telecommunications company and turns the results into practical retention actions. It combines exploratory analysis, SQL-style reporting, and a predictive model so you can answer both “what’s happening?” and “who should we intervene on?”

<h2 style="font-size: 1.4em;">Contents</h2>

- [Business problem](#business-problem)
- [Approach](#approach)
- [Dataset](#dataset)
- [Python analysis](#python-analysis)
- [SQL analysis (SQLite)](#sql-analysis-sqlite)
- [Predictive modeling](#predictive-modeling)
- [Dashboard (Power BI)](#dashboard-power-bi)
- [Business impact](#business-impact)
- [How to run](#how-to-run)
- [Project outputs](#project-outputs)
- [Project structure](#project-structure)
- [Contact](#contact)

<h2 style="font-size: 1.4em;">Business problem</h2>

Customer churn is expensive. In this dataset the churn rate is **26.54%** (1,869 of 7,043 customers). The goal is to:

- Identify the strongest churn drivers (segments, services, pricing signals)
- Quantify revenue at risk
- Build a model to flag customers likely to churn
- Translate findings into concrete retention actions

<h2 style="font-size: 1.4em;">Approach</h2>

1. **Explore** the raw data to understand structure and churn distribution  
2. **Clean + engineer features** (fix types, handle missing values, create helpful columns)  
3. **EDA** to find churn patterns across tenure, contract, services, and payment method  
4. **SQL analysis** in SQLite to demonstrate query-based reporting and “revenue at risk” metrics  
5. **Model** churn with a baseline (Logistic Regression) and a stronger model (Random Forest)  
6. Package outputs for reporting and dashboarding

<h2 style="font-size: 1.4em;">Dataset</h2>

- **Source**: Kaggle — Telco Customer Churn (`blastchar/telco-customer-churn`)
- **Rows**: 7,043
- **Target**: `Churn` (Yes/No; encoded as 1/0 in the cleaned dataset)

<h2 style="font-size: 1.4em;">Python analysis</h2>

<h3 style="font-size: 1.2em;">Step 1 — Data exploration</h3>

Run `1_data_exploration.py` to:

- Print shape, sample rows, dtypes, and churn distribution
- Save (and optionally display) a couple of starter charts:
  - `churn_distribution.png`
  - `churn_by_gender.png`

<h3 style="font-size: 1.2em;">Step 2 — Cleaning & preprocessing</h3>

Run `2_data_cleaning.py` to:

- Convert `TotalCharges` from text to numeric (empty strings become missing)
- Encode binary fields (`Yes/No`, `Male/Female`) as 1/0
- Create features:
  - `tenure_group` (lifecycle bucket)
  - `avg_monthly_charge` (TotalCharges / (tenure + 1))
  - `num_services` (count of add-on services)
- Output: `telco_churn_cleaned.csv`

<h3 style="font-size: 1.2em;">Step 3 — Exploratory data analysis (EDA)</h3>

Run `3_eda_analysis.py` to generate a fuller set of insights and charts. Key outputs include:

- `churn_by_tenure.png`
- `churn_by_contract.png`
- `churn_by_monthly_charges.png`
- `churn_by_internet_service.png`
- `churn_by_payment_method.png`
- `churn_by_num_services.png`
- `correlation_heatmap.png`

<h2 style="font-size: 1.4em;">SQL analysis (SQLite)</h2>

Run `5_sql_analysis.py` to:

- Create `churn_analysis.db` with one table: `customers`
- Run 10 analytical queries (also exported to `sql_queries.sql`)
- Calculate revenue at risk and segment summaries

Selected results from the run:

- **Monthly revenue at risk** (sum of MonthlyCharges for churned customers): **$139,130.85**
- **Annual revenue at risk**: **$1,669,570.20**
- High-risk profile (month-to-month + tenure < 12 + MonthlyCharges > 70): **814 customers**, **69.53%** actual churn rate

<h2 style="font-size: 1.4em;">Predictive modeling</h2>

Run `4_modeling.py` to train and evaluate:

- Logistic Regression (baseline)
- Random Forest (non-linear model with feature importance)

<h3 style="font-size: 1.2em;">Model performance (test set)</h3>

From the latest run:

- **Logistic Regression**: Accuracy **0.7918**, ROC-AUC **0.8368**, F1 **0.5820**
- **Random Forest**: Accuracy **0.7846**, ROC-AUC **0.8303**, F1 **0.5430**

This is an imbalanced classification problem (most customers do not churn), so ROC-AUC and class-specific metrics (precision/recall) matter more than accuracy alone.

<h3 style="font-size: 1.2em;">Risk segmentation (Random Forest)</h3>

Customers are bucketed by predicted churn probability:

- Low risk (0–0.30): **832** customers, **10.22%** actual churn
- Medium risk (0.30–0.70): **465** customers, **44.09%** actual churn
- High risk (0.70–1.00): **110** customers, **76.36%** actual churn

Saved model outputs:

- `confusion_matrix_logistic_regression.png`
- `confusion_matrix_random_forest.png`
- `roc_curve_comparison.png`
- `feature_importance.png`
- `churn_risk_segments.png`
- `business_recommendations.txt`

<h2 style="font-size: 1.4em;">Dashboard (Power BI)</h2>

Power BI dashboards are built directly from `telco_churn_cleaned.csv`.

1. Power BI Desktop → **Get Data** → **Text/CSV**
2. Select `telco_churn_cleaned.csv`
3. Load and build visuals (contract churn, tenure churn, revenue at risk, high-risk customer table)

Exports included in this repo:

- Interactive report: `Customer_Churn_Dashboard.pbix`
- Static export: [`Customer_Churn_Dashboard.pdf`](Customer_Churn_Dashboard.pdf)

<h2 style="font-size: 1.4em;">Business impact</h2>

The analysis points to a few clear levers:

- **Contract type**: Month-to-month customers are the highest-churn group (42.71% churn)
- **Tenure**: Early lifecycle customers churn much more; the first year is critical
- **Internet + payment**: Fiber optic and electronic check segments show much higher churn
- **Bundling**: Customers with more add-on services churn less

With **$139K/month** in revenue at risk, even a modest churn reduction in the highest-risk segments can have meaningful financial return. The modeling output supports a practical workflow: score customers regularly, prioritize the high-risk segment, and track retention outcomes.

<h2 style="font-size: 1.4em;">How to run</h2>

From this folder:

```bash
pip install -r requirements.txt
python 1_data_exploration.py
python 2_data_cleaning.py
python 3_eda_analysis.py
python 4_modeling.py
python 5_sql_analysis.py
```

<h2 style="font-size: 1.4em;">Project outputs</h2>

Core data outputs:

- `telco_churn.csv` (raw)
- `telco_churn_cleaned.csv` (cleaned + engineered features)
- `churn_analysis.db` (SQLite database)
- `sql_queries.sql` (exported queries)

Key charts (sample):

- `churn_by_contract.png`
- `churn_by_tenure.png`
- `correlation_heatmap.png`
- `roc_curve_comparison.png`
- `feature_importance.png`

<h2 style="font-size: 1.4em;">Project structure</h2>

```
customer_churn_project/
  1_data_exploration.py
  2_data_cleaning.py
  3_eda_analysis.py
  4_modeling.py
  5_sql_analysis.py
  requirements.txt
  README.md

  telco_churn.csv
  telco_churn_cleaned.csv
  churn_analysis.db
  sql_queries.sql

  *.png (EDA + modeling visuals)
  business_recommendations.txt
```

<h2 style="font-size: 1.4em;">Contact</h2>

Add your details here before publishing:

- Name:
- Email:
- LinkedIn:
- GitHub:
