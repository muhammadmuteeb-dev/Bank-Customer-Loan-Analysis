"""
Bank Customer & Loan Analysis - Customer Analysis Module
Analyzes customer demographics, income distribution, deposit balances,
product ownership, and digital banking engagement across regions and branches.
"""

import pandas as pd
import numpy as np

def analyze_customers(df: pd.DataFrame) -> dict:
    """
    Performs comprehensive customer demographic and wealth analysis.
    Returns a dictionary of aggregated metrics and summary DataFrames.
    """
    print("=" * 70)
    print("BANK CUSTOMER & LOAN ANALYSIS - CUSTOMER DEMOGRAPHIC & WEALTH ANALYSIS")
    print("=" * 70)

    total_customers = len(df)
    
    # 1. Demographics Overview
    gender_counts = df["Gender"].value_counts()
    gender_pct = (gender_counts / total_customers * 100).round(2)

    age_stats = {
        "mean": round(df["Age"].mean(), 1),
        "median": int(df["Age"].median()),
        "std": round(df["Age"].std(), 1),
        "min": int(df["Age"].min()),
        "max": int(df["Age"].max())
    }

    age_group_dist = df["Age_Group"].value_counts(sort=False)
    age_group_pct = (age_group_dist / total_customers * 100).round(2)

    # 2. Financial Metrics
    income_stats = {
        "mean": round(df["Annual_Income"].mean(), 2),
        "median": round(df["Annual_Income"].median(), 2),
        "std": round(df["Annual_Income"].std(), 2),
        "min": round(df["Annual_Income"].min(), 2),
        "max": round(df["Annual_Income"].max(), 2),
        "total": round(df["Annual_Income"].sum(), 2)
    }

    balance_stats = {
        "mean": round(df["Account_Balance"].mean(), 2),
        "median": round(df["Account_Balance"].median(), 2),
        "std": round(df["Account_Balance"].std(), 2),
        "min": round(df["Account_Balance"].min(), 2),
        "max": round(df["Account_Balance"].max(), 2),
        "total": round(df["Account_Balance"].sum(), 2)
    }

    # 3. Product & Channel Engagement
    credit_card_pen = round((df["Credit_Card"] == "Yes").mean() * 100, 2)
    debit_card_pen = round((df["Debit_Card"] == "Yes").mean() * 100, 2)
    online_pen = round((df["Online_Banking"] == "Yes").mean() * 100, 2)
    mobile_pen = round((df["Mobile_Banking"] == "Yes").mean() * 100, 2)
    avg_products = round(df["Number_of_Products"].mean(), 2)

    # 4. Regional Customer Distribution
    region_summary = df.groupby("Region").agg(
        Customer_Count=("Customer_ID", "count"),
        Avg_Income=("Annual_Income", "mean"),
        Total_Deposits=("Account_Balance", "sum"),
        Avg_Balance=("Account_Balance", "mean"),
        Avg_Credit_Score=("Credit_Score", "mean"),
        Avg_Products=("Number_of_Products", "mean")
    ).reset_index()

    region_summary["Customer_Pct"] = (region_summary["Customer_Count"] / total_customers * 100).round(2)
    region_summary["Avg_Income"] = region_summary["Avg_Income"].round(2)
    region_summary["Total_Deposits_M"] = (region_summary["Total_Deposits"] / 1_000_000).round(2)
    region_summary["Avg_Balance"] = region_summary["Avg_Balance"].round(2)
    region_summary["Avg_Credit_Score"] = region_summary["Avg_Credit_Score"].round(1)
    region_summary["Avg_Products"] = region_summary["Avg_Products"].round(2)

    # 5. Branch Summary
    branch_summary = df.groupby(["Branch_ID", "Branch_Name", "City", "State", "Region"]).agg(
        Customer_Count=("Customer_ID", "count"),
        Avg_Income=("Annual_Income", "mean"),
        Total_Deposits=("Account_Balance", "sum"),
        Avg_Balance=("Account_Balance", "mean")
    ).reset_index().sort_values(by="Customer_Count", ascending=False)

    branch_summary["Total_Deposits_M"] = (branch_summary["Total_Deposits"] / 1_000_000).round(2)
    branch_summary["Avg_Income"] = branch_summary["Avg_Income"].round(2)
    branch_summary["Avg_Balance"] = branch_summary["Avg_Balance"].round(2)

    print(f"[+] Total Customer Base: {total_customers:,}")
    print(f"[+] Mean Age: {age_stats['mean']} years | Median: {age_stats['median']} years")
    print(f"[+] Mean Income: ${income_stats['mean']:,.2f} | Median: ${income_stats['median']:,.2f}")
    print(f"[+] Mean Balance: ${balance_stats['mean']:,.2f} | Median: ${balance_stats['median']:,.2f}")
    print(f"[+] Digital Banking Adoption: Online {online_pen}% | Mobile {mobile_pen}%")
    print(f"[+] Card Penetration: Debit {debit_card_pen}% | Credit {credit_card_pen}%")
    print(f"[+] Average Products Per Customer: {avg_products}")

    return {
        "total_customers": total_customers,
        "age_stats": age_stats,
        "income_stats": income_stats,
        "balance_stats": balance_stats,
        "gender_breakdown": gender_pct.to_dict(),
        "age_group_dist": age_group_pct.to_dict(),
        "digital_adoption": {
            "credit_card_pct": credit_card_pen,
            "debit_card_pct": debit_card_pen,
            "online_banking_pct": online_pen,
            "mobile_banking_pct": mobile_pen,
            "avg_products": avg_products
        },
        "region_summary": region_summary,
        "branch_summary": branch_summary
    }

if __name__ == "__main__":
    import os
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "bank_customer_loan_clean.csv")
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path)
        analyze_customers(df)
