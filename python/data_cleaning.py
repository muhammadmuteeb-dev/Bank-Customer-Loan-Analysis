"""
Bank Customer & Loan Analysis - Data Cleaning & Feature Engineering Module
Inspects raw data, handles duplicates, missing values, incorrect types, outliers,
standardizes categorical variables, performs domain feature engineering,
and exports cleaned dataset + Power BI Star Schema dimension/fact tables.
"""

import os
import re
import numpy as np
import pandas as pd
from datetime import datetime

def clean_bank_data(raw_csv_path: str, clean_csv_path: str = None) -> pd.DataFrame:
    """
    Executes end-to-end cleaning and feature engineering pipeline on raw banking data.
    """
    print("=" * 70)
    print("BANK CUSTOMER & LOAN ANALYSIS - DATA CLEANING PIPELINE")
    print("=" * 70)
    
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw data file not found at: {raw_csv_path}")

    # 1. Load Raw Data
    df_raw = pd.read_csv(raw_csv_path, low_memory=False)
    initial_rows, initial_cols = df_raw.shape
    print(f"[*] Loaded raw dataset: {initial_rows:,} rows × {initial_cols} columns")

    df = df_raw.copy()

    # 2. Check & Remove Duplicates
    n_exact_dups = df.duplicated().sum()
    n_cust_dups = df.duplicated(subset=["Customer_ID"]).sum()
    print(f"[*] Detected duplicate records: {n_exact_dups:,} exact duplicates, {n_cust_dups:,} Customer_ID duplicates.")
    
    df = df.drop_duplicates(subset=["Customer_ID"], keep="first").reset_index(drop=True)
    print(f"[+] Deduplication complete: {len(df):,} unique customer records retained ({initial_rows - len(df):,} duplicates removed).")

    # 3. Clean and Cast Annual_Income
    print("[*] Sanitizing and casting 'Annual_Income'...")
    def parse_income(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip().replace("$", "").replace(",", "")
        try:
            return float(val_str)
        except ValueError:
            return np.nan

    df["Annual_Income"] = df["Annual_Income"].apply(parse_income)
    # If any nulls remain, impute with median income
    median_income = df["Annual_Income"].median()
    df["Annual_Income"] = df["Annual_Income"].fillna(median_income)

    # 4. Clean and Standardize Age & DOB
    print("[*] Validating 'Age' and 'Date_of_Birth'...")
    # Fix outlier ages (< 18 or > 80)
    invalid_age_mask = (df["Age"] < 18) | (df["Age"] > 80)
    if invalid_age_mask.sum() > 0:
        print(f"    - Found {invalid_age_mask.sum()} records with invalid age. Recalibrating from median...")
        df.loc[invalid_age_mask, "Age"] = int(df["Age"].median())
    df["Age"] = df["Age"].astype(int)

    # Convert Date columns
    date_columns = ["Date_of_Birth", "Account_Open_Date", "Loan_Application_Date", "Approval_Date", "Last_Transaction_Date"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # 5. Clean Account_Balance and DTI Outliers
    print("[*] Validating numerical financial columns...")
    # Balance cannot be negative for standard checking/savings
    df["Account_Balance"] = df["Account_Balance"].apply(lambda x: max(0.0, float(x)) if pd.notnull(x) else 0.0)
    df["Savings_Balance"] = df["Savings_Balance"].apply(lambda x: max(0.0, float(x)) if pd.notnull(x) else 0.0)
    df["Current_Account_Balance"] = df["Current_Account_Balance"].apply(lambda x: max(0.0, float(x)) if pd.notnull(x) else 0.0)

    # DTI Ratio bounded between 0.01 and 0.85
    df["Debt_to_Income_Ratio"] = df["Debt_to_Income_Ratio"].apply(lambda x: min(max(float(x), 0.01), 0.85) if pd.notnull(x) else 0.35)
    df["Outstanding_Debt"] = np.round(df["Annual_Income"] * df["Debt_to_Income_Ratio"], 2)

    # 6. Standardize Categorical Columns
    print("[*] Standardizing categorical values...")
    # Gender
    gender_map = {
        "M": "Male", "m": "Male", "male": "Male", "Male": "Male", "Male ": "Male",
        "F": "Female", "f": "Female", "female": "Female", "Female": "Female", "Female ": "Female"
    }
    df["Gender"] = df["Gender"].astype(str).str.strip().map(gender_map).fillna("Male")

    # Employment Status
    emp_map = {
        "self employed": "Self-Employed",
        "Self_Employed": "Self-Employed",
        "self-employed": "Self-Employed",
        "Self-Employed": "Self-Employed",
        "Salaried": "Salaried",
        "Employed": "Salaried", # Standardize to Salaried
        "Contract": "Contract",
        "Unemployed": "Unemployed",
        "Retired": "Retired"
    }
    df["Employment_Status"] = df["Employment_Status"].astype(str).str.strip().map(emp_map).fillna("Salaried")

    # Clean string columns: trim whitespace
    str_cols = ["Marital_Status", "Education", "Occupation", "City", "State", "Region", "Branch_Name",
                "Account_Type", "Credit_Card", "Debit_Card", "Online_Banking", "Mobile_Banking",
                "Loan_Type", "Loan_Status", "Loan_Purpose", "Risk_Category", "Customer_Segment", "Customer_Status"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 7. Missing Value Imputation
    print("[*] Imputing missing values...")
    # Marital Status
    if "Marital_Status" in df.columns:
        df["Marital_Status"] = df["Marital_Status"].replace(["nan", "None", ""], "Married")
    # Education
    if "Education" in df.columns:
        df["Education"] = df["Education"].replace(["nan", "None", ""], "Bachelor")
    # Online Banking
    if "Online_Banking" in df.columns:
        df["Online_Banking"] = df["Online_Banking"].replace(["nan", "None", ""], "Yes")

    # 8. Feature Engineering
    print("[*] Engineering domain features...")

    # Age_Group
    age_bins = [17, 25, 35, 50, 65, 100]
    age_labels = ["18-25", "26-35", "36-50", "51-65", "65+"]
    df["Age_Group"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, right=True)

    # Income_Group
    inc_bins = [0, 35000, 60000, 100000, 150000, np.inf]
    inc_labels = ["Low (<$35k)", "Lower-Middle ($35k-$60k)", "Middle ($60k-$100k)", "Upper-Middle ($100k-$150k)", "High (>=$150k)"]
    df["Income_Group"] = pd.cut(df["Annual_Income"], bins=inc_bins, labels=inc_labels, right=False)

    # Credit_Score_Category
    cs_bins = [299, 579, 669, 739, 799, 851]
    cs_labels = ["Poor (300-579)", "Fair (580-669)", "Good (670-739)", "Very Good (740-799)", "Excellent (800-850)"]
    df["Credit_Score_Category"] = pd.cut(df["Credit_Score"], bins=cs_bins, labels=cs_labels, right=True)

    # Balance_Category
    bal_bins = [0, 5000, 25000, 75000, 150000, np.inf]
    bal_labels = ["Low (<$5k)", "Moderate ($5k-$25k)", "Healthy ($25k-$75k)", "High ($75k-$150k)", "Affluent (>=$150k)"]
    df["Balance_Category"] = pd.cut(df["Account_Balance"], bins=bal_bins, labels=bal_labels, right=False)

    # Loan_Amount_Category
    loan_bins = [0, 10000, 25000, 75000, 200000, np.inf]
    loan_labels = ["Micro (<$10k)", "Small ($10k-$25k)", "Medium ($25k-$75k)", "Large ($75k-$200k)", "Jumbo (>=$200k)"]
    df["Loan_Amount_Category"] = pd.cut(df["Loan_Amount"], bins=loan_bins, labels=loan_labels, right=False)

    # Customer_Tenure_Group
    tenure_bins = [0, 1.0, 3.0, 7.0, 10.0, np.inf]
    tenure_labels = ["New (<1 yr)", "Developing (1-3 yrs)", "Established (3-7 yrs)", "Loyal (7-10 yrs)", "Veteran (10+ yrs)"]
    df["Customer_Tenure_Group"] = pd.cut(df["Customer_Tenure_Years"], bins=tenure_bins, labels=tenure_labels, right=False)

    # Debt_to_Income_Category
    dti_bins = [0, 0.20, 0.35, 0.50, np.inf]
    dti_labels = ["Low (<20%)", "Moderate (20-35%)", "Manageable (36-49%)", "Critical (>=50%)"]
    df["Debt_to_Income_Category"] = pd.cut(df["Debt_to_Income_Ratio"], bins=dti_bins, labels=dti_labels, right=False)

    # Customer_Value_Category
    def get_customer_value(row):
        inc = row["Annual_Income"]
        bal = row["Account_Balance"]
        if inc >= 140000 or bal >= 90000:
            return "Platinum"
        elif inc >= 85000 or bal >= 45000:
            return "Gold"
        elif inc >= 45000 or bal >= 15000:
            return "Silver"
        else:
            return "Bronze"

    df["Customer_Value_Category"] = df.apply(get_customer_value, axis=1)

    # Loan_Approval_Flag & Binary Default Flag
    df["Loan_Approval_Flag"] = (df["Loan_Status"] == "Approved").astype(int)
    # Default flag only applies to approved loans
    df["Default_Flag"] = np.where(df["Loan_Status"] == "Approved", df["Default_Flag"].astype(int), 0)

    # Monthly_Income & Estimated_Annual_Interest
    df["Monthly_Income"] = np.round(df["Annual_Income"] / 12.0, 2)
    df["Estimated_Annual_Interest"] = np.round(df["Loan_Amount"] * (df["Interest_Rate"] / 100.0), 2)

    # Validate Dates strings for CSV export
    for col in date_columns:
        if col in df.columns:
            df[col] = df[col].dt.strftime("%Y-%m-%d").fillna("")

    print(f"[+] Feature engineering complete: {df.shape[1]} total columns.")

    # 9. Save Cleaned Dataset
    if clean_csv_path:
        os.makedirs(os.path.dirname(clean_csv_path), exist_ok=True)
        df.to_csv(clean_csv_path, index=False)
        print(f"[OK] Processed dataset saved to: {os.path.abspath(clean_csv_path)}")

    return df

def export_powerbi_star_schema(df: pd.DataFrame, output_dir: str):
    """
    Exports normalized dimension and fact tables for Star-Schema modeling in Power BI.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Exporting Star Schema tables to: {os.path.abspath(output_dir)}...")

    # 1. DimCustomer
    dim_customer_cols = [
        "Customer_ID", "First_Name", "Last_Name", "Gender", "Age", "Age_Group",
        "Date_of_Birth", "Marital_Status", "Education", "Occupation", "Employment_Status",
        "Annual_Income", "Income_Group", "Monthly_Income", "Customer_Segment",
        "Customer_Value_Category", "Customer_Status", "Customer_Tenure_Years",
        "Customer_Tenure_Group", "Credit_Score", "Credit_Score_Category",
        "Account_Type", "Account_Open_Date", "Account_Balance", "Balance_Category",
        "Savings_Balance", "Current_Account_Balance", "Number_of_Products",
        "Credit_Card", "Debit_Card", "Online_Banking", "Mobile_Banking", "Last_Transaction_Date"
    ]
    dim_customer = df[dim_customer_cols].copy()
    dim_customer.to_csv(os.path.join(output_dir, "DimCustomer.csv"), index=False)
    print(f"    - DimCustomer.csv ({len(dim_customer):,} rows)")

    # 2. DimBranch
    dim_branch_cols = ["Branch_ID", "Branch_Name", "City", "State", "Region"]
    dim_branch = df[dim_branch_cols].drop_duplicates(subset=["Branch_ID"]).sort_values("Branch_ID").reset_index(drop=True)
    dim_branch.to_csv(os.path.join(output_dir, "DimBranch.csv"), index=False)
    print(f"    - DimBranch.csv ({len(dim_branch):,} rows)")

    # 3. DimLoanType
    loan_types_data = [
        {"Loan_Type": "Home Loan", "Secured_Status": "Secured", "Collateral_Type": "Real Estate", "Base_Risk_Rating": "Low"},
        {"Loan_Type": "Auto Loan", "Secured_Status": "Secured", "Collateral_Type": "Vehicle", "Base_Risk_Rating": "Moderate"},
        {"Loan_Type": "Business Loan", "Secured_Status": "Semi-Secured", "Collateral_Type": "Commercial Assets", "Base_Risk_Rating": "Moderate-High"},
        {"Loan_Type": "Education Loan", "Secured_Status": "Unsecured", "Collateral_Type": "None", "Base_Risk_Rating": "Moderate"},
        {"Loan_Type": "Personal Loan", "Secured_Status": "Unsecured", "Collateral_Type": "None", "Base_Risk_Rating": "High"}
    ]
    dim_loan_type = pd.DataFrame(loan_types_data)
    dim_loan_type.to_csv(os.path.join(output_dir, "DimLoanType.csv"), index=False)
    print(f"    - DimLoanType.csv ({len(dim_loan_type):,} rows)")

    # 4. DimDate (covering 2020-01-01 to 2025-12-31)
    date_range = pd.date_range(start="2020-01-01", end="2025-12-31", freq="D")
    dim_date = pd.DataFrame({
        "Date": date_range.strftime("%Y-%m-%d"),
        "Year": date_range.year,
        "Quarter": "Q" + date_range.quarter.astype(str),
        "Month_Number": date_range.month,
        "Month_Name": date_range.strftime("%B"),
        "Month_Short": date_range.strftime("%b"),
        "Day_of_Month": date_range.day,
        "Day_Name": date_range.strftime("%A"),
        "Day_of_Week": date_range.dayofweek + 1,
        "Year_Month": date_range.strftime("%Y-%m"),
        "Is_Weekend": np.where(date_range.dayofweek >= 5, "Weekend", "Weekday")
    })
    dim_date.to_csv(os.path.join(output_dir, "DimDate.csv"), index=False)
    print(f"    - DimDate.csv ({len(dim_date):,} rows)")

    # 5. FactLoan
    fact_loan_cols = [
        "Loan_ID", "Customer_ID", "Branch_ID", "Loan_Type", "Loan_Purpose",
        "Loan_Application_Date", "Approval_Date", "Loan_Amount", "Loan_Amount_Category",
        "Interest_Rate", "Loan_Tenure_Months", "Monthly_Installment", "Loan_Status",
        "Loan_Approval_Flag", "Risk_Category", "Default_Probability", "Default_Flag",
        "Outstanding_Debt", "Debt_to_Income_Ratio", "Debt_to_Income_Category", "Estimated_Annual_Interest"
    ]
    fact_loan = df[fact_loan_cols].copy()
    fact_loan.to_csv(os.path.join(output_dir, "FactLoan.csv"), index=False)
    print(f"    - FactLoan.csv ({len(fact_loan):,} rows)")

    print("[OK] Star Schema table generation complete.")

def main():
    base_dir = os.path.dirname(__file__)
    raw_path = os.path.join(base_dir, "..", "data", "raw", "bank_customer_loan_raw.csv")
    clean_path = os.path.join(base_dir, "..", "data", "processed", "bank_customer_loan_clean.csv")
    powerbi_dir = os.path.join(base_dir, "..", "data", "processed", "powerbi_tables")

    df_clean = clean_bank_data(raw_path, clean_path)
    export_powerbi_star_schema(df_clean, powerbi_dir)

if __name__ == "__main__":
    main()
