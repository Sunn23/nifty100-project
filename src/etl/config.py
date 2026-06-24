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

TIME_SERIES_TABLES = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "market_cap",
    "financial_ratios"
]

TABLE_SCHEMAS = {
    "profitandloss": [
        "company_id",
        "year",
        "sales",
        "net_profit"
    ],
    "balancesheet": [
        "company_id",
        "year",
        "total_assets",
        "total_liabilities"
    ],
    "cashflow": [
        "company_id",
        "year",
        "net_cash_flow"
    ],
    "market_cap": [
        "company_id",
        "year",
        "market_cap_crore"
    ],
    "financial_ratios": [
        "company_id",
        "year",
        "return_on_equity_pct"
    ]
}