from aguaclara.core.units import u
from aguaclara.core import constants as con
import numpy as np

# vel_diffuser will be calculated in previous step
def validate_inlet_manifold(diam, pi_flow_manifold, vel_diffuser, q_input):
    try:
        q_calc = (np.pi * (vel_diffuser * np.sqrt(2 * (1 - pi_flow_manifold ** 2) / (pi_flow_manifold ** 2 + 1))) * diam ** 2) / 4
        q_calc = q_calc.to(u.L / u.s)

        assert q_calc > q_input

        print("The design flow rate, {!s}, is less than "
              "the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The design flow rate, {!s}, is "
              "greater than the one calculated by this "
              "validation code, {!s}.\n".format(q_input, q_calc))

# First should be invalid, second valid:
validate_inlet_manifold(3 * u.inch, 0.8, 285.6 * u.mm / u.s, 0.05, 1 * u.L/u.s)
validate_inlet_manifold(ac.ID_SDR(3.0 * u.inch, 26), 0.8, 285.6 * u.mm / u.s, 0.05, 1 * u.L/u.s)

def validate_plate_settlers(vel_capture, n_plate, l_plate, w_plate, space_plate, angle_plate, plate_thickness, q_input):
    try:
        q_calc = vel_capture * (n_plate * w_plate * (l_plate * np.cos(angle_plate) + (space_plate / np.sin(angle_plate))))
        q_calc = q_calc.to(u.L / u.s)

        assert q_calc > q_input

        print("The design flow rate, {!s}, is less than "
              "the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The design flow rate, {!s}, is "
              "greater than the one calculated by this "
              "validation code, {!s}.\n".format(q_input, q_calc))

validate_plate_settlers(0.12*u.mm/u.s, 26, 60*u.cm, 42*u.inch, 2.5*u.cm, 60*u.deg, 1*u.mm, 0.05, 1*u.L/u.s)

def validate_tank(length, width, vel_up, q_input):
    try:
        q_calc = length * width * vel_up
        q_calc = q_calc.to(u.L / u.s)

        assert q_calc > q_input

        print("The design flow rate, {!s}, is less than "
              "the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The design flow rate, {!s}, is "
              "greater than the one calculated by this "
              "validation code, {!s}.\n".format(q_input, q_calc))

validate_tank(1.1*u.m, 42*u.inch, 0.85*u.mm/u.s, 0.05, 1*u.L/u.s)

def validate_diffuser(w_sed, w_diffuser, vel_up, max_hl, temp, shear_floc_max=0.5*u.Pa, pi_plane_jet=0.0124):
    rho = ac.density_water(temp)
    nu = ac.viscosity_kinematic_water(temp)
    vel_diffuser = vel_up * w_sed / w_diffuser

    try:
        vel_max_shear = ((shear_floc_max/rho)**(1/2)*(vel_up*w_sed/(nu*pi_plane_jet))**(1/4)).to(u.mm/u.s)
        assert vel_diffuser < vel_max_shear

        print("The max diffuser velocity based on floc shear, {!s}, "
              "is greater than the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The max diffuser velocity based on floc shear, {!s}, "
              "is less than the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))

    try:
        head_loss = (vel_diffuser**2 / (2*u.g_0)).to(u.cm)
        assert head_loss < max_hl

        print("The max head loss, {!s}, is greater than "
              "the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The max head loss, {!s}, "
              "is less than the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))

validate_diffuser(42*u.inch, 1/8*u.inch, 0.85*u.mm/u.s, 1*u.cm, 20*u.degC)

def validate_outlet_manifold(n_orifices, diam_orifice, hl_design, q_input):
    try:
        q_calc = pc.flow_orifice(diam_orifice, hl_design, con.VC_ORIFICE_RATIO) * n_orifices
        assert q_calc > q_input

        print("The design flow rate, {!s}, is less than "
              "the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The design flow rate, {!s}, is "
              "greater than the one calculated by this "
              "validation code, {!s}.\n".format(q_input, q_calc))

# TODO: add test case
# validate_outlet_manifold()
