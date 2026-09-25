"""
Bank Customer & Loan Analysis - Loan Portfolio Analysis Module
Analyzes loan application volume, approval/rejection rates, funded amounts,
interest rate dynamics, loan tenure, monthly installments, and regional loan performance.
"""

import pandas as pd
import numpy as np

def analyze_loans(df: pd.DataFrame) -> dict:
    """
    Performs comprehensive loan portfolio analytics.
    Returns summary statistics and aggregated portfolio DataFrames.
    """
    print("=" * 70)
    print("BANK CUSTOMER & LOAN ANALYSIS - LOAN PORTFOLIO ANALYSIS")
    print("=" * 70)

    total_applications = len(df)
    status_counts = df["Loan_Status"].value_counts()
    
    approved_loans = status_counts.get("Approved", 0)
    rejected_loans = status_counts.get("Rejected", 0)
    pending_loans = status_counts.get("Pending", 0)

    approval_rate = round((approved_loans / total_applications) * 100, 2)
    rejection_rate = round((rejected_loans / total_applications) * 100, 2)
    pending_rate = round((pending_loans / total_applications) * 100, 2)

    total_applied_amount = df["Loan_Amount"].sum()
    avg_applied_amount = round(df["Loan_Amount"].mean(), 2)

    # Filter for Approved Loans (Funded Portfolio)
    df_approved = df[df["Loan_Status"] == "Approved"].copy()
    total_funded_amount = df_approved["Loan_Amount"].sum()
    avg_funded_amount = round(df_approved["Loan_Amount"].mean(), 2)
    avg_interest_rate = round(df_approved["Interest_Rate"].mean(), 2)
    avg_tenure_months = round(df_approved["Loan_Tenure_Months"].mean(), 1)
    avg_monthly_installment = round(df_approved["Monthly_Installment"].mean(), 2)
    total_est_annual_interest = round(df_approved["Estimated_Annual_Interest"].sum(), 2)

    # 1. Performance by Loan Type
    loan_type_summary = df.groupby("Loan_Type").agg(
        Total_Applications=("Loan_ID", "count"),
        Approved_Count=("Loan_Approval_Flag", "sum"),
        Total_Application_Volume=("Loan_Amount", "sum"),
        Avg_Interest_Rate=("Interest_Rate", "mean"),
        Avg_Tenure_Months=("Loan_Tenure_Months", "mean"),
        Avg_Installment=("Monthly_Installment", "mean")
    ).reset_index()

    # Calculate approved volume
    appr_vol = df_approved.groupby("Loan_Type")["Loan_Amount"].sum().rename("Total_Funded_Volume")
    appr_avg = df_approved.groupby("Loan_Type")["Loan_Amount"].mean().rename("Avg_Funded_Amount")
    
    loan_type_summary = loan_type_summary.merge(appr_vol, on="Loan_Type", how="left").merge(appr_avg, on="Loan_Type", how="left")
    loan_type_summary["Approval_Rate"] = round((loan_type_summary["Approved_Count"] / loan_type_summary["Total_Applications"]) * 100, 2)
    loan_type_summary["Total_Funded_Volume_M"] = round(loan_type_summary["Total_Funded_Volume"] / 1_000_000, 2)
    loan_type_summary["Total_Application_Volume_M"] = round(loan_type_summary["Total_Application_Volume"] / 1_000_000, 2)
    loan_type_summary["Avg_Funded_Amount"] = round(loan_type_summary["Avg_Funded_Amount"], 2)
    loan_type_summary["Avg_Interest_Rate"] = round(loan_type_summary["Avg_Interest_Rate"], 2)
    loan_type_summary["Avg_Tenure_Months"] = round(loan_type_summary["Avg_Tenure_Months"], 1)
    loan_type_summary["Avg_Installment"] = round(loan_type_summary["Avg_Installment"], 2)

    # 2. Performance by Purpose
    purpose_summary = df.groupby("Loan_Purpose").agg(
        Applications=("Loan_ID", "count"),
        Approval_Rate=("Loan_Approval_Flag", lambda x: round(x.mean() * 100, 2)),
        Total_Volume_M=("Loan_Amount", lambda x: round(x.sum() / 1_000_000, 2)),
        Avg_Amount=("Loan_Amount", lambda x: round(x.mean(), 2)),
        Avg_Rate=("Interest_Rate", lambda x: round(x.mean(), 2))
    ).reset_index().sort_values(by="Applications", ascending=False)

    # 3. Regional Loan Metrics
    region_loan_summary = df.groupby("Region").agg(
        Total_Applications=("Loan_ID", "count"),
        Approved_Count=("Loan_Approval_Flag", "sum"),
        Approval_Rate=("Loan_Approval_Flag", lambda x: round(x.mean() * 100, 2)),
        Total_Loan_Volume_M=("Loan_Amount", lambda x: round(x.sum() / 1_000_000, 2)),
        Avg_Loan_Amount=("Loan_Amount", lambda x: round(x.mean(), 2)),
        Avg_Interest_Rate=("Interest_Rate", lambda x: round(x.mean(), 2))
    ).reset_index().sort_values(by="Total_Loan_Volume_M", ascending=False)

    # 4. Branch Loan Metrics
    branch_loan_summary = df.groupby(["Branch_ID", "Branch_Name", "Region"]).agg(
        Total_Applications=("Loan_ID", "count"),
        Approved_Count=("Loan_Approval_Flag", "sum"),
        Approval_Rate=("Loan_Approval_Flag", lambda x: round(x.mean() * 100, 2)),
        Total_Volume_M=("Loan_Amount", lambda x: round(x.sum() / 1_000_000, 2)),
        Avg_Amount=("Loan_Amount", lambda x: round(x.mean(), 2))
    ).reset_index().sort_values(by="Total_Volume_M", ascending=False)

    print(f"[+] Total Loan Applications: {total_applications:,}")
    print(f"[+] Approved Loans: {approved_loans:,} ({approval_rate}%)")
    print(f"[+] Rejected Loans: {rejected_loans:,} ({rejection_rate}%)")
    print(f"[+] Total Funded Loan Amount: ${total_funded_amount:,.2f} (${total_funded_amount / 1e6:.2f}M)")
    print(f"[+] Average Funded Loan Amount: ${avg_funded_amount:,.2f}")
    print(f"[+] Average Interest Rate: {avg_interest_rate}%")
    print(f"[+] Average Loan Tenure: {avg_tenure_months} months")
    print(f"[+] Average Monthly Installment: ${avg_monthly_installment:,.2f}")

    return {
        "total_applications": total_applications,
        "approved_loans": approved_loans,
        "rejected_loans": rejected_loans,
        "pending_loans": pending_loans,
        "approval_rate": approval_rate,
        "rejection_rate": rejection_rate,
        "pending_rate": pending_rate,
        "total_applied_amount": total_applied_amount,
        "avg_applied_amount": avg_applied_amount,
        "total_funded_amount": total_funded_amount,
        "avg_funded_amount": avg_funded_amount,
        "avg_interest_rate": avg_interest_rate,
        "avg_tenure_months": avg_tenure_months,
        "avg_monthly_installment": avg_monthly_installment,
        "total_est_annual_interest": total_est_annual_interest,
        "loan_type_summary": loan_type_summary,
        "purpose_summary": purpose_summary,
        "region_loan_summary": region_loan_summary,
        "branch_loan_summary": branch_loan_summary
    }

if __name__ == "__main__":
    import os
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "bank_customer_loan_clean.csv")
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path)
        analyze_loans(df)
