import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.i18n import get, LANGUAGES
from io_manager import Dataset, save, load
from solver import solve_bvp


METHODS = ["RK45", "RK23", "DOP853", "Radau", "BDF", "LSODA"]
COLORS  = ["#2c6fad", "#e05a2b", "#4a8f5f", "#8e44ad", "#c0392b", "#16a085"]

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

        left = ttk.Frame(self.tab_solution, padding=(0, 0, 14, 0), width=310)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        ttk.Separator(self.tab_solution, orient="vertical").pack(side="left", fill="y")

        right = ttk.Frame(self.tab_solution, padding=(14, 0, 0, 0))
        right.pack(side="left", fill="both", expand=True)

        self._build_input_panel(left)
        self._build_output_panel(right)

    def _build_input_panel(self, parent):
        self.lbl_interval = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_interval.pack(anchor="w", pady=(0, 2))

        ab = ttk.Frame(parent)
        ab.pack(fill="x", pady=(0, 10))
        self.entry_a = ttk.Entry(ab, width=8)
        self.entry_a.pack(side="left")
        ttk.Label(ab, text="  —  ").pack(side="left")
        self.entry_b = ttk.Entry(ab, width=8)
        self.entry_b.pack(side="left")

        self.lbl_tstar = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_tstar.pack(anchor="w", pady=(0, 2))
        self.entry_tstar = ttk.Entry(parent, width=18)
        self.entry_tstar.pack(fill="x", pady=(0, 10))

        self.lbl_equations = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_equations.pack(anchor="w")
        self.eq_container, self.eq_rows = self._build_table(parent, self_rows_ref="eq")

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=8)

        self.lbl_boundary = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_boundary.pack(anchor="w")
        self.bc_container, self.bc_rows = self._build_table(parent, self_rows_ref="bc")

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=8)

        self.lbl_p0 = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_p0.pack(anchor="w", pady=(0, 2))
        self.entry_p0 = ttk.Entry(parent, width=30)
        self.entry_p0.pack(fill="x", pady=(0, 12))

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

    def _build_table(self, parent, self_rows_ref=None):
        header = ttk.Frame(parent)
        header.pack(fill="x", pady=(2, 2))

        rows = []
        container = ttk.Frame(parent)
        container.pack(fill="x")

        def on_add():
            if self_rows_ref == "eq":
                self._add_row(self.eq_rows, self.eq_container)
                self._add_row(self.bc_rows, self.bc_container)
            elif self_rows_ref == "bc":
                self._add_row(self.bc_rows, self.bc_container)
                self._add_row(self.eq_rows, self.eq_container)
            else:
                self._add_row(rows, container)

        def on_remove():
            if self_rows_ref == "eq":
                self._remove_row(self.eq_rows)
                self._remove_row(self.bc_rows)
            elif self_rows_ref == "bc":
                self._remove_row(self.bc_rows)
                self._remove_row(self.eq_rows)
            else:
                self._remove_row(rows)

        tk.Button(header, text="+", font=FONT_BOLD, bg=ACCENT, fg=WHITE,
                  relief="flat", padx=8, cursor="hand2",
                  activebackground=ACCENT, activeforeground=WHITE,
                  command=on_add).pack(side="right", padx=2)
        tk.Button(header, text="−", font=FONT_BOLD, bg=GREY, fg=WHITE,
                  relief="flat", padx=8, cursor="hand2",
                  activebackground=GREY, activeforeground=WHITE,
                  command=on_remove).pack(side="right", padx=2)

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

        self.fig = Figure(figsize=(5, 3.5), dpi=96, facecolor=BG)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(WHITE)
        self.ax.tick_params(labelsize=11)
        self.fig.tight_layout(pad=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.lbl_table = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_table.pack(anchor="w", pady=(10, 2))

        self.tree_frame = ttk.Frame(parent)
        self.tree_frame.pack(fill="x")
        self.tree = None

    def _rebuild_tree(self, var_names):
        if self.tree:
            self.tree.destroy()

        cols = ["t"] + var_names
        self.tree = ttk.Treeview(self.tree_frame, columns=cols,
                                  show="headings", height=5)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=max(80, 200 // len(cols)), anchor="center")
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

        self.combo_outer      = row(0, "lbl_outer_method", combobox=True, default="RK45")
        self.combo_inner      = row(1, "lbl_inner_method", combobox=True, default="RK45")
        self.entry_outer_rtol = row(2, "lbl_outer_tol",  default="1e-4")
        self.entry_inner_rtol = row(3, "lbl_inner_tol",  default="1e-6")
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

        photo_path = os.path.join(os.path.dirname(__file__), "..", "images", "IMG_2705 W.jpg")
        try:
            img = Image.open(photo_path)
            img.thumbnail((120, 150))
            self._photo = ImageTk.PhotoImage(img)
            tk.Label(photo_box, image=self._photo, bg="#d0d8e4").place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            tk.Label(photo_box, text="photo", bg="#d0d8e4",
                     font=FONT_SMALL, fg="#888888").place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(inner, text="Дроздов Александр Юрьевич", font=FONT_BOLD).pack()
        ttk.Label(inner, text="Группа 313", font=FONT).pack(pady=(4, 24))

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
    #  Input collection                                                    #
    # ------------------------------------------------------------------ #
    def _collect_input(self):
        if len(self.eq_rows) != len(self.bc_rows):
            raise ValueError(self._t("err_count_mismatch"))

        a      = float(self.entry_a.get())
        b      = float(self.entry_b.get())
        t_star = float(self.entry_tstar.get()) if self.entry_tstar.get().strip() else a
        eqs    = [e.get().strip() for _, e in self.eq_rows]
        bcs    = [e.get().strip() for _, e in self.bc_rows]
        p0     = [float(v.strip()) for v in self.entry_p0.get().split(",")]
        n      = len(eqs)
        vars_  = [f"x{i+1}" for i in range(n)]

        return dict(
            f_strings    = eqs,
            R_strings    = bcs,
            var_names    = vars_,
            t_name       = "t",
            p0           = p0,
            t_span       = (a, b),
            t_star       = t_star,
            inner_method = self.combo_inner.get(),
            outer_method = self.combo_outer.get(),
            inner_rtol   = float(self.entry_inner_rtol.get()),
            inner_atol   = float(self.entry_inner_rtol.get()),
            outer_rtol   = float(self.entry_outer_rtol.get()),
            outer_atol   = float(self.entry_outer_rtol.get()),
            max_iter     = int(self.entry_max_iter.get()),
        ), vars_

    # ------------------------------------------------------------------ #
    #  Solve                                                               #
    # ------------------------------------------------------------------ #
    def _on_solve(self):
        try:
            params, var_names = self._collect_input()
        except ValueError as e:
            messagebox.showerror("", str(e))
            return

        self.lbl_status.config(text=self._t("status_solving"), foreground="#888888")
        self.btn_solve.config(state="disabled")

        def worker():
            try:
                _, t, x = solve_bvp(**params)
                self.root.after(0, lambda: self._update_results(t, x, var_names))
            except Exception as e:
                self.root.after(0, lambda: self._on_error(str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def _update_results(self, t, x, var_names):
        self.ax.clear()
        self.ax.set_facecolor(WHITE)
        self.ax.tick_params(labelsize=11)

        for i, name in enumerate(var_names):
            color = COLORS[i % len(COLORS)]
            self.ax.plot(t, x[i], color=color, linewidth=2, label=name)

        self.ax.legend(fontsize=11)
        self.ax.set_xlabel("t", fontsize=12)
        self.fig.tight_layout(pad=2)
        self.canvas.draw()

        self._rebuild_tree(var_names)
        step = max(1, len(t) // 50)
        for j in range(0, len(t), step):
            row = [f"{t[j]:.4f}"] + [f"{x[i][j]:.6f}" for i in range(len(var_names))]
            self.tree.insert("", "end", values=row)

        self.lbl_status.config(text=self._t("status_done"), foreground=GREEN)
        self.btn_solve.config(state="normal")

    def _on_error(self, msg):
        self.lbl_status.config(text=self._t("status_error", msg=msg), foreground=RED)
        self.btn_solve.config(state="normal")

    # ------------------------------------------------------------------ #
    #  Save / Load                                                         #
    # ------------------------------------------------------------------ #
    def _on_save(self):
        try:
            params, _ = self._collect_input()
        except ValueError as e:
            messagebox.showerror("", str(e))
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")]
        )
        if not path:
            return

        a, b = params["t_span"]
        ds = Dataset(
            equations          = params["f_strings"],
            boundary_conditions= params["R_strings"],
            variables          = params["var_names"],
            t_var              = params["t_name"],
            a=a, b=b,
            t_star             = params["t_star"],
            p0                 = params["p0"],
            inner_method       = params["inner_method"],
            inner_rtol         = params["inner_rtol"],
            inner_atol         = params["inner_atol"],
            outer_method       = params["outer_method"],
            outer_rtol         = params["outer_rtol"],
            outer_atol         = params["outer_atol"],
            max_iter           = params["max_iter"],
        )
        save(ds, path)

    def _on_load(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return

        ds = load(path)

        self.entry_a.delete(0, "end");     self.entry_a.insert(0, str(ds.a))
        self.entry_b.delete(0, "end");     self.entry_b.insert(0, str(ds.b))
        self.entry_tstar.delete(0, "end"); self.entry_tstar.insert(0, str(ds.t_star))
        self.entry_p0.delete(0, "end");    self.entry_p0.insert(0, ", ".join(str(v) for v in ds.p0))

        while len(self.eq_rows) > 1:
            self._remove_row(self.eq_rows)
        while len(self.bc_rows) > 1:
            self._remove_row(self.bc_rows)

        _, e = self.eq_rows[0]; e.delete(0, "end"); e.insert(0, ds.equations[0])
        _, e = self.bc_rows[0]; e.delete(0, "end"); e.insert(0, ds.boundary_conditions[0])

        for eq in ds.equations[1:]:
            self._add_row(self.eq_rows, self.eq_container)
            _, e = self.eq_rows[-1]; e.insert(0, eq)

        for bc in ds.boundary_conditions[1:]:
            self._add_row(self.bc_rows, self.bc_container)
            _, e = self.bc_rows[-1]; e.insert(0, bc)

        self.combo_inner.set(ds.inner_method)
        self.combo_outer.set(ds.outer_method)
        self.entry_inner_rtol.delete(0, "end"); self.entry_inner_rtol.insert(0, str(ds.inner_rtol))
        self.entry_outer_rtol.delete(0, "end"); self.entry_outer_rtol.insert(0, str(ds.outer_rtol))
        self.entry_max_iter.delete(0, "end");   self.entry_max_iter.insert(0, str(ds.max_iter))

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
