import pytest
import time
from aguaclara.core.units import u
from aide_validation.report_writer import ReportWriter
from aide_validation.lfom_validation import flow_lfom_vert, check_flow_lfom_vert

# set skip_all_tests = True to focus on single test
skip_all_tests = False
# sleep one second so reports won't have the same name
time.sleep(1)
writer = ReportWriter()


@pytest.fixture
def report_writer():
    # reset result to its default between tests
    writer.set_result("Valid")
    return writer


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "height, d_ori, h_ori, n_oris, expected",
    [
        (
            0.2 * u.m,
            0.0157875 * u.m,
            [
                0.0079375,
                0.02467613636363637,
                0.04141477272727274,
                0.0581534090909091,
                0.07489204545454548,
                0.09163068181818185,
                0.1083693181818182,
                0.1251079545454546,
                0.14184659090909096,
                0.15858522727272734,
                0.1753238636363637,
                0.19206250000000008,
            ] * u.m,
            [
                17.0,
                4.0,
                6.0,
                3.0,
                4.0,
                3.0,
                3.0,
                3.0,
                3.0,
                2.0,
                3.0,
                1.0,
            ],
            10.081949072000105 * u.L / u.s,
        ),
        (
            0.1 * u.m,
            0.0157875 * u.m,
            [
                0.00396875,
                0.0125,
                0.0207074,
                0.02925,
                0.0375,
                0.045,
                0.055,
                0.0625,
                0.072,
                0.08,
                0.087,
                0.096,
            ] * u.m,
            [
                17.0,
                4.0,
                6.0,
                3.0,
                4.0,
                3.0,
                3.0,
                3.0,
                3.0,
                2.0,
                3.0,
                1.0,
            ],
            7.117078350360663 * u.L / u.s,
        ),
    ],
)
def test_flow_lfom_vert(height, d_ori, h_ori, n_oris, expected):
    result = flow_lfom_vert(height, d_ori, h_ori, n_oris)
    assert result == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "diameter, ori_heights, ori_numbers, cutoff, q_input, expected",
    [
        (
            0.0157875 * u.m,
            [
                0.0079375,
                0.02467613636363637,
                0.04141477272727274,
                0.0581534090909091,
                0.07489204545454548,
                0.09163068181818185,
                0.1083693181818182,
                0.1251079545454546,
                0.14184659090909096,
                0.15858522727272734,
                0.1753238636363637,
                0.19206250000000008,
            ] * u.m,
            [
                17.0,
                4.0,
                6.0,
                3.0,
                4.0,
                3.0,
                3.0,
                3.0,
                3.0,
                2.0,
                3.0,
                1.0,
            ],
            0.05,
            10 * u.L / u.s,
            "Valid",
        ),
        (
            0.0157875 * u.m,
            [
                0.00396875,
                0.0125,
                0.0207074,
                0.02925,
                0.0375,
                0.045,
                0.055,
                0.0625,
                0.072,
                0.08,
                0.087,
                0.096,
            ] * u.m,
            [
                17.0,
                4.0,
                6.0,
                3.0,
                4.0,
                3.0,
                3.0,
                3.0,
                3.0,
                2.0,
                3.0,
                1.0,
            ],
            0.05,
            10 * u.L / u.s,
            "Invalid: Check Validation Report",
        ),
        (
            0.0157875 * u.m,
            [
                0.00396875,
                0.0125,
                0.0207074,
                0.02925,
                0.0375,
                0.045,
                0.055,
                0.0625,
                0.072,
                0.08,
                0.087,
                0.096,
            ] * u.m,
            [
                17.0,
                4.0,
                6.0,
                3.0,
                4.0,
                3.0,
                3.0,
                3.0,
                3.0,
                2.0,
                3.0,
                1.0,
            ],
            0.05,
            7.15 * u.L / u.s,
            "Valid",
        ),
    ],
)
def test_check_flow_lfom_vert(
    diameter, ori_heights, ori_numbers, cutoff, q_input, expected, report_writer
):
    check_flow_lfom_vert(
        diameter, ori_heights, ori_numbers, cutoff, q_input, report_writer
    )
    assert report_writer.get_result() == expected
