-- ==============================================================================
-- BANK CUSTOMER & LOAN ANALYSIS — SQL SCRIPT 02
-- LOAN PORTFOLIO & UNDERWRITING PERFORMANCE
-- Table: bank_customer_loan (Unified cleaned dataset)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Query 1: Executive Loan Portfolio Underwriting KPIs
-- Evaluates total applications, approval/rejection rates, and capital requested vs funded.
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(Loan_ID) AS Total_Loan_Applications,
    SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) AS Approved_Loans,
    SUM(CASE WHEN Loan_Status = 'Rejected' THEN 1 ELSE 0 END) AS Rejected_Loans,
    SUM(CASE WHEN Loan_Status = 'Pending' THEN 1 ELSE 0 END) AS Pending_Loans,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Approval_Rate_Pct,
    ROUND(SUM(CASE WHEN Loan_Status = 'Rejected' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Rejection_Rate_Pct,
    ROUND(SUM(Loan_Amount) / 1000000.0, 2) AS Total_Requested_Volume_M,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Total_Funded_Volume_M,
    ROUND(AVG(Loan_Amount), 2) AS Avg_Requested_Amount,
    ROUND(AVG(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE NULL END), 2) AS Avg_Funded_Amount
FROM bank_customer_loan;

-- ------------------------------------------------------------------------------
-- Query 2: Loan Portfolio Performance by Product Line (Loan Type)
-- Breakdown of loan volume, approval %, average interest rate, and terms.
-- ------------------------------------------------------------------------------
SELECT 
    Loan_Type,
    COUNT(Loan_ID) AS Applications_Count,
    SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) AS Approved_Count,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Approval_Rate_Pct,
    ROUND(SUM(Loan_Amount) / 1000000.0, 2) AS Total_Requested_M,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Total_Funded_M,
    ROUND(AVG(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE NULL END), 2) AS Avg_Funded_Loan_Size,
    ROUND(AVG(Interest_Rate), 2) AS Avg_Interest_Rate,
    ROUND(AVG(Loan_Tenure_Months), 1) AS Avg_Tenure_Months,
    ROUND(AVG(Monthly_Installment), 2) AS Avg_Monthly_Installment
FROM bank_customer_loan
GROUP BY Loan_Type
ORDER BY Total_Funded_M DESC;

-- ------------------------------------------------------------------------------
-- Query 3: Loan Portfolio by Stated Purpose
-- Identifies primary borrower financing motivations and approval likelihood.
-- ------------------------------------------------------------------------------
SELECT 
    Loan_Purpose,
    COUNT(Loan_ID) AS Total_Applications,
    ROUND(COUNT(Loan_ID) * 100.0 / (SELECT COUNT(*) FROM bank_customer_loan), 2) AS Application_Share_Pct,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Approval_Rate_Pct,
    ROUND(SUM(Loan_Amount) / 1000000.0, 2) AS Total_Volume_M,
    ROUND(AVG(Loan_Amount), 2) AS Avg_Loan_Size,
    ROUND(AVG(Interest_Rate), 2) AS Avg_Interest_Rate
FROM bank_customer_loan
GROUP BY Loan_Purpose
ORDER BY Total_Applications DESC;

-- ------------------------------------------------------------------------------
-- Query 4: Branch Network Lending League Table
-- Evaluates branch performance, origination volume, and underwriting pass rates.
-- ------------------------------------------------------------------------------
SELECT 
    Branch_ID,
    Branch_Name,
    Region,
    COUNT(Loan_ID) AS Total_Applications,
    SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) AS Approved_Loans,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Approval_Rate_Pct,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Funded_Volume_M,
    ROUND(AVG(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE NULL END), 2) AS Avg_Funded_Loan_Size
FROM bank_customer_loan
GROUP BY Branch_ID, Branch_Name, Region
ORDER BY Funded_Volume_M DESC;

-- ------------------------------------------------------------------------------
-- Query 5: Regional Loan Origination and Demand
-- Macro regional lending distribution comparing requested vs funded capital.
-- ------------------------------------------------------------------------------
SELECT 
    Region,
    COUNT(Loan_ID) AS Applications_Count,
    ROUND(SUM(Loan_Amount) / 1000000.0, 2) AS Requested_Capital_M,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Funded_Capital_M,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Approval_Rate_Pct,
    ROUND(AVG(Interest_Rate), 2) AS Avg_Interest_Rate
FROM bank_customer_loan
GROUP BY Region
ORDER BY Funded_Capital_M DESC;

-- ------------------------------------------------------------------------------
-- Query 6: Loan Underwriting Decisions Across Borrower Income Groups
-- Evaluates credit approval criteria across socioeconomic tiers.
-- ------------------------------------------------------------------------------
SELECT 
    Income_Group,
    COUNT(Loan_ID) AS Total_Applicants,
    SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) AS Approved_Applicants,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Approval_Rate_Pct,
    ROUND(AVG(Loan_Amount), 2) AS Avg_Requested_Amount,
    ROUND(AVG(Debt_to_Income_Ratio) * 100.0, 2) AS Avg_DTI_Pct
FROM bank_customer_loan
GROUP BY Income_Group
ORDER BY 
    CASE Income_Group
        WHEN 'Low (<$35k)' THEN 1
        WHEN 'Lower-Middle ($35k-$60k)' THEN 2
        WHEN 'Middle ($60k-$100k)' THEN 3
        WHEN 'Upper-Middle ($100k-$150k)' THEN 4
        WHEN 'High (>=$150k)' THEN 5
        ELSE 6
    END;

-- ------------------------------------------------------------------------------
-- Query 7: Loan Size Distribution by Loan Amount Category
-- Analyzes loan portfolio granularity across size classifications.
-- ------------------------------------------------------------------------------
SELECT 
    Loan_Amount_Category,
    COUNT(Loan_ID) AS Loan_Count,
    ROUND(COUNT(Loan_ID) * 100.0 / (SELECT COUNT(*) FROM bank_customer_loan), 2) AS Count_Pct,
    ROUND(SUM(Loan_Amount) / 1000000.0, 2) AS Total_Amount_M,
    ROUND(SUM(Loan_Amount) * 100.0 / (SELECT SUM(Loan_Amount) FROM bank_customer_loan), 2) AS Volume_Pct,
    ROUND(AVG(Interest_Rate), 2) AS Avg_Interest_Rate
FROM bank_customer_loan
GROUP BY Loan_Amount_Category
ORDER BY 
    CASE Loan_Amount_Category
        WHEN 'Micro (<$10k)' THEN 1
        WHEN 'Small ($10k-$25k)' THEN 2
        WHEN 'Medium ($25k-$75k)' THEN 3
        WHEN 'Large ($75k-$200k)' THEN 4
        WHEN 'Jumbo (>=$200k)' THEN 5
        ELSE 6
    END;
