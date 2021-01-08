import time
import pytest
from aguaclara.core.units import u
from validator import Validator

# set skip_all_tests = True to focus on single test
skip_all_tests = False


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/v/2990aab7c08553622d0c1402/e/e09d11406e7a9143537efe3a", "Error: 'Flow'"),
        ("https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/v/4c90f8401c6635b9b12d0d87/e/e09d11406e7a9143537efe3a", "Valid"),
        ("https://cad.onshape.com/documents/ef6563f3c625eada2abf1b35/v/bde645d8c97fa07173d23530/e/c34757f94d5576b2c0bc4954", "Valid"),
        ("https://cad.onshape.com/documents/ef6563f3c625eada2abf1b35/v/d36b0e82911fa0eaa5d0ebdf/e/c34757f94d5576b2c0bc4954",
         "Invalid: No Unit Process Selected by Onshape Documenter"),
    ],
)
def test_validate(url, expected):
    # sleep one second so reports won't have the same name
    time.sleep(1)

    validator = Validator()
    result = validator.validate(url)

    assert result == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
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
           "Flow": 15 * u.L,
           "TempCelsius": 21,},
          "Invalid: Check Validation Report"),
    ],
)
def test_validate_lfom(measure, expected):
    # sleep one second so reports won't have the same name
    time.sleep(1)

    validator = Validator()
    result = validator.validate_lfom(measure)

    assert result == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "measure, expected",
    [
        ({"Flow": 15 * u.L,}, "Error: 'TempCelsius'"),
        ({"Flow": 30 * u.L,
          "TempCelsius": 20,
          "N.FlocChannels": 8,
          "N.FlocChannelBaffles": 5,
          "S.FlocBaffle": 0.3085 * u.m,
          "W.FlocChannel": 0.312 * u.m,
          "L.FlocChannel": 1.851 * u.m,
          "H.FlocChannel": 2.528 * u.m,
          "FB": 0.1 * u.m},
         "Valid")
    ],
)
def test_validate_floc(measure, expected):
    # sleep one second so reports won't have the same name
    time.sleep(1)

    validator = Validator()
    result = validator.validate_floc(measure)

    assert result == expected
