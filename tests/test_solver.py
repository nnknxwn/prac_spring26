import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
from solver import solve_bvp


def test_linear():
    # x1' = x2,  x2' = 0
    # x1(0) = 0,  x1(1) = 1  →  solution: x1 = t, x2 = 1
    _, t, x = solve_bvp(
        f_strings=["x2", "0"],
        R_strings=["xa0 - 0", "xb0 - 1"],
        var_names=["x1", "x2"],
        t_name="t",
        p0=[0.0, 0.5],
        t_span=(0.0, 1.0),
        t_star=0.0,
    )
    x1_half = np.interp(0.5, t, x[0])
    assert abs(x1_half - 0.5) < 1e-3


def test_exponential():
    # x' = x,  x(0) = 1  →  solution: x(t) = e^t
    _, t, x = solve_bvp(
        f_strings=["x1"],
        R_strings=["xa0 - 1"],
        var_names=["x1"],
        t_name="t",
        p0=[1.0],
        t_span=(0.0, 1.0),
        t_star=0.0,
    )
    assert abs(x[0][-1] - np.e) < 1e-3


def test_two_body():
    from examples.two_body import EQUATIONS, BOUNDARY_CONDITIONS, VARIABLES, T_VAR, T, P0_1
    p, _, _ = solve_bvp(
        f_strings=EQUATIONS,
        R_strings=BOUNDARY_CONDITIONS,
        var_names=VARIABLES,
        t_name=T_VAR,
        p0=P0_1,
        t_span=(0.0, T),
        t_star=0.0,
    )
    assert abs(p[0] - 2.0) < 1e-4
    assert abs(p[1] - 0.0) < 1e-4
    assert abs(p[3] - 0.5) < 1e-3


if __name__ == "__main__":
    test_linear();       print("test_linear        OK")
    test_exponential();  print("test_exponential   OK")
    test_two_body();     print("test_two_body      OK")
