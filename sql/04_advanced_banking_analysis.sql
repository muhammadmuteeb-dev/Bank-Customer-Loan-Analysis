-- ==============================================================================
-- BANK CUSTOMER & LOAN ANALYSIS — SQL SCRIPT 04
-- ADVANCED BANKING ANALYTICS (CTEs, WINDOW FUNCTIONS, LEAD GENERATION)
-- Table: bank_customer_loan (Unified cleaned dataset)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Query 1: Customer Segmentation Comprehensive Performance Matrix
-- Profiling the 5 strategic segments across deposits, lending, and delinquency.
-- ------------------------------------------------------------------------------
SELECT 
    Customer_Segment,
    COUNT(Customer_ID) AS Customer_Count,
    ROUND(COUNT(Customer_ID) * 100.0 / (SELECT COUNT(*) FROM bank_customer_loan), 2) AS Customer_Share_Pct,
    ROUND(AVG(Annual_Income), 2) AS Avg_Income,
    ROUND(AVG(Account_Balance), 2) AS Avg_Balance,
    ROUND(SUM(Account_Balance) / 1000000.0, 2) AS Total_Deposits_M,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Loan_Approval_Rate_Pct,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' AND Default_Flag = 1 THEN 1 ELSE 0 END) * 100.0 / 
          NULLIF(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END), 0), 2) AS Default_Rate_Pct
FROM bank_customer_loan
GROUP BY Customer_Segment
ORDER BY 
    CASE Customer_Segment
        WHEN 'High Value' THEN 1
        WHEN 'Premium' THEN 2
        WHEN 'Standard' THEN 3
        WHEN 'Emerging' THEN 4
        WHEN 'High Risk' THEN 5
        ELSE 6
    END;

-- ------------------------------------------------------------------------------
-- Query 2: Window Function: Branch Regional League Table Ranking
-- Uses DENSE_RANK() to rank branches within each geographic region by funded volume.
-- ------------------------------------------------------------------------------
WITH Branch_Funded_Summary AS (
    SELECT 
        Branch_ID,
        Branch_Name,
        Region,
        COUNT(Loan_ID) AS Total_Applications,
        SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) AS Approved_Loans,
        ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE 0 END) / 1000000.0, 2) AS Funded_Volume_M,
        ROUND(AVG(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE NULL END), 2) AS Avg_Funded_Amount
    FROM bank_customer_loan
    GROUP BY Branch_ID, Branch_Name, Region
)
SELECT 
    Region,
    DENSE_RANK() OVER (PARTITION BY Region ORDER BY Funded_Volume_M DESC) AS Regional_Rank,
    Branch_ID,
    Branch_Name,
    Total_Applications,
    Approved_Loans,
    Funded_Volume_M,
    Avg_Funded_Amount
FROM Branch_Funded_Summary
ORDER BY Region, Regional_Rank;

-- ------------------------------------------------------------------------------
-- Query 3: Window Function: Cumulative Running Origination of Loan Capital
-- Calculates running monthly funded volume and cumulative percentage of portfolio.
-- ------------------------------------------------------------------------------
WITH Monthly_Origination AS (
    SELECT 
        SUBSTR(Loan_Application_Date, 1, 7) AS Year_Month,
        COUNT(Loan_ID) AS Applications_Count,
        SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) AS Approved_Count,
        SUM(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE 0 END) AS Monthly_Funded_Capital
    FROM bank_customer_loan
    WHERE Loan_Application_Date IS NOT NULL AND Loan_Application_Date != ''
    GROUP BY SUBSTR(Loan_Application_Date, 1, 7)
)
SELECT 
    Year_Month,
    Applications_Count,
    Approved_Count,
    ROUND(Monthly_Funded_Capital / 1000000.0, 2) AS Monthly_Funded_M,
    ROUND(SUM(Monthly_Funded_Capital) OVER (ORDER BY Year_Month) / 1000000.0, 2) AS Cumulative_Funded_M,
    ROUND(SUM(Monthly_Funded_Capital) OVER (ORDER BY Year_Month) * 100.0 / 
          (SELECT SUM(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE 0 END) FROM bank_customer_loan), 2) AS Cumulative_Pct_Of_Total
FROM Monthly_Origination
ORDER BY Year_Month;

-- ------------------------------------------------------------------------------
-- Query 4: Window Function: Customer Wealth Quintiles (NTILE) & Credit Demand
-- Partitions entire customer base into 5 deposit quintiles to measure loan adoption.
-- ------------------------------------------------------------------------------
WITH Customer_Quintiles AS (
    SELECT 
        Customer_ID,
        Annual_Income,
        Account_Balance,
        Credit_Score,
        Loan_Status,
        Loan_Amount,
        NTILE(5) OVER (ORDER BY Account_Balance DESC) AS Wealth_Quintile
    FROM bank_customer_loan
)
SELECT 
    Wealth_Quintile,
    COUNT(Customer_ID) AS Customers_In_Quintile,
    ROUND(MIN(Account_Balance), 2) AS Min_Balance,
    ROUND(MAX(Account_Balance), 2) AS Max_Balance,
    ROUND(AVG(Account_Balance), 2) AS Avg_Balance,
    ROUND(AVG(Annual_Income), 2) AS Avg_Income,
    ROUND(AVG(Credit_Score), 1) AS Avg_Credit_Score,
    ROUND(SUM(CASE WHEN Loan_Status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Loan_Approval_Rate_Pct,
    ROUND(AVG(CASE WHEN Loan_Status = 'Approved' THEN Loan_Amount ELSE NULL END), 2) AS Avg_Loan_Size
FROM Customer_Quintiles
GROUP BY Wealth_Quintile
ORDER BY Wealth_Quintile ASC;

-- ------------------------------------------------------------------------------
-- Query 5: Strategic Opportunity CTE: High-Deposit Low-Borrowing Cross-Sell Leads
-- Identifies affluent depositors who hold no active loans or had loan rejected.
-- Target cohort for bespoke pre-approved wealth lending and mortgage offers.
-- ------------------------------------------------------------------------------
WITH Cross_Sell_Targets AS (
    SELECT 
        Customer_ID,
        First_Name,
        Last_Name,
        Age,
        Occupation,
        Annual_Income,
        Account_Balance,
        Credit_Score,
        Loan_Status,
        Customer_Segment,
        Branch_Name,
        Region
    FROM bank_customer_loan
    WHERE Account_Balance >= 50000
      AND Credit_Score >= 720
      AND (Loan_Status != 'Approved' OR Loan_Status IS NULL)
)
SELECT 
    Customer_ID,
    First_Name,
    Last_Name,
    Age,
    Occupation,
    Annual_Income,
    Account_Balance,
    Credit_Score,
    Customer_Segment,
    Branch_Name,
    Region,
    'Priority Prime Lending Lead' AS Action_Recommendation
FROM Cross_Sell_Targets
ORDER BY Account_Balance DESC
LIMIT 25;

-- ------------------------------------------------------------------------------
-- Query 6: Early Warning Risk CTE: High-Exposure Highly-Leveraged Borrowers
-- Filters borrowers with DTI >= 45%, Credit Score < 640, and existing loans.
-- ------------------------------------------------------------------------------
WITH Delinquency_Risk_Watchlist AS (
    SELECT 
        Customer_ID,
        First_Name,
        Last_Name,
        Branch_Name,
        Loan_Type,
        Loan_Amount,
        Monthly_Installment,
        Credit_Score,
        Debt_to_Income_Ratio,
        Existing_Loans,
        Risk_Category,
        Default_Flag
    FROM bank_customer_loan
    WHERE Loan_Status = 'Approved'
      AND Debt_to_Income_Ratio >= 0.45
      AND Credit_Score < 640
)
SELECT 
    Customer_ID,
    First_Name,
    Last_Name,
    Branch_Name,
    Loan_Type,
    Loan_Amount,
    Monthly_Installment,
    Credit_Score,
    ROUND(Debt_to_Income_Ratio * 100.0, 2) AS DTI_Pct,
    Existing_Loans,
    Risk_Category,
    CASE WHEN Default_Flag = 1 THEN 'Defaulted' ELSE 'At-Risk (Current)' END AS Monitoring_Status
FROM Delinquency_Risk_Watchlist
ORDER BY Debt_to_Income_Ratio DESC, Credit_Score ASC
LIMIT 25;

-- ------------------------------------------------------------------------------
-- Query 7: Top Customer per Branch (Window Function: ROW_NUMBER)
-- Extracts the highest-earning customer anchored to each specific branch.
-- ------------------------------------------------------------------------------
WITH Ranked_Branch_Customers AS (
    SELECT 
        Branch_ID,
        Branch_Name,
        Customer_ID,
        First_Name,
        Last_Name,
        Occupation,
        Annual_Income,
        Account_Balance,
        Customer_Segment,
        ROW_NUMBER() OVER (PARTITION BY Branch_ID ORDER BY Annual_Income DESC) AS Earning_Rank
    FROM bank_customer_loan
)
SELECT 
    Branch_ID,
    Branch_Name,
    Customer_ID,
    First_Name,
    Last_Name,
    Occupation,
    Annual_Income,
    Account_Balance,
    Customer_Segment
FROM Ranked_Branch_Customers
WHERE Earning_Rank = 1
ORDER BY Annual_Income DESC;
