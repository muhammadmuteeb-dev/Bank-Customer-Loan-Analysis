"""
Bank Customer & Loan Analysis - Data Generation Module
Generates a realistic synthetic banking dataset with logical financial relationships
and controlled data-quality issues for cleaning demonstrations.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_bank_data(n_records: int = 20000, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic banking dataset with realistic cross-variable relationships.
    """
    np.random.seed(random_seed)
    print(f"[*] Generating {n_records:,} base customer records (Seed={random_seed})...")

    # 1. Names and Demographics
    first_names_male = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas",
        "Charles", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew",
        "Kenneth", "Joshua", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason",
        "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry",
        "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Alexander", "Frank", "Patrick"
    ]
    first_names_female = [
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah",
        "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra", "Ashley", "Kimberly", "Emily",
        "Donna", "Michelle", "Carol", "Amanda", "Dorothy", "Melissa", "Deborah", "Stephanie", "Rebecca",
        "Sharon", "Laura", "Cynthia", "Kathleen", "Amy", "Angela", "Shirley", "Anna", "Brenda",
        "Pamela", "Emma", "Nicole", "Helen", "Samantha", "Katherine", "Christine", "Debra", "Rachel"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
        "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
        "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
        "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott",
        "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera"
    ]

    # Assign Gender
    genders_clean = np.random.choice(["Male", "Female"], size=n_records, p=[0.51, 0.49])
    first_names = []
    for g in genders_clean:
        if g == "Male":
            first_names.append(np.random.choice(first_names_male))
        else:
            first_names.append(np.random.choice(first_names_female))
    
    last_names_selected = np.random.choice(last_names, size=n_records)
    customer_ids = [f"CUST-{10001 + i}" for i in range(n_records)]

    # Age distribution: Realistic working age (18 - 75), normal-skewed around 41
    ages_raw = np.random.normal(loc=41.5, scale=12.5, size=n_records)
    ages = np.clip(np.round(ages_raw), 18, 75).astype(int)

    # Date of birth relative to reference date (2024-06-30)
    ref_date = datetime(2024, 6, 30)
    dobs = [ref_date - timedelta(days=int(age * 365.25 + np.random.randint(0, 365))) for age in ages]
    dob_strs = [d.strftime("%Y-%m-%d") for d in dobs]

    # Marital status correlated with age
    marital_statuses = []
    for age in ages:
        if age < 25:
            marital_statuses.append(np.random.choice(["Single", "Married"], p=[0.85, 0.15]))
        elif age < 35:
            marital_statuses.append(np.random.choice(["Single", "Married", "Divorced"], p=[0.45, 0.50, 0.05]))
        elif age < 55:
            marital_statuses.append(np.random.choice(["Single", "Married", "Divorced", "Widowed"], p=[0.20, 0.65, 0.12, 0.03]))
        else:
            marital_statuses.append(np.random.choice(["Single", "Married", "Divorced", "Widowed"], p=[0.12, 0.60, 0.18, 0.10]))

    # Education levels
    education_levels = np.random.choice(
        ["High School", "Associate", "Bachelor", "Master", "Doctorate"],
        size=n_records,
        p=[0.22, 0.15, 0.42, 0.17, 0.04]
    )

    # Occupation & Employment Status
    occupations = []
    employment_statuses = []
    for edu, age in zip(education_levels, ages):
        if age >= 65 and np.random.rand() < 0.60:
            occupations.append("Retired")
            employment_statuses.append("Retired")
        elif age <= 22 and np.random.rand() < 0.35:
            occupations.append("Student")
            employment_statuses.append("Unemployed")
        else:
            if edu in ["Master", "Doctorate"]:
                occ = np.random.choice(["Management", "Professional", "Technology", "Healthcare"], p=[0.35, 0.35, 0.20, 0.10])
                emp = np.random.choice(["Salaried", "Self-Employed", "Contract"], p=[0.78, 0.16, 0.06])
            elif edu == "Bachelor":
                occ = np.random.choice(["Professional", "Management", "Technology", "Sales", "Finance", "Healthcare"], p=[0.30, 0.22, 0.18, 0.15, 0.10, 0.05])
                emp = np.random.choice(["Salaried", "Self-Employed", "Contract", "Employed"], p=[0.70, 0.15, 0.08, 0.07])
            elif edu == "Associate":
                occ = np.random.choice(["Administrative", "Sales", "Skilled Labor", "Healthcare", "Services"], p=[0.28, 0.25, 0.22, 0.15, 0.10])
                emp = np.random.choice(["Salaried", "Employed", "Self-Employed", "Contract"], p=[0.55, 0.25, 0.12, 0.08])
            else: # High School
                occ = np.random.choice(["Skilled Labor", "Services", "Sales", "Administrative", "Logistics"], p=[0.35, 0.30, 0.18, 0.10, 0.07])
                emp = np.random.choice(["Employed", "Salaried", "Self-Employed", "Unemployed"], p=[0.50, 0.32, 0.12, 0.06])
            occupations.append(occ)
            employment_statuses.append(emp)

    # 2. Annual Income (log-normal, conditioned on Education, Age, Occupation)
    annual_incomes = []
    for edu, occ, emp, age in zip(education_levels, occupations, employment_statuses, ages):
        if emp == "Unemployed" or occ == "Student":
            base = np.random.uniform(14000, 26000)
        elif occ == "Retired":
            base = np.random.normal(48000, 15000)
        else:
            # Baseline mean log income
            edu_multipliers = {
                "High School": 1.0,
                "Associate": 1.22,
                "Bachelor": 1.65,
                "Master": 2.10,
                "Doctorate": 2.50
            }
            occ_multipliers = {
                "Management": 1.45, "Professional": 1.30, "Technology": 1.40, "Finance": 1.38,
                "Healthcare": 1.25, "Sales": 1.15, "Administrative": 0.95, "Skilled Labor": 0.92,
                "Logistics": 0.88, "Services": 0.82
            }
            age_factor = 1.0 + (min(age, 55) - 20) * 0.015 # experience premium up to age 55
            base = 32000 * edu_multipliers.get(edu, 1.0) * occ_multipliers.get(occ, 1.0) * age_factor
            noise = np.random.lognormal(mean=0, sigma=0.25)
            base = base * noise
        
        income = max(18000.0, round(float(base), -2))
        annual_incomes.append(income)

    # 3. Branch & Geographic Information
    branches = [
        # Northeast
        {"Branch_ID": "BR-001", "Branch_Name": "NYC Metro Branch", "City": "New York", "State": "NY", "Region": "Northeast"},
        {"Branch_ID": "BR-002", "Branch_Name": "Boston Harbor Branch", "City": "Boston", "State": "MA", "Region": "Northeast"},
        {"Branch_ID": "BR-003", "Branch_Name": "Philadelphia Central Branch", "City": "Philadelphia", "State": "PA", "Region": "Northeast"},
        # Midwest
        {"Branch_ID": "BR-004", "Branch_Name": "Chicago Loop Branch", "City": "Chicago", "State": "IL", "Region": "Midwest"},
        {"Branch_ID": "BR-005", "Branch_Name": "Detroit Downtown Branch", "City": "Detroit", "State": "MI", "Region": "Midwest"},
        {"Branch_ID": "BR-006", "Branch_Name": "Minneapolis Gateway Branch", "City": "Minneapolis", "State": "MN", "Region": "Midwest"},
        # South
        {"Branch_ID": "BR-007", "Branch_Name": "Atlanta Midtown Branch", "City": "Atlanta", "State": "GA", "Region": "South"},
        {"Branch_ID": "BR-008", "Branch_Name": "Dallas Commercial Branch", "City": "Dallas", "State": "TX", "Region": "South"},
        {"Branch_ID": "BR-009", "Branch_Name": "Charlotte Queen City Branch", "City": "Charlotte", "State": "NC", "Region": "South"},
        {"Branch_ID": "BR-010", "Branch_Name": "Miami Coastal Branch", "City": "Miami", "State": "FL", "Region": "South"},
        # West
        {"Branch_ID": "BR-011", "Branch_Name": "San Francisco Tech Branch", "City": "San Francisco", "State": "CA", "Region": "West"},
        {"Branch_ID": "BR-012", "Branch_Name": "Seattle Sound Branch", "City": "Seattle", "State": "WA", "Region": "West"},
        {"Branch_ID": "BR-013", "Branch_Name": "Denver Mile High Branch", "City": "Denver", "State": "CO", "Region": "West"},
        {"Branch_ID": "BR-014", "Branch_Name": "Phoenix Valley Branch", "City": "Phoenix", "State": "AZ", "Region": "West"},
        {"Branch_ID": "BR-015", "Branch_Name": "Los Angeles Metro Branch", "City": "Los Angeles", "State": "CA", "Region": "West"},
    ]
    # Realistic weights for branch allocation
    branch_weights = np.array([0.10, 0.07, 0.06, 0.09, 0.05, 0.05, 0.08, 0.08, 0.06, 0.07, 0.08, 0.06, 0.05, 0.04, 0.06])
    branch_weights = branch_weights / branch_weights.sum()
    selected_branch_indices = np.random.choice(len(branches), size=n_records, p=branch_weights)
    branch_records = [branches[idx] for idx in selected_branch_indices]

    branch_ids = [b["Branch_ID"] for b in branch_records]
    branch_names = [b["Branch_Name"] for b in branch_records]
    cities = [b["City"] for b in branch_records]
    states = [b["State"] for b in branch_records]
    regions = [b["Region"] for b in branch_records]

    # 4. Banking Information & Account Balances
    account_types = np.random.choice(
        ["Savings", "Checking", "Money Market", "Certificate of Deposit"],
        size=n_records,
        p=[0.46, 0.36, 0.13, 0.05]
    )

    # Customer Tenure (0.2 to 20 years, constrained by customer age)
    tenure_years = []
    account_open_dates = []
    for age in ages:
        max_possible_tenure = max(0.5, float(age - 18))
        tenure = min(round(np.random.exponential(scale=5.2) + 0.3, 1), max_possible_tenure, 20.0)
        tenure_years.append(tenure)
        open_d = ref_date - timedelta(days=int(tenure * 365.25))
        account_open_dates.append(open_d.strftime("%Y-%m-%d"))

    # Account balances realistically correlated with income and tenure
    account_balances = []
    savings_balances = []
    current_balances = []

    for inc, ten, acct_type in zip(annual_incomes, tenure_years, account_types):
        # Baseline balance is typically 15% - 60% of annual income + tenure savings
        bal_ratio = np.random.beta(a=2.0, b=4.5) # skewed towards 0.20-0.35
        base_bal = inc * bal_ratio * (1.0 + ten * 0.035)
        # Type multiplier
        if acct_type == "Money Market":
            base_bal *= 1.45
        elif acct_type == "Certificate of Deposit":
            base_bal *= 1.80
        elif acct_type == "Checking":
            base_bal *= 0.65
        
        total_bal = max(250.0, round(float(base_bal), 2))
        account_balances.append(total_bal)

        # Split into savings and current account balance
        split_prop = np.random.uniform(0.55, 0.85)
        sav_bal = round(total_bal * split_prop, 2)
        cur_bal = round(total_bal - sav_bal, 2)
        savings_balances.append(sav_bal)
        current_balances.append(cur_bal)

    # Number of products and digital engagement
    n_products = []
    credit_cards = []
    debit_cards = []
    online_bankings = []
    mobile_bankings = []

    for inc, bal, ten in zip(annual_incomes, account_balances, tenure_years):
        # Propensity for products increases with balance, income, and tenure
        score = (inc / 100000.0) + (bal / 50000.0) + (ten / 10.0)
        p_num = min(5, max(1, int(1 + np.random.poisson(lam=1.5 + 0.3 * score))))
        n_products.append(p_num)

        # Cards & Digital Banking
        cc_prob = min(0.95, 0.40 + 0.000004 * inc)
        credit_cards.append("Yes" if np.random.rand() < cc_prob else "No")
        debit_cards.append("Yes" if np.random.rand() < 0.88 else "No")
        online_bankings.append("Yes" if np.random.rand() < 0.82 else "No")
        mobile_bankings.append("Yes" if np.random.rand() < 0.78 else "No")

    # 5. Credit Information
    # Credit Score (300 to 850, FICO distribution with mean ~695, std ~75)
    credit_scores = []
    existing_loans_list = []
    outstanding_debts = []
    dtis = []

    for inc, age, bal in zip(annual_incomes, ages, account_balances):
        # Base credit score influenced by age and stability
        age_bonus = min(age - 20, 40) * 1.8
        inc_bonus = min(inc / 10000.0, 15) * 3.5
        cs_raw = np.random.normal(loc=660 + age_bonus + inc_bonus, scale=60)
        cs = int(np.clip(round(cs_raw), 320, 850))
        credit_scores.append(cs)

        # Existing loans
        if cs > 740:
            ex_loans = np.random.choice([0, 1, 2, 3], p=[0.30, 0.45, 0.20, 0.05])
        elif cs > 640:
            ex_loans = np.random.choice([0, 1, 2, 3, 4], p=[0.20, 0.38, 0.27, 0.12, 0.03])
        else:
            ex_loans = np.random.choice([1, 2, 3, 4], p=[0.30, 0.40, 0.22, 0.08])
        existing_loans_list.append(ex_loans)

        # Debt to income ratio (DTI)
        # Typically between 0.10 and 0.55
        if cs > 750:
            dti = np.random.beta(2.0, 6.0) * 0.45 + 0.05 # lower DTI
        elif cs > 650:
            dti = np.random.beta(3.0, 5.0) * 0.55 + 0.08
        else:
            dti = np.random.beta(4.0, 4.0) * 0.65 + 0.12 # higher DTI
        
        dti = round(float(np.clip(dti, 0.05, 0.68)), 4)
        dtis.append(dti)

        out_debt = round(inc * dti, 2)
        outstanding_debts.append(out_debt)

    # Credit Score Category mapping
    def get_credit_cat(cs):
        if cs >= 800:
            return "Excellent"
        elif cs >= 740:
            return "Very Good"
        elif cs >= 670:
            return "Good"
        elif cs >= 580:
            return "Fair"
        else:
            return "Poor"

    credit_score_categories = [get_credit_cat(cs) for cs in credit_scores]

    # 6. Loan Information
    loan_ids = [f"LN-{100001 + i}" for i in range(n_records)]
    loan_types = np.random.choice(
        ["Home Loan", "Personal Loan", "Auto Loan", "Education Loan", "Business Loan"],
        size=n_records,
        p=[0.32, 0.26, 0.22, 0.11, 0.09]
    )

    loan_amounts = []
    interest_rates = []
    loan_tenures = []
    monthly_installments = []
    loan_purposes = []
    loan_statuses = []
    approval_dates = []
    application_dates = []

    # Application dates distributed over 3.5 years (2021-01-01 to 2024-06-30)
    start_app_date = datetime(2021, 1, 1)
    date_range_days = (ref_date - start_app_date).days

    for i in range(n_records):
        ltype = loan_types[i]
        inc = annual_incomes[i]
        cs = credit_scores[i]
        dti = dtis[i]
        emp = employment_statuses[i]

        # Loan application date
        app_d = start_app_date + timedelta(days=int(np.random.randint(0, date_range_days)))
        application_dates.append(app_d.strftime("%Y-%m-%d"))

        # Amount and Tenure parameters by Loan Type
        if ltype == "Home Loan":
            purpose = np.random.choice(["Home Purchase", "Refinance", "Home Improvement"], p=[0.70, 0.20, 0.10])
            tenure = np.random.choice([180, 240, 360], p=[0.20, 0.25, 0.55])
            base_amt = min(inc * np.random.uniform(2.5, 4.8), 550000.0)
            base_rate = 5.25
        elif ltype == "Auto Loan":
            purpose = np.random.choice(["New Vehicle", "Used Vehicle", "Refinance Auto"], p=[0.58, 0.35, 0.07])
            tenure = np.random.choice([36, 48, 60, 72], p=[0.15, 0.30, 0.40, 0.15])
            base_amt = min(inc * np.random.uniform(0.20, 0.55), 75000.0)
            base_rate = 6.75
        elif ltype == "Business Loan":
            purpose = np.random.choice(["Business Expansion", "Working Capital", "Equipment Purchase"], p=[0.45, 0.35, 0.20])
            tenure = np.random.choice([24, 36, 60, 84, 120], p=[0.15, 0.30, 0.35, 0.12, 0.08])
            base_amt = min(inc * np.random.uniform(0.60, 1.8), 280000.0)
            base_rate = 8.50
        elif ltype == "Education Loan":
            purpose = np.random.choice(["Undergraduate Studies", "Graduate School", "Vocational Training"], p=[0.55, 0.35, 0.10])
            tenure = np.random.choice([60, 84, 120, 180], p=[0.25, 0.35, 0.25, 0.15])
            base_amt = min(inc * np.random.uniform(0.25, 0.70), 85000.0)
            base_rate = 5.80
        else: # Personal Loan
            purpose = np.random.choice(["Debt Consolidation", "Medical Expenses", "Major Purchase", "Home Renovation", "Wedding"], p=[0.42, 0.20, 0.18, 0.12, 0.08])
            tenure = np.random.choice([12, 24, 36, 48, 60], p=[0.15, 0.25, 0.35, 0.15, 0.10])
            base_amt = min(inc * np.random.uniform(0.08, 0.30), 45000.0)
            base_rate = 11.50

        # Adjust amount
        amt = max(3000.0, round(float(base_amt), -2))
        loan_amounts.append(amt)
        loan_tenures.append(tenure)
        loan_purposes.append(purpose)

        # Risk-adjusted interest rate
        # High credit score -> lower rate; high DTI -> higher rate
        cs_adjustment = (750 - cs) * 0.015 # e.g. cs=600 -> +2.25%
        dti_adjustment = (dti - 0.30) * 4.0 # e.g. dti=0.50 -> +0.80%
        rate = round(float(np.clip(base_rate + cs_adjustment + dti_adjustment + np.random.normal(0, 0.35), 3.25, 21.5)), 2)
        interest_rates.append(rate)

        # Monthly installment calculation: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        monthly_r = (rate / 100.0) / 12.0
        n_months = tenure
        if monthly_r > 0:
            installment = amt * (monthly_r * ((1.0 + monthly_r) ** n_months)) / (((1.0 + monthly_r) ** n_months) - 1.0)
        else:
            installment = amt / n_months
        monthly_installments.append(round(float(installment), 2))

        # Underwriting / Approval decision logic
        # Multi-factor underwriting scorecard
        scorecard = 0.0
        # 1. Credit Score score
        if cs >= 780: scorecard += 45
        elif cs >= 720: scorecard += 35
        elif cs >= 660: scorecard += 20
        elif cs >= 600: scorecard += 5
        else: scorecard -= 25

        # 2. DTI score
        if dti < 0.25: scorecard += 30
        elif dti < 0.38: scorecard += 20
        elif dti < 0.45: scorecard += 5
        elif dti < 0.52: scorecard -= 15
        else: scorecard -= 35

        # 3. Employment & Income
        if emp in ["Salaried", "Professional", "Management"]: scorecard += 15
        elif emp == "Self-Employed": scorecard += 8
        elif emp == "Unemployed": scorecard -= 45

        # 4. Loan to income ratio
        lti = amt / max(inc, 1.0)
        if ltype == "Home Loan" and lti > 4.5: scorecard -= 15
        elif ltype != "Home Loan" and lti > 1.2: scorecard -= 20

        # Logistic approval probability
        # Calibrated so approval rate sits realistically around 70-74%
        p_approval = 1.0 / (1.0 + np.exp(-(scorecard - 18.0) / 16.0))
        
        # Determine status
        rand_val = np.random.rand()
        if rand_val < p_approval * 0.94:
            status = "Approved"
            # Approval date 3 to 14 days after application
            appr_d = app_d + timedelta(days=int(np.random.randint(3, 15)))
            approval_dates.append(appr_d.strftime("%Y-%m-%d"))
        elif rand_val < p_approval * 0.94 + 0.04: # 4% pending
            status = "Pending"
            approval_dates.append(None)
        else:
            status = "Rejected"
            approval_dates.append(None)
        
        loan_statuses.append(status)

    # 7. Risk Analysis & Default Modeling
    default_probabilities = []
    risk_categories = []
    default_flags = []

    for i in range(n_records):
        cs = credit_scores[i]
        dti = dtis[i]
        rate = interest_rates[i]
        ltype = loan_types[i]
        status = loan_statuses[i]

        # Log-odds of default
        # Lower credit score, higher DTI, higher interest rate increase default odds
        log_odds = -3.20 + ((680 - cs) / 60.0) * 0.85 + ((dti - 0.35) * 4.2) + ((rate - 7.5) * 0.08)
        # Loan type adjustment (Collateralized loans like Home & Auto default less)
        if ltype == "Home Loan": log_odds -= 0.65
        elif ltype == "Auto Loan": log_odds -= 0.25
        elif ltype == "Personal Loan": log_odds += 0.45
        elif ltype == "Business Loan": log_odds += 0.30

        def_prob = 1.0 / (1.0 + np.exp(-log_odds))
        def_prob = round(float(np.clip(def_prob, 0.008, 0.72)), 4)
        default_probabilities.append(def_prob)

        # Risk Category
        if def_prob < 0.05:
            rcat = "Low Risk"
        elif def_prob < 0.15:
            rcat = "Medium Risk"
        elif def_prob < 0.30:
            rcat = "High Risk"
        else:
            rcat = "Very High Risk"
        risk_categories.append(rcat)

        # Default Flag (Only applicable to approved loans)
        if status == "Approved":
            # Bernoulli trial based on def_prob
            is_default = 1 if np.random.rand() < def_prob else 0
        else:
            is_default = 0
        default_flags.append(is_default)

    # 8. Customer Segment & Status
    customer_segments = []
    customer_statuses = []
    last_tx_dates = []

    for inc, bal, cs, p_num, ten in zip(annual_incomes, account_balances, credit_scores, n_products, tenure_years):
        # Segmentation heuristic:
        # High Value: High income (>=120k) and high balance (>=60k) with good credit
        if inc >= 120000 and bal >= 60000 and cs >= 700:
            seg = "High Value"
        # Premium: Good income (>=80k) or high balance (>=35k) with good credit
        elif (inc >= 80000 or bal >= 35000) and cs >= 660:
            seg = "Premium"
        # High Risk: Low credit score (<600) or very high DTI
        elif cs < 600:
            seg = "High Risk"
        # Emerging: Younger or newer with growing balances
        elif ten <= 2.5 and cs >= 640:
            seg = "Emerging"
        # Standard: Broad base
        else:
            seg = "Standard"
        customer_segments.append(seg)

        # Customer Status & Last Transaction Date
        # Most active, small % inactive or dormant
        c_stat = np.random.choice(["Active", "Inactive", "Dormant"], p=[0.88, 0.09, 0.03])
        customer_statuses.append(c_stat)

        if c_stat == "Active":
            tx_d = ref_date - timedelta(days=int(np.random.randint(1, 45)))
        elif c_stat == "Inactive":
            tx_d = ref_date - timedelta(days=int(np.random.randint(46, 180)))
        else:
            tx_d = ref_date - timedelta(days=int(np.random.randint(181, 700)))
        last_tx_dates.append(tx_d.strftime("%Y-%m-%d"))

    # Assemble Base DataFrame
    df = pd.DataFrame({
        "Customer_ID": customer_ids,
        "First_Name": first_names,
        "Last_Name": last_names_selected,
        "Gender": genders_clean,
        "Age": ages,
        "Date_of_Birth": dob_strs,
        "Marital_Status": marital_statuses,
        "Education": education_levels,
        "Occupation": occupations,
        "Employment_Status": employment_statuses,
        "Annual_Income": annual_incomes,
        "City": cities,
        "State": states,
        "Region": regions,
        "Branch_ID": branch_ids,
        "Branch_Name": branch_names,
        "Account_Type": account_types,
        "Account_Open_Date": account_open_dates,
        "Customer_Tenure_Years": tenure_years,
        "Account_Balance": account_balances,
        "Savings_Balance": savings_balances,
        "Current_Account_Balance": current_balances,
        "Number_of_Products": n_products,
        "Credit_Card": credit_cards,
        "Debit_Card": debit_cards,
        "Online_Banking": online_bankings,
        "Mobile_Banking": mobile_bankings,
        "Credit_Score": credit_scores,
        "Credit_Score_Category": credit_score_categories,
        "Existing_Loans": existing_loans_list,
        "Outstanding_Debt": outstanding_debts,
        "Debt_to_Income_Ratio": dtis,
        "Loan_ID": loan_ids,
        "Loan_Type": loan_types,
        "Loan_Application_Date": application_dates,
        "Loan_Amount": loan_amounts,
        "Interest_Rate": interest_rates,
        "Loan_Tenure_Months": loan_tenures,
        "Monthly_Installment": monthly_installments,
        "Loan_Status": loan_statuses,
        "Approval_Date": approval_dates,
        "Loan_Purpose": loan_purposes,
        "Risk_Category": risk_categories,
        "Default_Flag": default_flags,
        "Default_Probability": default_probabilities,
        "Customer_Segment": customer_segments,
        "Customer_Status": customer_statuses,
        "Last_Transaction_Date": last_tx_dates
    })

    print(f"[+] Base dataset constructed: {df.shape[0]:,} rows × {df.shape[1]} columns.")

    # 9. Inject Controlled Data Quality Defects for Cleaning Demonstrations
    print("[*] Injecting controlled data quality issues (duplicates, missing values, inconsistent casing, outliers)...")
    df_dirty = df.copy()

    # A. Inconsistent Casing & Formatting in Categoricals
    gender_mask_m = (df_dirty["Gender"] == "Male") & (np.random.rand(len(df_dirty)) < 0.15)
    gender_mask_f = (df_dirty["Gender"] == "Female") & (np.random.rand(len(df_dirty)) < 0.15)
    df_dirty.loc[gender_mask_m, "Gender"] = np.random.choice(["M", "male", "Male "], size=gender_mask_m.sum())
    df_dirty.loc[gender_mask_f, "Gender"] = np.random.choice(["F", "female", "Female "], size=gender_mask_f.sum())

    emp_mask = (df_dirty["Employment_Status"] == "Self-Employed") & (np.random.rand(len(df_dirty)) < 0.25)
    df_dirty.loc[emp_mask, "Employment_Status"] = np.random.choice(["self employed", "Self_Employed", "self-employed"], size=emp_mask.sum())

    # B. Missing Values (~2-3% in selected columns)
    null_marital = np.random.rand(len(df_dirty)) < 0.025
    df_dirty.loc[null_marital, "Marital_Status"] = np.nan

    null_edu = np.random.rand(len(df_dirty)) < 0.020
    df_dirty.loc[null_edu, "Education"] = np.nan

    null_online = np.random.rand(len(df_dirty)) < 0.018
    df_dirty.loc[null_online, "Online_Banking"] = np.nan

    null_emp = np.random.rand(len(df_dirty)) < 0.015
    df_dirty.loc[null_emp, "Employment_Status"] = np.nan
    # C. Formatting Inconsistencies (string formatted numbers in raw data)
    df_dirty["Annual_Income"] = df_dirty["Annual_Income"].astype(object)
    str_inc_mask = np.random.choice(len(df_dirty), size=40, replace=False)
    for idx in str_inc_mask:
        df_dirty.at[idx, "Annual_Income"] = f" ${df_dirty.at[idx, 'Annual_Income']:,.0f} "

    # D. Outliers (anomalous age, negative balance, etc.)
    outlier_indices = np.random.choice(len(df_dirty), size=12, replace=False)
    df_dirty.at[outlier_indices[0], "Age"] = 125
    df_dirty.at[outlier_indices[1], "Age"] = -3
    df_dirty.at[outlier_indices[2], "Account_Balance"] = -500.0
    df_dirty.at[outlier_indices[3], "Debt_to_Income_Ratio"] = 2.85

    # E. Duplicate Rows (~450 duplicate rows appended)
    dup_indices = np.random.choice(len(df_dirty), size=450, replace=False)
    dup_rows = df_dirty.iloc[dup_indices].copy()
    df_dirty = pd.concat([df_dirty, dup_rows], ignore_index=True)

    # Shuffle rows
    df_dirty = df_dirty.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    print(f"[OK] Final raw dataset created with {len(df_dirty):,} rows (including {len(dup_indices)} duplicates).")

    return df_dirty

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    raw_path = os.path.join(raw_dir, "bank_customer_loan_raw.csv")

    df_raw = generate_bank_data(n_records=20000, random_seed=42)
    df_raw.to_csv(raw_path, index=False)
    print(f"[OK] Raw dataset successfully saved to: {os.path.abspath(raw_path)}")

if __name__ == "__main__":
    main()
