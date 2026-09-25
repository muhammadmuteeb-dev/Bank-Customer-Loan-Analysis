"""
Bank Customer & Loan Analysis - Exploratory Data Analysis & Visualizations Module
Generates 18 publication-grade charts saved to outputs/charts/
using Matplotlib and Seaborn with custom banking/financial styling.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

# Set global aesthetics
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#CCCCCC"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#E5E5E5"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.7

NAVY = "#1B365D"
TEAL = "#008080"
SLATE = "#4A6572"
CORAL = "#E74C3C"
GOLD = "#F39C12"
GREEN = "#27AE60"
LIGHT_BLUE = "#3498DB"
PALETTE = [NAVY, TEAL, LIGHT_BLUE, GOLD, CORAL, GREEN, SLATE]

def generate_all_charts(df: pd.DataFrame, output_dir: str):
    """
    Renders and exports 18 high-resolution analytical charts.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Generating 18 analytical charts to: {os.path.abspath(output_dir)}...")

    df_approved = df[df["Loan_Status"] == "Approved"].copy()

    # -------------------------------------------------------------
    # 1. Customer Age Distribution
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    ax = sns.histplot(df["Age"], bins=30, kde=True, color=NAVY, alpha=0.6, edgecolor="white")
    mean_age = df["Age"].mean()
    median_age = df["Age"].median()
    plt.axvline(mean_age, color=CORAL, linestyle="--", linewidth=2, label=f"Mean: {mean_age:.1f} yrs")
    plt.axvline(median_age, color=GOLD, linestyle="-.", linewidth=2, label=f"Median: {median_age:.0f} yrs")
    plt.title("Customer Age Distribution (N = {:,})".format(len(df)), fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Customer Age (Years)", fontsize=11)
    plt.ylabel("Number of Customers", fontsize=11)
    plt.legend(frameon=True, facecolor="white", edgecolor="#DDD")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "01_age_distribution.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 2. Annual Income Distribution
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Annual_Income"] / 1000, bins=35, kde=True, color=TEAL, alpha=0.6, edgecolor="white")
    plt.axvline(df["Annual_Income"].median() / 1000, color=CORAL, linestyle="--", linewidth=2, 
                label=f"Median Income: ${df['Annual_Income'].median():,.0f}")
    plt.title("Annual Income Distribution", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Annual Income ($ in Thousands)", fontsize=11)
    plt.ylabel("Customer Count", fontsize=11)
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x:,.0f}k"))
    plt.legend(frameon=True, facecolor="white", edgecolor="#DDD")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "02_income_distribution.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 3. Account Balance Distribution by Account Type
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 6))
    order = ["Checking", "Savings", "Money Market", "Certificate of Deposit"]
    existing_order = [o for o in order if o in df["Account_Type"].unique()]
    sns.boxplot(x="Account_Type", y="Account_Balance", data=df, order=existing_order, palette=PALETTE[:len(existing_order)], showmeans=True,
                meanprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "black", "markersize": "7"})
    plt.title("Account Balance Distribution by Product Type", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Account Type", fontsize=11)
    plt.ylabel("Account Balance ($)", fontsize=11)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"${y:,.0f}"))
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "03_account_balance_distribution.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 4. Credit Score Distribution
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Credit_Score"], bins=35, kde=True, color=LIGHT_BLUE, alpha=0.7, edgecolor="white")
    plt.axvspan(300, 579, color="#E74C3C", alpha=0.12, label="Poor (300-579)")
    plt.axvspan(580, 669, color="#E67E22", alpha=0.12, label="Fair (580-669)")
    plt.axvspan(670, 739, color="#F1C40F", alpha=0.12, label="Good (670-739)")
    plt.axvspan(740, 799, color="#2ECC71", alpha=0.12, label="Very Good (740-799)")
    plt.axvspan(800, 850, color="#27AE60", alpha=0.15, label="Excellent (800-850)")
    plt.title("Credit Score Distribution Across FICO Bands", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Credit Score", fontsize=11)
    plt.ylabel("Number of Customers", fontsize=11)
    plt.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#DDD")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "04_credit_score_distribution.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 5. Customer Segments
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    seg_counts = df["Customer_Segment"].value_counts()[["High Value", "Premium", "Standard", "Emerging", "High Risk"]]
    colors = [GOLD, TEAL, NAVY, LIGHT_BLUE, CORAL]
    bars = plt.bar(seg_counts.index, seg_counts.values, color=colors, edgecolor="none", width=0.6)
    for bar in bars:
        height = bar.get_height()
        pct = (height / len(df)) * 100
        plt.text(bar.get_x() + bar.get_width() / 2.0, height + 100, f"{height:,}\n({pct:.1f}%)", 
                 ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.title("Customer Distribution by Behavioral Segment", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Customer Segment", fontsize=11)
    plt.ylabel("Customer Count", fontsize=11)
    plt.ylim(0, max(seg_counts.values) * 1.18)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "05_customer_segments.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 6. Loan Type Distribution (Applications & Volume)
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 6))
    type_agg = df.groupby("Loan_Type")["Loan_Amount"].agg(["count", "sum"]).reset_index()
    type_agg["sum_M"] = type_agg["sum"] / 1_000_000
    type_agg = type_agg.sort_values(by="sum_M", ascending=False)
    
    fig, ax1 = plt.subplots(figsize=(11, 6))
    ax2 = ax1.twinx()
    
    x = np.arange(len(type_agg))
    w = 0.35
    b1 = ax1.bar(x - w/2, type_agg["count"], width=w, color=NAVY, label="Applications (Count)")
    b2 = ax2.bar(x + w/2, type_agg["sum_M"], width=w, color=TEAL, label="Total Volume ($M)")
    
    ax1.set_xlabel("Loan Product", fontsize=11)
    ax1.set_ylabel("Applications Count", fontsize=11, color=NAVY)
    ax2.set_ylabel("Loan Volume ($ Millions)", fontsize=11, color=TEAL)
    ax1.set_xticks(x)
    ax1.set_xticklabels(type_agg["Loan_Type"], fontsize=10)
    plt.title("Loan Portfolio Demand: Application Volume vs Capital Value", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "06_loan_type_distribution.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 7. Loan Approval Status
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 8))
    status_counts = df["Loan_Status"].value_counts()
    status_colors = [GREEN, CORAL, GOLD]
    wedges, texts, autotexts = plt.pie(
        status_counts, labels=status_counts.index, autopct="%1.1f%%",
        startangle=140, colors=status_colors, explode=(0.04, 0.04, 0.04),
        textprops=dict(color="#333", fontsize=12)
    )
    plt.setp(autotexts, size=11, weight="bold", color="white")
    plt.title("Loan Underwriting Decision Breakdown", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "07_loan_approval_status.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 8. Loan Amount Distribution
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Loan_Amount"] / 1000, bins=40, kde=True, color=NAVY, alpha=0.6, edgecolor="white")
    plt.axvline(df["Loan_Amount"].median() / 1000, color=CORAL, linestyle="--", linewidth=2,
                label=f"Median: ${df['Loan_Amount'].median():,.0f}")
    plt.title("Requested Loan Amount Distribution", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Loan Amount ($ in Thousands)", fontsize=11)
    plt.ylabel("Number of Applications", fontsize=11)
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x:,.0f}k"))
    plt.legend(frameon=True, facecolor="white", edgecolor="#DDD")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "08_loan_amount_distribution.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 9. Loan Amount by Loan Type
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 6))
    sns.boxplot(x="Loan_Type", y="Loan_Amount", data=df, palette=PALETTE[:5], showmeans=True,
                meanprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "black", "markersize": "7"})
    plt.title("Loan Amount Distribution by Product Line", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Loan Type", fontsize=11)
    plt.ylabel("Loan Amount ($)", fontsize=11)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"${y:,.0f}"))
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "09_loan_amount_by_type.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 10. Loan Approval Rate by Credit Category
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    cs_order = ["Poor (300-579)", "Fair (580-669)", "Good (670-739)", "Very Good (740-799)", "Excellent (800-850)"]
    appr_by_cs = df.groupby("Credit_Score_Category", observed=False)["Loan_Approval_Flag"].mean() * 100
    bars = plt.bar(cs_order, [appr_by_cs.get(c, 0) for c in cs_order], color=[CORAL, GOLD, LIGHT_BLUE, TEAL, GREEN], width=0.55)
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, h + 1.5, f"{h:.1f}%", ha="center", va="bottom", fontsize=11, fontweight="bold")
    plt.title("Underwriting Approval Rate by Credit Tier", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Credit Score Band", fontsize=11)
    plt.ylabel("Approval Rate (%)", fontsize=11)
    plt.ylim(0, 105)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "10_approval_by_credit_category.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 11. Default Rate by Risk Category
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    risk_order = ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"]
    def_by_risk = df_approved.groupby("Risk_Category")["Default_Flag"].mean() * 100
    def_vals = [def_by_risk.get(r, 0) for r in risk_order]
    bars = plt.bar(risk_order, def_vals, color=[GREEN, GOLD, "#E67E22", CORAL], width=0.55)
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, h + 0.8, f"{h:.1f}%", ha="center", va="bottom", fontsize=11, fontweight="bold")
    plt.title("Delinquency Default Rate by Internal Risk Rating", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Risk Category", fontsize=11)
    plt.ylabel("Default Rate (%) on Approved Loans", fontsize=11)
    plt.ylim(0, max(def_vals) * 1.25)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "11_default_rate_by_risk.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 12. Default Rate by Loan Type
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    def_by_type = (df_approved.groupby("Loan_Type")["Default_Flag"].mean() * 100).sort_values(ascending=False)
    bars = plt.bar(def_by_type.index, def_by_type.values, color=CORAL, alpha=0.85, width=0.55)
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, h + 0.3, f"{h:.2f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.title("Default Rate by Loan Product Line", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Loan Type", fontsize=11)
    plt.ylabel("Default Rate (%)", fontsize=11)
    plt.ylim(0, max(def_by_type.values) * 1.25)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "12_default_rate_by_loan_type.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 13. Customers and Deposits by Region
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    reg_summary = df.groupby("Region").agg(
        Cust_Count=("Customer_ID", "count"),
        Deposits_M=("Account_Balance", lambda x: x.sum() / 1_000_000)
    ).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    x = np.arange(len(reg_summary))
    w = 0.35
    ax1.bar(x - w/2, reg_summary["Cust_Count"], width=w, color=NAVY, label="Customers")
    ax2.bar(x + w/2, reg_summary["Deposits_M"], width=w, color=TEAL, label="Deposits ($M)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(reg_summary["Region"], fontsize=11)
    ax1.set_ylabel("Customer Count", fontsize=11, color=NAVY)
    ax2.set_ylabel("Total Deposit Volume ($ Millions)", fontsize=11, color=TEAL)
    plt.title("Geographic Performance: Customer Base & Deposits by Region", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "13_customers_by_region.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 14. Loan Volume by Region
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    reg_loans = (df.groupby("Region")["Loan_Amount"].sum() / 1_000_000).sort_values(ascending=False)
    bars = plt.bar(reg_loans.index, reg_loans.values, color=SLATE, width=0.55)
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, h + 10, f"${h:,.1f}M", ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.title("Total Loan Application Volume by Geographic Region", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Region", fontsize=11)
    plt.ylabel("Loan Capital Requested ($ Millions)", fontsize=11)
    plt.ylim(0, max(reg_loans.values) * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "14_loan_amount_by_region.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 15. Income vs Loan Amount by Loan Status
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    sample_df = df.sample(min(2500, len(df)), random_state=42)
    sns.scatterplot(
        x=sample_df["Annual_Income"] / 1000,
        y=sample_df["Loan_Amount"] / 1000,
        hue=sample_df["Loan_Status"],
        palette={"Approved": GREEN, "Rejected": CORAL, "Pending": GOLD},
        alpha=0.6,
        s=40
    )
    plt.title("Annual Income vs Loan Amount (Sampled N=2,500)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Annual Income ($k)", fontsize=11)
    plt.ylabel("Loan Amount ($k)", fontsize=11)
    plt.legend(title="Loan Status", frameon=True, facecolor="white", edgecolor="#DDD")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "15_income_vs_loan_amount.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 16. Credit Score vs Loan Amount
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x=sample_df["Credit_Score"],
        y=sample_df["Loan_Amount"] / 1000,
        hue=sample_df["Loan_Status"],
        palette={"Approved": GREEN, "Rejected": CORAL, "Pending": GOLD},
        alpha=0.6,
        s=40
    )
    plt.axvline(640, color="#E67E22", linestyle="--", linewidth=1.5, label="Subprime Threshold (640)")
    plt.title("Credit Score vs Requested Loan Amount", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Credit Score (FICO)", fontsize=11)
    plt.ylabel("Loan Amount ($k)", fontsize=11)
    plt.legend(frameon=True, facecolor="white", edgecolor="#DDD")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "16_credit_score_vs_loan_amount.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 17. Debt-to-Income (DTI) vs Default Rate
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    dti_order = ["Low (<20%)", "Moderate (20-35%)", "Manageable (36-49%)", "Critical (>=50%)"]
    dti_summary = df_approved.groupby("Debt_to_Income_Category", observed=False)["Default_Flag"].mean() * 100
    bars = plt.bar(dti_order, [dti_summary.get(d, 0) for d in dti_order], color=[GREEN, LIGHT_BLUE, GOLD, CORAL], width=0.55)
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, h + 0.3, f"{h:.2f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.title("Default Probability by Debt-to-Income (DTI) Leverage Band", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("DTI Category", fontsize=11)
    plt.ylabel("Default Rate (%) on Approved Loans", fontsize=11)
    plt.ylim(0, max(dti_summary.values) * 1.25)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "17_debt_to_income_distribution.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 18. Branch Performance Matrix (Volume vs Approval Rate)
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 7))
    b_perf = df.groupby(["Branch_ID", "Branch_Name", "Region"]).agg(
        Total_Volume_M=("Loan_Amount", lambda x: x.sum() / 1_000_000),
        Approval_Rate=("Loan_Approval_Flag", lambda x: x.mean() * 100),
        Cust_Count=("Customer_ID", "count")
    ).reset_index()

    sns.scatterplot(
        data=b_perf, x="Total_Volume_M", y="Approval_Rate", hue="Region",
        size="Cust_Count", sizes=(100, 500), palette=PALETTE[:4], alpha=0.85
    )
    for _, row in b_perf.iterrows():
        plt.text(row["Total_Volume_M"] + 1.5, row["Approval_Rate"], row["Branch_Name"].replace(" Branch", ""),
                 fontsize=8.5, alpha=0.85)
    plt.title("Branch Performance Matrix: Loan Capital vs Underwriting Approval Rate", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Total Loan Volume ($ Millions)", fontsize=11)
    plt.ylabel("Approval Rate (%)", fontsize=11)
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "18_branch_performance_matrix.png"), dpi=300)
    plt.close()

    print(f"[OK] Successfully saved all 18 publication-quality charts to {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "bank_customer_loan_clean.csv")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path)
        generate_all_charts(df, out_dir)
