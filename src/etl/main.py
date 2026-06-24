from loader import load_all
from normalizer import normalize_company_id, normalize_year
from validator import (
    validate_required_columns,
    validate_missing_values,
    validate_duplicate_keys,
    validate_balance_sheet,
    validate_positive_sales,
    validate_market_cap,
    validate_stock_prices,
    validate_year_format,
    validate_company_id_not_null,
    validate_positive_assets,
    validate_positive_liabilities,
    validate_price_range,
    validate_volume,
    validate_roe,
    validate_eps,
    validate_net_profit
)
from deduplicator import remove_duplicates
from sqlite_loader import load_to_sqlite
from audit import create_audit_log
from report import save_validation_report
from config import TABLE_SCHEMAS, TIME_SERIES_TABLES


def run_deduplication(tables):
    """
    Remove duplicate records from all time-series tables.
    Returns audit information.
    """

    audit_records = []

    print("\n========== DEDUPLICATION ==========")

    for table in TIME_SERIES_TABLES:

        tables[table], before, after, removed = remove_duplicates(
            tables[table],
            ["company_id", "year"]
        )

        print(f"\nTable: {table}")
        print(f"Rows before : {before}")
        print(f"Rows after  : {after}")
        print(f"Removed     : {removed}")

        audit_records.append({
            "table": table,
            "rows_before": before,
            "rows_after": after,
            "duplicates_removed": removed
        })

    return audit_records


def run_validation(tables):
    """
    Validate all configured tables.
    """

    failures = []

    print("\n========== VALIDATION ==========")

    for table_name, required_columns in TABLE_SCHEMAS.items():

        failures.extend(
            validate_required_columns(
                tables[table_name],
                required_columns,
                table_name
            )
        )

        failures.extend(
            validate_missing_values(
                tables[table_name],
                required_columns,
                table_name
            )
        )

        failures.extend(
            validate_duplicate_keys(
                tables[table_name],
                ["company_id", "year"],
                table_name
            )
        )
        
        failures.extend(
            validate_year_format(
                tables[table_name],
                table_name
            )
        )
        failures.extend(
            validate_company_id_not_null(
                tables[table_name],
                table_name
            )
        )
        
    failures.extend(
        validate_balance_sheet(
            tables["balancesheet"],
            "balancesheet"
        )
    )

    failures.extend(
        validate_positive_sales(
            tables["profitandloss"],
            "profitandloss"
        )
    )

    failures.extend(
        validate_market_cap(
            tables["market_cap"],
            "market_cap"
        )
    )

    failures.extend(
        validate_stock_prices(
            tables["stock_prices"],
            "stock_prices"
        )
    )

    failures.extend(
        validate_positive_assets(
            tables["balancesheet"],
            "balancesheet"
        )
    )

    failures.extend(
        validate_positive_liabilities(
            tables["balancesheet"],
            "balancesheet"
        )
    )

    failures.extend(
        validate_price_range(
            tables["stock_prices"],
            "stock_prices"
        )
    )

    failures.extend(
        validate_volume(
            tables["stock_prices"],
            "stock_prices"
        )
    )

    failures.extend(
        validate_roe(
            tables["financial_ratios"],
            "financial_ratios"
        )
    )

    failures.extend(
        validate_eps(
            tables["profitandloss"],
            "profitandloss"
        )
    )

    failures.extend(
        validate_net_profit(
            tables["profitandloss"],
            "profitandloss"
        )
    )

    if failures:

        print(f"\nFound {len(failures)} validation issue(s).\n")

        for failure in failures:
            print(failure)

    else:

        print("✅ No validation failures found.")

    save_validation_report(
        failures,
        "validation_failures.csv"
    )

    return failures


def main():

    # ----------------------------------
    # STEP 1: Load Excel Files
    # ----------------------------------

    print("\n========== STEP 1 : LOAD DATA ==========")

    tables = load_all("data/raw")
    print(tables["cashflow"].loc[[487,488]])
    

    print("✅ Excel files loaded successfully.")

    # ----------------------------------
    # STEP 2: Normalize Data
    # ----------------------------------

    print("\n========== STEP 2 : NORMALIZE DATA ==========")

    for name, df in tables.items():

        df = normalize_company_id(df)

        if "year" in df.columns:
            df["year"] = df["year"].apply(normalize_year)

            tables[name] = df

    print("✅ Data normalization completed.")
    

    # ----------------------------------
    # STEP 3: Remove Duplicates
    # ----------------------------------

    print("\n========== STEP 3 : REMOVE DUPLICATES ==========")

    audit_records = run_deduplication(tables)
    
    tables["cashflow"] = tables["cashflow"].dropna(
        subset=[
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow"
        ],
        how="all"
    )
    # ----------------------------------
    # STEP 4: Validate Data
    # ----------------------------------

    print("\n========== STEP 4 : VALIDATE ==========")

    failures = run_validation(tables)

    # ----------------------------------
    # STEP 5: Load into SQLite
    # ----------------------------------

    print("\n========== STEP 5 : LOAD SQLITE ==========")

    load_to_sqlite(
        tables,
        "nifty100.db"
    )

    print("✅ SQLite database created.")

    # ----------------------------------
    # STEP 6: Create Audit Log
    # ----------------------------------

    print("\n========== STEP 6 : CREATE AUDIT LOG ==========")

    create_audit_log(
        audit_records,
        "load_audit.csv"
    )

    print("✅ Audit log created.")

    # ----------------------------------
    # ETL Completed
    # ----------------------------------

    print("\n===================================")
    if failures:
        print("\n⚠️ ETL completed with validation issues.")
    else:
        print("\n✅ ETL completed successfully.")
    print("===================================")


if __name__ == "__main__":
    main()
    