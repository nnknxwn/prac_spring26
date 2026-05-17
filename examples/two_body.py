"""Two-body problem — kept for backward compatibility with tests.

The actual data is in examples.library; this module re-exports the values
expected by tests/test_solver.py.
"""

from examples.library import get_example


_data = get_example("two_body_1")

T = _data["b"]
EQUATIONS = _data["equations"]
BOUNDARY_CONDITIONS = _data["boundary"]
VARIABLES = [f"x{i+1}" for i in range(_data["n"])]
T_VAR = "t"
P0_1 = _data["p0"]
P0_2 = get_example("two_body_2")["p0"]
