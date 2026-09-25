"""
Bank Customer & Loan Analysis - Customer Segmentation Module
Applies heuristic behavioral profiling and K-Means Machine Learning clustering
to segment bank customers into actionable tiers:
1. High Value Customers
2. Premium Customers
3. Standard Customers
4. Emerging Customers
5. High Risk Customers
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def perform_customer_segmentation(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validates heuristic customer segments and runs K-Means clustering (k=5)
    to provide statistical profiling and business recommendations.
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]:
            - df with updated 'Customer_Segment' and 'Cluster_ID'
            - summary DataFrame with segment metrics
    """
    print("=" * 70)
    print("BANK CUSTOMER & LOAN ANALYSIS - CUSTOMER SEGMENTATION")
    print("=" * 70)

    # 1. Feature Selection for Clustering
    cluster_features = [
        "Annual_Income", "Account_Balance", "Credit_Score",
        "Customer_Tenure_Years", "Number_of_Products", "Debt_to_Income_Ratio"
    ]
    
    X = df[cluster_features].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. K-Means Clustering (k=5)
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    df["Cluster_ID"] = clusters

    print(f"[+] K-Means clustering completed on {len(df):,} customers across 5 clusters.")

    # 3. Aggregate Profile by Business Segment
    summary_cols = {
        "Customer_ID": "Customer_Count",
        "Annual_Income": "Avg_Annual_Income",
        "Account_Balance": "Avg_Account_Balance",
        "Credit_Score": "Avg_Credit_Score",
        "Debt_to_Income_Ratio": "Avg_DTI",
        "Number_of_Products": "Avg_Products",
        "Customer_Tenure_Years": "Avg_Tenure_Years",
        "Loan_Amount": "Avg_Loan_Amount",
        "Loan_Approval_Flag": "Approval_Rate",
        "Default_Flag": "Default_Rate"
    }

    # If df has default flags for all loans, default rate should be calculated among approved loans
    approved_mask = df["Loan_Status"] == "Approved"
    
    seg_summary = df.groupby("Customer_Segment").agg({
        "Customer_ID": "count",
        "Annual_Income": "mean",
        "Account_Balance": "mean",
        "Credit_Score": "mean",
        "Debt_to_Income_Ratio": "mean",
        "Number_of_Products": "mean",
        "Customer_Tenure_Years": "mean",
        "Loan_Amount": "mean",
        "Loan_Approval_Flag": "mean"
    }).rename(columns=summary_cols)

    # Default rate among approved loans per segment
    def_rates = df[approved_mask].groupby("Customer_Segment")["Default_Flag"].mean().rename("Default_Rate")
    seg_summary = seg_summary.join(def_rates).fillna(0.0)

    seg_summary["Customer_Pct"] = (seg_summary["Customer_Count"] / len(df)) * 100.0
    seg_summary["Total_Balance_Millions"] = (df.groupby("Customer_Segment")["Account_Balance"].sum()) / 1_000_000.0
    seg_summary["Total_Loan_Millions"] = (df[approved_mask].groupby("Customer_Segment")["Loan_Amount"].sum()) / 1_000_000.0

    # Sort in strategic order
    segment_order = ["High Value", "Premium", "Standard", "Emerging", "High Risk"]
    existing_order = [s for s in segment_order if s in seg_summary.index]
    seg_summary = seg_summary.reindex(existing_order)

    # Round numerical metrics
    seg_summary["Avg_Annual_Income"] = seg_summary["Avg_Annual_Income"].round(2)
    seg_summary["Avg_Account_Balance"] = seg_summary["Avg_Account_Balance"].round(2)
    seg_summary["Avg_Credit_Score"] = seg_summary["Avg_Credit_Score"].round(1)
    seg_summary["Avg_DTI"] = (seg_summary["Avg_DTI"] * 100).round(2)
    seg_summary["Avg_Products"] = seg_summary["Avg_Products"].round(2)
    seg_summary["Avg_Tenure_Years"] = seg_summary["Avg_Tenure_Years"].round(1)
    seg_summary["Avg_Loan_Amount"] = seg_summary["Avg_Loan_Amount"].round(2)
    seg_summary["Approval_Rate"] = (seg_summary["Approval_Rate"] * 100).round(2)
    seg_summary["Default_Rate"] = (seg_summary["Default_Rate"] * 100).round(2)
    seg_summary["Customer_Pct"] = seg_summary["Customer_Pct"].round(2)
    seg_summary["Total_Balance_Millions"] = seg_summary["Total_Balance_Millions"].round(2)
    seg_summary["Total_Loan_Millions"] = seg_summary["Total_Loan_Millions"].round(2)

    print("\n[+] Customer Segmentation Strategic Profiles:")
    print(seg_summary[["Customer_Count", "Customer_Pct", "Avg_Annual_Income", "Avg_Account_Balance", "Avg_Credit_Score", "Approval_Rate", "Default_Rate"]])

    return df, seg_summary

if __name__ == "__main__":
    import os
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "bank_customer_loan_clean.csv")
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path)
        df, summary = perform_customer_segmentation(df)
