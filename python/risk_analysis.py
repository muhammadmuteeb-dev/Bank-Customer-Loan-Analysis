"""
Bank Customer & Loan Analysis - Credit Risk & Delinquency Analysis Module
Analyzes loan default probability, default rates across credit score tiers,
debt-to-income (DTI) exposure, risk categories, and high-risk customer segments.
"""

import pandas as pd
import numpy as np

def analyze_risk(df: pd.DataFrame) -> dict:
    """
    Performs comprehensive credit risk and delinquency analytics on the banking portfolio.
    Calculates default rates specifically on approved loans.
    """
    print("=" * 70)
    print("BANK CUSTOMER & LOAN ANALYSIS - CREDIT RISK & DEFAULT ANALYSIS")
    print("=" * 70)

    # Filter for Approved Loans (only approved loans are active and can default)
    df_approved = df[df["Loan_Status"] == "Approved"].copy()
    total_approved = len(df_approved)
    total_defaulted = df_approved["Default_Flag"].sum()
    overall_default_rate = round((total_defaulted / total_approved) * 100, 2)

    total_approved_amount = df_approved["Loan_Amount"].sum()
    defaulted_amount = df_approved[df_approved["Default_Flag"] == 1]["Loan_Amount"].sum()
    default_amount_rate = round((defaulted_amount / total_approved_amount) * 100, 2)

    # 1. Defaulters vs Non-Defaulters Comparative Profile
    comparison = df_approved.groupby("Default_Flag").agg(
        Count=("Customer_ID", "count"),
        Avg_Credit_Score=("Credit_Score", "mean"),
        Avg_DTI=("Debt_to_Income_Ratio", lambda x: x.mean() * 100),
        Avg_Income=("Annual_Income", "mean"),
        Avg_Loan_Amount=("Loan_Amount", "mean"),
        Avg_Interest_Rate=("Interest_Rate", "mean"),
        Avg_Tenure_Years=("Customer_Tenure_Years", "mean")
    ).reset_index()
    comparison["Status"] = comparison["Default_Flag"].map({0: "Non-Defaulter", 1: "Defaulter"})
    comparison["Avg_Credit_Score"] = comparison["Avg_Credit_Score"].round(1)
    comparison["Avg_DTI"] = comparison["Avg_DTI"].round(2)
    comparison["Avg_Income"] = comparison["Avg_Income"].round(2)
    comparison["Avg_Loan_Amount"] = comparison["Avg_Loan_Amount"].round(2)
    comparison["Avg_Interest_Rate"] = comparison["Avg_Interest_Rate"].round(2)
    comparison["Avg_Tenure_Years"] = comparison["Avg_Tenure_Years"].round(1)

    # 2. Default Rate by Risk Category
    risk_cat_summary = df_approved.groupby("Risk_Category").agg(
        Total_Loans=("Loan_ID", "count"),
        Default_Loans=("Default_Flag", "sum"),
        Total_Amount_M=("Loan_Amount", lambda x: round(x.sum() / 1_000_000, 2)),
        Default_Amount_M=("Loan_Amount", lambda x: round(x[df_approved.loc[x.index, "Default_Flag"] == 1].sum() / 1_000_000, 2)),
        Avg_Credit_Score=("Credit_Score", lambda x: round(x.mean(), 1)),
        Avg_DTI=("Debt_to_Income_Ratio", lambda x: round(x.mean() * 100, 2))
    ).reset_index()
    risk_cat_summary["Default_Rate"] = round((risk_cat_summary["Default_Loans"] / risk_cat_summary["Total_Loans"]) * 100, 2)
    risk_order = ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"]
    risk_cat_summary["Risk_Category"] = pd.Categorical(risk_cat_summary["Risk_Category"], categories=risk_order, ordered=True)
    risk_cat_summary = risk_cat_summary.sort_values("Risk_Category").reset_index(drop=True)

    # 3. Default Rate by Credit Score Category
    credit_cat_summary = df_approved.groupby("Credit_Score_Category", observed=False).agg(
        Total_Loans=("Loan_ID", "count"),
        Default_Loans=("Default_Flag", "sum")
    ).reset_index()
    credit_cat_summary["Default_Rate"] = round((credit_cat_summary["Default_Loans"] / credit_cat_summary["Total_Loans"]) * 100, 2)

    # 4. Default Rate by Loan Type
    loan_type_risk = df_approved.groupby("Loan_Type").agg(
        Total_Loans=("Loan_ID", "count"),
        Default_Loans=("Default_Flag", "sum"),
        Funded_Amount_M=("Loan_Amount", lambda x: round(x.sum() / 1_000_000, 2)),
        Default_Amount_M=("Loan_Amount", lambda x: round(x[df_approved.loc[x.index, "Default_Flag"] == 1].sum() / 1_000_000, 2)),
        Avg_Interest_Rate=("Interest_Rate", lambda x: round(x.mean(), 2))
    ).reset_index()
    loan_type_risk["Default_Rate"] = round((loan_type_risk["Default_Loans"] / loan_type_risk["Total_Loans"]) * 100, 2)
    loan_type_risk = loan_type_risk.sort_values(by="Default_Rate", ascending=False).reset_index(drop=True)

    # 5. Default Rate by Debt-to-Income (DTI) Category
    dti_risk = df_approved.groupby("Debt_to_Income_Category", observed=False).agg(
        Total_Loans=("Loan_ID", "count"),
        Default_Loans=("Default_Flag", "sum")
    ).reset_index()
    dti_risk["Default_Rate"] = round((dti_risk["Default_Loans"] / dti_risk["Total_Loans"]) * 100, 2)

    # 6. Default Rate by Customer Segment
    segment_risk = df_approved.groupby("Customer_Segment").agg(
        Total_Loans=("Loan_ID", "count"),
        Default_Loans=("Default_Flag", "sum"),
        Avg_Credit_Score=("Credit_Score", lambda x: round(x.mean(), 1))
    ).reset_index()
    segment_risk["Default_Rate"] = round((segment_risk["Default_Loans"] / segment_risk["Total_Loans"]) * 100, 2)

    # 7. Default Rate by Region
    region_risk = df_approved.groupby("Region").agg(
        Total_Loans=("Loan_ID", "count"),
        Default_Loans=("Default_Flag", "sum")
    ).reset_index()
    region_risk["Default_Rate"] = round((region_risk["Default_Loans"] / region_risk["Total_Loans"]) * 100, 2)

    print(f"[+] Total Active Approved Loans: {total_approved:,}")
    print(f"[+] Defaulted Loans: {total_defaulted:,} ({overall_default_rate}%)")
    print(f"[+] Total Capital at Default: ${defaulted_amount:,.2f} ({default_amount_rate}% of funded volume)")
    print(f"[+] Non-Defaulters Avg Credit Score: {comparison.loc[comparison['Default_Flag']==0, 'Avg_Credit_Score'].values[0]}")
    print(f"[+] Defaulters Avg Credit Score: {comparison.loc[comparison['Default_Flag']==1, 'Avg_Credit_Score'].values[0]}")
    print(f"[+] Non-Defaulters Avg DTI: {comparison.loc[comparison['Default_Flag']==0, 'Avg_DTI'].values[0]}%")
    print(f"[+] Defaulters Avg DTI: {comparison.loc[comparison['Default_Flag']==1, 'Avg_DTI'].values[0]}%")

    return {
        "total_approved": total_approved,
        "total_defaulted": total_defaulted,
        "overall_default_rate": overall_default_rate,
        "total_approved_amount": total_approved_amount,
        "defaulted_amount": defaulted_amount,
        "default_amount_rate": default_amount_rate,
        "defaulter_comparison": comparison,
        "risk_cat_summary": risk_cat_summary,
        "credit_cat_summary": credit_cat_summary,
        "loan_type_risk": loan_type_risk,
        "dti_risk": dti_risk,
        "segment_risk": segment_risk,
        "region_risk": region_risk
    }

if __name__ == "__main__":
    import os
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "bank_customer_loan_clean.csv")
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path)
        analyze_risk(df)
