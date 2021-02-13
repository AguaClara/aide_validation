import pytest
from aguaclara.core.units import u
from aide_validation.report_writer import ReportWriter
from aide_validation.floc_validation import check_baffle_spacing, check_G_theta

# set skip_all_tests = True to focus on single test
skip_all_tests = False
writer = ReportWriter()


@pytest.fixture
def report_writer():
    # reset result to its default between tests
    writer.set_result("Valid")
    return writer


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "channel_l, baffle_s, expected",
    [
        (1.9 * u.m, 0.3085 * u.m, "Invalid: Check Validation Report"),
        (0.9 * u.m, 0.3085 * u.m, "Invalid: Check Validation Report"),
        (1.851 * u.m, 0.3085 * u.m, "Valid"),
    ],
)
def test_check_baffle_spacing(channel_l, baffle_s, expected, report_writer):
    check_baffle_spacing(channel_l, baffle_s, report_writer)

    assert report_writer.get_result() == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "q, channel_l, design_water_height, channel_n, channel_w, hl, temp, min_G_theta,"
    "expected",
    [
        (
            30 * u.L / u.s,
            1.851 * u.m,
            2.428 * u.m,
            8,
            0.312 * u.m,
            0.594365454 * u.m,
            20 * u.degC,
            30000,
            "Valid",
        ),
        (
            30 * u.L / u.s,
            1.851 * u.m,
            2.428 * u.m,
            8,
            0.1 * u.m,
            0.5 * u.m,
            20 * u.degC,
            30000,
            "Invalid: Check Validation Report",
        ),
        (
            30 * u.L / u.s,
            1.851 * u.m,
            2.428 * u.m,
            8,
            0.312 * u.m,
            0.594365454 * u.m,
            20 * u.degC,
            50000,
            "Invalid: Check Validation Report",
        ),
        (
            30 * u.L / u.s,
            1.851 * u.m,
            2.428 * u.m,
            8,
            0.5 * u.m,
            0.8 * u.m,
            20 * u.degC,
            50000,
            "Valid",
        ),
    ],
)
def test_check_G_theta(
    q,
    channel_l,
    design_water_height,
    channel_n,
    channel_w,
    hl,
    temp,
    min_G_theta,
    expected,
    report_writer,
):
    check_G_theta(
        q,
        channel_l,
        design_water_height,
        channel_n,
        channel_w,
        hl,
        temp,
        report_writer,
        min_G_theta=min_G_theta
    )
    assert report_writer.get_result() == expected
