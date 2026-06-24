import pandas as pd

def normalize_company_id(df):
    """
    Standardize company_id column:
    - remove extra spaces
    - convert to uppercase
    """

    if "company_id" in df.columns:

        df["company_id"] = (
            df["company_id"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    return df

sample = pd.DataFrame({
    "company_id": [" tcs ", "infy", " hdfcbank "]
})


import re
import pandas as pd
from datetime import datetime

def normalize_year(value):
    if pd.isna(value):
        return value

    value = str(value).strip()

    # Already normalized
    if re.match(r"^\d{4}-\d{2}$", value):
        return value

    # Mar-24
    try:
        return datetime.strptime(value, "%b-%y").strftime("%Y-%m")
    except:
        pass

    # Jun 2013
    try:
        return datetime.strptime(value, "%b %Y").strftime("%Y-%m")
    except:
        pass

    # Mar 2016 9m
    # Mar 2023 15
    match = re.match(r"([A-Za-z]{3})\s+(\d{4})", value)
    if match:
        month, year = match.groups()
        return datetime.strptime(
            f"{month} {year}",
            "%b %Y"
        ).strftime("%Y-%m")

    # 2024.5 → 2024-09
    if value == "2024.5":
        return "2024-09"
    # Plain year: 2019
    if re.match(r"^\d{4}$", value):
        return f"{value}-03"
    # 2019.0 -> 2019-03
    if re.match(r"^\d{4}\.0$", value):
        return f"{value[:4]}-03"
    return value