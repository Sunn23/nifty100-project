import pandas as pd

def validate_required_columns(df, required_columns, table_name):

    failures = []

    for column in required_columns:

        if column not in df.columns:

            failures.append({
                "table": table_name,
                "field": column,
                "issue": "Missing column",
                "severity": "CRITICAL"
            })

    return failures
def validate_missing_values(df, columns, table_name):

    failures = []

    for column in columns:

        if column in df.columns:

            missing_rows = df[df[column].isna()]

            for index in missing_rows.index:

                failures.append({
                    "table": table_name,
                    "row": index,
                    "field": column,
                    "issue": "Missing value",
                    "severity": "CRITICAL"
                })

    return failures

def validate_duplicate_keys(df, key_columns, table_name):

    failures = []

    if all(column in df.columns for column in key_columns):

        duplicates = df[df.duplicated(subset=key_columns, keep=False)]

        for index, row in duplicates.iterrows():

            failures.append({
                "table": table_name,
                "row": index,
                "field": ",".join(key_columns),
                "issue": "Duplicate key",
                "severity": "CRITICAL"
            })

    return failures

# DQ 3 Foreign Key integrity
def validate_foreign_keys(
    child_df,
    parent_df,
    table_name
):

    failures = []

    valid_company_ids = set(parent_df["id"])

    invalid_rows = child_df[
        ~child_df["company_id"].isin(valid_company_ids)
    ]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "company_id",
            "issue": "Foreign key violation",
            "severity": "CRITICAL"
        })

    return failures

def validate_company_pk(companies_df):

    failures = []

    duplicates = companies_df[
        companies_df.duplicated(
            subset=["id"],
            keep=False
        )
    ]

    for index in duplicates.index:

        failures.append({
            "table": "companies",
            "row": index,
            "field": "id",
            "issue": "Duplicate company ID",
            "severity": "CRITICAL"
        })

    return failures

#DQ-04: Balance Sheet Balances (<1% difference)
def validate_balance_sheet(df, table_name):

    failures = []

    required = ["total_assets", "total_liabilities"]

    if not all(col in df.columns for col in required):
        return failures

    for index, row in df.iterrows():

        assets = row["total_assets"]
        liabilities = row["total_liabilities"]

        if (
            pd.notna(assets)
            and pd.notna(liabilities)
            and assets != 0
        ):

            difference_pct = abs(assets - liabilities) / assets

            if difference_pct > 0.01:

                failures.append({
                    "table": table_name,
                    "row": index,
                    "field": "total_assets,total_liabilities",
                    "issue": "Balance sheet mismatch >1%",
                    "severity": "WARNING"
                })

    return failures

#DQ-05: Positive Sales
def validate_positive_sales(df, table_name):

    failures = []

    if "sales" not in df.columns:
        return failures

    invalid_rows = df[df["sales"] < 0]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "sales",
            "issue": "Sales must be positive",
            "severity": "CRITICAL"
        })

    return failures

#DQ-06: Positive Market Cap
def validate_market_cap(df, table_name):

    failures = []

    if "market_cap_crore" not in df.columns:
        return failures

    invalid_rows = df[df["market_cap_crore"] <= 0]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "market_cap_crore",
            "issue": "Market cap must be positive",
            "severity": "CRITICAL"
        })

    return failures

#DQ-06: Positive Market Cap
def validate_stock_prices(df, table_name):

    failures = []

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price"
    ]

    for column in price_columns:

        if column in df.columns:

            invalid_rows = df[df[column] <= 0]

            for index in invalid_rows.index:

                failures.append({
                    "table": table_name,
                    "row": index,
                    "field": column,
                    "issue": "Stock price must be positive",
                    "severity": "CRITICAL"
                })

    return failures

#DQ-08: Year Format Check
def validate_year_format(df, table_name):

    failures = []

    if "year" not in df.columns:
        return failures

    pattern = r"^\d{4}-\d{2}$"

    invalid_rows = df[
        ~df["year"].astype(str).str.match(pattern)
        & (df["year"] != "TTM")
    ]
    for index, row in invalid_rows.iterrows():
        print(
            f"Invalid year in {table_name}: "
            f"{row['year']}"
            )
    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "year",
            "issue": "Invalid year format",
            "severity": "WARNING"
        })

    return failures

#DQ 9 No missing Company ID
def validate_company_id_not_null(df, table_name):

    failures = []

    if "company_id" not in df.columns:
        return failures

    missing_rows = df[df["company_id"].isna()]

    for index in missing_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "company_id",
            "issue": "Missing company_id",
            "severity": "CRITICAL"
        })

    return failures

#DQ-10: Total Assets Cannot Be Negative
def validate_positive_assets(df, table_name):

    failures = []

    if "total_assets" not in df.columns:
        return failures

    invalid_rows = df[df["total_assets"] < 0]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "total_assets",
            "issue": "Negative assets",
            "severity": "CRITICAL"
        })

    return failures

#DQ-11: Total Liabilities Cannot Be Negative
def validate_positive_liabilities(df, table_name):

    failures = []

    if "total_liabilities" not in df.columns:
        return failures

    invalid_rows = df[df["total_liabilities"] < 0]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "total_liabilities",
            "issue": "Negative liabilities",
            "severity": "CRITICAL"
        })

    return failures

#DQ-12: Stock Price Range Check
def validate_price_range(df, table_name):

    failures = []

    required = [
        "high_price",
        "low_price"
    ]

    if not all(col in df.columns for col in required):
        return failures

    invalid_rows = df[
        df["high_price"] < df["low_price"]
    ]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "high_price,low_price",
            "issue": "High price lower than low price",
            "severity": "CRITICAL"
        })

    return failures

#DQ-13: Volume Cannot Be Negative
def validate_volume(df, table_name):

    failures = []

    if "volume" not in df.columns:
        return failures

    invalid_rows = df[df["volume"] < 0]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "volume",
            "issue": "Negative volume",
            "severity": "CRITICAL"
        })

    return failures

#DQ-14: ROE Range Check
def validate_roe(df, table_name):

    failures = []

    if "return_on_equity_pct" not in df.columns:
        return failures

    invalid_rows = df[
        (df["return_on_equity_pct"] < -100)
        |
        (df["return_on_equity_pct"] > 100)
    ]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "return_on_equity_pct",
            "issue": "Unusual ROE",
            "severity": "WARNING"
        })

    return failures

#DQ-15: EPS 
def validate_eps(df, table_name):

    failures = []

    if "eps" not in df.columns:
        return failures

    invalid_rows = df[abs(df["eps"]) > 1000]

    for index in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "eps",
            "issue": "Unusually large EPS",
            "severity": "WARNING"
        })

    return failures

# DQ-16: Net Profit cannot be missing

def validate_net_profit(df, table_name):

    failures = []

    if "net_profit" not in df.columns:
        return failures

    missing_rows = df[df["net_profit"].isna()]

    for index in missing_rows.index:

        failures.append({
            "table": table_name,
            "row": index,
            "field": "net_profit",
            "issue": "Missing net profit",
            "severity": "CRITICAL"
        })

    return failures