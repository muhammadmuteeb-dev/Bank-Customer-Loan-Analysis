"""
Bank Customer & Loan Analysis - SQL Runner & Query Verification Module
Loads the processed banking dataset into an in-memory SQLite database,
executes all analytical SQL queries across the 4 SQL scripts,
verifies syntax and schema alignment, and prints query outputs.
"""

import os
import re
import sqlite3
import pandas as pd

def run_sql_analysis(clean_csv_path: str, sql_dir: str):
    """
    Executes and validates all SQL scripts against SQLite engine.
    """
    print("=" * 70)
    print("BANK CUSTOMER & LOAN ANALYSIS - SQL VERIFICATION RUNNER")
    print("=" * 70)

    if not os.path.exists(clean_csv_path):
        raise FileNotFoundError(f"Clean data file not found: {clean_csv_path}")

    # 1. Load Clean Dataset into SQLite
    print(f"[*] Loading processed dataset into SQLite in-memory database...")
    df = pd.read_csv(clean_csv_path, low_memory=False)
    
    conn = sqlite3.connect(":memory:")
    # Write to table 'bank_customer_loan'
    df.to_sql("bank_customer_loan", conn, index=False, if_exists="replace")
    print(f"[OK] Table 'bank_customer_loan' loaded with {len(df):,} rows.")

    # 2. Iterate through SQL Scripts
    sql_files = [
        "01_basic_customer_analysis.sql",
        "02_loan_analysis.sql",
        "03_risk_analysis.sql",
        "04_advanced_banking_analysis.sql"
    ]

    total_queries_executed = 0

    for sql_file in sql_files:
        file_path = os.path.join(sql_dir, sql_file)
        if not os.path.exists(file_path):
            print(f"[-] File not found: {file_path}")
            continue

        print(f"\n" + "-" * 70)
        print(f"EXECUTING: {sql_file}")
        print("-" * 70)

        with open(file_path, "r", encoding="utf-8") as f:
            sql_text = f.read()

        # Split SQL text into individual queries (by semicolon, ignoring comments)
        # Remove single line comments
        clean_sql = re.sub(r"--.*", "", sql_text)
        queries = [q.strip() for q in clean_sql.split(";") if q.strip()]

        for q_idx, query in enumerate(queries, start=1):
            try:
                result_df = pd.read_sql_query(query, conn)
                total_queries_executed += 1
                first_line = query.split("\n")[0][:60]
                print(f"[Query {q_idx:02d} OK] Rows returned: {len(result_df)} | Snippet: {first_line}...")
                if len(result_df) > 0 and q_idx in [1, 2]:
                    # Print preview of first 2 queries in each file
                    print(result_df.head(3).to_string(index=False))
                    print()
            except Exception as e:
                print(f"[Query {q_idx:02d} ERROR] Failed to execute query: {e}")
                print(f"Query was:\n{query}")
                raise e

    conn.close()
    print("\n" + "=" * 70)
    print(f"[OK] All {total_queries_executed} SQL queries executed successfully with 0 errors!")
    print("=" * 70)

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    clean_csv = os.path.join(base_dir, "..", "data", "processed", "bank_customer_loan_clean.csv")
    sql_folder = os.path.join(base_dir, "..", "sql")
    run_sql_analysis(clean_csv, sql_folder)
