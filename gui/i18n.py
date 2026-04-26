"""Interface strings for Russian and English localizations."""

STRINGS = {
    "ru": {
        # Tabs
        "tab_solution":   "Решение",
        "tab_parameters": "Параметры",
        "tab_author":     "Автор",
        "tab_help":       "Помощь",

        # Solution tab
        "dimension":      "Размерность системы",
        "interval":       "Отрезок [a, b]",
        "t_star":         "Точка t*",
        "p0":             "Начальное приближение p₀",
        "equations":      "Уравнения  ẋ = f(t, x)",
        "boundary":       "Краевые условия  R(x(a), x(b)) = 0",
        "btn_add":        "+",
        "btn_remove":     "−",
        "btn_solve":      "Решить",
        "btn_save":       "Сохранить",
        "btn_load":       "Загрузить",
        "result_plot":    "График решения",
        "result_table":   "Таблица значений",

        # Parameters tab — cards
        "inner_card_title":  "Внутренняя задача",
        "inner_card_desc":   "Интегрирование физической системы ОДУ",
        "outer_card_title":  "Внешняя задача",
        "outer_card_desc":   "Метод продолжения по параметру (гомотопия)",
        "param_method":      "Метод интегрирования",
        "param_rtol":        "Относительная точность (rtol)",
        "param_atol":        "Абсолютная точность (atol)",
        "param_max_iter":    "Макс. итераций",

        # Author tab
        "btn_exit":       "Выход",

        # Help tab
        "help_text": (
            "Метод продолжения по параметру решает краевую задачу\n"
            "x' = f(t,x),  R(x(a), x(b)) = 0\n\n"
            "Введите систему ОДУ и краевые условия во вкладке «Решение».\n"
            "Число уравнений должно совпадать с числом краевых условий.\n"
            "Настройте численные методы во вкладке «Параметры»."
        ),

        # Errors / messages
        "err_count_mismatch": "Число уравнений должно совпадать с числом краевых условий.",
        "err_not_implemented": "Решатель пока не реализован.",
        "status_solving":     "Вычисление...",
        "status_done":        "Готово.",
        "status_error":       "Ошибка: {msg}",
    },

    "en": {
        # Tabs
        "tab_solution":   "Solution",
        "tab_parameters": "Parameters",
        "tab_author":     "Author",
        "tab_help":       "Help",

        # Solution tab
        "dimension":      "System dimension",
        "interval":       "Interval [a, b]",
        "t_star":         "Point t*",
        "p0":             "Initial guess p₀",
        "equations":      "Equations  ẋ = f(t, x)",
        "boundary":       "Boundary conditions  R(x(a), x(b)) = 0",
        "btn_add":        "+",
        "btn_remove":     "−",
        "btn_solve":      "Solve",
        "btn_save":       "Save",
        "btn_load":       "Load",
        "result_plot":    "Solution plot",
        "result_table":   "Value table",

        # Parameters tab — cards
        "inner_card_title":  "Inner Problem",
        "inner_card_desc":   "ODE system integration",
        "outer_card_title":  "Outer Problem",
        "outer_card_desc":   "Parameter continuation method (homotopy)",
        "param_method":      "Integration method",
        "param_rtol":        "Relative tolerance (rtol)",
        "param_atol":        "Absolute tolerance (atol)",
        "param_max_iter":    "Max iterations",

        # Author tab
        "btn_exit":       "Exit",

        # Help tab
        "help_text": (
            "The parameter continuation method solves the BVP\n"
            "x' = f(t,x),  R(x(a), x(b)) = 0\n\n"
            "Enter the ODE system and boundary conditions in the 'Solution' tab.\n"
            "The number of equations must equal the number of boundary conditions.\n"
            "Configure numerical methods in the 'Parameters' tab."
        ),

        # Errors / messages
        "err_count_mismatch": "Number of equations must equal number of boundary conditions.",
        "err_not_implemented": "Solver is not implemented yet.",
        "status_solving":     "Computing...",
        "status_done":        "Done.",
        "status_error":       "Error: {msg}",
    },
}

LANGUAGES = list(STRINGS.keys())


def get(lang: str, key: str, **kwargs) -> str:
    text = STRINGS[lang][key]
    return text.format(**kwargs) if kwargs else text
