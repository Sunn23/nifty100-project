import pandas as pd

CORE_FILES = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons"
]

SUPP_FILES = [
    "sectors",
    "stock_prices",
    "market_cap",
    "financial_ratios",
    "peer_groups"
]

def load_excel(path, header):
    return pd.read_excel(path, header=header)

def load_all(data_folder):

    tables = {}

    for file in CORE_FILES:
        tables[file] = load_excel(
            f"{data_folder}/{file}.xlsx",
            header=1
        )

    for file in SUPP_FILES:
        tables[file] = load_excel(
            f"{data_folder}/{file}.xlsx",
            header=0
        )

    return tables

