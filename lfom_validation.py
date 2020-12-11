import os
import numpy as np
from datetime import datetime
from aguaclara.core.units import u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.onshape_parser as par
from aguaclara.design.lfom import LFOM


def flow_lfom_vert(height, d_ori, h_ori, n_oris):
    """Returns the flow through the LFOM as a function of height"""
    flow = pc.flow_orifice_vert(d_ori, height - h_ori, con.VC_ORIFICE_RATIO)* n_oris
    return (sum(flow)).to(u.L/u.s)


def check_flow_lfom_vert(diameter, ori_heights, ori_numbers, cutoff, q_input, report_file, message):
    for height in ori_heights:
        try:
            q_calc = flow_lfom_vert(height + 0.5 * diameter, diameter, height, ori_numbers)
            assert cutoff > (q_calc - q_input) / q_input
            assert -cutoff < (q_calc - q_input) / q_input
            report_file.write('The expected flow rate, {!s}, very close to the one calculated by this validation code, '
                              '{!s}.\n'.format(q_input, q_calc))
        except AssertionError:
            report_file.write('INVALID: The expected flow rate, {!s}, is different from the one calculated by this '
                              'validation code, {!s}.\n'.format(q_input, q_calc))
            message = 'Invalid: Check Validation Report'

    return message


def validate_lfom(url):
    try:
        q = 15 * u.L / u.s
        temp = 21 * u.degC

        measurements, templates = par.get_parsed_measurements(link=url)
        print(measurements)
        hl = float(measurements['HL.Lfom'].split(' ')[0]) / 100 * u.m
        d_orifices = float(measurements['D.LfomOrifices'].split(' ')[0]) / 100 * u.m
        b_rows = float(measurements['B.LfomRows'].split(' ')[0]) / 100 * u.m
        n_orifices = measurements['N.LfomOrifices']
        h_orifices = [float(n.split(' ')[0]) / 100 * u.m for n in measurements['H.LfomOrifices']]

        # Acceptable tolerance
        tol = 0.05
        now = datetime.now()
        str_now = now.strftime('%m.%d.%Y.%H.%M.%S')
        report_name = 'Reports/Validation_Report_' + str_now + '.txt'
        report_file = open(report_name, 'x')
        report_file.write('AIDE Validation Report\n')
        message = 'Valid'

        message = check_flow_lfom_vert(d_orifices, h_orifices, n_orifices, tol, q, report_file, message)

        report_file.close()

    except Exception as e:
        message = 'Error: {}'.format(e)

    return message

msg = validate('https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/v/2990aab7c08553622d0c1402/e/e09d11406e7a9143537efe3a')
print(msg)
