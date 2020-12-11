import math
from aguaclara.core.units import u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.onshape_parser as par
from aguaclara.design.floc import Flocculator


# TODO: create general validate() wrapper which reads unit process enum and calls
# correct validation method accordingly
def validate_floc(url):
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

    # check G theta is > 30000 (no maximum)
    theta = (channel_l * design_water_height * channel_n * channel_w) / q
    G_theta = math.sqrt(con.GRAVITY * hl * theta / pc.viscosity_kinematic_water(temp))
    # print(hl)
    # print(theta)
    # print(con.GRAVITY / pc.viscosity_kinematic_water(temp))
    assert G_theta > 30000

    # check 3 < H_e / S < 6 (bot H_e and S can be given by model geometry)
    assert 3 <= channel_l / baffle_s
    assert channel_l / baffle_s <= 6

validate_floc('https://cad.onshape.com/documents/ef6563f3c625eada2abf1b35/w/6449a255140a68e725160b27/e/c34757f94d5576b2c0bc4954')
