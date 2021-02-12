# First should be invalid, second valid:
check_inlet_manifold(3 * u.inch, 0.8, 285.6 * u.mm / u.s, 0.05, 1 * u.L/u.s)
check_inlet_manifold(ac.ID_SDR(3.0 * u.inch, 26), 0.8, 285.6 * u.mm / u.s, 0.05, 1 * u.L/u.s)

# invalid test case still needed
check_plate_settlers(0.12*u.mm/u.s, 26, 60*u.cm, 42*u.inch, 2.5*u.cm, 60*u.deg, 1*u.mm, 0.05, 1*u.L/u.s)

# invalid test case still needed
check_sed_tank(1.1*u.m, 42*u.inch, 0.85*u.mm/u.s, 0.05, 1*u.L/u.s)

# invalid test case still needed
check_diffuser(42*u.inch, 1/8*u.inch, 0.85*u.mm/u.s, 1*u.cm, 20*u.degC)

# TODO: add test case
# check_outlet_manifold()
