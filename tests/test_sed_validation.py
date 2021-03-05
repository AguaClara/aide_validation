import pytest
import time
from aguaclara.core.units import u
import aguaclara.core.pipes as pipe
from aide_validation.report_writer import ReportWriter
import aide_validation.sed_validation as sed

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
    "diam, pi_flow_manifold, vel_diffuser, q_input, expected",
    [
        (
            3 * u.inch,
            0.8,
            285.6 * u.mm / u.s,
            1 * u.L / u.s,
            "Invalid: Check Validation Report",
        ),
        (
            pipe.ID_SDR(3.0 * u.inch, 26),
            0.8,
            285.6 * u.mm / u.s,
            1 * u.L / u.s,
            "Valid",
        ),
    ],
)
def test_check_inlet_manifold(
    diam, pi_flow_manifold, vel_diffuser, q_input, expected, report_writer
):
    sed.check_inlet_manifold(
        diam, pi_flow_manifold, vel_diffuser, q_input, report_writer
    )
    assert report_writer.get_result() == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "vel_capture, n_plate, l_plate, w_plate, space_plate, angle_plate, "
    "plate_thickness, q_input, expected",
    [
        (
            0.12 * u.mm / u.s,
            26,
            60 * u.cm,
            42 * u.inch,
            2.5 * u.cm,
            60 * u.deg,
            1 * u.mm,
            1 * u.L / u.s,
            "Valid",
        ),
        (
            0.12 * u.mm / u.s,
            26,
            60 * u.cm,
            42 * u.inch,
            2.5 * u.cm,
            60 * u.deg,
            1 * u.mm,
            1.2 * u.L / u.s,
            "Invalid: Check Validation Report",
        ),
    ],
)
def test_check_plate_settlers(
    vel_capture,
    n_plate,
    l_plate,
    w_plate,
    space_plate,
    angle_plate,
    plate_thickness,
    q_input,
    expected,
    report_writer,
):
    sed.check_plate_settlers(
        vel_capture,
        n_plate,
        l_plate,
        w_plate,
        space_plate,
        angle_plate,
        plate_thickness,
        q_input,
        report_writer,
    )
    assert report_writer.get_result() == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "length, width, vel_up, q_input, expected",
    [
        (
            1.1 * u.m,
            42 * u.inch,
            0.85 * u.mm / u.s,
            1 * u.L / u.s,
            "Invalid: Check Validation Report",
        ),
        (1.1 * u.m, 42 * u.inch, 0.85 * u.mm / u.s, 0.975 * u.L / u.s, "Valid"),
    ],
)
def test_check_sed_tank(length, width, vel_up, q_input, expected, report_writer):
    sed.check_sed_tank(length, width, vel_up, q_input, report_writer)
    assert report_writer.get_result() == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "w_sed, w_diffuser, vel_up, max_hl, temp, expected",
    [
        (
            42 * u.inch,
            1 / 8 * u.inch,
            0.85 * u.mm / u.s,
            1 * u.cm,
            20 * u.degC,
            "Valid",
        ),
        (
            42 * u.inch,
            1 / 8 * u.inch,
            1.5 * u.mm / u.s,
            1 * u.cm,
            20 * u.degC,
            "Invalid: Check Validation Report",
        ),
        (
            42 * u.inch,
            1 / 8 * u.inch,
            1.0 * u.mm / u.s,
            0.5 * u.cm,
            20 * u.degC,
            "Invalid: Check Validation Report",
        ),
    ],
)
def test_check_diffuser(
    w_sed, w_diffuser, vel_up, max_hl, temp, expected, report_writer
):
    sed.check_diffuser(w_sed, w_diffuser, vel_up, max_hl, temp, report_writer)
    assert report_writer.get_result() == expected


@pytest.mark.skipif(skip_all_tests, reason="Exclude all tests")
@pytest.mark.parametrize(
    "n_orifices, diam_orifice, hl_design, q_input, expected",
    [
        (
            32,
            1 / 8 * u.inch,
            1 * u.cm,
            1 * u.L / u.s,
            "Invalid: Check Validation Report",
        ),
        (9, 0.015875 * u.m, 0.05 * u.m, 1 * u.L / u.s, "Valid"),
    ],
)
def test_check_outlet_manifold(
    n_orifices, diam_orifice, hl_design, q_input, expected, report_writer
):
    sed.check_outlet_manifold(
        n_orifices, diam_orifice, hl_design, q_input, report_writer
    )
    assert report_writer.get_result() == expected
