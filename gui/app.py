import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.i18n import get, LANGUAGES
from solver import solve_bvp


METHODS = ["RK45", "RK23", "DOP853", "Radau", "BDF", "LSODA"]
COLORS  = ["#3a5fc8", "#e05a2b", "#2a9d60", "#8e44ad", "#c0392b", "#0d8a8a"]

FONT       = ("Segoe UI", 13)
FONT_BOLD  = ("Segoe UI", 13, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SMALL = ("Segoe UI", 11)

BG      = "#f4f6f9"
BG_CARD = "#ffffff"
ACCENT  = "#3a5fc8"
WHITE   = "#ffffff"
GREEN   = "#2a9d60"
GREY    = "#6b7280"
RED     = "#dc3545"
BORDER  = "#d1d5db"
FG      = "#1f2937"


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
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure(".",
                     background=BG, foreground=FG, font=FONT)
        s.configure("TFrame",          background=BG)
        s.configure("Card.TFrame",     background=BG_CARD,
                     relief="flat")
        s.configure("TLabel",          background=BG,     foreground=FG, font=FONT)
        s.configure("Card.TLabel",     background=BG_CARD, foreground=FG, font=FONT)
        s.configure("TEntry",          font=FONT, padding=5,
                     fieldbackground=BG_CARD, foreground=FG,
                     insertwidth=2, insertcolor=FG)
        s.configure("TCombobox",       font=FONT,
                     fieldbackground=BG_CARD, foreground=FG)
        s.configure("TNotebook",       background=BG, tabmargins=[2, 6, 2, 0])
        s.configure("TNotebook.Tab",   font=FONT, padding=[16, 7])
        s.map("TNotebook.Tab",
              background=[("selected", BG_CARD), ("!selected", BG)],
              foreground=[("selected", ACCENT),  ("!selected", GREY)])
        s.configure("Treeview",        font=FONT, rowheight=28,
                     background=BG_CARD, fieldbackground=BG_CARD)
        s.configure("Treeview.Heading", font=FONT_BOLD,
                     background=BG, foreground=FG)
        s.configure("TSeparator",      background=BORDER)

    def _btn(self, parent, key, color, command, small=False, **kw):
        f = FONT if not small else FONT_SMALL
        b = tk.Button(parent, text=self._t(key), font=f,
                      bg=color, fg=FG, relief="solid",
                      padx=14, pady=6, cursor="hand2",
                      activebackground=color, activeforeground=FG,
                      bd=1, highlightthickness=0,
                      highlightbackground=BORDER,
                      command=command, **kw)
        return b

    # ------------------------------------------------------------------ #
    #  Scrollable frame helper                                             #
    # ------------------------------------------------------------------ #
    def _make_scrollable(self, parent, height=160, expand=False):
        outer = ttk.Frame(parent)
        outer.pack(fill="both" if expand else "x", expand=expand)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0, height=height)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)

        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = ttk.Frame(canvas)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_resize(e):
            canvas.itemconfig(win_id, width=e.width)

        def on_configure(_):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_resize)
        inner.bind("<Configure>", on_configure)

        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        inner.bind("<MouseWheel>", on_mousewheel)

        return inner

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #
    def _build(self):
        top = ttk.Frame(self.root, padding=(16, 10), style="TFrame")
        top.configure(style="TFrame")
        top.pack(fill="x")

        ttk.Label(top, text="BVP Solver", font=FONT_TITLE,
                  foreground=ACCENT).pack(side="left")

        close_btn = tk.Button(top, text="✕", font=FONT_BOLD,
                               bg=BG, fg=FG, relief="solid",
                               padx=10, pady=4, cursor="hand2", bd=1,
                               highlightthickness=0, highlightbackground=BORDER,
                               activebackground=BG, activeforeground=FG,
                               command=self.root.quit)
        close_btn.pack(side="right", padx=(6, 0))

        self.lang_btn = tk.Button(top, text="EN", font=FONT_BOLD,
                                   bg=ACCENT, fg=FG, relief="solid",
                                   padx=12, pady=4, cursor="hand2", bd=1,
                                   highlightthickness=0, highlightbackground=BORDER,
                                   activebackground=ACCENT, activeforeground=FG,
                                   command=self._toggle_lang)
        self.lang_btn.pack(side="right")

        tk.Frame(self.root, height=1, bg=BORDER).pack(fill="x")

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
        self.tab_solution = ttk.Frame(self.nb, padding=12)
        self.nb.add(self.tab_solution, text="")

        pane = ttk.PanedWindow(self.tab_solution, orient="horizontal")
        pane.pack(fill="both", expand=True)

        left = ttk.Frame(pane, padding=(0, 0, 8, 0))
        right = ttk.Frame(pane, padding=(8, 0, 0, 0))

        pane.add(left,  weight=1)
        pane.add(right, weight=2)

        def _set_sash():
            w = pane.winfo_width()
            if w > 1:
                pane.sashpos(0, w // 3)
            else:
                self.root.after(20, _set_sash)
        self.root.after(10, _set_sash)

        self._build_input_panel(left)
        self._build_output_panel(right)

    def _build_input_panel(self, parent):
        # Interval
        self.lbl_interval = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_interval.pack(anchor="w", pady=(0, 2))

        ab = ttk.Frame(parent)
        ab.pack(fill="x", pady=(0, 10))
        self.entry_a = ttk.Entry(ab, width=8)
        self.entry_a.pack(side="left")
        ttk.Label(ab, text="  —  ").pack(side="left")
        self.entry_b = ttk.Entry(ab, width=8)
        self.entry_b.pack(side="left")

        tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", pady=6)

        # t*
        tstar_row = ttk.Frame(parent)
        tstar_row.pack(fill="x", pady=(0, 10))
        self.lbl_tstar = ttk.Label(tstar_row, font=FONT_BOLD)
        self.lbl_tstar.pack(side="left", padx=(0, 8))
        self.entry_tstar = ttk.Entry(tstar_row, width=10)
        self.entry_tstar.pack(side="left")

        tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", pady=6)

        # p0 inline
        p0_row = ttk.Frame(parent)
        p0_row.pack(fill="x", pady=(0, 10))
        self.lbl_p0 = ttk.Label(p0_row, font=FONT_BOLD)
        self.lbl_p0.pack(side="left", padx=(0, 8))
        self.entry_p0 = ttk.Entry(p0_row, width=16)
        self.entry_p0.pack(side="left")

        tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", pady=6)

        # Equations + BC table header
        hdr = ttk.Frame(parent)
        hdr.pack(fill="x")
        ttk.Label(hdr, text=" ", width=3).pack(side="left")
        self.lbl_equations = ttk.Label(hdr, font=FONT_BOLD)
        self.lbl_equations.pack(side="left", padx=(0, 30))
        self.lbl_boundary = ttk.Label(hdr, font=FONT_BOLD)
        self.lbl_boundary.pack(side="left")

        self.eq_bc_scroll = self._make_scrollable(parent, height=90, expand=True)
        self.eq_bc_rows = []
        self.eq_bc_container = self.eq_bc_scroll
        self._add_table_row(self.eq_bc_rows, self.eq_bc_container)

        # +/− кнопки
        ctrl_pm = ttk.Frame(parent)
        ctrl_pm.pack(anchor="w", pady=(4, 0))
        ctrl_pm.columnconfigure(0, weight=1)
        ctrl_pm.columnconfigure(1, weight=1)

        def on_add():
            self._add_table_row(self.eq_bc_rows, self.eq_bc_container)

        def on_remove():
            self._remove_table_row(self.eq_bc_rows)

        tk.Button(ctrl_pm, text="+", font=FONT_BOLD, bg=ACCENT, fg=FG,
                  relief="solid", padx=10, cursor="hand2", bd=1,
                  highlightthickness=0, highlightbackground=BORDER,
                  activebackground=ACCENT, activeforeground=FG,
                  command=on_add).grid(row=0, column=0, sticky="ew")
        tk.Button(ctrl_pm, text="−", font=FONT_BOLD, bg=GREY, fg=FG,
                  relief="solid", padx=10, cursor="hand2", bd=1,
                  highlightthickness=0, highlightbackground=BORDER,
                  activebackground=GREY, activeforeground=FG,
                  command=on_remove).grid(row=0, column=1, sticky="ew", padx=(4, 0))

        # Разделитель — полная ширина
        tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", pady=6)

        # Кнопка «Решить» — ширина как у ctrl_pm
        ctrl_solve = tk.Frame(parent, bg=BG)
        ctrl_solve.pack(anchor="w")
        ctrl_solve.pack_propagate(False)

        self.btn_solve = self._btn(ctrl_solve, "btn_solve", ACCENT, self._on_solve)
        self.btn_solve.pack(fill="x", expand=True)

        def _sync_solve():
            w = ctrl_pm.winfo_reqwidth()
            h = ctrl_pm.winfo_reqheight()
            if w > 1:
                ctrl_solve.config(width=w, height=h)
            else:
                self.root.after(20, _sync_solve)
        self.root.after(10, _sync_solve)

        self.lbl_status = ttk.Label(parent, font=FONT_SMALL, foreground=GREY)
        self.lbl_status.pack(anchor="w", pady=(6, 0))

    def _add_table_row(self, rows, container):
        idx = len(rows) + 1
        frame = ttk.Frame(container)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=f"{idx}.", width=3).pack(side="left")
        eq_entry = ttk.Entry(frame, font=FONT, width=14)
        eq_entry.pack(side="left", padx=(0, 30))
        bc_entry = ttk.Entry(frame, font=FONT, width=14)
        bc_entry.pack(side="left")
        rows.append((frame, eq_entry, bc_entry))

    def _remove_table_row(self, rows):
        if len(rows) <= 1:
            return
        frame, _, _ = rows.pop()
        frame.destroy()

    def _build_output_panel(self, parent):
        self.lbl_plot = ttk.Label(parent, font=FONT_BOLD)
        self.lbl_plot.pack(anchor="w", pady=(0, 4))

        self.fig = Figure(figsize=(5, 3.5), dpi=96, facecolor=BG_CARD)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(BG_CARD)
        self.ax.tick_params(labelsize=11, colors=FG)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(BORDER)
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
        self.tab_params = ttk.Frame(self.nb, padding=28)
        self.nb.add(self.tab_params, text="")

        def row(r, lbl_attr, combobox=False, default=""):
            lbl = ttk.Label(self.tab_params, font=FONT)
            lbl.grid(row=r, column=0, sticky="w", pady=10, padx=(0, 24))
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
                              bg=BORDER, relief="flat", bd=1)
        photo_box.pack(pady=(0, 18))
        photo_box.pack_propagate(False)

        photo_path = os.path.join(os.path.dirname(__file__), "..", "images", "IMG_2705 W.jpg")
        try:
            img = Image.open(photo_path)
            img.thumbnail((120, 150))
            self._photo = ImageTk.PhotoImage(img)
            tk.Label(photo_box, image=self._photo, bg=BORDER).place(
                relx=0.5, rely=0.5, anchor="center")
        except Exception:
            tk.Label(photo_box, text="photo", bg=BORDER,
                     font=FONT_SMALL, fg=GREY).place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(inner, text="Дроздов Александр Юрьевич", font=FONT_BOLD).pack()
        ttk.Label(inner, text="Группа 313", font=FONT, foreground=GREY).pack(pady=(4, 0))

    # ------------------------------------------------------------------ #
    #  Tab 4 — Help                                                        #
    # ------------------------------------------------------------------ #
    def _build_help_tab(self):
        self.tab_help = ttk.Frame(self.nb, padding=20)
        self.nb.add(self.tab_help, text="")

        self.help_widget = tk.Text(self.tab_help, font=FONT,
                                    bg=BG_CARD, fg=FG, relief="flat",
                                    wrap="word", state="disabled",
                                    padx=20, pady=16,
                                    insertbackground=FG)
        self.help_widget.pack(fill="both", expand=True)

    # ------------------------------------------------------------------ #
    #  Input collection                                                    #
    # ------------------------------------------------------------------ #
    def _collect_input(self):
        a      = float(self.entry_a.get())
        b      = float(self.entry_b.get())
        t_star = float(self.entry_tstar.get()) if self.entry_tstar.get().strip() else a
        eqs    = [eq_e.get().strip() for _, eq_e, _ in self.eq_bc_rows]
        bcs    = [bc_e.get().strip() for _, _, bc_e in self.eq_bc_rows]
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

        self.lbl_status.config(text=self._t("status_solving"), foreground=GREY)
        self.btn_solve.config(state="disabled")

        def worker():
            try:
                _, t, x = solve_bvp(**params)
                self.root.after(0, lambda: self._update_results(t, x, var_names))
            except Exception as e:
                msg = str(e)
                self.root.after(0, lambda: self._on_error(msg))

        threading.Thread(target=worker, daemon=True).start()

    def _update_results(self, t, x, var_names):
        self.ax.clear()
        self.ax.set_facecolor(BG_CARD)
        self.ax.tick_params(labelsize=11, colors=FG)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(BORDER)

        for i, name in enumerate(var_names):
            self.ax.plot(t, x[i], color=COLORS[i % len(COLORS)],
                         linewidth=2, label=name)

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
        self.lbl_plot.config(text=self._t("result_plot"))
        self.lbl_table.config(text=self._t("result_table"))

        self.lbl_outer_method.config(text=self._t("outer_method"))
        self.lbl_inner_method.config(text=self._t("inner_method"))
        self.lbl_outer_tol.config(text=self._t("outer_tol"))
        self.lbl_inner_tol.config(text=self._t("inner_tol"))
        self.lbl_max_iter.config(text=self._t("max_iter"))

        self.help_widget.config(state="normal")
        self.help_widget.delete("1.0", "end")
        self.help_widget.insert("1.0", self._t("help_text"))
        self.help_widget.config(state="disabled")

    def run(self):
        self.root.mainloop()
