from src.etl.normalizer import normalize_company_id
import pandas as pd


def test_uppercase():
    df = pd.DataFrame({"company_id":["tcs"]})
    result = normalize_company_id(df)
    assert result["company_id"][0] == "TCS"


def test_strip_spaces():
    df = pd.DataFrame({"company_id":["  infy  "]})
    result = normalize_company_id(df)
    assert result["company_id"][0] == "INFY"


def test_hdfc():
    df = pd.DataFrame({"company_id":["hdfcbank"]})
    result = normalize_company_id(df)
    assert result["company_id"][0] == "HDFCBANK"


def test_multiple_rows():
    df = pd.DataFrame({
        "company_id":["tcs","infy"]
    })
    result = normalize_company_id(df)
    assert result["company_id"].tolist() == ["TCS","INFY"]


def test_already_clean():
    df = pd.DataFrame({"company_id":["RELIANCE"]})
    result = normalize_company_id(df)
    assert result["company_id"][0] == "RELIANCE"