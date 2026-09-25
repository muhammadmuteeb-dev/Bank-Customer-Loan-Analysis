# Executive Analytics & Risk Report: Bank Customer & Loan Portfolio
**Prepared for**: Board of Directors, Chief Risk Officer, and Head of Retail Lending  
**Report Generated**: 2026-09-08 19:28:45  
**Portfolio Scope**: 20,000 Retail Banking Customers | 15 Commercial Branches | 5 Core Credit Products  

---

## 1. Executive Summary & Key Performance Indicators

This enterprise analytics report presents empirical findings from the **Bank Customer & Loan Analysis** pipeline. All metrics have been rigorously verified through Python data analysis, SQLite database queries, and Power BI DAX reconciliation.

| Core Executive Metric | Computed Value | Strategic Benchmark | Status / Health Rating |
| :--- | :--- | :--- | :--- |
| **Total Customer Base** | **20,000** | Target: 20,000 | Normal |
| **Total Depository Balances** | **$579.24M** | Target: >$500M | Healthy Liquidity |
| **Average Depository Balance** | **$28,961.94** | Median: $20,919.81 | Positive Skew |
| **Average Annual Income** | **$81,793.40** | Median: $76,800.00 | Prime Middle-Income |
| **Average Customer Credit Score** | **717.0 FICO** | Threshold: >680 | Prime Quality |
| **Total Loan Applications** | **20,000** | 100% evaluated | Full Funnel |
| **Approved Loan Applications** | **15,403 (77.02%)** | Benchmark: 70–78% | Balanced Underwriting |
| **Declined Loan Applications** | **3,827 (19.13%)** | Risk Controls | Controlled Risk |
| **Total Capital Requested** | **$2,351.04M** | Full Demand | Strong Demand |
| **Total Capital Funded** | **$1,892.98M** | Net Disbursed | High Deployment |
| **Average Funded Loan Ticket** | **$122,896.65** | Portfolio Mean | Robust Facility Size |
| **Portfolio Default Rate (Count)** | **2.25% (346 loans)** | Tolerance: < 3.5% | Low Default Environment |
| **Defaulted Capital Loss** | **$25.29M (1.34%)** | Cap: < 2.0% | Strong Collateralization |
| **Projected Annual Interest Yield** | **$106.01M** | Net Yield | High Margin |

---

## 2. Customer Demographics & Socioeconomic Profile

* **Gender Breakdown**: Male borrowers represent **51.21%** and Female borrowers represent **48.79%**, demonstrating balanced demographic engagement.
* **Age Distribution**: The customer base spans ages 18 to 75, with a mean age of **41.5 years** and a median of **41 years**. Core borrowing demand is concentrated between ages 26 and 50.
* **Digital Banking Engagement**:
  * **Online Banking Adoption**: **82.26%**
  * **Mobile Banking Adoption**: **78.16%**
  * **Credit Card Penetration**: **71.58%**
  * **Debit Card Penetration**: **88.24%**
  * **Average Products Per Customer**: **2.99 products**, indicating strong cross-selling potential.

---

## 3. Loan Portfolio Underwriting & Product Line Performance

Analysis of the bank's credit products demonstrates distinct capital allocation, margin yields, and term structures:

```text
     Loan_Type  Total_Applications  Approved_Count  Total_Application_Volume  Avg_Interest_Rate  Avg_Tenure_Months  Avg_Installment  Total_Funded_Volume  Avg_Funded_Amount  Approval_Rate  Total_Funded_Volume_M  Total_Application_Volume_M
     Auto Loan                4281            3317               130170100.0               6.98               54.7           673.74          105191000.0           31712.69          77.48                 105.19                      130.17
 Business Loan                1808            1311               177918800.0               8.74               55.5          2564.79          133769500.0          102036.23          72.51                 133.77                      177.92
Education Loan                2188            1686                82413100.0               6.05              101.0           527.52           66716300.0           39570.76          77.06                  66.72                       82.41
     Home Loan                6477            4992              1879512200.0               5.46              293.0          1856.03         1520778100.0          304643.05          77.07                1520.78                     1879.51
 Personal Loan                5246            4097                81025000.0              11.72               33.5           655.21           66522200.0           16236.81          78.10                  66.52                       81.03
```

### Strategic Product Insights:
1. **Home Loans (Mortgages)**: Account for the vast majority of balance sheet capital (**$1,520.78M**), serving as the foundational collateralized asset anchor for retail banking.
2. **Auto Loans**: Generated strong origination velocity (**3,317 approvals**) with an average ticket size of **$31,712.69**.
3. **Personal Loans**: While carrying higher default risk, deliver the bank's highest average gross margin with interest rates averaging **11.72%**.
4. **Commercial Business Loans**: Produced **$133.77M** in funded volume, fueling local business expansion across commercial branch centers.

---

## 4. Credit Risk, Leverage & Delinquency Diagnostics

* **Total Active Loans Evaluated**: **15,403 facilities**
* **Total Defaulted Accounts**: **346 accounts**
* **Net Delinquency Rate**: **2.25%**

### Risk Category Distribution:
```text
 Risk_Category  Total_Loans  Default_Loans  Default_Rate  Total_Amount_M  Avg_Credit_Score
      Low Risk        13789            205          1.49         1829.03             748.5
   Medium Risk         1403            100          7.13           59.65             668.7
     High Risk          180             26         14.44            3.75             626.3
Very High Risk           31             15         48.39            0.55             596.2
```

### Defaulter vs Non-Defaulter Comparative Profile:
* **Credit Score Divergence**: Non-defaulters average a prime score of **740.6 FICO**, whereas defaulting borrowers average **693.4 FICO** (a **47.2 point spread**).
* **Leverage Stress (DTI)**: Defaulters exhibit significantly higher debt burden, averaging a DTI of **29.98%** compared to **23.09%** for performing borrowers.

---

## 5. Strategic Customer Segmentation Breakdown

Using multi-variable behavioral profiling and K-Means clustering, the customer base has been categorized into 5 distinct tiers:

```text
                  Customer_Count  Customer_Pct  Avg_Annual_Income  Avg_Account_Balance  Avg_Credit_Score  Approval_Rate  Default_Rate
Customer_Segment                                                                                                                     
High Value                   995          4.98          157442.11             94003.35             773.5          89.65          1.35
Premium                     8442         42.21          108868.76             36744.66             749.7          87.76          1.65
Standard                    6551         32.76           54495.27             17802.14             701.9          68.72          3.35
Emerging                    3438         17.19           49600.03             13850.30             720.9          73.97          2.08
High Risk                    574          2.87           56828.75             19630.63             573.1           9.93         14.04
```

* **High Value Segment**: Represents high net-worth individuals commanding **$94,003.35** in average balances and **89.65%** loan approval rates with negligible default risk (**1.35%**).
* **Premium Segment**: Represents the bank's core commercial engine (**8,442 clients, 42.21% of customer base**), holding **$310.20M** in total deposits.
* **High Risk Segment**: Exhibits elevated delinquency (**14.04% default rate**), warranting stringent collateral enforcement and lower credit limits.

---

## 6. Executive Recommendations for Bank Management

1. **Deposit Mobilization from Affluent Non-Borrowers**: Target the **high-balance, low-credit-utilization customer group** identified in SQL analysis (Query 7, Script 01). Launch structured wealth management and premier certificate of deposit campaigns.
2. **Implement Automated DTI Caps on Unsecured Borrowing**: Historical delinquency spikes sharply when borrower DTI exceeds **40%**. Impose an automated policy cap of 45% DTI on Personal Loans unless backed by cash collateral.
3. **Expand Mortgage Originations in Top Performing Branches**: Branches such as **NYC Metro Branch**, **Chicago Loop Branch**, and **Los Angeles Metro Branch** generate high quality origination with below-average default rates. Increase allocated lending capacity in these commercial centers.
4. **Digital Cross-Sell Acceleration**: With **78.16% mobile adoption**, embed real-time pre-approved auto and personal loan offers directly inside the mobile banking app for customers in the *Premium* and *Emerging* segments.
5. **Early Warning Credit Surveillance**: Automate quarterly credit score re-pulls for borrowers in the *Medium Risk* and *High Risk* tiers to identify pre-delinquency distress prior to 90-day delinquency.

---
*Report certified by Bank Analytics & Risk Underwriting Engineering.*
