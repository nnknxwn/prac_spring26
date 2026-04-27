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
        "btn_solve":      "Решить",
        "result_plot":    "График решения",
        "result_table":   "Таблица значений",

        # Parameters tab — cards
        "inner_card_title":  "Внутренняя задача",
        "inner_card_desc":   "Интегрирование физической системы ОДУ",
        "outer_card_title":  "Внешняя задача",
        "outer_card_desc":   "Метод продолжения по параметру (гомотопия)",
        "param_method":      "Метод интегрирования",
        "param_tol":         "Точность",
        "param_max_iter":    "Макс. итераций",

        # Help tab — sections
        "help_intro_title": "О программе",
        "help_intro_body": (
            "Программа решает краевую задачу для системы ОДУ методом продолжения "
            "по параметру (метод стрельбы с гомотопией).<br><br>"
            "Дана система: <b>ẋ = f(t, x)</b>, &nbsp; t ∈ [a, b]<br>"
            "Краевые условия: <b>R(x(a), x(b)) = 0</b><br>"
            "Число уравнений = число краевых условий = n."
        ),
        "help_input_title": "Вкладка «Решение» — ввод данных",
        "help_input_body": (
            "<b>Размерность (n)</b> — число уравнений в системе. "
            "Поля ввода обновляются автоматически.<br><br>"
            "<b>Уравнения ẋ = f(t, x)</b> — правые части системы ОДУ. "
            "Переменные: x1, x2, ..., t<br>"
            "Пример (n=2): x1' = x2, &nbsp; x2' = -x1<br><br>"
            "<b>Краевые условия R = 0</b> — используйте обозначения:<br>"
            "• xa0, xa1, ... — значения x1(a), x2(a), ...<br>"
            "• xb0, xb1, ... — значения x1(b), x2(b), ...<br>"
            "Пример: R1 = xa0 &nbsp;(x1(0)=0), &nbsp; R2 = xb0 - 1 &nbsp;(x1(1)=1)<br><br>"
            "<b>Отрезок [a, b]</b> — границы интервала интегрирования.<br><br>"
            "<b>Точка t*</b> — точка старта интегрирования (обычно t* = a).<br><br>"
            "<b>Начальное приближение p₀</b> — догадка для x(t*). "
            "Чем ближе к решению — тем быстрее сходимость."
        ),
        "help_params_title": "Вкладка «Параметры»",
        "help_params_body": (
            "<b>Внутренняя задача</b> — интегрирование системы ОДУ:<br>"
            "• Метод: Рунге-Кутта, Радо, BDF, LSODA<br>"
            "• Точность: используется как rtol и atol<br><br>"
            "<b>Внешняя задача</b> — метод продолжения по параметру:<br>"
            "• Метод: обычно Рунге-Кутта 4(5) достаточно<br>"
            "• Точность: критерий остановки ||Φ(p)|| &lt; tol<br>"
            "• Макс. итераций: предел внешних итераций<br><br>"
            "При смене метода точность подставляется автоматически."
        ),
        "help_plot_title": "График и таблица",
        "help_plot_body": (
            "• Кнопка <b>«•»</b> — показать/скрыть узлы сетки интегратора<br>"
            "• Кнопка <b>«🎨»</b> — сменить цвет линии для каждой переменной<br>"
            "• Таблица показывает значения в узлах сетки (до ~50 строк)"
        ),
        "help_example_title": "Пример",
        "help_example_body": (
            "Задача: x'' = 0, &nbsp; x(0) = 0, &nbsp; x(1) = 1<br>"
            "Решение: x(t) = t<br><br>"
            "Ввод (n = 2):<br>"
            "&nbsp;&nbsp;x1' = x2<br>"
            "&nbsp;&nbsp;x2' = 0<br>"
            "&nbsp;&nbsp;R1 = xa0<br>"
            "&nbsp;&nbsp;R2 = xb0 - 1<br>"
            "&nbsp;&nbsp;a = 0, &nbsp; b = 1, &nbsp; t* = 0<br>"
            "&nbsp;&nbsp;p1₀ = 0, &nbsp; p2₀ = 1<br><br>"
            "Результат: прямая x1 = t, константа x2 = 1."
        ),
        "help_shortcuts_title": "Горячие клавиши",
        "help_shortcuts_body": (
            "• <b>Tab</b> — переход между полями ввода<br>"
            "• <b>🌙/☀</b> — смена темы (светлая/тёмная)<br>"
            "• <b>EN/RU</b> — смена языка интерфейса"
        ),

        # Errors / messages
        "err_count_mismatch": "Число уравнений должно совпадать с числом краевых условий.",
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
        "btn_solve":      "Solve",
        "result_plot":    "Solution plot",
        "result_table":   "Value table",

        # Parameters tab — cards
        "inner_card_title":  "Inner Problem",
        "inner_card_desc":   "ODE system integration",
        "outer_card_title":  "Outer Problem",
        "outer_card_desc":   "Parameter continuation method (homotopy)",
        "param_method":      "Integration method",
        "param_tol":         "Tolerance",
        "param_max_iter":    "Max iterations",

        # Help tab — sections
        "help_intro_title": "About",
        "help_intro_body": (
            "This application solves boundary value problems for ODE systems "
            "using the parameter continuation method (shooting with homotopy).<br><br>"
            "Given: <b>ẋ = f(t, x)</b>, &nbsp; t ∈ [a, b]<br>"
            "Boundary conditions: <b>R(x(a), x(b)) = 0</b><br>"
            "Number of equations = number of BCs = n."
        ),
        "help_input_title": "Solution Tab — Data Input",
        "help_input_body": (
            "<b>Dimension (n)</b> — number of equations. "
            "Input fields update automatically.<br><br>"
            "<b>Equations ẋ = f(t, x)</b> — right-hand sides. "
            "Variables: x1, x2, ..., t<br>"
            "Example (n=2): x1' = x2, &nbsp; x2' = -x1<br><br>"
            "<b>Boundary conditions R = 0</b> — use notation:<br>"
            "• xa0, xa1, ... — values x1(a), x2(a), ...<br>"
            "• xb0, xb1, ... — values x1(b), x2(b), ...<br>"
            "Example: R1 = xa0 &nbsp;(x1(0)=0), &nbsp; R2 = xb0 - 1 &nbsp;(x1(1)=1)<br><br>"
            "<b>Interval [a, b]</b> — integration boundaries.<br><br>"
            "<b>Point t*</b> — integration start point (usually t* = a).<br><br>"
            "<b>Initial guess p₀</b> — guess for x(t*). "
            "Closer to solution = faster convergence."
        ),
        "help_params_title": "Parameters Tab",
        "help_params_body": (
            "<b>Inner problem</b> — ODE system integration:<br>"
            "• Method: Runge-Kutta, Radau, BDF, LSODA<br>"
            "• Tolerance: used as both rtol and atol<br><br>"
            "<b>Outer problem</b> — parameter continuation:<br>"
            "• Method: Runge-Kutta 4(5) usually sufficient<br>"
            "• Tolerance: stopping criterion ||Φ(p)|| &lt; tol<br>"
            "• Max iterations: outer iteration limit<br><br>"
            "Tolerance auto-updates when method is changed."
        ),
        "help_plot_title": "Plot and Table",
        "help_plot_body": (
            "• Button <b>«•»</b> — show/hide integrator grid points<br>"
            "• Button <b>«🎨»</b> — change line color per variable<br>"
            "• Table shows values at grid nodes (up to ~50 rows)"
        ),
        "help_example_title": "Example",
        "help_example_body": (
            "Problem: x'' = 0, &nbsp; x(0) = 0, &nbsp; x(1) = 1<br>"
            "Solution: x(t) = t<br><br>"
            "Input (n = 2):<br>"
            "&nbsp;&nbsp;x1' = x2<br>"
            "&nbsp;&nbsp;x2' = 0<br>"
            "&nbsp;&nbsp;R1 = xa0<br>"
            "&nbsp;&nbsp;R2 = xb0 - 1<br>"
            "&nbsp;&nbsp;a = 0, &nbsp; b = 1, &nbsp; t* = 0<br>"
            "&nbsp;&nbsp;p1₀ = 0, &nbsp; p2₀ = 1<br><br>"
            "Result: line x1 = t, constant x2 = 1."
        ),
        "help_shortcuts_title": "Shortcuts",
        "help_shortcuts_body": (
            "• <b>Tab</b> — navigate between input fields<br>"
            "• <b>🌙/☀</b> — toggle theme (light/dark)<br>"
            "• <b>EN/RU</b> — switch interface language"
        ),

        # Errors / messages
        "err_count_mismatch": "Number of equations must equal number of boundary conditions.",
        "status_solving":     "Computing...",
        "status_done":        "Done.",
        "status_error":       "Error: {msg}",
    },
}

LANGUAGES = list(STRINGS.keys())


def get(lang: str, key: str, **kwargs) -> str:
    text = STRINGS[lang][key]
    return text.format(**kwargs) if kwargs else text
