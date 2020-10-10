import aguaclara.core.constants as con
import aguaclara.core.physchem as pc
import parse as par
import numpy as np
from aguaclara.design.lfom import LFOM
from aguaclara.core.units import u

def validate(url):
    measurements, templates = par.get_parsed_measurements(link=url)
    return measurements

# define the inputs to the Onshape model
q = 10 * u.L / u.s
temp = 21 * u.degC

# define variables that will be output by Onshape
hl = 0.2 * u.m  # head loss
d_orifices = 0.016 * u.m  # diameter of orifices
b_rows = 0.017 * u.m  # space between rows
n_orifices = [17, 4, 6, 3, 4, 3, 3, 3, 3, 2, 3, 1]  # number of orifices per row
# height of the center of each row from the bottom of the bottom row
h_orifices = [0.0079375, 0.02467613636363637, 0.04141477272727274,
              0.0581534090909091, 0.07489204545454548, 0.09163068181818185,
              0.1083693181818182, 0.1251079545454546, 0.14184659090909096,
              0.15858522727272734, 0.1753238636363637, 0.19206250000000008] * u.m

# set an acceptable tolerance
# (I'll have to think harder about what this is in the future, for now I just picked 5%)
tol = 0.05