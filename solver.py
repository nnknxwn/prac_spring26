def solve_cauchy(f_sym, x_sym, t_sym, t_star, p, t_span,
                 method="RK45", rtol=1e-6, atol=1e-6):
    raise NotImplementedError


def solve_bvp(f_sym, R_sym, x_sym, t_sym, p0, t_span, t_star=None,
              inner_method="RK45", outer_method="RK45",
              inner_rtol=1e-6, inner_atol=1e-6,
              outer_rtol=1e-4, outer_atol=1e-4,
              max_iter=10):
    raise NotImplementedError
