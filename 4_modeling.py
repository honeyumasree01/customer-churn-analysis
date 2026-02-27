"""
Customer Churn Analysis - Part 4: Predictive Modeling
This script builds and evaluates a machine learning model to predict churn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report,
                             roc_auc_score, roc_curve)
import warnings
warnings.filterwarnings('ignore')

def load_cleaned_data():
    """Load the cleaned dataset"""
    print("Loading cleaned data...")
    df = pd.read_csv('telco_churn_cleaned.csv')
    print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df

def prepare_data_for_modeling(df):
    """Prepare features and target for modeling"""

    print("="*70)
    print("PREPARING DATA FOR MODELING")
    print("="*70)

    # Create a copy
    df_model = df.copy()

    # Drop customerID (not useful for prediction)
    if 'customerID' in df_model.columns:
        df_model = df_model.drop('customerID', axis=1)

    # Drop tenure_group (we'll use numeric tenure instead)
    if 'tenure_group' in df_model.columns:
        df_model = df_model.drop('tenure_group', axis=1)

    # Drop rows with any missing values (e.g. from categorical NaNs)
    before_drop = len(df_model)
    df_model = df_model.dropna()
    if len(df_model) < before_drop:
        print(f"\nDropped {before_drop - len(df_model)} rows with missing values.")

    # Encode categorical variables
    print("\nEncoding categorical variables...")
    categorical_cols = df_model.select_dtypes(include=['object']).columns.tolist()

    le = LabelEncoder()
    for col in categorical_cols:
        if col != 'Churn':  # Don't encode target yet
            print(f"  Encoding: {col}")
            df_model[col] = le.fit_transform(df_model[col].astype(str))

    # Separate features and target
    X = df_model.drop('Churn', axis=1)
    y = df_model['Churn']

    print(f"\nFeatures shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"\nFeatures: {list(X.columns)}")

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\nTrain set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    print(f"\nChurn distribution in train set:")
    print(y_train.value_counts(normalize=True) * 100)

    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Convert back to DataFrame for easier handling
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns)

    return X_train_scaled, X_test_scaled, y_train, y_test, X.columns

def train_logistic_regression(X_train, y_train):
    """Train Logistic Regression model"""
    print("\n" + "="*70)
    print("TRAINING LOGISTIC REGRESSION")
    print("="*70)

    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)

    print("Model trained successfully!")
    return model

def train_random_forest(X_train, y_train):
    """Train Random Forest model"""
    print("\n" + "="*70)
    print("TRAINING RANDOM FOREST")
    print("="*70)

    model = RandomForestClassifier(n_estimators=100, random_state=42,
                                   max_depth=10, min_samples_split=10)
    model.fit(X_train, y_train)

    print("Model trained successfully!")
    return model

def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    """Evaluate model performance"""

    print(f"\n{'='*70}")
    print(f"{model_name} - MODEL EVALUATION")
    print("="*70)

    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    y_test_proba = model.predict_proba(X_test)[:, 1]

    # Metrics
    print("\nTRAIN SET PERFORMANCE:")
    print(f"  Accuracy:  {accuracy_score(y_train, y_train_pred):.4f}")
    print(f"  Precision: {precision_score(y_train, y_train_pred):.4f}")
    print(f"  Recall:    {recall_score(y_train, y_train_pred):.4f}")
    print(f"  F1-Score:  {f1_score(y_train, y_train_pred):.4f}")

    print("\nTEST SET PERFORMANCE:")
    print(f"  Accuracy:  {accuracy_score(y_test, y_test_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_test_pred):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_test_pred):.4f}")
    print(f"  F1-Score:  {f1_score(y_test, y_test_pred):.4f}")
    print(f"  ROC-AUC:   {roc_auc_score(y_test, y_test_proba):.4f}")

    # Classification report
    print("\nDETAILED CLASSIFICATION REPORT:")
    print(classification_report(y_test, y_test_pred,
                                target_names=['No Churn', 'Churn']))

    return y_test_pred, y_test_proba

def plot_confusion_matrix(y_test, y_pred, model_name):
    """Plot confusion matrix"""

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['No Churn', 'Churn'],
                yticklabels=['No Churn', 'Churn'])
    plt.title(f'Confusion Matrix - {model_name}', fontweight='bold', fontsize=14)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')

    # Add percentages
    total = cm.sum()
    for i in range(2):
        for j in range(2):
            pct = (cm[i, j] / total) * 100
            plt.text(j + 0.5, i + 0.7, f'({pct:.1f}%)',
                    ha='center', va='center', fontsize=10, color='gray')

    filename = f'confusion_matrix_{model_name.lower().replace(" ", "_")}.png'
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {filename}")
    plt.close()

def plot_roc_curve(y_test, y_proba_lr, y_proba_rf):
    """Plot ROC curves for both models"""

    fpr_lr, tpr_lr, _ = roc_curve(y_test, y_proba_lr)
    fpr_rf, tpr_rf, _ = roc_curve(y_test, y_proba_rf)

    auc_lr = roc_auc_score(y_test, y_proba_lr)
    auc_rf = roc_auc_score(y_test, y_proba_rf)

    plt.figure(figsize=(10, 6))
    plt.plot(fpr_lr, tpr_lr, label=f'Logistic Regression (AUC = {auc_lr:.3f})',
             linewidth=2, color='blue')
    plt.plot(fpr_rf, tpr_rf, label=f'Random Forest (AUC = {auc_rf:.3f})',
             linewidth=2, color='green')
    plt.plot([0, 1], [0, 1], 'r--', linewidth=2, label='Random Classifier')

    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curve Comparison', fontweight='bold', fontsize=14)
    plt.legend(loc='lower right', fontsize=11)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('roc_curve_comparison.png', dpi=300, bbox_inches='tight')
    print("\nSaved: roc_curve_comparison.png")
    plt.close()

def plot_feature_importance(model, feature_names):
    """Plot feature importance from Random Forest"""

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:15]  # Top 15 features

    plt.figure(figsize=(12, 8))
    plt.barh(range(len(indices)), importances[indices], color='steelblue')
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel('Feature Importance', fontsize=12)
    plt.title('Top 15 Most Important Features (Random Forest)',
              fontweight='bold', fontsize=14)
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print("\nSaved: feature_importance.png")
    plt.close()

def create_churn_risk_scores(model, X_test, y_test):
    """Create churn risk segmentation"""

    print("\n" + "="*70)
    print("CHURN RISK SEGMENTATION")
    print("="*70)

    # Get probability scores
    churn_proba = model.predict_proba(X_test)[:, 1]

    # Create risk segments
    risk_segments = pd.cut(churn_proba,
                           bins=[0, 0.3, 0.7, 1.0],
                           labels=['Low Risk', 'Medium Risk', 'High Risk'])

    # Create summary
    risk_summary = pd.DataFrame({
        'Actual_Churn': y_test.values,
        'Churn_Probability': churn_proba,
        'Risk_Segment': risk_segments
    })

    print("\nRisk Segment Distribution:")
    print(risk_summary['Risk_Segment'].value_counts().sort_index())

    print("\nActual Churn Rate by Risk Segment:")
    churn_by_risk = risk_summary.groupby('Risk_Segment')['Actual_Churn'].mean() * 100
    for segment, rate in churn_by_risk.items():
        print(f"  {segment}: {rate:.2f}%")

    # Visualize
    plt.figure(figsize=(10, 6))
    risk_summary.groupby('Risk_Segment')['Actual_Churn'].mean().plot(kind='bar',
                                                                      color=['green', 'orange', 'red'])
    plt.xlabel('Risk Segment')
    plt.ylabel('Actual Churn Rate')
    plt.title('Actual Churn Rate by Predicted Risk Segment',
              fontweight='bold', fontsize=14)
    plt.xticks(rotation=0)
    plt.ylim(0, 1)

    # Add percentage labels
    for i, v in enumerate(churn_by_risk.values):
        plt.text(i, v/100 + 0.02, f'{v:.1f}%', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('churn_risk_segments.png', dpi=300, bbox_inches='tight')
    print("\nSaved: churn_risk_segments.png")
    plt.close()

    return risk_summary

def generate_business_recommendations():
    """Generate actionable business recommendations"""

    print("\n" + "="*70)
    print("BUSINESS RECOMMENDATIONS")
    print("="*70)

    recommendations = """
    Based on the churn analysis and predictive model, here are key recommendations:

    1. CONTRACT RETENTION STRATEGY
       - Offer incentives for month-to-month customers to upgrade to 1-2 year contracts
       - Provide discounts or loyalty benefits for long-term commitments
       - Target: Reduce month-to-month churn from 42% to below 30%

    2. EARLY INTERVENTION PROGRAM
       - Monitor customers in their first 6 months closely
       - Implement onboarding support and check-in calls
       - Offer trial periods for additional services
       - Target: New customers (0-6 months tenure)

    3. PAYMENT METHOD OPTIMIZATION
       - Encourage migration from electronic check to automatic payment methods
       - Offer small discounts for automatic payment enrollment
       - Target: Electronic check users (highest churn segment)

    4. SERVICE BUNDLING
       - Promote bundled packages (online security + tech support)
       - Customers with more services show lower churn rates
       - Target: Single-service customers

    5. FIBER OPTIC CUSTOMER EXPERIENCE
       - Investigate why fiber optic customers churn more
       - Improve customer service and technical support
       - Consider pricing adjustments or value-add services
       - Target: Fiber optic internet customers

    6. PREDICTIVE RETENTION CAMPAIGNS
       - Use the model to score all customers monthly
       - Reach out to high-risk customers (probability > 70%) with:
         * Personalized retention offers
         * Account reviews and service optimization
         * Loyalty rewards or discounts
       - Target: Top 20% highest risk scores

    7. PRICING STRATEGY REVIEW
       - Analyze if high monthly charges correlate with value perception
       - Consider tiered pricing or promotional periods
       - Target: Customers with charges > $70/month

    ESTIMATED IMPACT:
    - Implementing these strategies could reduce churn by 30-40%
    - Focus on high-risk segments first for maximum ROI
    - Monthly monitoring and model retraining recommended
    """

    print(recommendations)

    # Save to file
    with open('business_recommendations.txt', 'w') as f:
        f.write(recommendations)
    print("\nSaved: business_recommendations.txt")

if __name__ == "__main__":
    # Load data
    df = load_cleaned_data()

    # Prepare data
    X_train, X_test, y_train, y_test, feature_names = prepare_data_for_modeling(df)

    # Train models
    lr_model = train_logistic_regression(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)

    # Evaluate Logistic Regression
    y_pred_lr, y_proba_lr = evaluate_model(lr_model, X_train, X_test, y_train, y_test,
                                           "Logistic Regression")
    plot_confusion_matrix(y_test, y_pred_lr, "Logistic Regression")

    # Evaluate Random Forest
    y_pred_rf, y_proba_rf = evaluate_model(rf_model, X_train, X_test, y_train, y_test,
                                           "Random Forest")
    plot_confusion_matrix(y_test, y_pred_rf, "Random Forest")

    # Compare models
    plot_roc_curve(y_test, y_proba_lr, y_proba_rf)

    # Feature importance
    plot_feature_importance(rf_model, feature_names)

    # Risk segmentation
    risk_summary = create_churn_risk_scores(rf_model, X_test, y_test)

    # Business recommendations
    generate_business_recommendations()

    print("\n" + "="*70)
    print("MODELING COMPLETE!")
    print("="*70)
    print("\nYour complete churn analysis project is ready!")
    print("\nFiles created:")
    print("  - Multiple visualizations (.png files)")
    print("  - Cleaned dataset (telco_churn_cleaned.csv)")
    print("  - Business recommendations (business_recommendations.txt)")
    print("\nYou now have a complete portfolio project!")
