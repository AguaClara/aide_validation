import time
import pytest
from aguaclara.core.units import u
from validator import Validator

# set skip_all_tests = True to focus on single test
skip_all_tests = True

# TODO: add tests for invalid models
@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "url, expected",
    [("https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/v/2990aab7c08553622d0c1402/e/e09d11406e7a9143537efe3a", "Valid"),
     ("https://cad.onshape.com/documents/ef6563f3c625eada2abf1b35/w/6449a255140a68e725160b27/e/c34757f94d5576b2c0bc4954", "Valid")],
)
def test_validate(url, expected):
    validator = Validator()
    result = validator.validate(url)

    assert result == expected


# @pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "measure, expected",
    [
        ({}, "Error: 'Flow'"),
        ({"N.LfomOrifices": [17.0, 4.0, 6.0, 3.0, 4.0, 3.0, 3.0, 3.0, 3.0, 2.0, 3.0, 1.0],
          "H.LfomOrifices":
              [0.0079375 * u.m, 0.02467613636363637 * u.m,
               0.04141477272727274 * u.m, 0.0581534090909091 * u.m,
               0.07489204545454548 * u.m, 0.09163068181818185 * u.m,
               0.1083693181818182 * u.m, 0.1251079545454546 * u.m,
               0.14184659090909096 * u.m, 0.15858522727272734 * u.m,
               0.1753238636363637 * u.m, 0.19206250000000008 * u.m],
          "D.LfomOrifices": 0.015875 * u.m,
          "B.LfomRows": 0.016666666666666666 * u.m,
          "HL.Lfom": 0.2 * u.m,
          "Flow": 10 * u.L,
          "TempCelsius": 21,},
         "Valid"),
          # ({}, "INVALID")
    ],
)
def test_validate_lfom(measure, expected):
    # sleep one second so reports can't have the same name
    time.sleep(1)

    validator = Validator()
    result = validator.validate_lfom(measure)

    assert result == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "measure, expected",
    [
        ({}, "INVALID"),
        ({}, "Valid")
    ],
)
def test_validate_floc(measure, expected):
    validator = Validator()
    result = validator.validate_floc(measure)

    assert result == expected
