from aguaclara.core.units import u
import numpy as np

# vel_diffuser will be calculated in previous step
def validate_manifold(diam, pi_flow_manifold, vel_diffuser, cutoff, q_input):
    try:
        q_calc = (np.pi * (vel_diffuser * np.sqrt(2 * (1 - pi_flow_manifold ** 2) / (pi_flow_manifold ** 2 + 1))) * diam ** 2) / 4
        q_calc = q_calc.to(u.L / u.s)

        assert cutoff > (q_calc - q_input) / q_input
        assert -cutoff < (q_calc - q_input) / q_input

        print("The expected flow rate, {!s}, was very close "
              "to the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The expected flow rate, {!s}, is "
              "different from the one calculated by this "
              "validation code, {!s}.\n".format(q_input, q_calc))

# First should be invalid, second valid:
validate_manifold(3 * u.inch, 0.8, 285.6 * u.mm / u.s, 0.05, 1 * u.L/u.s)
validate_manifold(ac.ID_SDR(3.0 * u.inch, 26), 0.8, 285.6 * u.mm / u.s, 0.05, 1 * u.L/u.s)

def validate_plate_settlers(vel_capture, n_plate, l_plate, w_plate, space_plate, angle_plate, plate_thickness, cutoff, q_input):
    try:
        q_calc = vel_capture * (n_plate * w_plate * (l_plate * np.cos(angle_plate) + (space_plate / np.sin(angle_plate))))
        q_calc = q_calc.to(u.L / u.s)

        assert cutoff > (q_calc - q_input) / q_input
        assert -cutoff < (q_calc - q_input) / q_input

        print("The expected flow rate, {!s}, was very close "
              "to the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The expected flow rate, {!s}, is "
              "different from the one calculated by this "
              "validation code, {!s}.\n".format(q_input, q_calc))

# this returns invalid but shouldn't, maybe change the tolerance
# or have it be just min instead of checking max as well
validate_plate_settlers(0.12*u.mm/u.s, 26, 60*u.cm, 42*u.inch, 2.5*u.cm, 60*u.deg, 1*u.mm, 0.05, 1*u.L/u.s)

def validate_tank(length, width, vel_up, cutoff, q_input):
    try:
        q_calc = length * width * vel_up
        q_calc = q_calc.to(u.L / u.s)

        assert cutoff > (q_calc - q_input) / q_input
        assert -cutoff < (q_calc - q_input) / q_input

        print("The expected flow rate, {!s}, was very close "
              "to the one calculated by this validation "
              "code, {!s}.\n".format(q_input, q_calc))
    except AssertionError:
        print("INVALID: The expected flow rate, {!s}, is "
              "different from the one calculated by this "
              "validation code, {!s}.\n".format(q_input, q_calc))

validate_tank(1.1*u.m, 42*u.inch, 0.85*u.mm/u.s, 0.05, 1*u.L/u.s)

def validate_diffuser(w_sed, w_diffuser, vel_up, max_hl, temp, shear_floc_max=0.5*u.Pa, pi_plane_jet=0.0124):
    rho = ac.density_water(temp)
    nu = ac.viscosity_kinematic_water(temp)
    vel_diffuser = vel_up * w_sed / w_diffuser
    
    vel_max_shear = ((shear_floc_max/rho)**(1/2)*(vel_up*w_sed/(nu*pi_plane_jet))**(1/4)).to(u.mm/u.s)
    assert vel_diffuser < vel_max_shear

    head_loss = (vel_diffuser**2 / (2*u.g_0)).to(u.cm)
    assert head_loss < max_hl

validate_diffuser(42*u.inch, 1/8*u.inch, 0.85*u.mm/u.s, 1*u.cm, 20*u.degC)
