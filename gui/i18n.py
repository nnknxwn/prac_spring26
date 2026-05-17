"""Interface strings for Russian and English localizations."""

STRINGS = {
    "ru": {
        # App title
        "app_title":      "Решатель краевых задач",

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
        "result_phase":   "Фазовая плоскость",
        "result_table":   "Таблица значений",
        "table_step":     "Шаг Δt:",
        "table_step_placeholder": "авто",
        "phase_x":        "X:",
        "phase_y":        "Y:",
        "tip_markers":    "Показать/скрыть узлы сетки",
        "tip_phase":      "Фазовая плоскость",
        "tip_colors":     "Цвета линий",
        "tip_axes":       "Границы осей",
        "tip_table_step": "Шаг по t для таблицы (например, 0.1). Должен быть ≤ b−a. Пусто = автопрорежение.",
        "btn_axes_reset": "Сбросить",

        # Library / Save / Load
        "btn_library":    "📚 Примеры",
        "btn_save":       "💾 Сохранить",
        "btn_load":       "📂 Открыть",
        "lib_tutorial":   "Учебные",
        "lib_article":    "Из статьи (Аввакумов, Киселев, 2006)",
        "save_dialog":    "Сохранить задачу",
        "load_dialog":    "Открыть задачу",
        "json_filter":    "JSON файлы (*.json)",
        "save_error":     "Не удалось сохранить: {msg}",
        "load_error":     "Не удалось загрузить: {msg}",

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
            "Чем ближе к решению — тем быстрее сходимость.<br><br>"
            "<b>Кнопки управления:</b><br>"
            "• <b>«📚 Примеры»</b> — встроенная библиотека: учебные задачи и "
            "примеры из статьи Аввакумова-Киселева (2006)<br>"
            "• <b>«📂 Открыть»</b> — загрузить задачу из JSON<br>"
            "• <b>«💾 Сохранить»</b> — сохранить текущую задачу в JSON"
        ),
        "help_params_title": "Вкладка «Параметры»",
        "help_params_body": (
            "<b>Внутренняя задача</b> — интегрирование системы ОДУ:<br>"
            "• Метод: RK45, Radau, LSODA<br>"
            "• Точность: используется как rtol и atol<br><br>"
            "<b>Внешняя задача</b> — метод продолжения по параметру:<br>"
            "• Метод: обычно Рунге-Кутта 4(5) достаточно<br>"
            "• Точность: критерий остановки ||Φ(p)|| &lt; tol<br>"
            "• Макс. итераций: предел внешних итераций<br><br>"
            "При смене метода точность подставляется автоматически.<br><br>"
            "<b>Доступные методы:</b><br>"
            "• <b>Рунге-Кутта 4(5) (RK45)</b> — явный метод Рунге-Кутта порядка 4(5) "
            "Дорманда-Принса. Универсальный, по умолчанию. Подходит для большинства "
            "нежёстких задач.<br>"
            "• <b>Радо IIA (Radau)</b> — неявный метод Рунге-Кутта 5-го порядка с "
            "А-устойчивостью. Для жёстких систем, когда переменные меняются на "
            "сильно разных временных масштабах.<br>"
            "• <b>LSODA</b> — адаптивный метод Адамса-Моултона, автоматически "
            "переключается между жёстким и нежёстким режимом. Использовать когда "
            "не уверен в природе задачи."
        ),
        "help_methods_title": "Когда какой метод выбирать",
        "help_methods_body": (
            "<b>Жёсткая система</b> — задача, в которой переменные меняются "
            "на сильно разных временных масштабах (большие коэффициенты разного порядка). "
            "Например, химкинетика с реакциями k₁=10⁶ и k₂=1.<br><br>"
            "<b>Краткие рекомендации:</b><br>"
            "• <b>RK45</b> — нежёсткие задачи: механика, орбиты, колебания.<br>"
            "• <b>Radau IIA</b> — жёсткие задачи: химкинетика, электрические цепи, "
            "задачи с резкими переключениями.<br>"
            "• <b>LSODA</b> — если не уверен в природе задачи.<br><br>"
            "<b>Уровни точности:</b><br>"
            "• <b>1e-2 / 1e-3</b> — грубая прикидка, форма решения<br>"
            "• <b>1e-4 / 1e-6</b> — стандарт, дефолт программы<br>"
            "• <b>1e-8 / 1e-9</b> — высокая точность<br>"
            "• <b>1e-10 / 1e-12</b> — научные расчёты<br><br>"
            "<i>Правило: точность внутренней задачи должна быть жёстче, чем внешней.</i>"
        ),
        "help_plot_title": "График и таблица",
        "help_plot_body": (
            "<b>Кнопки графика:</b><br>"
            "• <b>«📐»</b> — фазовая плоскость (для n ≥ 2): выбираешь, какие "
            "переменные на осях X и Y. Линия одна, вместо легенды.<br>"
            "• <b>«•»</b> — показать/скрыть узлы сетки интегратора.<br>"
            "• <b>«🎨»</b> — сменить цвет линии для каждой переменной.<br>"
            "• <b>«📏»</b> — задать границы осей вручную. Пустые поля = авто. "
            "Полезно, если автомасштаб накладывает легенду на кривые.<br><br>"
            "<b>Таблица значений:</b><br>"
            "• Строки нумеруются автоматически.<br>"
            "• Поле <b>«Шаг Δt»</b> — шаг по t для равномерной сетки. "
            "Например, при [a, b] = [0, 1] и шаге 0.1 будет 11 строк. "
            "Шаг должен быть ≤ b−a, иначе игнорируется.<br>"
            "• Пусто = автопрорежение узлов сетки интегратора до ~50 строк."
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
        "help_json_title": "Создание собственной задачи",
        "help_json_body": (
            "Можно сохранить текущую задачу в JSON через кнопку «💾 Сохранить» "
            "и открыть её позже через «📂 Открыть».<br><br>"
            "Можно создать JSON-файл вручную в любом текстовом редакторе:<br><br>"
            "<pre style='font-size:11px'>"
            "{<br>"
            "&nbsp;&nbsp;\"n\": 2,<br>"
            "&nbsp;&nbsp;\"equations\": [\"x2\", \"0\"],<br>"
            "&nbsp;&nbsp;\"boundary\": [\"xa0\", \"xb0 - 1\"],<br>"
            "&nbsp;&nbsp;\"a\": 0.0,<br>"
            "&nbsp;&nbsp;\"b\": 1.0,<br>"
            "&nbsp;&nbsp;\"t_star\": 0.0,<br>"
            "&nbsp;&nbsp;\"p0\": [0.0, 1.0],<br>"
            "&nbsp;&nbsp;\"inner_method\": \"RK45\",<br>"
            "&nbsp;&nbsp;\"outer_method\": \"RK45\",<br>"
            "&nbsp;&nbsp;\"inner_tol\": \"1e-6\",<br>"
            "&nbsp;&nbsp;\"outer_tol\": \"1e-4\",<br>"
            "&nbsp;&nbsp;\"max_iter\": 10<br>"
            "}"
            "</pre>"
            "<b>Поля:</b><br>"
            "• <b>n</b> — размерность системы<br>"
            "• <b>equations</b> — список из n правых частей ẋ = f(t, x)<br>"
            "• <b>boundary</b> — список из n краевых условий R = 0<br>"
            "• <b>a, b</b> — границы отрезка интегрирования<br>"
            "• <b>t_star</b> — точка старта (обычно равна a)<br>"
            "• <b>p0</b> — начальное приближение для x(t*) длины n<br>"
            "• <b>inner_method, outer_method</b> — RK45, Radau, LSODA<br>"
            "• <b>inner_tol, outer_tol</b> — точность строкой (например, \"1e-6\")<br>"
            "• <b>max_iter</b> — максимум внешних итераций"
        ),

        # Errors / messages
        "err_count_mismatch": "Число уравнений должно совпадать с числом краевых условий.",
        "status_solving":     "Вычисление...",
        "status_done":        "Готово.",
        "status_error":       "Ошибка: {msg}",
    },

    "en": {
        # App title
        "app_title":      "BVP Solver",

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
        "result_phase":   "Phase plane",
        "result_table":   "Value table",
        "table_step":     "Step Δt:",
        "table_step_placeholder": "auto",
        "phase_x":        "X:",
        "phase_y":        "Y:",
        "tip_markers":    "Show/hide grid points",
        "tip_phase":      "Phase plane",
        "tip_colors":     "Line colors",
        "tip_axes":       "Axes range",
        "tip_table_step": "Step in t for the table (e.g. 0.1). Must be ≤ b−a. Empty = auto-thinning.",
        "btn_axes_reset": "Reset",

        # Library / Save / Load
        "btn_library":    "📚 Examples",
        "btn_save":       "💾 Save",
        "btn_load":       "📂 Open",
        "lib_tutorial":   "Tutorial",
        "lib_article":    "From article (Avvakumov, Kiselev, 2006)",
        "save_dialog":    "Save problem",
        "load_dialog":    "Open problem",
        "json_filter":    "JSON files (*.json)",
        "save_error":     "Save failed: {msg}",
        "load_error":     "Load failed: {msg}",

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
            "Closer to solution = faster convergence.<br><br>"
            "<b>Toolbar buttons:</b><br>"
            "• <b>«📚 Examples»</b> — built-in library: tutorial problems and "
            "examples from the Avvakumov-Kiselev article (2006)<br>"
            "• <b>«📂 Open»</b> — load problem from JSON<br>"
            "• <b>«💾 Save»</b> — save current problem to JSON"
        ),
        "help_params_title": "Parameters Tab",
        "help_params_body": (
            "<b>Inner problem</b> — ODE system integration:<br>"
            "• Method: RK45, Radau, LSODA<br>"
            "• Tolerance: used as both rtol and atol<br><br>"
            "<b>Outer problem</b> — parameter continuation:<br>"
            "• Method: Runge-Kutta 4(5) usually sufficient<br>"
            "• Tolerance: stopping criterion ||Φ(p)|| &lt; tol<br>"
            "• Max iterations: outer iteration limit<br><br>"
            "Tolerance auto-updates when method is changed.<br><br>"
            "<b>Available methods:</b><br>"
            "• <b>Runge-Kutta 4(5) (RK45)</b> — explicit Runge-Kutta of order 4(5) "
            "by Dormand-Prince. Universal, default. Fits most non-stiff problems.<br>"
            "• <b>Radau IIA (Radau)</b> — implicit Runge-Kutta of 5th order with "
            "A-stability. For stiff systems where variables change on very different "
            "time scales.<br>"
            "• <b>LSODA</b> — adaptive Adams-Moulton method, automatically switches "
            "between stiff and non-stiff modes. Use when unsure about the problem's "
            "nature."
        ),
        "help_methods_title": "When to use each method",
        "help_methods_body": (
            "<b>Stiff system</b> — a problem where variables change on very different "
            "time scales (large coefficients of different orders). "
            "Example: chemical kinetics with k₁=10⁶ and k₂=1.<br><br>"
            "<b>Quick recommendations:</b><br>"
            "• <b>RK45</b> — non-stiff problems: mechanics, orbits, oscillations.<br>"
            "• <b>Radau IIA</b> — stiff problems: chemical kinetics, electrical "
            "circuits, problems with sharp transitions.<br>"
            "• <b>LSODA</b> — when unsure about the problem's nature.<br><br>"
            "<b>Tolerance levels:</b><br>"
            "• <b>1e-2 / 1e-3</b> — rough estimate, solution shape<br>"
            "• <b>1e-4 / 1e-6</b> — standard, program default<br>"
            "• <b>1e-8 / 1e-9</b> — high accuracy<br>"
            "• <b>1e-10 / 1e-12</b> — scientific computations<br><br>"
            "<i>Rule: inner tolerance should be tighter than outer.</i>"
        ),
        "help_plot_title": "Plot and Table",
        "help_plot_body": (
            "<b>Plot buttons:</b><br>"
            "• <b>«📐»</b> — phase plane (for n ≥ 2): choose which variables go "
            "on X and Y axes. Single line, no legend.<br>"
            "• <b>«•»</b> — show/hide integrator grid points.<br>"
            "• <b>«🎨»</b> — change line color per variable.<br>"
            "• <b>«📏»</b> — set axes ranges manually. Empty fields = auto. "
            "Useful when autoscale puts the legend on top of the curves.<br><br>"
            "<b>Value table:</b><br>"
            "• Rows are numbered automatically.<br>"
            "• Field <b>«Step Δt»</b> — step in t for an evenly spaced grid. "
            "E.g. with [a, b] = [0, 1] and step 0.1 you get 11 rows. "
            "The step must be ≤ b−a, otherwise it is ignored.<br>"
            "• Empty = auto-thinning of integrator grid nodes to ~50 rows."
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
        "help_json_title": "Creating your own problem",
        "help_json_body": (
            "You can save the current problem to JSON via the «💾 Save» button "
            "and open it later via «📂 Open».<br><br>"
            "You can also create a JSON file manually in any text editor:<br><br>"
            "<pre style='font-size:11px'>"
            "{<br>"
            "&nbsp;&nbsp;\"n\": 2,<br>"
            "&nbsp;&nbsp;\"equations\": [\"x2\", \"0\"],<br>"
            "&nbsp;&nbsp;\"boundary\": [\"xa0\", \"xb0 - 1\"],<br>"
            "&nbsp;&nbsp;\"a\": 0.0,<br>"
            "&nbsp;&nbsp;\"b\": 1.0,<br>"
            "&nbsp;&nbsp;\"t_star\": 0.0,<br>"
            "&nbsp;&nbsp;\"p0\": [0.0, 1.0],<br>"
            "&nbsp;&nbsp;\"inner_method\": \"RK45\",<br>"
            "&nbsp;&nbsp;\"outer_method\": \"RK45\",<br>"
            "&nbsp;&nbsp;\"inner_tol\": \"1e-6\",<br>"
            "&nbsp;&nbsp;\"outer_tol\": \"1e-4\",<br>"
            "&nbsp;&nbsp;\"max_iter\": 10<br>"
            "}"
            "</pre>"
            "<b>Fields:</b><br>"
            "• <b>n</b> — system dimension<br>"
            "• <b>equations</b> — list of n RHS strings ẋ = f(t, x)<br>"
            "• <b>boundary</b> — list of n boundary conditions R = 0<br>"
            "• <b>a, b</b> — integration interval bounds<br>"
            "• <b>t_star</b> — starting point (usually equal to a)<br>"
            "• <b>p0</b> — initial guess for x(t*) of length n<br>"
            "• <b>inner_method, outer_method</b> — RK45, Radau, LSODA<br>"
            "• <b>inner_tol, outer_tol</b> — tolerance as string (e.g., \"1e-6\")<br>"
            "• <b>max_iter</b> — outer iteration limit"
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
