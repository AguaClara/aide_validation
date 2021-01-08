import math
from aguaclara.core.units import u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.onshape_parser as par
from aguaclara.design.floc import Flocculator

def check_baffle_spacing(channel_l, baffle_s, report_writer):
    """Evaluates whether 3 < H_e / S < 6 and writes the result to a report.
    (both H_e and S can be given by model geometry)

    Args:
        channel_l: length of channel (u.m)

        baffle_s: space (edge-to-edge) between two baffles (u.m)

        report_writer: ReportWriter object to record validation results

    Returns:
        none
    """
    try:
        assert 3 <= channel_l / baffle_s
        assert channel_l / baffle_s <= 6

        report_writer.write_message('Ratio of channel length, {!s}, '
                                    'to baffle spacing, {!s} '
                                    'was within the acceptable range '
                                    '(between 3 and 6).\n'.format(channel_l, baffle_s))
    except AssertionError:
        report_writer.write_message('INVALID: Ratio of channel length, {!s}, '
                                    'to baffle spacing, {!s} '
                                    'was not in the acceptable range '
                                    '(between 3 and 6).\n'.format(channel_l, baffle_s))
        report_writer.set_result('Invalid: Check Validation Report')

def check_G_theta(channel_l, design_water_height, channel_n, channel_w, hl, temp,
                  report_writer, min_G_theta=30000):
    """Evaluates whether G theta > 30000 (no maximum) and writes the result to a report.

    Args:
        channel_l: length of one channel (u.m)

        design_water_height: intended height of water in the flocculator (u.m)

        baffle_s: space (edge-to-edge) between two baffles (u.m)

        channel_n: number of flocculator channels

        channel_w: width of one channel (u.m)

        hl: headloss throught the flocculator (u.m)

        temp: design temperature (u.degC)

        report_writer: ReportWriter object to record validation results

        min_G_theta: minimum allowable G theta. Default: 30000

    Returns:
        none
    """
    try:
        theta = (channel_l * design_water_height * channel_n * channel_w) / q
        G_theta = math.sqrt(con.GRAVITY * hl * theta / pc.viscosity_kinematic_water(temp))
        assert G_theta > min_G_theta
        report_writer.write_message('The G Theta, {!s}, was above the minimum '
                                    'value of {!s}.\n'.format(G_theta, min_G_theta))
    except AssertionError:
        report_writer.write_message('INVALID: G Theta, {!s}, was below the minimum '
                                    'value of {!s}.\n'.format(G_theta, min_G_theta))
        report_writer.set_result('Invalid: Check Validation Report')

# TODO: create general validate() wrapper which reads unit process enum and calls
# correct validation method accordingly
def validate_floc(url):
    """Validates the flocculator model at the given URL is correct

    Args:
        url: URL of Onshape model to validate (string)

    Returns:
        result: text which represents validation result (string)
    """
    try:
        report_writer = ReportWriter()
        measurements, _ = par.get_parsed_measurements(link=url, for_docs=False)
        q = measurements['Flow'] / u.s
        temp = measurements['TempCelsius'] * u.degC
        channel_n = measurements['N.FlocChannels']
        baffle_n_per_chan = measurements['N.FlocChannelBaffles']
        baffle_s = measurements['S.FlocBaffle']
        channel_w = measurements['W.FlocChannel']
        channel_l = measurements['L.FlocChannel']
        channel_h = measurements['H.FlocChannel']
        design_water_height = channel_h - measurements['FB']

        # estimate head loss with minor loss equation and coefficient for the baffles
        spaces_n = (baffle_n_per_chan + 1) * channel_n
        k_minor = Flocculator().BAFFLE_K * spaces_n
        vel = q / (baffle_s * channel_w)
        hl = pc.headloss_minor_channel(vel, k_minor)

        check_G_theta(channel_l, design_water_height, channel_n, channel_w, hl, temp, report_writer)
        check_baffle_spacing(channel_l, baffle_s, report_writer)
    except Exception as e:
        report_writer.set_result('Error: {}'.format(e))

    report_writer.close_report()
    return report_writer.get_result()

# validate_floc('https://cad.onshape.com/documents/ef6563f3c625eada2abf1b35/w/6449a255140a68e725160b27/e/c34757f94d5576b2c0bc4954')
# print(msg)
