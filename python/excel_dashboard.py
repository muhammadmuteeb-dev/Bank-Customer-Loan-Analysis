"""
Bank Customer & Loan Analysis - Excel Dashboard Module
Automates the generation of a multi-tab, executive-ready Excel workbook
using openpyxl with KPI metric cards, structured tables, conditional formatting,
native Excel charts, professional banking styling, and data dictionary.
"""

import os
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, PieChart, Reference, Series

def create_excel_dashboard(df: pd.DataFrame, output_path: str):
    """
    Generates the Bank Customer & Loan Analysis Excel Workbook across 8 worksheets.
    """
    print("=" * 70)
    print("BANK CUSTOMER & LOAN ANALYSIS - EXCEL REPORT GENERATION")
    print("=" * 70)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb = Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styling Palettes
    NAVY_PRIMARY = "1B365D"
    NAVY_SECONDARY = "2C5364"
    TEAL_ACCENT = "008080"
    GRAY_LIGHT = "F4F6F9"
    GRAY_BORDER = "D1D5DB"
    WHITE = "FFFFFF"
    DARK_TEXT = "1F2937"
    MUTED_TEXT = "6B7280"
    GREEN_TEXT = "047857"
    RED_TEXT = "B91C1C"

    # Font definitions
    title_font = Font(name="Segoe UI", size=16, bold=True, color=WHITE)
    subtitle_font = Font(name="Segoe UI", size=10, italic=True, color="E2E8F0")
    section_font = Font(name="Segoe UI", size=12, bold=True, color=NAVY_PRIMARY)
    header_font = Font(name="Segoe UI", size=10, bold=True, color=WHITE)
    bold_font = Font(name="Segoe UI", size=10, bold=True, color=DARK_TEXT)
    regular_font = Font(name="Segoe UI", size=10, color=DARK_TEXT)
    kpi_val_font = Font(name="Segoe UI", size=16, bold=True, color=NAVY_PRIMARY)
    kpi_lbl_font = Font(name="Segoe UI", size=9, bold=True, color=MUTED_TEXT)

    # Fills
    title_fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
    header_fill = PatternFill(start_color=NAVY_SECONDARY, end_color=NAVY_SECONDARY, fill_type="solid")
    zebra_fill = PatternFill(start_color=GRAY_LIGHT, end_color=GRAY_LIGHT, fill_type="solid")
    kpi_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    accent_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")

    # Borders
    thin_side = Side(style="thin", color=GRAY_BORDER)
    thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    bottom_heavy = Border(bottom=Side(style="medium", color=NAVY_PRIMARY))

    # Alignments
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    def auto_fit_columns(ws, max_len_cap=35):
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    val_str = str(cell.value)
                    # Ignore title banner length
                    if cell.row in [1, 2]:
                        continue
                    max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(min(max_len + 4, max_len_cap), 12)

    # Key Aggregations for Workbook
    total_cust = len(df)
    df_approved = df[df["Loan_Status"] == "Approved"]
    total_approved = len(df_approved)
    approval_rate = total_approved / total_cust
    total_defaulted = df_approved["Default_Flag"].sum()
    default_rate = total_defaulted / total_approved if total_approved > 0 else 0
    total_loan_vol = df["Loan_Amount"].sum()
    total_funded_vol = df_approved["Loan_Amount"].sum()
    total_deposits = df["Account_Balance"].sum()
    avg_cs = df["Credit_Score"].mean()
    avg_income = df["Annual_Income"].mean()
    avg_loan_amt = df_approved["Loan_Amount"].mean()

    # -------------------------------------------------------------
    # 1. WORKSHEET: Executive Summary
    # -------------------------------------------------------------
    ws1 = wb.create_sheet(title="Executive Summary")
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
    ws1.merge_cells("A1:K2")
    ws1["A1"] = "BANK CUSTOMER & LOAN ANALYSIS — EXECUTIVE DASHBOARD"
    ws1["A1"].font = title_font
    ws1["A1"].fill = title_fill
    ws1["A1"].alignment = align_center

    ws1.merge_cells("A3:K3")
    ws1["A3"] = f"Comprehensive Portfolio Intelligence & Risk Performance Report | Records: {total_cust:,} Customers"
    ws1["A3"].font = subtitle_font
    ws1["A3"].fill = PatternFill(start_color=NAVY_SECONDARY, end_color=NAVY_SECONDARY, fill_type="solid")
    ws1["A3"].alignment = align_center

    # KPI Metric Cards (Row 5 - 7)
    kpis = [
        ("TOTAL CUSTOMERS", f"{total_cust:,}", "A", "B"),
        ("TOTAL LOAN DEMAND", f"${total_loan_vol / 1e6:,.1f}M", "C", "D"),
        ("FUNDED CAPITAL", f"${total_funded_vol / 1e6:,.1f}M", "E", "F"),
        ("APPROVAL RATE", f"{approval_rate * 100:.1f}%", "G", "H"),
        ("PORTFOLIO DEFAULT RATE", f"{default_rate * 100:.2f}%", "I", "I"),
        ("AVG CREDIT SCORE", f"{avg_cs:.0f}", "J", "J"),
        ("TOTAL DEPOSITS", f"${total_deposits / 1e6:,.1f}M", "K", "K"),
    ]

    ws1.row_dimensions[5].height = 20
    ws1.row_dimensions[6].height = 30
    for title, val, start_col, end_col in kpis:
        cell_lbl = f"{start_col}5"
        cell_val = f"{start_col}6"
        if start_col != end_col:
            ws1.merge_cells(f"{start_col}5:{end_col}5")
            ws1.merge_cells(f"{start_col}6:{end_col}6")
        
        ws1[cell_lbl] = title
        ws1[cell_lbl].font = kpi_lbl_font
        ws1[cell_lbl].alignment = align_center
        ws1[cell_lbl].fill = kpi_fill
        ws1[cell_lbl].border = thin_border

        ws1[cell_val] = val
        ws1[cell_val].font = kpi_val_font
        ws1[cell_val].alignment = align_center
        ws1[cell_val].fill = kpi_fill
        ws1[cell_val].border = thin_border

    # Section 1: Portfolio Breakdown by Loan Type (Row 9)
    ws1["A9"] = "Portfolio Overview by Product Type"
    ws1["A9"].font = section_font

    loan_headers = ["Loan Type", "Applications", "Funded Count", "Approval %", "Funded Volume ($)", "Avg Loan ($)", "Avg Rate %", "Default %"]
    for c_idx, h in enumerate(loan_headers, start=1):
        cell = ws1.cell(row=10, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    r_idx = 11
    type_group = df.groupby("Loan_Type")
    for ltype, grp in type_group:
        apps = len(grp)
        appr_grp = grp[grp["Loan_Status"] == "Approved"]
        appr_cnt = len(appr_grp)
        appr_pct = appr_cnt / apps if apps > 0 else 0
        funded_vol = appr_grp["Loan_Amount"].sum()
        avg_funded = appr_grp["Loan_Amount"].mean() if appr_cnt > 0 else 0
        avg_rate = grp["Interest_Rate"].mean()
        def_cnt = appr_grp["Default_Flag"].sum()
        def_pct = def_cnt / appr_cnt if appr_cnt > 0 else 0

        row_vals = [ltype, apps, appr_cnt, appr_pct, funded_vol, avg_funded, avg_rate / 100.0, def_pct]
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws1.cell(row=r_idx, column=col_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if col_idx == 1:
                cell.alignment = align_left
            elif col_idx in [2, 3]:
                cell.alignment = align_right
                cell.number_format = "#,##0"
            elif col_idx in [4, 7, 8]:
                cell.alignment = align_right
                cell.number_format = "0.0%"
            elif col_idx in [5, 6]:
                cell.alignment = align_right
                cell.number_format = "$#,##0"
            if r_idx % 2 == 0:
                cell.fill = zebra_fill
        r_idx += 1

    # Add Chart: Funded Volume by Loan Type
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Funded Loan Capital by Product Line"
    chart1.y_axis.title = "Funded Capital ($)"
    chart1.x_axis.title = "Loan Type"
    chart1.width = 16
    chart1.height = 9

    data_ref = Reference(ws1, min_col=5, min_row=10, max_row=r_idx - 1)
    cats_ref = Reference(ws1, min_col=1, min_row=11, max_row=r_idx - 1)
    chart1.add_data(data_ref, titles_from_data=True)
    chart1.set_categories(cats_ref)
    chart1.legend = None
    ws1.add_chart(chart1, f"A{r_idx + 2}")

    # Section 2: Regional Performance Summary (Row 10, Col I-K)
    ws1["H9"] = "Regional Performance Summary"
    ws1["H9"].font = section_font
    reg_headers = ["Region", "Customers", "Total Deposits ($)", "Loan Apps"]
    for c_idx, h in enumerate(reg_headers, start=8):
        cell = ws1.cell(row=10, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    reg_r = 11
    for reg, grp in df.groupby("Region"):
        c_cnt = len(grp)
        deps = grp["Account_Balance"].sum()
        l_apps = len(grp)
        vals = [reg, c_cnt, deps, l_apps]
        for col_idx, val in enumerate(vals, start=8):
            cell = ws1.cell(row=reg_r, column=col_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if col_idx == 8:
                cell.alignment = align_left
            elif col_idx in [9, 11]:
                cell.alignment = align_right
                cell.number_format = "#,##0"
            elif col_idx == 10:
                cell.alignment = align_right
                cell.number_format = "$#,##0"
        reg_r += 1

    auto_fit_columns(ws1)

    # -------------------------------------------------------------
    # 2. WORKSHEET: Customer Analysis
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Customer Analysis")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:G2")
    ws2["A1"] = "CUSTOMER DEMOGRAPHICS & WEALTH DISTRIBUTION"
    ws2["A1"].font = title_font
    ws2["A1"].fill = title_fill
    ws2["A1"].alignment = align_center

    # Demographic Tables: Age Groups
    ws2["A4"] = "Demographic Profile by Age Group"
    ws2["A4"].font = section_font
    age_headers = ["Age Group", "Customer Count", "Share %", "Avg Income ($)", "Avg Balance ($)", "Avg Products", "Avg Credit Score"]
    for c_idx, h in enumerate(age_headers, start=1):
        cell = ws2.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    r_idx = 6
    age_order = ["18-25", "26-35", "36-50", "51-65", "65+"]
    for grp_name in age_order:
        grp = df[df["Age_Group"] == grp_name]
        cnt = len(grp)
        pct = cnt / total_cust
        avg_inc = grp["Annual_Income"].mean()
        avg_bal = grp["Account_Balance"].mean()
        avg_prod = grp["Number_of_Products"].mean()
        avg_cs_grp = grp["Credit_Score"].mean()
        vals = [grp_name, cnt, pct, avg_inc, avg_bal, avg_prod, avg_cs_grp]
        for c_idx, v in enumerate(vals, start=1):
            cell = ws2.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 1: cell.alignment = align_left
            elif c_idx == 2: cell.number_format = "#,##0"; cell.alignment = align_right
            elif c_idx == 3: cell.number_format = "0.0%"; cell.alignment = align_right
            elif c_idx in [4, 5]: cell.number_format = "$#,##0"; cell.alignment = align_right
            elif c_idx == 6: cell.number_format = "0.00"; cell.alignment = align_right
            elif c_idx == 7: cell.number_format = "0.0"; cell.alignment = align_right
            if r_idx % 2 == 1: cell.fill = zebra_fill
        r_idx += 1

    # Income Groups Table
    r_idx += 2
    ws2.cell(row=r_idx, column=1, value="Income Group Distribution").font = section_font
    r_idx += 1
    inc_headers = ["Income Group", "Customers", "Share %", "Total Deposits ($)", "Avg DTI %", "Credit Card %"]
    for c_idx, h in enumerate(inc_headers, start=1):
        cell = ws2.cell(row=r_idx, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border
    r_idx += 1

    inc_order = ["Low (<$35k)", "Lower-Middle ($35k-$60k)", "Middle ($60k-$100k)", "Upper-Middle ($100k-$150k)", "High (>=$150k)"]
    for ig in inc_order:
        grp = df[df["Income_Group"] == ig]
        cnt = len(grp)
        pct = cnt / total_cust
        tot_dep = grp["Account_Balance"].sum()
        avg_dti = grp["Debt_to_Income_Ratio"].mean()
        cc_pct = (grp["Credit_Card"] == "Yes").mean()
        vals = [ig, cnt, pct, tot_dep, avg_dti, cc_pct]
        for c_idx, v in enumerate(vals, start=1):
            cell = ws2.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 1: cell.alignment = align_left
            elif c_idx == 2: cell.number_format = "#,##0"; cell.alignment = align_right
            elif c_idx in [3, 5, 6]: cell.number_format = "0.0%"; cell.alignment = align_right
            elif c_idx == 4: cell.number_format = "$#,##0"; cell.alignment = align_right
            if r_idx % 2 == 1: cell.fill = zebra_fill
        r_idx += 1

    auto_fit_columns(ws2)

    # -------------------------------------------------------------
    # 3. WORKSHEET: Loan Analysis
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Loan Analysis")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:H2")
    ws3["A1"] = "LOAN PORTFOLIO & UNDERWRITING PERFORMANCE"
    ws3["A1"].font = title_font
    ws3["A1"].fill = title_fill
    ws3["A1"].alignment = align_center

    ws3["A4"] = "Loan Purpose Performance Breakdown"
    ws3["A4"].font = section_font
    purp_headers = ["Loan Purpose", "Applications", "Approval %", "Total Volume ($)", "Avg Amount ($)", "Avg Rate %", "Avg Tenure (Mo)"]
    for c_idx, h in enumerate(purp_headers, start=1):
        cell = ws3.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    r_idx = 6
    for purp, grp in df.groupby("Loan_Purpose"):
        cnt = len(grp)
        appr_cnt = (grp["Loan_Status"] == "Approved").sum()
        appr_pct = appr_cnt / cnt if cnt > 0 else 0
        tot_vol = grp["Loan_Amount"].sum()
        avg_amt = grp["Loan_Amount"].mean()
        avg_rate = grp["Interest_Rate"].mean() / 100.0
        avg_ten = grp["Loan_Tenure_Months"].mean()
        vals = [purp, cnt, appr_pct, tot_vol, avg_amt, avg_rate, avg_ten]
        for c_idx, v in enumerate(vals, start=1):
            cell = ws3.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 1: cell.alignment = align_left
            elif c_idx == 2: cell.number_format = "#,##0"; cell.alignment = align_right
            elif c_idx in [3, 6]: cell.number_format = "0.0%"; cell.alignment = align_right
            elif c_idx in [4, 5]: cell.number_format = "$#,##0"; cell.alignment = align_right
            elif c_idx == 7: cell.number_format = "0.0"; cell.alignment = align_right
            if r_idx % 2 == 1: cell.fill = zebra_fill
        r_idx += 1

    auto_fit_columns(ws3)

    # -------------------------------------------------------------
    # 4. WORKSHEET: Risk Analysis
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="Risk Analysis")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:G2")
    ws4["A1"] = "CREDIT RISK & DELINQUENCY MONITORING"
    ws4["A1"].font = title_font
    ws4["A1"].fill = title_fill
    ws4["A1"].alignment = align_center

    ws4["A4"] = "Portfolio Delinquency by Risk Category"
    ws4["A4"].font = section_font
    risk_headers = ["Risk Category", "Approved Loans", "Defaulted Loans", "Default Rate %", "Defaulted Capital ($)", "Avg Credit Score", "Avg DTI %"]
    for c_idx, h in enumerate(risk_headers, start=1):
        cell = ws4.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    r_idx = 6
    risk_order = ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"]
    for rc in risk_order:
        grp = df_approved[df_approved["Risk_Category"] == rc]
        cnt = len(grp)
        def_cnt = grp["Default_Flag"].sum()
        def_rate = def_cnt / cnt if cnt > 0 else 0
        def_vol = grp[grp["Default_Flag"] == 1]["Loan_Amount"].sum()
        avg_cs_r = grp["Credit_Score"].mean()
        avg_dti_r = grp["Debt_to_Income_Ratio"].mean()
        vals = [rc, cnt, def_cnt, def_rate, def_vol, avg_cs_r, avg_dti_r]
        for c_idx, v in enumerate(vals, start=1):
            cell = ws4.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 1: cell.alignment = align_left
            elif c_idx in [2, 3]: cell.number_format = "#,##0"; cell.alignment = align_right
            elif c_idx in [4, 7]: cell.number_format = "0.0%"; cell.alignment = align_right
            elif c_idx == 5: cell.number_format = "$#,##0"; cell.alignment = align_right
            elif c_idx == 6: cell.number_format = "0.0"; cell.alignment = align_right
            if rc == "Very High Risk":
                cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
            elif rc == "Low Risk":
                cell.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
        r_idx += 1

    # Credit Tier Delinquency
    r_idx += 2
    ws4.cell(row=r_idx, column=1, value="Credit Score Band Default Metrics").font = section_font
    r_idx += 1
    cs_headers = ["Credit Score Band", "Active Loans", "Default Count", "Default Rate %", "Avg Interest Rate %"]
    for c_idx, h in enumerate(cs_headers, start=1):
        cell = ws4.cell(row=r_idx, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border
    r_idx += 1

    cs_bands = ["Poor (300-579)", "Fair (580-669)", "Good (670-739)", "Very Good (740-799)", "Excellent (800-850)"]
    for band in cs_bands:
        grp = df_approved[df_approved["Credit_Score_Category"] == band]
        cnt = len(grp)
        def_cnt = grp["Default_Flag"].sum()
        def_rate = def_cnt / cnt if cnt > 0 else 0
        avg_rate = grp["Interest_Rate"].mean() / 100.0
        vals = [band, cnt, def_cnt, def_rate, avg_rate]
        for c_idx, v in enumerate(vals, start=1):
            cell = ws4.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 1: cell.alignment = align_left
            elif c_idx in [2, 3]: cell.number_format = "#,##0"; cell.alignment = align_right
            elif c_idx in [4, 5]: cell.number_format = "0.0%"; cell.alignment = align_right
            if r_idx % 2 == 1: cell.fill = zebra_fill
        r_idx += 1

    auto_fit_columns(ws4)

    # -------------------------------------------------------------
    # 5. WORKSHEET: Customer Segments
    # -------------------------------------------------------------
    ws5 = wb.create_sheet(title="Customer Segments")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells("A1:I2")
    ws5["A1"] = "STRATEGIC CUSTOMER SEGMENTATION"
    ws5["A1"].font = title_font
    ws5["A1"].fill = title_fill
    ws5["A1"].alignment = align_center

    ws5["A4"] = "Segment Performance & Profitability Profiles"
    ws5["A4"].font = section_font
    seg_headers = ["Segment Name", "Customers", "Share %", "Avg Income ($)", "Avg Balance ($)", "Total Deposits ($M)", "Approval %", "Default %", "Actionable Strategy"]
    for c_idx, h in enumerate(seg_headers, start=1):
        cell = ws5.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    strategies = {
        "High Value": "Wealth Management, Premium Card Upgrades, Private Banking",
        "Premium": "Mortgage Cross-sell, Commercial Lending, Investment Advisory",
        "Standard": "Payroll Accounts, Auto Loans, Digital Engagement Push",
        "Emerging": "First-time Buyer Programs, Career Starter Lines of Credit",
        "High Risk": "Collateralized Lending Only, Strict DTI Caps, Financial Coaching"
    }

    r_idx = 6
    for seg_name in ["High Value", "Premium", "Standard", "Emerging", "High Risk"]:
        grp = df[df["Customer_Segment"] == seg_name]
        cnt = len(grp)
        pct = cnt / total_cust
        avg_inc = grp["Annual_Income"].mean()
        avg_bal = grp["Account_Balance"].mean()
        tot_dep_m = grp["Account_Balance"].sum() / 1e6
        appr_pct = (grp["Loan_Status"] == "Approved").mean()
        appr_grp = grp[grp["Loan_Status"] == "Approved"]
        def_pct = appr_grp["Default_Flag"].mean() if len(appr_grp) > 0 else 0
        strat = strategies.get(seg_name, "")
        vals = [seg_name, cnt, pct, avg_inc, avg_bal, tot_dep_m, appr_pct, def_pct, strat]
        for c_idx, v in enumerate(vals, start=1):
            cell = ws5.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [1, 9]: cell.alignment = align_left
            elif c_idx == 2: cell.number_format = "#,##0"; cell.alignment = align_right
            elif c_idx in [3, 7, 8]: cell.number_format = "0.0%"; cell.alignment = align_right
            elif c_idx in [4, 5]: cell.number_format = "$#,##0"; cell.alignment = align_right
            elif c_idx == 6: cell.number_format = "$#,##0.0"; cell.alignment = align_right
            if r_idx % 2 == 1: cell.fill = zebra_fill
        r_idx += 1

    auto_fit_columns(ws5)

    # -------------------------------------------------------------
    # 6. WORKSHEET: Branch Performance
    # -------------------------------------------------------------
    ws6 = wb.create_sheet(title="Branch Performance")
    ws6.views.sheetView[0].showGridLines = True

    ws6.merge_cells("A1:H2")
    ws6["A1"] = "BRANCH NETWORK PERFORMANCE SCORECARD"
    ws6["A1"].font = title_font
    ws6["A1"].fill = title_fill
    ws6["A1"].alignment = align_center

    ws6["A4"] = "Ranked Branch Metrics (Loan Capital & Deposits)"
    ws6["A4"].font = section_font
    branch_headers = ["Branch ID", "Branch Name", "Region", "Customers", "Total Deposits ($M)", "Loan Volume ($M)", "Approval Rate %", "Default Rate %"]
    for c_idx, h in enumerate(branch_headers, start=1):
        cell = ws6.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    r_idx = 6
    b_group = df.groupby(["Branch_ID", "Branch_Name", "Region"])
    branch_rows = []
    for (bid, bname, reg), grp in b_group:
        c_cnt = len(grp)
        dep_m = grp["Account_Balance"].sum() / 1e6
        loan_m = grp["Loan_Amount"].sum() / 1e6
        appr_pct = (grp["Loan_Status"] == "Approved").mean()
        appr_grp = grp[grp["Loan_Status"] == "Approved"]
        def_pct = appr_grp["Default_Flag"].mean() if len(appr_grp) > 0 else 0
        branch_rows.append((bid, bname, reg, c_cnt, dep_m, loan_m, appr_pct, def_pct))

    branch_rows.sort(key=lambda x: x[5], reverse=True)
    for vals in branch_rows:
        for c_idx, v in enumerate(vals, start=1):
            cell = ws6.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [1, 2, 3]: cell.alignment = align_left
            elif c_idx == 4: cell.number_format = "#,##0"; cell.alignment = align_right
            elif c_idx in [5, 6]: cell.number_format = "$#,##0.0"; cell.alignment = align_right
            elif c_idx in [7, 8]: cell.number_format = "0.0%"; cell.alignment = align_right
            if r_idx % 2 == 1: cell.fill = zebra_fill
        r_idx += 1

    auto_fit_columns(ws6)

    # -------------------------------------------------------------
    # 7. WORKSHEET: Regional Analysis
    # -------------------------------------------------------------
    ws7 = wb.create_sheet(title="Regional Analysis")
    ws7.views.sheetView[0].showGridLines = True

    ws7.merge_cells("A1:G2")
    ws7["A1"] = "GEOGRAPHIC REGIONAL INTELLIGENCE"
    ws7["A1"].font = title_font
    ws7["A1"].fill = title_fill
    ws7["A1"].alignment = align_center

    ws7["A4"] = "Regional Portfolio Footprint"
    ws7["A4"].font = section_font
    reg_hdrs = ["Region", "Customer Count", "Market Share %", "Total Deposits ($M)", "Loan Volume ($M)", "Avg Credit Score", "Default %"]
    for c_idx, h in enumerate(reg_hdrs, start=1):
        cell = ws7.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    r_idx = 6
    for reg, grp in df.groupby("Region"):
        c_cnt = len(grp)
        share = c_cnt / total_cust
        dep_m = grp["Account_Balance"].sum() / 1e6
        loan_m = grp["Loan_Amount"].sum() / 1e6
        avg_cs_reg = grp["Credit_Score"].mean()
        appr_grp = grp[grp["Loan_Status"] == "Approved"]
        def_pct = appr_grp["Default_Flag"].mean() if len(appr_grp) > 0 else 0
        vals = [reg, c_cnt, share, dep_m, loan_m, avg_cs_reg, def_pct]
        for c_idx, v in enumerate(vals, start=1):
            cell = ws7.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 1: cell.alignment = align_left
            elif c_idx == 2: cell.number_format = "#,##0"; cell.alignment = align_right
            elif c_idx in [3, 7]: cell.number_format = "0.0%"; cell.alignment = align_right
            elif c_idx in [4, 5]: cell.number_format = "$#,##0.0"; cell.alignment = align_right
            elif c_idx == 6: cell.number_format = "0.0"; cell.alignment = align_right
            if r_idx % 2 == 1: cell.fill = zebra_fill
        r_idx += 1

    auto_fit_columns(ws7)

    # -------------------------------------------------------------
    # 8. WORKSHEET: Data Dictionary & Sample
    # -------------------------------------------------------------
    ws8 = wb.create_sheet(title="Data Dictionary & Sample")
    ws8.views.sheetView[0].showGridLines = True

    ws8.merge_cells("A1:D2")
    ws8["A1"] = "DATA DICTIONARY & SCHEMA SPECIFICATION"
    ws8["A1"].font = title_font
    ws8["A1"].fill = title_fill
    ws8["A1"].alignment = align_center

    dict_headers = ["Field Name", "Data Type", "Business Definition", "Example Values"]
    for c_idx, h in enumerate(dict_headers, start=1):
        cell = ws8.cell(row=4, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    sample_dict = [
        ("Customer_ID", "String (PK)", "Unique alphanumeric identifier for each bank customer", "CUST-10001, CUST-10002"),
        ("First_Name", "String", "First name of the customer", "James, Mary, Robert"),
        ("Last_Name", "String", "Last name or surname of the customer", "Smith, Johnson, Williams"),
        ("Gender", "Categorical", "Biological gender (Standardized)", "Male, Female"),
        ("Age", "Integer", "Customer age in completed years (18-80)", "25, 42, 67"),
        ("Age_Group", "Categorical", "Engineered age bracket", "18-25, 26-35, 36-50, 51-65, 65+"),
        ("Annual_Income", "Decimal ($)", "Gross annual verified customer income", "$45,000.00, $125,000.00"),
        ("Income_Group", "Categorical", "Engineered socioeconomic income band", "Low (<$35k), Middle ($60k-$100k)"),
        ("City", "String", "City of customer primary branch location", "New York, Chicago, Dallas"),
        ("State", "String", "US State postal code", "NY, IL, TX, CA, MA"),
        ("Region", "Categorical", "Geographic US territory division", "Northeast, Midwest, South, West"),
        ("Branch_ID", "String (FK)", "Unique bank branch identifier code", "BR-001, BR-004, BR-011"),
        ("Branch_Name", "String", "Designated commercial name of the branch", "NYC Metro Branch, Dallas Commercial"),
        ("Account_Type", "Categorical", "Primary deposit account instrument held", "Savings, Checking, Money Market"),
        ("Customer_Tenure_Years", "Decimal", "Length of relationship with bank in years", "1.5, 4.2, 12.8"),
        ("Account_Balance", "Decimal ($)", "Total balance across deposit instruments", "$12,450.50, $85,200.00"),
        ("Number_of_Products", "Integer", "Total count of active banking products held (1-5)", "1, 2, 3, 4"),
        ("Credit_Score", "Integer", "Standardized FICO credit score (300-850)", "580, 695, 780"),
        ("Credit_Score_Category", "Categorical", "FICO risk tier definition", "Poor, Fair, Good, Very Good, Excellent"),
        ("Debt_to_Income_Ratio", "Decimal", "Monthly debt obligations divided by monthly income", "0.18, 0.35, 0.52"),
        ("Loan_ID", "String (PK)", "Unique credit application identifier", "LN-100001, LN-100002"),
        ("Loan_Type", "Categorical", "Credit product category", "Home Loan, Auto Loan, Personal Loan"),
        ("Loan_Amount", "Decimal ($)", "Principal loan balance requested", "$25,000.00, $250,000.00"),
        ("Interest_Rate", "Decimal (%)", "Annualized fixed interest rate charged", "5.25%, 8.50%, 12.00%"),
        ("Loan_Tenure_Months", "Integer", "Loan maturity schedule in months", "36, 60, 180, 360"),
        ("Monthly_Installment", "Decimal ($)", "Calculated amortized monthly debt service", "$485.20, $1,450.80"),
        ("Loan_Status", "Categorical", "Underwriting credit decision result", "Approved, Rejected, Pending"),
        ("Loan_Approval_Flag", "Binary (0/1)", "Indicator flag for approved applications", "1 = Approved, 0 = Otherwise"),
        ("Risk_Category", "Categorical", "Risk rating tier based on default probability", "Low Risk, Medium Risk, High Risk, Very High Risk"),
        ("Default_Flag", "Binary (0/1)", "Loan default status on approved loans (1=Default, 0=Current)", "0, 1"),
        ("Customer_Segment", "Categorical", "Target strategic customer segmentation profile", "High Value, Premium, Standard, Emerging, High Risk")
    ]

    r_idx = 5
    for item in sample_dict:
        for c_idx, v in enumerate(item, start=1):
            cell = ws8.cell(row=r_idx, column=c_idx, value=v)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 1:
                cell.font = bold_font
            if r_idx % 2 == 1:
                cell.fill = zebra_fill
        r_idx += 1

    auto_fit_columns(ws8, max_len_cap=70)

    # Save Workbook
    wb.save(output_path)
    print(f"[OK] Excel report successfully generated and saved to: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "bank_customer_loan_clean.csv")
    out_xlsx = os.path.join(os.path.dirname(__file__), "..", "outputs", "Bank_Customer_Loan_Analysis.xlsx")
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path)
        create_excel_dashboard(df, out_xlsx)
