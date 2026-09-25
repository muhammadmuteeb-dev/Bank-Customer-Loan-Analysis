**# Bank Customer & Loan Analysis — Complete End-to-End Analytics Project**

[![Python Version]\(https\://img.shields.io/badge/Python-3.13-blue.svg)]\(https\://www\.python.org/)

[![License]\(https\://img.shields.io/badge/License-MIT-green.svg)]\(LICENSE)

[![Pandas]\(https\://img.shields.io/badge/Pandas-2.3-orange.svg)]\(https\://pandas.pydata.org/)

[![Power BI]\(https\://img.shields.io/badge/Power_BI-Desktop-yellow\.svg)]\(https\://powerbi.microsoft.com/)

[![SQL]\(https\://img.shields.io/badge/SQL-SQLite%20%7C%20PostgreSQL%20%7C%20T--SQL-lightgrey.svg)]\(sql/)

A comprehensive, institutional-grade commercial banking analytics project demonstrating advanced capabilities across **\*\*Python, SQL, Excel, and Power BI\*\***. This project delivers an end-to-end data analytics pipeline—from synthetic dataset generation with complex cross-variable financial logic, data cleaning, statistical modeling, machine learning customer segmentation (K-Means), and automated Excel reporting, to SQL query suites and an interactive Power BI dashboard with 4 core business charts.

**---**

**## 1. Project Overview & Business Problem**

Modern commercial banks operate in a dynamic, capital-constrained macroeconomic environment characterized by interest rate fluctuations, credit risk exposure, and intense digital competition. Bank executive leadership and credit risk officers require unified business intelligence to answer critical strategic questions:

1\. **\*\*Portfolio Health & Deployment\*\***: What is the bank's total deployed credit capital, gross yield, and underwriting efficiency?

2\. **\*\*Underwriting Performance\*\***: What proportion of loan applications are approved versus declined across borrower income tiers and product types?

3\. **\*\*Credit Risk & Delinquency\*\***: Which borrower cohorts and leverage ratios drive portfolio default risk? Where is capital loss concentrated?

4\. **\*\*Customer Lifetime Value & Segments\*\***: Who are the bank's most profitable customers, and how can depository balances be mobilized from high-earning non-borrowers?

5\. **\*\*Branch & Geographic Efficiency\*\***: Which commercial branches and geographic regions generate top origination volume and superior risk-adjusted returns?

This project provides end-to-end data-driven solutions to these executive questions using an empirically verified dataset of **\*\*20,000 retail banking customers\*\*** across **\*\*15 commercial branch locations\*\***.

**---**

**## 2. Key Performance Indicators (Empirical Benchmarks)**

All metrics below are calculated directly from the processed dataset (\`20,000\` customer applications):

\| Domain | Key Performance Indicator | Computed Metric | Strategic Context & Benchmark |

\| :--- | :--- | :--- | :--- |

\| **\*\*Deposits & Wealth\*\*** | **\*\*Total Retail Customers\*\*** | **\*\*20,000\*\*** | Full commercial retail base |

\| **\*\*Deposits & Wealth\*\*** | **\*\*Total Depository Balances\*\*** | **\*\*$579.24 Million\*\*** | Aggregate customer liquidity |

\| **\*\*Deposits & Wealth\*\*** | **\*\*Average Customer Balance\*\*** | **\*\*$28,961.94\*\*** | Median: $21,430.50 (Positive skew) |

\| **\*\*Deposits & Wealth\*\*** | **\*\*Average Annual Income\*\*** | **\*\*$81,793.40\*\*** | Median: $72,400.00 |

\| **\*\*Credit Origination\*\*** | **\*\*Total Loan Applications\*\*** | **\*\*20,000\*\*** | 100% evaluated through underwriting |

\| **\*\*Credit Origination\*\*** | **\*\*Approved Loans\*\*** | **\*\*15,403\*\*** | **\*\*77.02% Underwriting Approval Rate\*\*** |

\| **\*\*Credit Origination\*\*** | **\*\*Declined / Rejected Loans\*\*** | **\*\*3,827\*\*** | **\*\*19.14% Rejection Rate\*\*** |

\| **\*\*Credit Origination\*\*** | **\*\*Pending Applications\*\*** | **\*\*770\*\*** | **\*\*3.85% Under Review\*\*** |

\| **\*\*Capital Allocation\*\*** | **\*\*Total Capital Requested\*\*** | **\*\*$2,351.04 Million ($2.35B)\*\*** | Gross borrowing demand |

\| **\*\*Capital Allocation\*\*** | **\*\*Total Capital Funded\*\*** | **\*\*$1,892.98 Million ($1.89B)\*\*** | Net funded balance sheet capital |

\| **\*\*Capital Allocation\*\*** | **\*\*Average Funded Loan Size\*\*** | **\*\*$122,896.65\*\*** | Weighted ticket size across facilities |

\| **\*\*Risk & Delinquency\*\*** | **\*\*Active Loan Portfolio Defaults\*\*** | **\*\*346 Loans\*\*** | **\*\*2.25% Default Rate (on approved loans)\*\*** |

\| **\*\*Risk & Delinquency\*\*** | **\*\*Defaulted Capital Loss Exposure\*\*** | **\*\*$25.29 Million\*\*** | **\*\*1.34% Capital Loss Severity Rate\*\*** |

\| **\*\*Portfolio Margin\*\*** | **\*\*Average Funded Interest Rate\*\*** | **\*\*6.27%\*\*** | Weighted gross lending rate |

\| **\*\*Portfolio Margin\*\*** | **\*\*Est. Annual Gross Interest Income\*\*** | **\*\*$107.82 Million\*\*** | Annualized interest cash flow |

**---**

**## 3. Technology Stack & Skills Demonstrated**

\`\`\`mermaid

flowchart LR

    subgraph Data_Pipeline [Data Engineering & Modeling]

        P[Python 3.13] --> PD[Pandas & NumPy]

        PD --> SK[Scikit-Learn K-Means]

    end

    subgraph Visual_Analytics [Visual & Reporting Layer]

        PD --> PLT[Matplotlib & Seaborn]

        PD --> XL[OpenPyXL Excel Engine]

        PD --> PBI[Power BI Star Schema]

    end

    subgraph Query_Engine [Relational Verification]

        PD --> SQL[SQL / SQLite Engine]

    end

\`\`\`

\* **\*\*Python 3.13\*\***: Modular architecture, data generation with probabilistic business rules, IQR outlier remediation, string sanitization, and automated pipeline orchestration.

\* **\*\*Pandas & NumPy\*\***: High-performance vectorized transformations, category binning, financial installment amortization formulas, and feature engineering.

\* **\*\*Scikit-Learn\*\***: StandardScaler feature normalization and K-Means machine learning clustering ($k=5$).

\* **\*\*Matplotlib & Seaborn\*\***: 18 publication-quality 300-DPI visualizations styled in an executive banking theme (\`#1B365D\`, \`#008080\`, \`#E74C3C\`).

\* **\*\*SQL (ANSI / SQLite / PostgreSQL)\*\***: 31 production-grade queries across 4 scripts utilizing CTEs, window functions (\`DENSE_RANK\`, \`NTILE\`, \`ROW_NUMBER\`, \`SUM() OVER\`), multi-table aggregations, and subqueries.

\* **\*\*Microsoft Excel (OpenPyXL)\*\***: Programmatic generation of an 8-worksheet stylized workbook with KPI cards, formatted financial tables, zebra striping, conditional formatting, and native Excel charts.

\* **\*\*Microsoft Power BI Desktop\*\***: Enterprise Star Schema architecture (4 Dimensions, 1 Fact), 39 DAX measures across 6 display folders, and an interactive dashboard with 4 core business charts.

**---**

**## 4. Repository Structure**

\`\`\`text

Bank-Customer-Loan-Analysis/

│

├── data/

│   ├── raw/

│   │   └── bank_customer_loan_raw\.csv           <- Synthetic raw dataset with injected defects (20,450 rows)

│   └── processed/

│       ├── bank_customer_loan_clean.csv         <- Cleaned, engineered master dataset (20,000 rows)

│       └── powerbi_tables/                      <- Normalized Star Schema tables for Power BI

│           ├── DimCustomer.csv                  <- Customer dimension (20,000 rows)

│           ├── DimBranch.csv                    <- Branch network dimension (15 rows)

│           ├── DimLoanType.csv                  <- Product line classification (5 rows)

│           ├── DimDate.csv                      <- Master calendar dimension (2,192 days)

│           └── FactLoan.csv                     <- Loan origination fact table (20,000 rows)

│

├── python/

│   ├── \_\_init\_\_.py                              <- Package marker

│   ├── data_generation.py                       <- Generates realistic dataset with controlled defects

│   ├── data_cleaning.py                         <- Deduplication, imputation, validation & Star Schema export

│   ├── customer_segmentation.py                 <- Behavioral profiling & Scikit-Learn K-Means clustering

│   ├── customer_analysis.py                     <- Customer demographics & wealth analytics

│   ├── loan_analysis.py                         <- Underwriting, volume, interest rate & duration analytics

│   ├── risk_analysis.py                         <- Delinquency modeling, DTI exposure & default diagnostics

│   ├── eda.py                                   <- Generates 18 high-resolution charts in outputs/charts/

│   ├── excel_dashboard.py                       <- Builds automated 8-worksheet Excel workbook

│   ├── sql_runner.py                            <- In-memory SQLite runner validating all 31 SQL queries

│   └── main.py                                  <- Single master CLI orchestrator executing full pipeline

│

├── sql/

│   ├── 01_basic_customer_analysis.sql           <- Demographics, wealth rankings, digital banking adoption

│   ├── 02_loan_analysis.sql                     <- Underwriting funnels, product line volumes, regional demand

│   ├── 03_risk_analysis.sql                     <- Delinquency rates, credit tiers, high-leverage watchlists

│   └── 04_advanced_banking_analysis.sql         <- Window functions, running totals, quintiles & cross-sell CTEs

│

├── powerbi/

│   ├── Bank data.pbix                       <- Step-by-step implementation and publishing manual

\* **\*\*[\`DASHBOARD_DESIGN.md\`]\(**powerbi/DASHBOARD_DESIGN.md**\)\*\***: Detailed Power BI dashboard layout and visual specifications, including canvas coordinates, visual types, fields, slicers, KPI cards, tables, 4 core charts, conditional formatting rules, and executive color theme palettes.

│   └── POWER_BI_CHECKLIST.md                    <- 40-point quality assurance & validation checklist

│

├── outputs/

│   ├── charts/                                  <- 18 High-resolution publication charts (300 DPI)

│   │   ├── 01_age_distribution.png

│   │   ├── 02_income_distribution.png

│   │   ├── 03_account_balance_distribution.png

│   │   ├── 04_credit_score_distribution.png

│   │   ├── 05_customer_segments.png

│   │   ├── 06_loan_type_distribution.png

│   │   ├── 07_loan_approval_status.png

│   │   ├── 08_loan_amount_distribution.png

│   │   ├── 09_loan_amount_by_type.png

│   │   ├── 10_approval_by_credit_category.png

│   │   ├── 11_default_rate_by_risk.png

│   │   ├── 12_default_rate_by_loan_type.png

│   │   ├── 13_customers_by_region.png

│   │   ├── 14_loan_amount_by_region.png

│   │   ├── 15_income_vs_loan_amount.png

│   │   ├── 16_credit_score_vs_loan_amount.png

│   │   ├── 17_debt_to_income_distribution.png

│   │   └── 18_branch_performance_matrix.png

│   ├── Bank_Customer_Loan_Analysis.xlsx         <- Automated 8-tab Excel report generated via Python

│   └── executive_summary.md                     <- Comprehensive C-suite risk & performance briefing

│

├── requirements.txt                             <- Clean project dependencies

├── .gitignore                                   <- Production Git ignore configuration

└── README.md                                    <- Master GitHub portfolio documentation

\`\`\`

**---**

**## 5. End-to-End Analytics Workflow**

**### Step 1: Realistic Data Generation with Controlled Defects**

\* Generates 20,000 base customer applications using correlated financial distributions:

  \* **\*\*Income\*\***: Log-normal distribution conditioned on education, age, and occupation.

  \* **\*\*Balances\*\***: Correlated with income and customer tenure (0.2 to 20 years).

  \* **\*\*Credit Scores\*\***: FICO distribution (300–850) centered around 695–715 with realistic subprime tails.

  \* **\*\*Underwriting\*\***: Multi-factor scorecard assessing Credit Score, DTI, Income, and Loan-to-Income ratios.

  \* **\*\*Delinquency\*\***: Modeled default probabilities calibrated to real-world commercial benchmarks.

\* **\*\*Controlled Noise\*\***: Appends 450 duplicate rows (\~2.2%), injects missing values (2–3% in non-critical attributes), inserts dirty string formatting (e.g. \` $75,000 \`), and introduces bounded age/balance outliers to demonstrate data cleaning.

**### Step 2: Data Cleaning & Feature Engineering Pipeline**

\* **\*\*Deduplication\*\***: Identifies and removes duplicate records, preserving 20,000 unique records.

\* **\*\*Sanitization\*\***: Strips formatting symbols, parses ISO dates, and clamps invalid age/balance anomalies.

\* **\*\*Domain Feature Engineering\*\***:

  \* \`Age_Group\`: \`18-25\`, \`26-35\`, \`36-50\`, \`51-65\`, \`65+\`

  \* \`Income_Group\`: \`Low (<$35k)\`, \`Lower-Middle ($35k-$60k)\`, \`Middle ($60k-$100k)\`, \`Upper-Middle ($100k-$150k)\`, \`High (>=$150k)\`

  \* \`Credit_Score_Category\`: \`Poor (300-579)\`, \`Fair (580-669)\`, \`Good (670-739)\`, \`Very Good (740-799)\`, \`Excellent (800-850)\`

  \* \`Loan_Amount_Category\`: \`Micro (<$10k)\`, \`Small ($10k-$25k)\`, \`Medium ($25k-$75k)\`, \`Large ($75k-$200k)\`, \`Jumbo (>=$200k)\`

  \* \`Debt_to_Income_Category\`: \`Low (<20%)\`, \`Moderate (20-35%)\`, \`Manageable (36-49%)\`, \`Critical (>=50%)\`

  \* \`Monthly_Income\`: \`Annual_Income / 12\`

  \* \`Estimated_Annual_Interest\`: \`Loan_Amount \* (Interest_Rate / 100)\`

\* **\*\*Star Schema Export\*\***: Automatically splits the cleaned flat dataset into 4 dimension tables and 1 central fact table in \`data/processed/powerbi_tables/\`.

**---**

**## 6. Strategic Customer Segmentation (Behavioral & K-Means)**

The customer base was segmented into 5 strategic tiers using both domain-driven heuristic profiling and unsupervised **\*\*K-Means Clustering\*\*** ($k=5$, standardized on 6 numerical features):

\| Customer Segment | Customer Count | Share (%) | Avg Annual Income | Avg Account Balance | Total Deposits ($M) | Approval Rate (%) | Default Rate (%) | Strategic Banking Action |

\| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

\| **\*\*High Value\*\*** | **\*\*995\*\*** | **\*\*4.97%\*\*** | **\*\*$157,442.11\*\*** | **\*\*$94,003.35\*\*** | **\*\*$93.53M\*\*** | **\*\*89.65%\*\*** | **\*\*1.35%\*\*** | Private Banking, Wealth Management, Bespoke Mortgages |

\| **\*\*Premium\*\*** | **\*\*8,442\*\*** | **\*\*42.21%\*\*** | **\*\*$108,868.76\*\*** | **\*\*$36,744.66\*\*** | **\*\*$310.20M\*\*** | **\*\*87.76%\*\*** | **\*\*1.65%\*\*** | Commercial Lending, Investment Advisory, Card Upgrades |

\| **\*\*Standard\*\*** | **\*\*6,551\*\*** | **\*\*32.76%\*\*** | **\*\*$54,495.27\*\*** | **\*\*$17,802.14\*\*** | **\*\*$116.62M\*\*** | **\*\*68.72%\*\*** | **\*\*3.35%\*\*** | Automated Payroll, Auto Financing, Digital Cross-sell |

\| **\*\*Emerging\*\*** | **\*\*2,752\*\*** | **\*\*13.76%\*\*** | **\*\*$48,320.45\*\*** | **\*\*$16,840.10\*\*** | **\*\*$46.34M\*\*** | **\*\*66.82%\*\*** | **\*\*2.83%\*\*** | First-Time Homebuyer Programs, Career Starter Credit |

\| **\*\*High Risk\*\*** | **\*\*1,260\*\*** | **\*\*6.30%\*\*** | **\*\*$39,210.80\*\*** | **\*\*$9,950.25\*\*** | **\*\*$12.54M\*\*** | **\*\*38.41%\*\*** | **\*\*9.28%\*\*** | Collateralized Credit Only, Strict DTI Caps, Financial Coaching |

**---**

**## 7. Loan Portfolio Performance by Product Line**

\| Loan Product Line | Applications | Approved Count | Approval Rate (%) | Total Requested ($M) | Total Funded ($M) | Avg Funded Size | Avg Interest Rate | Avg Tenure (Mo) | Default Rate (%) |

\| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

\| **\*\*Home Loan\*\*** | 6,477 | 4,992 | **\*\*77.07%\*\*** | $1,879.51M | **\*\*$1,520.78M\*\*** | $304,643.05 | 5.46% | 293.0 | **\*\*1.14%\*\*** |

\| **\*\*Business Loan\*\*** | 1,808 | 1,311 | **\*\*72.51%\*\*** | $177.92M | **\*\*$133.77M\*\*** | $102,036.23 | 8.74% | 55.5 | **\*\*3.05%\*\*** |

\| **\*\*Auto Loan\*\*** | 4,281 | 3,317 | **\*\*77.48%\*\*** | $130.17M | **\*\*$105.19M\*\*** | $31,712.69 | 6.98% | 54.7 | **\*\*1.87%\*\*** |

\| **\*\*Education Loan\*\*** | 2,213 | 1,702 | **\*\*76.91%\*\*** | $84.28M | **\*\*$67.89M\*\*** | $39,888.37 | 6.01% | 108.5 | **\*\*2.29%\*\*** |

\| **\*\*Personal Loan\*\*** | 5,221 | 4,081 | **\*\*78.16%\*\*** | $79.16M | **\*\*$65.35M\*\*** | $16,014.21 | 11.75% | 38.2 | **\*\*4.61%\*\*** |

\| **\*\*Total / Overall\*\*** | **\*\*20,000\*\*** | **\*\*15,403\*\*** | **\*\*77.02%\*\*** | **\*\*$2,351.04M\*\*** | **\*\*$1,892.98M\*\*** | **\*\*$122,896.65\*\*** | **\*\*6.27%\*\*** | **\*\*123.4\*\*** | **\*\*2.25%\*\*** |

**---**

**## 8. Credit Risk, Leverage & Delinquency Diagnostics**

\* **\*\*Credit Score Divergence\*\***: Defaulters average a FICO score of **\*\*635.8\*\***, compared to **\*\*749.2\*\*** for performing borrowers (an empirical **\*\*113.4-point risk gap\*\***).

\* **\*\*Leverage Shock (DTI)\*\***: Defaulters hold an average DTI of **\*\*41.2%\*\***, versus **\*\*22.8%\*\*** for non-defaulters.

\* **\*\*Internal Risk Rating Validation\*\***:

  \* **\*\*Low Risk\*\***: Accounts for **\*\*89.5%\*\*** of funded loans with a **\*\*1.49%\*\*** default rate.

  \* **\*\*Medium Risk\*\***: Accounts for **\*\*9.1%\*\*** of funded loans with a **\*\*7.13%\*\*** default rate.

  \* **\*\*High Risk\*\***: Accounts for **\*\*1.2%\*\*** of funded loans with a **\*\*14.44%\*\*** default rate.

  \* **\*\*Very High Risk\*\***: Defaults exceed **\*\*25.0%\*\***, confirming underwriting filter accuracy.

**---**

**## 9. Automated Excel Report (\`outputs/Bank_Customer_Loan_Analysis.xlsx\`)**

The automated Python \`openpyxl\` engine compiles an 8-worksheet executive workbook:

1\. **\*\*Executive Summary\*\***: KPI blocks, summary portfolio tables, and an embedded native column chart.

2\. **\*\*Customer Analysis\*\***: Age group demographics, socioeconomic income groups, and product penetration tables.

3\. **\*\*Loan Analysis\*\***: Loan purpose breakdown, term distributions, and application ticket sizing.

4\. **\*\*Risk Analysis\*\***: Delinquency tables by risk category, credit score bands, and conditional formatting.

5\. **\*\*Customer Segments\*\***: Strategic profiles, deposit concentration, and targeted banking actions.

6\. **\*\*Branch Performance\*\***: Ranked table of all 15 branches by origination volume and default percentage.

7\. **\*\*Regional Analysis\*\***: Footprint analysis across Midwest, Northeast, South, and West territories.

8\. **\*\*Data Dictionary & Sample\*\***: Schema specifications, column types, descriptions, and sample records.

**---**

**## 10. Power BI Dashboard Documentation Suite (\`powerbi/\`)**

The project includes an enterprise-grade documentation and blueprint suite for Power BI implementation:

\* **\*\*[\`POWER_BI_GUIDE.md\`]\(**powerbi/POWER_BI_GUIDE.md**)\*\***: Comprehensive guide covering architecture, data loading instructions, modeling steps, relationship creation, DAX measure implementation, visual design specifications, dashboard creation guide, publish/sharing workflow, maintenance plan, and business insights interpretation.

\* **\*\*[\`DATA_MODEL.md\`]\(**powerbi/DATA_MODEL.md**)\*\***: Complete Data Model blueprint documenting the Star Schema architecture, fact and dimension tables, key relationships, cardinality, cross-filter directions, surrogate keys, date table specification, column descriptions, and data types.

\* **\*\*[\`DAX_MEASURES.md\`]\(**powerbi/DAX_MEASURES.md**)\*\***: Exhaustive library of 39 verified DAX measures organized into 6 display folders (Core Portfolio KPIs, Loan Performance KPIs, Risk & Credit KPIs, Customer & Demographic KPIs, Time Intelligence KPIs, and Dynamic Formatting & Auxiliary Measures) with formulas, descriptions, formats, and business usage.

\* **\*\*[\`DASHBOARD_DESIGN.md\`]\(**powerbi/DASHBOARD_DESIGN.md**\)\*\***: Detailed Power BI dashboard layout and visual specifications, including canvas coordinates, visual types, fields, slicers, KPI cards, tables, 4 core charts, conditional formatting rules, and executive color theme palettes.

\* **\*\*[\`POWER_BI_CHECKLIST.md\`]\(**powerbi/POWER_BI_CHECKLIST.md**)\*\***: 40-point quality assurance checklist covering data validation, relationship validation, DAX validation, visual layout validation, performance optimization, and publishing verification.

**---**

**## 11. SQL Analytical Query Engine (\`sql/\`)**

31 production-grade SQL queries are organized into 4 modular scripts and verified using an SQLite engine:

\* **\*\*\`01_basic_customer_analysis.sql\`\*\***: Demographic aggregations, wealth rankings, high-income low-balance mobilization leads, and digital adoption rates.

\* **\*\*\`02_loan_analysis.sql\`\*\***: Approval/rejection funnels, product line performance, stated purposes, and branch league tables.

\* **\*\*\`03_risk_analysis.sql\`\*\***: Delinquency rates across risk categories, FICO tiers, high-risk watchlists, and comparative defaulter profiles.

\* **\*\*\`04_advanced_banking_analysis.sql\`\*\***: Advanced CTEs, \`DENSE_RANK()\` branch rankings, cumulative monthly funded volume running totals (\`SUM() OVER\`), and wealth quintiles (\`NTILE(5)\`).

**---**

**## 12. Strategic Business Recommendations for Bank Management**

1\. **\*\*Deposit Mobilization Campaign for Affluent Non-Borrowers\*\***: Leverage SQL Query 7 (Script 01) to identify high-earning depositors ($100k+ income) who hold low balance or no credit facilities. Deploy relationship managers to offer premium high-yield certificates of deposit.

2\. **\*\*Implement Automated DTI Caps on Unsecured Borrowing\*\***: Delinquency accelerates rapidly when borrower DTI surpasses **\*\*40%\*\***. Establish an automated underwriting threshold capping unsecured personal credit at 40% DTI unless supported by collateral.

3\. **\*\*Scale Lending Capacity in High-Performing Branches\*\***: **\*\*NYC Metro Branch\*\*** ($188.5M funded), **\*\*Chicago Loop Branch\*\*** ($172.8M funded), and **\*\*Dallas Commercial Branch\*\*** ($158.2M funded) demonstrate strong origination volume and low delinquency (< 2.0%). Allocate additional lending quotas to these hubs.

4\. **\*\*Digital Mobile Cross-Sell Acceleration\*\***: With **\*\*77.8% mobile app adoption\*\***, embed instant pre-approved auto and personal loan offers directly within the mobile application for customers in the *\*Premium\** and *\*Emerging\** segments.

5\. **\*\*Early Warning Surveillance on Subprime Borrowers\*\***: Automate quarterly credit score re-pulls for active borrowers with credit scores below 640 to identify deteriorating credit capacity before 90-day delinquency occurs.

**---**

**## 13. How to Run the Complete Project**

**### Prerequisites**

\* Python 3.10+ (Tested on Python 3.13)

\* Git

**### Installation**

\`\`\`bash

\# 1. Clone this repository

git clone https\://github.com/muteebshafique.dev/Bank-Customer-Loan-Analysis.git

cd Bank-Customer-Loan-Analysis

\# 2. Create and activate a virtual environment (optional but recommended)

python -m venv venv

\# On Windows:

venv\Scripts\activate

\# On macOS/Linux:

source venv/bin/activate

\# 3. Install required dependencies

pip install -r requirements.txt

\`\`\`

**### Run the Master Pipeline**

\`\`\`bash

python python/main.py

\`\`\`

This single command executes the entire pipeline:

1\. Generates the raw dataset (\`data/raw/bank_customer_loan_raw\.csv\`).

2\. Cleans the data, handles defects, and engineers features (\`data/processed/bank_customer_loan_clean.csv\`).

3\. Exports Star Schema tables (\`data/processed/powerbi_tables/\`).

4\. Performs customer segmentation and K-Means clustering.

5\. Performs customer, loan, and risk analytics.

6\. Renders all 18 publication-quality charts (\`outputs/charts/\`).

7\. Builds the 8-worksheet Excel dashboard (\`outputs/Bank_Customer_Loan_Analysis.xlsx\`).

8\. Validates all 31 SQL queries against the in-memory database.

9\. Compiles the executive summary report (\`outputs/executive_summary.md\`).

**---**

**## 14. License & Author**

\* **\*\*Author\*\***: Antigravity Data Analytics & Financial Intelligence Team

\* **\*\*License\*\***: MIT License — open for personal portfolio use, recruitment evaluations, and commercial adaptation.
