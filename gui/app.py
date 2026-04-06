import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.i18n import get, LANGUAGES


METHODS = ["RK45", "RK23", "DOP853", "Radau", "BDF", "LSODA"]

FONT       = ("Segoe UI", 13)
FONT_BOLD  = ("Segoe UI", 13, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SMALL = ("Segoe UI", 11)

BG     = "#f0f4f8"
ACCENT = "#2c6fad"
WHITE  = "#ffffff"
GREEN  = "#4a8f5f"
GREY   = "#757575"
RED    = "#b03020"


class App:
    def __init__(self):
        self.lang = "ru"
        self.root = tk.Tk()
        self._setup_style()
        self._build()

    def _t(self, key, **kwargs):
        return get(self.lang, key, **kwargs)

    def _setup_style(self):
        self.root.title("BVP Solver")
        self.root.geometry("1050x700")
        self.root.minsize(850, 580)
        self.root.configure(bg=BG)

        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure(".",              background=BG,   foreground="#222222", font=FONT)
        s.configure("TFrame",         background=BG)
        s.configure("TLabel",         background=BG,   font=FONT)
        s.configure("TEntry",         font=FONT,       padding=4)
        s.configure("TCombobox",      font=FONT)
        s.configure("TNotebook",      background=BG,   tabmargins=[2, 6, 2, 0])
        s.configure("TNotebook.Tab",  font=FONT,       padding=[14, 6])
        s.configure("Treeview",       font=FONT,       rowheight=28, background=WHITE)
        s.configure("Treeview.Heading", font=FONT_BOLD)
        s.configure("TSeparator",     background="#c8d0da")

    def _btn(self, parent, key, color, command, **kw):
        b = tk.Button(parent, text=self._t(key), font=FONT_BOLD,
                      bg=color, fg=WHITE, relief="flat",
                      padx=14, pady=6, cursor="hand2",
                      activebackground=color, activeforeground=WHITE,
                      command=command, **kw)
        return b

    def _build(self):
        top = ttk.Frame(self.root, padding=(14, 8))
        top.pack(fill="x")

        ttk.Label(top, text="BVP Solver", font=FONT_TITLE).pack(side="left")

        self.lang_btn = tk.Button(top, text="EN", font=FONT_BOLD,
                                   bg=ACCENT, fg=WHITE, relief="flat",
                                   padx=12, pady=4, cursor="hand2",
                                   activebackground=ACCENT, activeforeground=WHITE,
                                   command=self._toggle_lang)
        self.lang_btn.pack(side="right")

        ttk.Separator(self.root, orient="horizontal").pack(fill="x")

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_solution_tab()
        self._build_params_tab()
        self._build_author_tab()
        self._build_help_tab()

        self._refresh_labels()

    # ------------------------------------------------------------------ #
    #  Tab 1 — Solution                                                    #
    # ------------------------------------------------------------------ #
    def _build_solution_tab(self):
        self.tab_solution = ttk.Frame(self.nb, padding=10)
        self.nb.add(self.tab_solution, text="")

        left = ttk.Frame(self.tab_solution, padding=(0, 0, 14, 0))
        left.pack(side="left", fill="y")

        ttk.Separator(self.tab_solution, orient="vertical").pack(side="left", fill="y")

        right = ttk.Frame(self.tab_solution, padding=(14, 0, 0, 0))
        right.pack(side="left", fill="both", expand=True)

        self._build_input_panel(left)
        self._build_output_panel(right)

    def _build_input_panel(self, parent):
        # Interval [a, b]
        self.lbl_interval = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_interval.pack(anchor="w", pady=(0, 2))

        ab = ttk.Frame(parent)
        ab.pack(fill="x", pady=(0, 10))
        self.entry_a = ttk.Entry(ab, width=8)
        self.entry_a.pack(side="left")
        ttk.Label(ab, text="  —  ").pack(side="left")
        self.entry_b = ttk.Entry(ab, width=8)
        self.entry_b.pack(side="left")

        # t*
        self.lbl_tstar = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_tstar.pack(anchor="w", pady=(0, 2))
        self.entry_tstar = ttk.Entry(parent, width=18)
        self.entry_tstar.pack(fill="x", pady=(0, 10))

        # Equations
        self.lbl_equations = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_equations.pack(anchor="w")
        self.eq_container, self.eq_rows = self._build_table(parent)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=8)

        # Boundary conditions
        self.lbl_boundary = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_boundary.pack(anchor="w")
        self.bc_container, self.bc_rows = self._build_table(parent)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=8)

        # p0
        self.lbl_p0 = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_p0.pack(anchor="w", pady=(0, 2))
        self.entry_p0 = ttk.Entry(parent, width=30)
        self.entry_p0.pack(fill="x", pady=(0, 12))

        # Buttons
        btns = ttk.Frame(parent)
        btns.pack(fill="x")

        self.btn_solve = self._btn(btns, "btn_solve", ACCENT, self._on_solve)
        self.btn_solve.pack(side="left", padx=(0, 6))

        self.btn_save = self._btn(btns, "btn_save", GREEN, self._on_save)
        self.btn_save.pack(side="left", padx=(0, 4))

        self.btn_load = self._btn(btns, "btn_load", GREY, self._on_load)
        self.btn_load.pack(side="left")

        self.lbl_status = ttk.Label(parent, font=FONT_SMALL, foreground="#888888")
        self.lbl_status.pack(anchor="w", pady=(6, 0))

    def _build_table(self, parent):
        header = ttk.Frame(parent)
        header.pack(fill="x", pady=(2, 2))

        rows = []

        container = ttk.Frame(parent)
        container.pack(fill="x")

        tk.Button(header, text="+", font=FONT_BOLD, bg=ACCENT, fg=WHITE,
                  relief="flat", padx=8, cursor="hand2",
                  activebackground=ACCENT, activeforeground=WHITE,
                  command=lambda: self._add_row(rows, container)).pack(side="right", padx=2)
        tk.Button(header, text="−", font=FONT_BOLD, bg=GREY, fg=WHITE,
                  relief="flat", padx=8, cursor="hand2",
                  activebackground=GREY, activeforeground=WHITE,
                  command=lambda: self._remove_row(rows)).pack(side="right", padx=2)

        self._add_row(rows, container)
        return container, rows

    def _add_row(self, rows, container):
        idx = len(rows) + 1
        frame = ttk.Frame(container)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=f"{idx}.", width=3).pack(side="left")
        entry = ttk.Entry(frame, font=FONT)
        entry.pack(side="left", fill="x", expand=True)
        rows.append((frame, entry))

    def _remove_row(self, rows):
        if len(rows) <= 1:
            return
        frame, _ = rows.pop()
        frame.destroy()

    def _build_output_panel(self, parent):
        self.lbl_plot = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_plot.pack(anchor="w", pady=(0, 4))

        fig = Figure(figsize=(5, 3.5), dpi=96, facecolor=BG)
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor(WHITE)
        self.ax.tick_params(labelsize=11)
        fig.tight_layout(pad=2)

        self.canvas = FigureCanvasTkAgg(fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.lbl_table = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_table.pack(anchor="w", pady=(10, 2))

        cols = ("t", "x")
        self.tree = ttk.Treeview(parent, columns=cols, show="headings", height=5)
        self.tree.heading("t", text="t")
        self.tree.heading("x", text="x(t)")
        self.tree.column("t", width=110, anchor="center")
        self.tree.column("x", width=220, anchor="center")
        self.tree.pack(fill="x")

    # ------------------------------------------------------------------ #
    #  Tab 2 — Parameters                                                  #
    # ------------------------------------------------------------------ #
    def _build_params_tab(self):
        self.tab_params = ttk.Frame(self.nb, padding=24)
        self.nb.add(self.tab_params, text="")

        def row(r, lbl_attr, combobox=False, default=""):
            lbl = ttk.Label(self.tab_params)
            lbl.grid(row=r, column=0, sticky="w", pady=8, padx=(0, 20))
            setattr(self, lbl_attr, lbl)
            if combobox:
                w = ttk.Combobox(self.tab_params, values=METHODS,
                                  state="readonly", width=14, font=FONT)
                w.set(default)
            else:
                w = ttk.Entry(self.tab_params, width=14, font=FONT)
                w.insert(0, default)
            w.grid(row=r, column=1, sticky="w")
            return w

        self.combo_inner   = row(0, "lbl_inner_method", combobox=True, default="RK45")
        self.combo_outer   = row(1, "lbl_outer_method", combobox=True, default="RK45")
        self.entry_inner_rtol = row(2, "lbl_inner_tol",  default="1e-6")
        self.entry_outer_rtol = row(3, "lbl_outer_tol",  default="1e-4")
        self.entry_max_iter   = row(4, "lbl_max_iter",   default="10")

    # ------------------------------------------------------------------ #
    #  Tab 3 — Author                                                      #
    # ------------------------------------------------------------------ #
    def _build_author_tab(self):
        self.tab_author = ttk.Frame(self.nb, padding=20)
        self.nb.add(self.tab_author, text="")

        inner = ttk.Frame(self.tab_author)
        inner.place(relx=0.5, rely=0.45, anchor="center")

        photo_box = tk.Frame(inner, width=120, height=150,
                              bg="#d0d8e4", relief="groove", bd=2)
        photo_box.pack(pady=(0, 18))
        photo_box.pack_propagate(False)
        tk.Label(photo_box, text="photo", bg="#d0d8e4",
                 font=FONT_SMALL, fg="#888888").place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(inner, text="Иванов Иван Иванович", font=FONT_BOLD).pack()
        ttk.Label(inner, text="Группа 000-000", font=FONT).pack(pady=(4, 24))

        self.btn_exit = tk.Button(inner, font=FONT_BOLD,
                                   bg=RED, fg=WHITE, relief="flat",
                                   padx=24, pady=8, cursor="hand2",
                                   activebackground=RED, activeforeground=WHITE,
                                   command=self.root.quit)
        self.btn_exit.pack()

    # ------------------------------------------------------------------ #
    #  Tab 4 — Help                                                        #
    # ------------------------------------------------------------------ #
    def _build_help_tab(self):
        self.tab_help = ttk.Frame(self.nb, padding=20)
        self.nb.add(self.tab_help, text="")

        self.help_widget = tk.Text(self.tab_help, font=FONT,
                                    bg=WHITE, relief="flat",
                                    wrap="word", state="disabled",
                                    padx=16, pady=16)
        self.help_widget.pack(fill="both", expand=True)

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #
    def _on_solve(self):
        if len(self.eq_rows) != len(self.bc_rows):
            messagebox.showerror("", self._t("err_count_mismatch"))
            return
        self.lbl_status.config(text=self._t("status_solving"))
        self.root.after(50, self._stub_solve)

    def _stub_solve(self):
        self.lbl_status.config(text=self._t("err_not_implemented"))

    def _on_save(self):
        filedialog.asksaveasfilename(defaultextension=".json",
                                      filetypes=[("JSON", "*.json")])

    def _on_load(self):
        filedialog.askopenfilename(filetypes=[("JSON", "*.json")])

    # ------------------------------------------------------------------ #
    #  Language                                                            #
    # ------------------------------------------------------------------ #
    def _toggle_lang(self):
        idx = LANGUAGES.index(self.lang)
        self.lang = LANGUAGES[(idx + 1) % len(LANGUAGES)]
        self._refresh_labels()

    def _refresh_labels(self):
        self.nb.tab(0, text=self._t("tab_solution"))
        self.nb.tab(1, text=self._t("tab_parameters"))
        self.nb.tab(2, text=self._t("tab_author"))
        self.nb.tab(3, text=self._t("tab_help"))

        self.lang_btn.config(text="EN" if self.lang == "ru" else "RU")

        self.lbl_interval.config(text=self._t("interval"))
        self.lbl_tstar.config(text=self._t("t_star"))
        self.lbl_equations.config(text=self._t("equations"))
        self.lbl_boundary.config(text=self._t("boundary"))
        self.lbl_p0.config(text=self._t("p0"))
        self.btn_solve.config(text=self._t("btn_solve"))
        self.btn_save.config(text=self._t("btn_save"))
        self.btn_load.config(text=self._t("btn_load"))
        self.lbl_plot.config(text=self._t("result_plot"))
        self.lbl_table.config(text=self._t("result_table"))

        self.lbl_inner_method.config(text=self._t("inner_method"))
        self.lbl_outer_method.config(text=self._t("outer_method"))
        self.lbl_inner_tol.config(text=self._t("inner_tol"))
        self.lbl_outer_tol.config(text=self._t("outer_tol"))
        self.lbl_max_iter.config(text=self._t("max_iter"))

        self.btn_exit.config(text=self._t("btn_exit"))

        self.help_widget.config(state="normal")
        self.help_widget.delete("1.0", "end")
        self.help_widget.insert("1.0", self._t("help_text"))
        self.help_widget.config(state="disabled")

    def run(self):
        self.root.mainloop()
