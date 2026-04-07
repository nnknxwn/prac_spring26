import numpy as np
from scipy.integrate import solve_ivp
from sympy import symbols, Matrix, lambdify
from sympy.parsing.sympy_parser import parse_expr


def _build_functions(f_strings, R_strings, var_names, t_name):
    n = len(var_names)

    t_sym   = symbols(t_name)
    x_syms  = list(symbols(var_names))
    xa_syms = list(symbols([f"xa{i}" for i in range(n)]))
    xb_syms = list(symbols([f"xb{i}" for i in range(n)]))

    f_locals = {name: sym for name, sym in zip(var_names, x_syms)}
    f_locals[t_name] = t_sym

    R_locals = {f"xa{i}": s for i, s in enumerate(xa_syms)}
    R_locals.update({f"xb{i}": s for i, s in enumerate(xb_syms)})

    f_vec = Matrix([parse_expr(s, local_dict=f_locals) for s in f_strings])
    R_vec = Matrix([parse_expr(s, local_dict=R_locals) for s in R_strings])

    fx  = f_vec.jacobian(x_syms)
    Rxa = R_vec.jacobian(xa_syms)
    Rxb = R_vec.jacobian(xb_syms)

    f_num   = lambdify([t_sym] + x_syms,        f_vec, modules="numpy")
    fx_num  = lambdify([t_sym] + x_syms,        fx,    modules="numpy")
    R_num   = lambdify(xa_syms + xb_syms,       R_vec, modules="numpy")
    Rxa_num = lambdify(xa_syms + xb_syms,       Rxa,   modules="numpy")
    Rxb_num = lambdify(xa_syms + xb_syms,       Rxb,   modules="numpy")

    return f_num, fx_num, R_num, Rxa_num, Rxb_num


def _inner_solve(f_num, fx_num, t_star, p, t_span, method, rtol, atol):
    n = len(p)
    a, b = t_span

    def rhs(t, y):
        x  = y[:n]
        X  = y[n:].reshape(n, n)
        fv = np.array(f_num(t, *x),  dtype=float).flatten()
        Jv = np.array(fx_num(t, *x), dtype=float).reshape(n, n)
        return np.concatenate([fv, (Jv @ X).flatten()])

    y0 = np.concatenate([p, np.eye(n).flatten()])

    if np.isclose(t_star, a):
        ya = y0
    else:
        sol = solve_ivp(rhs, [t_star, a], y0, method=method, rtol=rtol, atol=atol)
        ya  = sol.y[:, -1]

    if np.isclose(t_star, b):
        yb = y0
    else:
        sol = solve_ivp(rhs, [t_star, b], y0, method=method, rtol=rtol, atol=atol)
        yb  = sol.y[:, -1]

    return ya[:n], yb[:n], ya[n:].reshape(n, n), yb[n:].reshape(n, n)


def solve_bvp(f_strings, R_strings, var_names, t_name, p0, t_span, t_star=None,
              inner_method="RK45", outer_method="RK45",
              inner_rtol=1e-6, inner_atol=1e-6,
              outer_rtol=1e-4, outer_atol=1e-4,
              max_iter=10):

    a, b = t_span
    if t_star is None:
        t_star = a

    p = np.array(p0, dtype=float)
    n = len(p)

    f_num, fx_num, R_num, Rxa_num, Rxb_num = _build_functions(
        f_strings, R_strings, var_names, t_name
    )

    def Phi(p_cur):
        xa, xb, _, _ = _inner_solve(f_num, fx_num, t_star, p_cur, t_span,
                                     inner_method, inner_rtol, inner_atol)
        return np.array(R_num(*xa, *xb), dtype=float).flatten()

    def Phi_prime(p_cur):
        xa, xb, Xa, Xb = _inner_solve(f_num, fx_num, t_star, p_cur, t_span,
                                        inner_method, inner_rtol, inner_atol)
        Ja = np.array(Rxa_num(*xa, *xb), dtype=float).reshape(n, n)
        Jb = np.array(Rxb_num(*xa, *xb), dtype=float).reshape(n, n)
        return Ja @ Xa + Jb @ Xb

    for _ in range(max_iter):
        Phi0 = Phi(p)
        if np.linalg.norm(Phi0) < outer_rtol:
            break

        Phi0_fixed = Phi0.copy()

        def outer_rhs(_, p_cur):
            J = Phi_prime(p_cur)
            try:
                return -np.linalg.solve(J, Phi0_fixed)
            except np.linalg.LinAlgError:
                raise RuntimeError("Jacobian matrix is singular")

        sol = solve_ivp(outer_rhs, [0.0, 1.0], p,
                        method=outer_method, rtol=outer_rtol, atol=outer_atol)
        p = sol.y[:, -1]

    def f_rhs(t, x):
        return np.array(f_num(t, *x), dtype=float).flatten()

    if np.isclose(t_star, a):
        traj = solve_ivp(f_rhs, [a, b], p,
                         method=inner_method, rtol=inner_rtol, atol=inner_atol,
                         dense_output=True)
        t_out = traj.t
        x_out = traj.y
    else:
        traj_fwd = solve_ivp(f_rhs, [t_star, b], p,
                              method=inner_method, rtol=inner_rtol, atol=inner_atol)
        traj_bwd = solve_ivp(f_rhs, [t_star, a], p,
                              method=inner_method, rtol=inner_rtol, atol=inner_atol)
        t_out = np.concatenate([traj_bwd.t[::-1], traj_fwd.t[1:]])
        x_out = np.concatenate([traj_bwd.y[:, ::-1], traj_fwd.y[:, 1:]], axis=1)

    return p, t_out, x_out
