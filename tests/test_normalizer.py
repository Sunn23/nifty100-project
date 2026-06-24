from src.etl.normalizer import normalize_year


def test_mar_24():
    assert normalize_year("Mar-24") == "2024-03"


def test_jun_2013():
    assert normalize_year("Jun 2013") == "2013-06"


def test_mar_2016_9m():
    assert normalize_year("Mar 2016 9m") == "2016-03"


def test_mar_2023_15():
    assert normalize_year("Mar 2023 15") == "2023-03"


def test_plain_year():
    assert normalize_year("2019") == "2019-03"


def test_float_year():
    assert normalize_year("2019.0") == "2019-03"


def test_2024_5():
    assert normalize_year("2024.5") == "2024-09"


def test_already_normalized():
    assert normalize_year("2022-03") == "2022-03"


def test_none():
    assert normalize_year(None) is None

def test_empty_string():
    assert normalize_year("") == ""
    
def test_jan_2020():
    assert normalize_year("Jan 2020") == "2020-01"

def test_feb_2021():
    assert normalize_year("Feb 2021") == "2021-02"

def test_apr_2022():
    assert normalize_year("Apr 2022") == "2022-04"

def test_may_2023():
    assert normalize_year("May 2023") == "2023-05"

def test_aug_2018():
    assert normalize_year("Aug 2018") == "2018-08"

def test_sep_2017():
    assert normalize_year("Sep 2017") == "2017-09"

def test_oct_2016():
    assert normalize_year("Oct 2016") == "2016-10"

def test_nov_2015():
    assert normalize_year("Nov 2015") == "2015-11"

def test_dec_2014():
    assert normalize_year("Dec 2014") == "2014-12"

def test_jan_19():
    assert normalize_year("Jan-19") == "2019-01"

def test_feb_20():
    assert normalize_year("Feb-20") == "2020-02"

def test_mar_21():
    assert normalize_year("Mar-21") == "2021-03"

def test_apr_22():
    assert normalize_year("Apr-22") == "2022-04"

def test_trim_spaces():
    assert normalize_year("  Mar-24  ") == "2024-03"

def test_ttm():
    assert normalize_year("TTM") == "TTM"

def test_unknown_text():
    assert normalize_year("Hello") == "Hello"

def test_numeric_string():
    assert normalize_year("2020") == "2020-03"

def test_2018_float():
    assert normalize_year("2018.0") == "2018-03"

def test_2017_float():
    assert normalize_year("2017.0") == "2017-03"

def test_2016_float():
    assert normalize_year("2016.0") == "2016-03"