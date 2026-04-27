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
        "param_tol":         "Точность",
        "param_max_iter":    "Макс. итераций",

        # Author tab
        "btn_exit":       "Выход",

        # Help tab
        "help_text": (
            "═══════════════════════════════════════════\n"
            "  РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ — BVP Solver\n"
            "═══════════════════════════════════════════\n\n"
            "Программа решает краевую задачу для системы ОДУ\n"
            "методом продолжения по параметру (метод стрельбы\n"
            "с гомотопией).\n\n"
            "───────────────────────────────────────────\n"
            "  ПОСТАНОВКА ЗАДАЧИ\n"
            "───────────────────────────────────────────\n\n"
            "Дана система ОДУ:\n"
            "   ẋ = f(t, x),   t ∈ [a, b]\n\n"
            "с краевыми условиями:\n"
            "   R(x(a), x(b)) = 0\n\n"
            "Число уравнений = число краевых условий = n.\n\n"
            "───────────────────────────────────────────\n"
            "  ВКЛАДКА «РЕШЕНИЕ» — ВВОД ДАННЫХ\n"
            "───────────────────────────────────────────\n\n"
            "1. Размерность (n)\n"
            "   Число уравнений в системе. При изменении\n"
            "   автоматически обновляются поля ввода.\n\n"
            "2. Уравнения ẋ = f(t, x)\n"
            "   Правые части системы ОДУ. Переменные: x1, x2, ..., t\n"
            "   Пример (n=2): x1' = x2,  x2' = -x1\n\n"
            "3. Краевые условия R(x(a), x(b)) = 0\n"
            "   Используйте обозначения:\n"
            "   • xa0, xa1, ... — значения x1(a), x2(a), ...\n"
            "   • xb0, xb1, ... — значения x1(b), x2(b), ...\n"
            "   Пример: R1 = xa0       (x1(0) = 0)\n"
            "           R2 = xb0 - 1   (x1(1) = 1)\n\n"
            "4. Отрезок [a, b]\n"
            "   Границы интервала интегрирования.\n\n"
            "5. Точка t*\n"
            "   Точка, из которой начинается интегрирование.\n"
            "   Обычно t* = a (левый край).\n\n"
            "6. Начальное приближение p₀\n"
            "   Начальная догадка для x(t*). Чем ближе к\n"
            "   истинному решению — тем быстрее сходимость.\n\n"
            "7. Кнопка «Решить»\n"
            "   Запускает вычисление. Результат — график и таблица.\n\n"
            "───────────────────────────────────────────\n"
            "  ВКЛАДКА «ПАРАМЕТРЫ»\n"
            "───────────────────────────────────────────\n\n"
            "Внутренняя задача — интегрирование системы ОДУ:\n"
            "  • Метод: выбор численного метода (Рунге-Кутта,\n"
            "    Радо, BDF, LSODA)\n"
            "  • Точность: используется как rtol и atol\n\n"
            "Внешняя задача — метод продолжения по параметру:\n"
            "  • Метод: обычно Рунге-Кутта 4(5) достаточно\n"
            "  • Точность: критерий остановки ||Φ(p)|| < tol\n"
            "  • Макс. итераций: предел внешних итераций\n\n"
            "При смене метода точность подставляется автоматически.\n\n"
            "───────────────────────────────────────────\n"
            "  ГРАФИК И ТАБЛИЦА\n"
            "───────────────────────────────────────────\n\n"
            "• Кнопка «•» — показать/скрыть узлы сетки\n"
            "  интегратора на графике\n"
            "• Кнопка «🎨» — сменить цвет линии для\n"
            "  каждой переменной\n"
            "• Таблица показывает значения в узлах сетки\n"
            "  (прореженные до ~50 строк)\n\n"
            "───────────────────────────────────────────\n"
            "  ПРИМЕР\n"
            "───────────────────────────────────────────\n\n"
            "Задача: x'' = 0,  x(0) = 0,  x(1) = 1\n"
            "Решение: x(t) = t\n\n"
            "Ввод (n = 2):\n"
            "  x1' = x2\n"
            "  x2' = 0\n"
            "  R1  = xa0\n"
            "  R2  = xb0 - 1\n"
            "  a = 0,  b = 1,  t* = 0\n"
            "  p1₀ = 0,  p2₀ = 1\n\n"
            "Результат: прямая x1 = t, константа x2 = 1.\n\n"
            "───────────────────────────────────────────\n"
            "  ГОРЯЧИЕ КЛАВИШИ\n"
            "───────────────────────────────────────────\n\n"
            "• Tab — переход между полями ввода\n"
            "• 🌙/☀ — смена темы (светлая/тёмная)\n"
            "• EN/RU — смена языка интерфейса\n"
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
        "param_tol":         "Tolerance",
        "param_max_iter":    "Max iterations",

        # Author tab
        "btn_exit":       "Exit",

        # Help tab
        "help_text": (
            "═══════════════════════════════════════════\n"
            "  USER GUIDE — BVP Solver\n"
            "═══════════════════════════════════════════\n\n"
            "This application solves boundary value problems\n"
            "for ODE systems using the parameter continuation\n"
            "method (shooting with homotopy).\n\n"
            "───────────────────────────────────────────\n"
            "  PROBLEM STATEMENT\n"
            "───────────────────────────────────────────\n\n"
            "Given an ODE system:\n"
            "   ẋ = f(t, x),   t ∈ [a, b]\n\n"
            "with boundary conditions:\n"
            "   R(x(a), x(b)) = 0\n\n"
            "Number of equations = number of BCs = n.\n\n"
            "───────────────────────────────────────────\n"
            "  SOLUTION TAB — DATA INPUT\n"
            "───────────────────────────────────────────\n\n"
            "1. Dimension (n)\n"
            "   Number of equations. Input fields update\n"
            "   automatically when changed.\n\n"
            "2. Equations ẋ = f(t, x)\n"
            "   Right-hand sides of the ODE. Variables: x1, x2, ..., t\n"
            "   Example (n=2): x1' = x2,  x2' = -x1\n\n"
            "3. Boundary conditions R(x(a), x(b)) = 0\n"
            "   Use notation:\n"
            "   • xa0, xa1, ... — values x1(a), x2(a), ...\n"
            "   • xb0, xb1, ... — values x1(b), x2(b), ...\n"
            "   Example: R1 = xa0       (x1(0) = 0)\n"
            "            R2 = xb0 - 1   (x1(1) = 1)\n\n"
            "4. Interval [a, b]\n"
            "   Integration interval boundaries.\n\n"
            "5. Point t*\n"
            "   Starting point for integration.\n"
            "   Usually t* = a (left boundary).\n\n"
            "6. Initial guess p₀\n"
            "   Initial guess for x(t*). Closer to the true\n"
            "   solution = faster convergence.\n\n"
            "7. Solve button\n"
            "   Starts computation. Result: plot and table.\n\n"
            "───────────────────────────────────────────\n"
            "  PARAMETERS TAB\n"
            "───────────────────────────────────────────\n\n"
            "Inner problem — ODE system integration:\n"
            "  • Method: numerical method (Runge-Kutta,\n"
            "    Radau, BDF, LSODA)\n"
            "  • Tolerance: used as both rtol and atol\n\n"
            "Outer problem — parameter continuation:\n"
            "  • Method: Runge-Kutta 4(5) usually sufficient\n"
            "  • Tolerance: stopping criterion ||Φ(p)|| < tol\n"
            "  • Max iterations: outer iteration limit\n\n"
            "Tolerance auto-updates when method is changed.\n\n"
            "───────────────────────────────────────────\n"
            "  PLOT AND TABLE\n"
            "───────────────────────────────────────────\n\n"
            "• Button «•» — show/hide integrator grid\n"
            "  points on the plot\n"
            "• Button «🎨» — change line color for each\n"
            "  variable\n"
            "• Table shows values at grid nodes\n"
            "  (thinned to ~50 rows)\n\n"
            "───────────────────────────────────────────\n"
            "  EXAMPLE\n"
            "───────────────────────────────────────────\n\n"
            "Problem: x'' = 0,  x(0) = 0,  x(1) = 1\n"
            "Solution: x(t) = t\n\n"
            "Input (n = 2):\n"
            "  x1' = x2\n"
            "  x2' = 0\n"
            "  R1  = xa0\n"
            "  R2  = xb0 - 1\n"
            "  a = 0,  b = 1,  t* = 0\n"
            "  p1₀ = 0,  p2₀ = 1\n\n"
            "Result: line x1 = t, constant x2 = 1.\n\n"
            "───────────────────────────────────────────\n"
            "  SHORTCUTS\n"
            "───────────────────────────────────────────\n\n"
            "• Tab — navigate between input fields\n"
            "• 🌙/☀ — toggle theme (light/dark)\n"
            "• EN/RU — switch interface language\n"
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
