T = 7.0

EQUATIONS = [
    "x3",
    "x4",
    "-x1 / (x1**2 + x2**2)**1.5",
    "-x2 / (x1**2 + x2**2)**1.5",
]

BOUNDARY_CONDITIONS = [
    "xa0 - 2",
    "xa1 - 0",
    "xb0 - 1.0738644361",
    "xb1 + 1.0995343576",
]

VARIABLES = ["x1", "x2", "x3", "x4"]
T_VAR = "t"

P0_1 = [2.0, 0.0, -0.5,  0.5]
P0_2 = [2.0, 0.0,  0.5, -0.5]

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    import numpy as np
    from solver import solve_bvp

    for label, p0 in [("p01", P0_1), ("p02", P0_2)]:
        print(f"\nSolving with {label} = {p0}")
        p, t, x = solve_bvp(
            EQUATIONS, BOUNDARY_CONDITIONS, VARIABLES, T_VAR,
            p0, (0.0, T), t_star=0.0,
        )
        print(f"  p = {np.round(p, 10)}")
