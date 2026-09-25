-- ==============================================================================
-- BANK CUSTOMER & LOAN ANALYSIS — SQL SCRIPT 03
-- CREDIT RISK & DELINQUENCY MONITORING
-- Table: bank_customer_loan (Unified cleaned dataset)
-- Note: Delinquency and default rates are strictly evaluated on Approved Loans.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Query 1: Active Loan Portfolio Default KPIs
-- Overall default rate, total defaulted accounts, and capital loss exposure.
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(Loan_ID) AS Total_Active_Loans,
    SUM(Default_Flag) AS Total_Defaulted_Loans,
    ROUND(SUM(Default_Flag) * 100.0 / COUNT(*), 2) AS Default_Rate_Pct,
    ROUND(SUM(Loan_Amount) / 1000000.0, 2) AS Total_Active_Capital_M,
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Defaulted_Capital_M,
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN Loan_Amount ELSE 0 END) * 100.0 / SUM(Loan_Amount), 2) AS Capital_Loss_Rate_Pct
FROM bank_customer_loan
WHERE Loan_Status = 'Approved';

-- ------------------------------------------------------------------------------
-- Query 2: Delinquency Rate by Internal Risk Rating Category
-- Validates risk category calibration against empirical loan performance.
-- ------------------------------------------------------------------------------
SELECT 
    Risk_Category,
    COUNT(Loan_ID) AS Active_Loans,
    SUM(Default_Flag) AS Defaulted_Loans,
    ROUND(SUM(Default_Flag) * 100.0 / COUNT(*), 2) AS Default_Rate_Pct,
    ROUND(SUM(Loan_Amount) / 1000000.0, 2) AS Funded_Volume_M,
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Defaulted_Volume_M,
    ROUND(AVG(Credit_Score), 1) AS Avg_Credit_Score,
    ROUND(AVG(Debt_to_Income_Ratio) * 100.0, 2) AS Avg_DTI_Pct
FROM bank_customer_loan
WHERE Loan_Status = 'Approved'
GROUP BY Risk_Category
ORDER BY 
    CASE Risk_Category
        WHEN 'Low Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'High Risk' THEN 3
        WHEN 'Very High Risk' THEN 4
        ELSE 5
    END;

-- ------------------------------------------------------------------------------
-- Query 3: Default Rates Across FICO Credit Score Categories
-- Demonstrates empirical inverse relationship between credit score and default.
-- ------------------------------------------------------------------------------
SELECT 
    Credit_Score_Category,
    COUNT(Loan_ID) AS Active_Loans,
    SUM(Default_Flag) AS Default_Count,
    ROUND(SUM(Default_Flag) * 100.0 / COUNT(*), 2) AS Default_Rate_Pct,
    ROUND(AVG(Interest_Rate), 2) AS Avg_Interest_Rate,
    ROUND(AVG(Debt_to_Income_Ratio) * 100.0, 2) AS Avg_DTI_Pct
FROM bank_customer_loan
WHERE Loan_Status = 'Approved'
GROUP BY Credit_Score_Category
ORDER BY 
    CASE Credit_Score_Category
        WHEN 'Poor (300-579)' THEN 1
        WHEN 'Fair (580-669)' THEN 2
        WHEN 'Good (670-739)' THEN 3
        WHEN 'Very Good (740-799)' THEN 4
        WHEN 'Excellent (800-850)' THEN 5
        ELSE 6
    END;

-- ------------------------------------------------------------------------------
-- Query 4: High-Risk Borrower Concentration Watchlist
-- Identifies active borrowers with subprime credit (<620) and high leverage (DTI > 40%).
-- ------------------------------------------------------------------------------
SELECT 
    Customer_ID,
    First_Name,
    Last_Name,
    Branch_Name,
    Region,
    Loan_Type,
    Loan_Amount,
    Credit_Score,
    Debt_to_Income_Ratio,
    Risk_Category,
    Default_Flag
FROM bank_customer_loan
WHERE Loan_Status = 'Approved'
  AND Credit_Score < 620
  AND Debt_to_Income_Ratio > 0.40
ORDER BY Default_Flag DESC, Debt_to_Income_Ratio DESC
LIMIT 25;

-- ------------------------------------------------------------------------------
-- Query 5: Default Rates and Loss Severity by Loan Product Line
-- Compares collateralized products (Home, Auto) vs unsecured products (Personal).
-- ------------------------------------------------------------------------------
SELECT 
    Loan_Type,
    COUNT(Loan_ID) AS Active_Loans,
    SUM(Default_Flag) AS Default_Count,
    ROUND(SUM(Default_Flag) * 100.0 / COUNT(*), 2) AS Default_Rate_Pct,
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Defaulted_Capital_M,
    ROUND(AVG(Interest_Rate), 2) AS Avg_Interest_Rate
FROM bank_customer_loan
WHERE Loan_Status = 'Approved'
GROUP BY Loan_Type
ORDER BY Default_Rate_Pct DESC;

-- ------------------------------------------------------------------------------
-- Query 6: Leverage Risk Analysis: Default Rates by Debt-to-Income (DTI) Bands
-- Examines default escalation as borrower leverage exceeds debt capacity limits.
-- ------------------------------------------------------------------------------
SELECT 
    Debt_to_Income_Category,
    COUNT(Loan_ID) AS Active_Loans,
    SUM(Default_Flag) AS Defaulted_Loans,
    ROUND(SUM(Default_Flag) * 100.0 / COUNT(*), 2) AS Default_Rate_Pct,
    ROUND(AVG(Credit_Score), 1) AS Avg_Credit_Score,
    ROUND(AVG(Loan_Amount), 2) AS Avg_Loan_Amount
FROM bank_customer_loan
WHERE Loan_Status = 'Approved'
GROUP BY Debt_to_Income_Category
ORDER BY 
    CASE Debt_to_Income_Category
        WHEN 'Low (<20%)' THEN 1
        WHEN 'Moderate (20-35%)' THEN 2
        WHEN 'Manageable (36-49%)' THEN 3
        WHEN 'Critical (>=50%)' THEN 4
        ELSE 5
    END;

-- ------------------------------------------------------------------------------
-- Query 7: Borrower Risk Profile: Defaulters vs Non-Defaulters Comparison
-- Contrasts financial, credit, and behavioral attributes of defaulting borrowers.
-- ------------------------------------------------------------------------------
SELECT 
    CASE WHEN Default_Flag = 1 THEN 'Defaulter' ELSE 'Non-Defaulter' END AS Borrower_Status,
    COUNT(Customer_ID) AS Customer_Count,
    ROUND(AVG(Credit_Score), 1) AS Avg_Credit_Score,
    ROUND(AVG(Debt_to_Income_Ratio) * 100.0, 2) AS Avg_DTI_Pct,
    ROUND(AVG(Annual_Income), 2) AS Avg_Annual_Income,
    ROUND(AVG(Account_Balance), 2) AS Avg_Account_Balance,
    ROUND(AVG(Loan_Amount), 2) AS Avg_Loan_Amount,
    ROUND(AVG(Interest_Rate), 2) AS Avg_Interest_Rate,
    ROUND(AVG(Customer_Tenure_Years), 1) AS Avg_Tenure_Years
FROM bank_customer_loan
WHERE Loan_Status = 'Approved'
GROUP BY Default_Flag;

-- ------------------------------------------------------------------------------
-- Query 8: Regional Credit Risk Distribution
-- Identifies geographical delinquency concentrations for credit audit targeting.
-- ------------------------------------------------------------------------------
SELECT 
    Region,
    COUNT(Loan_ID) AS Active_Loans,
    SUM(Default_Flag) AS Defaulted_Loans,
    ROUND(SUM(Default_Flag) * 100.0 / COUNT(*), 2) AS Default_Rate_Pct,
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Defaulted_Capital_M,
    ROUND(SUM(CASE WHEN Risk_Category IN ('High Risk', 'Very High Risk') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS High_Risk_Borrower_Pct
FROM bank_customer_loan
WHERE Loan_Status = 'Approved'
GROUP BY Region
ORDER BY Default_Rate_Pct DESC;
