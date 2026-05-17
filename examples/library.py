"""Built-in BVP examples library.

Each example is a dict with all data needed to load into the GUI.
Categories:
  - "tutorial" — simple textbook problems
  - "article"  — examples from Avvakumov, Kiselev (2006)

Fields:
  id            — unique identifier
  category      — group key
  name_ru/_en   — display name
  source_ru/_en — citation / origin
  n             — system dimension
  equations     — list of n RHS strings  (variables: x1..xn, t)
  boundary      — list of n BC strings   (variables: xa0..xa(n-1), xb0..xb(n-1))
  a, b, t_star  — interval and start point
  p0            — initial guess for x(t_star)
  inner_method  — solve_ivp method for inner problem
  outer_method  — solve_ivp method for outer problem
  inner_tol     — tolerance for inner problem
  outer_tol     — tolerance for outer problem
  max_iter      — outer iteration limit
"""


EXAMPLES = [
    # --------------------------------------------------------------- #
    # Tutorial examples                                                 #
    # --------------------------------------------------------------- #
    {
        "id": "linear",
        "category": "tutorial",
        "name_ru": "Линейная задача",
        "name_en": "Linear problem",
        "source_ru": "Учебный пример: x'' = 0, x(0)=0, x(1)=1, решение x(t)=t",
        "source_en": "Textbook: x'' = 0, x(0)=0, x(1)=1, solution x(t)=t",
        "n": 2,
        "equations": ["x2", "0"],
        "boundary": ["xa0", "xb0 - 1"],
        "a": 0.0, "b": 1.0, "t_star": 0.0,
        "p0": [0.0, 1.0],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },
    {
        "id": "exponential",
        "category": "tutorial",
        "name_ru": "Экспонента",
        "name_en": "Exponential",
        "source_ru": "Учебный пример: x' = x, x(0)=1, решение x(t)=e^t",
        "source_en": "Textbook: x' = x, x(0)=1, solution x(t)=e^t",
        "n": 1,
        "equations": ["x1"],
        "boundary": ["xa0 - 1"],
        "a": 0.0, "b": 1.0, "t_star": 0.0,
        "p0": [1.0],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },
    {
        "id": "harmonic",
        "category": "tutorial",
        "name_ru": "Гармонический осциллятор",
        "name_en": "Harmonic oscillator",
        "source_ru": "Учебный пример: x'' + x = 0, x(0)=0, x(π)=0, решение x(t)=sin(t)",
        "source_en": "Textbook: x'' + x = 0, x(0)=0, x(π)=0, solution x(t)=sin(t)",
        "n": 2,
        "equations": ["x2", "-x1"],
        "boundary": ["xa0", "xb0"],
        "a": 0.0, "b": 3.141592653589793, "t_star": 0.0,
        "p0": [0.0, 1.0],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },

    # --------------------------------------------------------------- #
    # Examples from Avvakumov, Kiselev (2006)                           #
    # --------------------------------------------------------------- #
    {
        "id": "two_body_1",
        "category": "article",
        "name_ru": "Задача двух тел (вариант 1)",
        "name_en": "Two-body problem (variant 1)",
        "source_ru": "Аввакумов, Киселев (2006), пример 1, p0=[2,0,-0.5,0.5]",
        "source_en": "Avvakumov, Kiselev (2006), example 1, p0=[2,0,-0.5,0.5]",
        "n": 4,
        "equations": [
            "x3",
            "x4",
            "-x1 / (x1**2 + x2**2)**1.5",
            "-x2 / (x1**2 + x2**2)**1.5",
        ],
        "boundary": [
            "xa0 - 2",
            "xa1",
            "xb0 - 1.0738644361",
            "xb1 + 1.0995343576",
        ],
        "a": 0.0, "b": 7.0, "t_star": 0.0,
        "p0": [2.0, 0.0, -0.5, 0.5],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },
    {
        "id": "two_body_2",
        "category": "article",
        "name_ru": "Задача двух тел (вариант 2)",
        "name_en": "Two-body problem (variant 2)",
        "source_ru": "Аввакумов, Киселев (2006), пример 1, p0=[2,0,0.5,-0.5]",
        "source_en": "Avvakumov, Kiselev (2006), example 1, p0=[2,0,0.5,-0.5]",
        "n": 4,
        "equations": [
            "x3",
            "x4",
            "-x1 / (x1**2 + x2**2)**1.5",
            "-x2 / (x1**2 + x2**2)**1.5",
        ],
        "boundary": [
            "xa0 - 2",
            "xa1",
            "xb0 - 1.0738644361",
            "xb1 + 1.0995343576",
        ],
        "a": 0.0, "b": 7.0, "t_star": 0.0,
        "p0": [2.0, 0.0, 0.5, -0.5],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },
    {
        "id": "ekweiler_1",
        "category": "article",
        "name_ru": "Предельный цикл Эквейлера №1",
        "name_en": "Ekweiler limit cycle #1",
        "source_ru": "Аввакумов, Киселев (2006), пример 2, p0=[2,0,2π,2]",
        "source_en": "Avvakumov, Kiselev (2006), example 2, p0=[2,0,2π,2]",
        "n": 4,
        "equations": [
            "x3*x2",
            "x3*(-x1 + sin(x2))",
            "0",
            "0",
        ],
        "boundary": [
            "xa0 - xa3",
            "xa1",
            "xb0 - xb3",
            "xb1",
        ],
        "a": 0.0, "b": 1.0, "t_star": 0.0,
        "p0": [2.0, 0.0, 6.283185307179586, 2.0],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },
    {
        "id": "ekweiler_2",
        "category": "article",
        "name_ru": "Предельный цикл Эквейлера №2",
        "name_en": "Ekweiler limit cycle #2",
        "source_ru": "Аввакумов, Киселев (2006), пример 2, p0=[6.5,0,2π,6.5]",
        "source_en": "Avvakumov, Kiselev (2006), example 2, p0=[6.5,0,2π,6.5]",
        "n": 4,
        "equations": [
            "x3*x2",
            "x3*(-x1 + sin(x2))",
            "0",
            "0",
        ],
        "boundary": [
            "xa0 - xa3",
            "xa1",
            "xb0 - xb3",
            "xb1",
        ],
        "a": 0.0, "b": 1.0, "t_star": 0.0,
        "p0": [6.5, 0.0, 6.283185307179586, 6.5],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },
    {
        "id": "ekweiler_3",
        "category": "article",
        "name_ru": "Предельный цикл Эквейлера №3",
        "name_en": "Ekweiler limit cycle #3",
        "source_ru": "Аввакумов, Киселев (2006), пример 2, p0=[9,0,2π,9]",
        "source_en": "Avvakumov, Kiselev (2006), example 2, p0=[9,0,2π,9]",
        "n": 4,
        "equations": [
            "x3*x2",
            "x3*(-x1 + sin(x2))",
            "0",
            "0",
        ],
        "boundary": [
            "xa0 - xa3",
            "xa1",
            "xb0 - xb3",
            "xb1",
        ],
        "a": 0.0, "b": 1.0, "t_star": 0.0,
        "p0": [9.0, 0.0, 6.283185307179586, 9.0],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },
    {
        "id": "triple_integrator",
        "category": "article",
        "name_ru": "Трёхкратный интегратор (энергия)",
        "name_en": "Triple integrator (energy)",
        "source_ru": "Аввакумов, Киселев (2006), пример 3, сглаженная sat, ν=1e-10",
        "source_en": "Avvakumov, Kiselev (2006), example 3, smoothed sat, ν=1e-10",
        "n": 6,
        "equations": [
            "x2",
            "x3",
            "0.5*(sqrt(1e-10 + (x6 + 1)**2) - sqrt(1e-10 + (x6 - 1)**2))",
            "0",
            "-x4",
            "-x5",
        ],
        "boundary": [
            "xa0 - 1",
            "xa1",
            "xa2",
            "xb0",
            "xb1",
            "xb2",
        ],
        "a": 0.0, "b": 3.275, "t_star": 3.275,
        "p0": [0.0, 0.0, 0.0, -2.9850435834, 4.8880088678, -2.9083874537],
        "inner_method": "RK45", "outer_method": "RK45",
        "inner_tol": "1e-6", "outer_tol": "1e-4",
        "max_iter": 10,
    },
]


def get_example(example_id):
    """Return example dict by id, or None."""
    for ex in EXAMPLES:
        if ex["id"] == example_id:
            return ex
    return None


def by_category(category):
    """Return all examples in given category."""
    return [ex for ex in EXAMPLES if ex["category"] == category]
