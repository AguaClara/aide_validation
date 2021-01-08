import os
import numpy as np
from datetime import datetime
from aguaclara.core.units import u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.onshape_parser as par
from aguaclara.design.lfom import LFOM
from report_writer import ReportWriter


def flow_lfom_vert(height, d_ori, h_ori, n_oris):
    """Returns the flow through the LFOM as a function of height

    Args:
        height: height of water in the LFOM (u.m)

        d_ori: diameter of each orifice (u.m)

        h_ori: height of each row of the LFOM (list)

        n_oris: number of orifices at each row of the LFOM (list of lists)

    Returns:
        flow: flow rate through the LFOM (u.L / u.s)
    """
    flow = pc.flow_orifice_vert(d_ori, height - h_ori, con.VC_ORIFICE_RATIO) * n_oris
    return (sum(flow)).to(u.L/u.s)


def check_flow_lfom_vert(diameter, ori_heights, ori_numbers, cutoff, q_input, report_writer):
    """Evaluates the flow

    Args:
        diameter: diameter of each orifice (u.m)

        ori_heights: height of each row of the LFOM (list)

        ori_numbers: number of orifices at each row of the LFOM (list of lists)

        cutoff: allowable tolerance between design and expected flow as a percent

        q_input: design flow rate (u.L / u.s)

        report_writer: ReportWriter object to record validation results

    Returns:
        flow: flow rate through the LFOM (u.L / u.s)
    """
    for height in ori_heights:
        try:
            q_calc = flow_lfom_vert(height + 0.5 * diameter, diameter, height, ori_numbers)
            assert cutoff > (q_calc - q_input) / q_input
            assert -cutoff < (q_calc - q_input) / q_input
            report_writer.write_message('The expected flow rate, {!s}, was very close '
                                        'to the one calculated by this validation '
                                        'code, {!s}.\n'.format(q_input, q_calc))
        except AssertionError:
            report_writer.write_message('INVALID: The expected flow rate, {!s}, is '
                                        'different from the one calculated by this '
                                        'validation code, {!s}.\n'.format(q_input, q_calc))
            report_writer.set_result('Invalid: Check Validation Report')


def validate_lfom(url):
    """Validates the LFOM model at the given URL is correct

    Args:
        url: URL of Onshape model to validate (string)

    Returns:
        result: text which represents validation result (string)
    """
    try:
        report_writer = ReportWriter()
        measurements, _ = par.get_parsed_measurements(link=url)
        q = measurements['Flow'] / u.s
        temp = measurements['TempCelsius'] * u.degC
        hl = float(measurements['HL.Lfom'].split(' ')[0]) / 100 * u.m
        d_orifices = float(measurements['D.LfomOrifices'].split(' ')[0]) / 100 * u.m
        b_rows = float(measurements['B.LfomRows'].split(' ')[0]) / 100 * u.m
        n_orifices = measurements['N.LfomOrifices']
        h_orifices = [float(n.split(' ')[0]) / 100 * u.m for n in measurements['H.LfomOrifices']]

        # Acceptable tolerance
        tol = 0.05
        # TODO: make ReportWriter and measurments attributes of validation
        # orchestrator instead of passing them between functions
        check_flow_lfom_vert(d_orifices, h_orifices, n_orifices, tol, q, report_writer, message)
    except Exception as e:
        report_writer.set_result('Error: {}'.format(e))

    report_writer.close_report()
    return report_writer.get_result()

# TODO: add these to a test.py along with invalid models
# msg = validate_lfom('https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/v/2990aab7c08553622d0c1402/e/e09d11406e7a9143537efe3a')
# print(msg)
