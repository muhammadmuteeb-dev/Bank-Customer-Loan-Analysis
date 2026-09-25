-- ==============================================================================
-- BANK CUSTOMER & LOAN ANALYSIS — SQL SCRIPT 01
-- BASIC CUSTOMER & DEMOGRAPHIC ANALYSIS
-- Table: bank_customer_loan (Unified cleaned dataset)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Query 1: High-Level Customer Base Summary KPIs
-- Calculates total customer count, average income, average balance, and credit score.
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(Customer_ID) AS Total_Customers,
    ROUND(AVG(Annual_Income), 2) AS Avg_Annual_Income,
    ROUND(AVG(Account_Balance), 2) AS Avg_Account_Balance,
    ROUND(AVG(Credit_Score), 1) AS Avg_Credit_Score,
    ROUND(SUM(Account_Balance) / 1000000.0, 2) AS Total_Deposits_Millions
FROM bank_customer_loan;

-- ------------------------------------------------------------------------------
-- Query 2: Customer Demographics by Gender
-- Breakdown of customer volume, income, balance, and creditworthiness by gender.
-- ------------------------------------------------------------------------------
SELECT 
    Gender,
    COUNT(Customer_ID) AS Customer_Count,
    ROUND(COUNT(Customer_ID) * 100.0 / (SELECT COUNT(*) FROM bank_customer_loan), 2) AS Pct_Share,
    ROUND(AVG(Annual_Income), 2) AS Avg_Income,
    ROUND(AVG(Account_Balance), 2) AS Avg_Balance,
    ROUND(AVG(Credit_Score), 1) AS Avg_Credit_Score
FROM bank_customer_loan
GROUP BY Gender
ORDER BY Customer_Count DESC;

-- ------------------------------------------------------------------------------
-- Query 3: Demographic Breakdown Across Age Groups
-- Evaluates wealth accumulation, tenure, and product ownership by age bracket.
-- ------------------------------------------------------------------------------
SELECT 
    Age_Group,
    COUNT(Customer_ID) AS Customer_Count,
    ROUND(COUNT(Customer_ID) * 100.0 / (SELECT COUNT(*) FROM bank_customer_loan), 2) AS Pct_Share,
    ROUND(AVG(Annual_Income), 2) AS Avg_Income,
    ROUND(AVG(Account_Balance), 2) AS Avg_Balance,
    ROUND(AVG(Customer_Tenure_Years), 1) AS Avg_Tenure_Years,
    ROUND(AVG(Number_of_Products), 2) AS Avg_Products_Held
FROM bank_customer_loan
GROUP BY Age_Group
ORDER BY 
    CASE Age_Group
        WHEN '18-25' THEN 1
        WHEN '26-35' THEN 2
        WHEN '36-50' THEN 3
        WHEN '51-65' THEN 4
        WHEN '65+' THEN 5
        ELSE 6
    END;

-- ------------------------------------------------------------------------------
-- Query 4: Customer Distribution by Education & Employment Status
-- Examines educational attainment vs employment stability and earnings.
-- ------------------------------------------------------------------------------
SELECT 
    Education,
    Employment_Status,
    COUNT(Customer_ID) AS Customer_Count,
    ROUND(AVG(Annual_Income), 2) AS Avg_Income,
    ROUND(AVG(Account_Balance), 2) AS Avg_Balance,
    ROUND(AVG(Credit_Score), 1) AS Avg_Credit_Score
FROM bank_customer_loan
GROUP BY Education, Employment_Status
ORDER BY Education, Customer_Count DESC;

-- ------------------------------------------------------------------------------
-- Query 5: Geographic Customer Distribution Across Regions and States
-- Analyzes market presence and deposit concentration by geography.
-- ------------------------------------------------------------------------------
SELECT 
    Region,
    State,
    COUNT(Customer_ID) AS Total_Customers,
    ROUND(SUM(Account_Balance) / 1000000.0, 2) AS Total_Deposits_M,
    ROUND(AVG(Annual_Income), 2) AS Avg_Income,
    ROUND(AVG(Account_Balance), 2) AS Avg_Balance
FROM bank_customer_loan
GROUP BY Region, State
ORDER BY Region, Total_Customers DESC;

-- ------------------------------------------------------------------------------
-- Query 6: Top 10 Depositors (High Net-Worth Customers)
-- Identifies top customers by total account balance for private banking prioritization.
-- ------------------------------------------------------------------------------
SELECT 
    Customer_ID,
    First_Name,
    Last_Name,
    City,
    State,
    Customer_Segment,
    Annual_Income,
    Account_Balance,
    Savings_Balance,
    Current_Account_Balance,
    Number_of_Products
FROM bank_customer_loan
ORDER BY Account_Balance DESC
LIMIT 10;

-- ------------------------------------------------------------------------------
-- Query 7: High-Income Low-Balance Target Customers (Deposit Mobilization Leads)
-- Identifies customers earning >$100,000 but holding <$10,000 in bank deposits.
-- ------------------------------------------------------------------------------
SELECT 
    Customer_ID,
    First_Name,
    Last_Name,
    Age,
    Occupation,
    Annual_Income,
    Account_Balance,
    Debt_to_Income_Ratio,
    Customer_Segment
FROM bank_customer_loan
WHERE Annual_Income >= 100000 
  AND Account_Balance < 10000
ORDER BY Annual_Income DESC
LIMIT 20;

-- ------------------------------------------------------------------------------
-- Query 8: Digital Banking Channel Adoption by Age Group
-- Assesses online and mobile banking engagement across generational cohorts.
-- ------------------------------------------------------------------------------
SELECT 
    Age_Group,
    COUNT(Customer_ID) AS Total_Customers,
    ROUND(SUM(CASE WHEN Online_Banking = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Online_Banking_Pct,
    ROUND(SUM(CASE WHEN Mobile_Banking = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Mobile_Banking_Pct,
    ROUND(SUM(CASE WHEN Credit_Card = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Credit_Card_Penetration_Pct
FROM bank_customer_loan
GROUP BY Age_Group
ORDER BY Age_Group;

-- ------------------------------------------------------------------------------
-- Query 9: Product Depth & Multi-Product Holding Distribution
-- Distribution of customers across the number of banking products held.
-- ------------------------------------------------------------------------------
SELECT 
    Number_of_Products,
    COUNT(Customer_ID) AS Customer_Count,
    ROUND(COUNT(Customer_ID) * 100.0 / (SELECT COUNT(*) FROM bank_customer_loan), 2) AS Pct_Share,
    ROUND(AVG(Account_Balance), 2) AS Avg_Balance,
    ROUND(AVG(Annual_Income), 2) AS Avg_Income
FROM bank_customer_loan
GROUP BY Number_of_Products
ORDER BY Number_of_Products ASC;
