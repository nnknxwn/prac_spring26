import os
import sys
import threading

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QComboBox, QTabWidget,
    QSplitter, QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QScrollArea, QTextEdit, QListView,
    QColorDialog, QFileDialog,
)

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from gui.i18n import get, LANGUAGES
from solver import solve_bvp


METHOD_KEYS = ["RK45", "Radau", "LSODA"]

METHOD_DISPLAY = {
    "ru": {
        "RK45":   "Рунге-Кутта 4(5)",
        "Radau":  "Радо IIA (неявный)",
        "LSODA":  "LSODA (автовыбор)",
    },
    "en": {
        "RK45":   "Runge-Kutta 4(5)",
        "Radau":  "Radau IIA (implicit)",
        "LSODA":  "LSODA (auto-select)",
    },
}

METHOD_TOOLTIPS = {
    "ru": {
        "RK45":   "Явный, нежёсткие задачи. Универсальный выбор.",
        "Radau":  "Неявный. Для жёстких систем.",
        "LSODA":  "Автоматически выбирает между жёстким и нежёстким.",
    },
    "en": {
        "RK45":   "Explicit, non-stiff problems. Universal choice.",
        "Radau":  "Implicit. For stiff systems.",
        "LSODA":  "Auto-selects between stiff and non-stiff.",
    },
}

# Smart defaults: tolerance per method (used as both rtol and atol)
TOLERANCE_OPTIONS = ["1e-2", "1e-3", "1e-4", "1e-6", "1e-8", "1e-9", "1e-10", "1e-12"]

METHOD_DEFAULTS = {
    "RK45":   "1e-6",
    "Radau":  "1e-6",
    "LSODA":  "1e-6",
}

COLORS  = ["#2554d6", "#f97316", "#10b981", "#a855f7", "#ef4444", "#06b6d4"]


LIGHT_COLORS = {
    "bg":                 "#fafafa",
    "topbar":             "#ffffff",
    "card":               "#ffffff",
    "border":             "#e5e7eb",
    "input_border":       "#d1d5db",
    "input_border_hover": "#9ca3af",
    "text":               "#111827",
    "muted":              "#6b7280",
    "field_label":        "#374151",
    "primary":            "#2563eb",
    "primary_hover":      "#1d4ed8",
    "primary_pressed":    "#1e40af",
    "primary_disabled":   "#9ca3af",
    "success":            "#10b981",
    "error":              "#dc2626",
    "top_btn_bg":         "#ffffff",
    "top_btn_hover":      "#f3f4f6",
    "table_header":       "#f9fafb",
    "header_text":        "#374151",
    "grid_line":          "#f3f4f6",
    "selection":          "#dbeafe",
    "scrollbar":          "#d1d5db",
    "scrollbar_hover":    "#9ca3af",
    "photo_placeholder":  "#f3f4f6",
}

DARK_COLORS = {
    "bg":                 "#0f172a",
    "topbar":             "#1e293b",
    "card":               "#1e293b",
    "border":             "#334155",
    "input_border":       "#475569",
    "input_border_hover": "#64748b",
    "text":               "#f1f5f9",
    "muted":              "#94a3b8",
    "field_label":        "#cbd5e1",
    "primary":            "#3b82f6",
    "primary_hover":      "#60a5fa",
    "primary_pressed":    "#2563eb",
    "primary_disabled":   "#475569",
    "success":            "#34d399",
    "error":              "#f87171",
    "top_btn_bg":         "#1e293b",
    "top_btn_hover":      "#334155",
    "table_header":       "#1e293b",
    "header_text":        "#cbd5e1",
    "grid_line":          "#334155",
    "selection":          "#1e3a8a",
    "scrollbar":          "#475569",
    "scrollbar_hover":    "#64748b",
    "photo_placeholder":  "#334155",
}


def _make_stylesheet(c):
    return f"""
QWidget#central, QScrollArea, QScrollArea > QWidget > QWidget {{
    background: {c["bg"]};
}}
QWidget#topbar {{
    background: {c["topbar"]};
}}
QFrame#divider {{
    background: {c["border"]};
    border: none;
}}
QFrame#card {{
    background: {c["card"]};
    border: 1px solid {c["border"]};
    border-radius: 10px;
}}
QLabel#title {{
    color: {c["text"]};
    font-size: 20px;
    font-weight: 700;
    letter-spacing: -0.3px;
}}
QLabel#section {{
    color: {c["text"]};
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.2px;
}}
QLabel#muted {{
    color: {c["muted"]};
    font-size: 12px;
}}
QLabel#fieldLabel {{
    color: {c["field_label"]};
    font-size: 13px;
}}
QLabel#status {{
    color: {c["muted"]};
    font-size: 12px;
}}
QLabel#statusOk {{
    color: {c["success"]};
    font-size: 12px;
    font-weight: 600;
}}
QLabel#statusErr {{
    color: {c["error"]};
    font-size: 12px;
    font-weight: 600;
}}
QLabel#authorName {{
    color: {c["text"]};
    font-size: 18px;
    font-weight: 600;
}}
QLabel#authorGroup {{
    color: {c["muted"]};
    font-size: 14px;
}}
QLabel#photoBox {{
    background: {c["photo_placeholder"]};
    border: 1px solid {c["border"]};
    border-radius: 10px;
}}

QLineEdit, QSpinBox, QComboBox {{
    background: {c["card"]};
    border: 1px solid {c["input_border"]};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    color: {c["text"]};
    min-height: 18px;
}}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {c["primary"]};
}}
QLineEdit:hover, QSpinBox:hover, QComboBox:hover {{
    border: 1px solid {c["input_border_hover"]};
}}
QSpinBox::up-button, QSpinBox::down-button {{
    width: 18px;
}}
QComboBox {{
    padding-right: 28px;
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 24px;
    border: none;
}}
QComboBox::down-arrow {{
    image: none;
    border: none;
}}

QPushButton#primary {{
    background: {c["primary"]};
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 11px 18px;
    font-size: 14px;
    font-weight: 600;
}}
QPushButton#primary:hover {{
    background: {c["primary_hover"]};
}}
QPushButton#primary:pressed {{
    background: {c["primary_pressed"]};
}}
QPushButton#primary:disabled {{
    background: {c["primary_disabled"]};
}}

QPushButton#topBtn {{
    background: {c["top_btn_bg"]};
    color: {c["text"]};
    border: 1px solid {c["input_border"]};
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    min-width: 32px;
}}
QPushButton#topBtn:hover {{
    background: {c["top_btn_hover"]};
    border-color: {c["input_border_hover"]};
}}

QTabWidget::pane {{
    border: none;
    background: {c["bg"]};
    top: -1px;
}}
QTabBar {{
    background: transparent;
}}
QTabBar::tab {{
    background: transparent;
    color: {c["muted"]};
    padding: 11px 18px;
    min-width: 110px;
    font-size: 13px;
    font-weight: 500;
    border: none;
    border-bottom: 2px solid transparent;
    margin-right: 4px;
}}
QTabBar::tab:selected {{
    color: {c["primary"]};
    border-bottom: 2px solid {c["primary"]};
}}
QTabBar::tab:hover:!selected {{
    color: {c["text"]};
}}

QTableWidget {{
    background: {c["card"]};
    border: 1px solid {c["border"]};
    border-radius: 6px;
    gridline-color: {c["grid_line"]};
    font-size: 12px;
    color: {c["text"]};
    alternate-background-color: {c["card"]};
}}
QTableWidget QTableCornerButton::section {{
    background: {c["table_header"]};
    border: none;
    border-right: 1px solid {c["border"]};
    border-bottom: 1px solid {c["border"]};
}}
QTableWidget::item {{
    padding: 6px;
    background: {c["card"]};
    color: {c["text"]};
}}
QHeaderView {{
    background: {c["table_header"]};
    border: none;
}}
QHeaderView::section {{
    background: {c["table_header"]};
    color: {c["header_text"]};
    border: none;
    border-right: 1px solid {c["border"]};
    border-bottom: 1px solid {c["border"]};
    padding: 8px;
    font-weight: 600;
    font-size: 12px;
}}
QHeaderView::section:last {{
    border-right: none;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {c["scrollbar"]};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {c["scrollbar_hover"]};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QTextEdit#help {{
    background: transparent;
    border: none;
    color: {c["text"]};
    font-size: 13px;
    selection-background-color: {c["selection"]};
}}

QMenu {{
    background-color: {c["card"]};
    color: {c["text"]};
    border: 1px solid {c["border"]};
    border-radius: 8px;
    padding: 4px;
}}
QMenu::item {{
    background: transparent;
    padding: 6px 14px 6px 10px;
    border-radius: 6px;
    margin: 2px 4px;
}}
QMenu::icon {{
    padding-left: 6px;
    padding-right: 4px;
}}
QMenu::item:selected {{
    background-color: {c["primary"]};
    color: #ffffff;
}}
QMenu::separator {{
    height: 1px;
    background: {c["border"]};
    margin: 4px 8px;
}}
QMenu::right-arrow {{
    width: 10px;
    height: 10px;
    margin-right: 6px;
}}
"""


class MainWindow(QMainWindow):
    solve_done = pyqtSignal(object, object, list, object)
    solve_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.lang = "ru"
        self.theme = "light"
        self._colors = LIGHT_COLORS
        self._last_result = None
        self._last_dense = None
        self._custom_colors = list(COLORS)  # mutable copy of plot colors
        self._status_key = None
        self._status_kwargs = {}
        self._status_object_name = "status"
        self._show_markers = False
        self._phase_mode = False
        self._phase_x_idx = 0
        self._phase_y_idx = 1
        self.eq_entries = []
        self.bc_entries = []
        self.p0_entries = []
        self._build()
        self.solve_done.connect(self._update_results)
        self.solve_error.connect(self._on_error)
        self._sync_n_fields(2)
        self._refresh_labels()
        self._apply_theme()

    def _t(self, key, **kwargs):
        return get(self.lang, key, **kwargs)

    # ------------------------------------------------------------------ #
    #  Build root                                                          #
    # ------------------------------------------------------------------ #
    def _build(self):
        self.setWindowTitle("BVP Solver")
        self.resize(1350, 850)
        self.setMinimumSize(1000, 660)

        font = QApplication.instance().font()
        font.setPointSize(13)
        QApplication.instance().setFont(font)

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_topbar())
        root.addWidget(self._hline())

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_solution_tab(), "")
        self.tabs.addTab(self._build_params_tab(), "")
        self.tabs.addTab(self._build_author_tab(), "")
        self.tabs.addTab(self._build_help_tab(), "")
        root.addWidget(self.tabs, stretch=1)

    def _hline(self):
        line = QFrame()
        line.setObjectName("divider")
        line.setFixedHeight(1)
        return line

    def _card(self):
        card = QFrame()
        card.setObjectName("card")
        return card

    # ------------------------------------------------------------------ #
    #  Topbar                                                              #
    # ------------------------------------------------------------------ #
    def _build_topbar(self):
        bar = QWidget()
        bar.setObjectName("topbar")
        bar.setFixedHeight(56)

        h = QHBoxLayout(bar)
        h.setContentsMargins(24, 0, 18, 0)
        h.setSpacing(10)

        title = QLabel("BVP Solver")
        title.setObjectName("title")
        self.lbl_app_title = title
        h.addWidget(title)

        h.addStretch()

        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setObjectName("topBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setToolTip("Theme")
        self.theme_btn.clicked.connect(self._toggle_theme)
        h.addWidget(self.theme_btn)

        self.lang_btn = QPushButton("EN")
        self.lang_btn.setObjectName("topBtn")
        self.lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lang_btn.clicked.connect(self._toggle_lang)
        h.addWidget(self.lang_btn)

        return bar

    # ------------------------------------------------------------------ #
    #  Tab 1 — Solution                                                    #
    # ------------------------------------------------------------------ #
    def _build_solution_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        v.setContentsMargins(20, 16, 20, 18)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(10)
        splitter.setChildrenCollapsible(False)

        splitter.addWidget(self._build_input_panel())
        splitter.addWidget(self._build_output_panel())
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([400, 800])

        v.addWidget(splitter)
        return tab

    def _build_input_panel(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setMinimumWidth(360)

        inner = QWidget()
        v = QVBoxLayout(inner)
        v.setContentsMargins(0, 0, 6, 0)
        v.setSpacing(12)

        # ---- Dimension card ----
        dim_card = self._card()
        dv = QVBoxLayout(dim_card)
        dv.setContentsMargins(16, 14, 16, 14)
        dv.setSpacing(8)

        self.lbl_dimension = QLabel()
        self.lbl_dimension.setObjectName("section")
        dv.addWidget(self.lbl_dimension)

        n_row = QHBoxLayout()
        n_row.setContentsMargins(0, 0, 0, 0)
        n_row.setSpacing(8)
        n_lbl = QLabel("n")
        n_lbl.setObjectName("muted")
        n_lbl.setFixedWidth(48)
        n_lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.spin_n = QSpinBox()
        self.spin_n.setRange(1, 10)
        self.spin_n.setValue(2)
        self.spin_n.setFixedWidth(90)
        self.spin_n.valueChanged.connect(self._sync_n_fields)
        n_row.addWidget(n_lbl)
        n_row.addWidget(self.spin_n)
        n_row.addStretch()
        dv.addLayout(n_row)
        v.addWidget(dim_card)

        # ---- Equations card ----
        self.eq_card = self._card()
        eqv = QVBoxLayout(self.eq_card)
        eqv.setContentsMargins(16, 14, 16, 14)
        eqv.setSpacing(8)

        self.lbl_equations = QLabel()
        self.lbl_equations.setObjectName("section")
        eqv.addWidget(self.lbl_equations)

        self.eq_layout = QVBoxLayout()
        self.eq_layout.setSpacing(6)
        eqv.addLayout(self.eq_layout)
        v.addWidget(self.eq_card)

        # ---- Boundary conditions card ----
        self.bc_card = self._card()
        bcv = QVBoxLayout(self.bc_card)
        bcv.setContentsMargins(16, 14, 16, 14)
        bcv.setSpacing(8)

        self.lbl_boundary = QLabel()
        self.lbl_boundary.setObjectName("section")
        bcv.addWidget(self.lbl_boundary)

        self.bc_layout = QVBoxLayout()
        self.bc_layout.setSpacing(6)
        bcv.addLayout(self.bc_layout)
        v.addWidget(self.bc_card)

        # ---- Interval + t* card ----
        int_card = self._card()
        iv = QVBoxLayout(int_card)
        iv.setContentsMargins(16, 14, 16, 14)
        iv.setSpacing(8)

        self.lbl_interval = QLabel()
        self.lbl_interval.setObjectName("section")
        iv.addWidget(self.lbl_interval)

        ab_row = QHBoxLayout()
        ab_row.setContentsMargins(0, 0, 0, 0)
        ab_row.setSpacing(8)
        a_lbl = QLabel("a")
        a_lbl.setObjectName("muted")
        a_lbl.setFixedWidth(48)
        a_lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.entry_a = QLineEdit("0")
        b_lbl = QLabel("b")
        b_lbl.setObjectName("muted")
        b_lbl.setFixedWidth(20)
        b_lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.entry_b = QLineEdit("1")
        ab_row.addWidget(a_lbl)
        ab_row.addWidget(self.entry_a, stretch=1)
        ab_row.addWidget(b_lbl)
        ab_row.addWidget(self.entry_b, stretch=1)
        iv.addLayout(ab_row)

        self.lbl_tstar = QLabel()
        self.lbl_tstar.setObjectName("section")
        iv.addWidget(self.lbl_tstar)

        tstar_row = QHBoxLayout()
        tstar_row.setContentsMargins(0, 0, 0, 0)
        tstar_row.setSpacing(8)
        tstar_spacer = QLabel("")
        tstar_spacer.setFixedWidth(48)
        self.entry_tstar = QLineEdit("0")
        tstar_row.addWidget(tstar_spacer)
        tstar_row.addWidget(self.entry_tstar, stretch=1)
        iv.addLayout(tstar_row)
        v.addWidget(int_card)

        # ---- p0 card ----
        self.p0_card = self._card()
        pv = QVBoxLayout(self.p0_card)
        pv.setContentsMargins(16, 14, 16, 14)
        pv.setSpacing(8)

        self.lbl_p0 = QLabel()
        self.lbl_p0.setObjectName("section")
        pv.addWidget(self.lbl_p0)

        self.p0_layout = QVBoxLayout()
        self.p0_layout.setSpacing(6)
        pv.addLayout(self.p0_layout)
        v.addWidget(self.p0_card)

        # ---- Library / Save / Load row ----
        toolbar_row = QHBoxLayout()
        toolbar_row.setSpacing(8)

        self.btn_library = QPushButton()
        self.btn_library.setObjectName("topBtn")
        self.btn_library.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_library.setMinimumHeight(34)
        self.btn_library.clicked.connect(self._show_library_menu)

        self.btn_save = QPushButton()
        self.btn_save.setObjectName("topBtn")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setMinimumHeight(34)
        self.btn_save.clicked.connect(self._on_save)

        self.btn_load = QPushButton()
        self.btn_load.setObjectName("topBtn")
        self.btn_load.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_load.setMinimumHeight(34)
        self.btn_load.clicked.connect(self._on_load)

        toolbar_row.addWidget(self.btn_library, stretch=1)
        toolbar_row.addWidget(self.btn_load,    stretch=1)
        toolbar_row.addWidget(self.btn_save,    stretch=1)
        v.addLayout(toolbar_row)

        # ---- Solve button + status ----
        self.btn_solve = QPushButton()
        self.btn_solve.setObjectName("primary")
        self.btn_solve.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_solve.setMinimumHeight(42)
        self.btn_solve.clicked.connect(self._on_solve)
        v.addWidget(self.btn_solve)

        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("status")
        v.addWidget(self.lbl_status)

        v.addStretch()
        scroll.setWidget(inner)
        return scroll

    def _build_output_panel(self):
        panel = QWidget()
        v = QVBoxLayout(panel)
        v.setContentsMargins(6, 0, 0, 0)
        v.setSpacing(12)

        # Plot card
        plot_card = self._card()
        pv = QVBoxLayout(plot_card)
        pv.setContentsMargins(16, 14, 16, 14)
        pv.setSpacing(8)

        plot_header = QHBoxLayout()
        self.lbl_plot = QLabel()
        self.lbl_plot.setObjectName("section")
        plot_header.addWidget(self.lbl_plot)
        plot_header.addStretch()

        self.btn_phase = QPushButton("📐")
        self.btn_phase.setObjectName("topBtn")
        self.btn_phase.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_phase.setCheckable(True)
        self.btn_phase.setChecked(False)
        self.btn_phase.clicked.connect(self._toggle_phase)
        plot_header.addWidget(self.btn_phase)

        self.lbl_phase_x = QLabel("X:")
        self.lbl_phase_x.setObjectName("muted")
        self.lbl_phase_x.setVisible(False)
        plot_header.addWidget(self.lbl_phase_x)
        self.combo_phase_x = QComboBox()
        self.combo_phase_x.setFixedWidth(80)
        self.combo_phase_x.setFixedHeight(30)
        self.combo_phase_x.setVisible(False)
        self.combo_phase_x.currentIndexChanged.connect(self._on_phase_axis_changed)
        plot_header.addWidget(self.combo_phase_x)

        self.lbl_phase_y = QLabel("Y:")
        self.lbl_phase_y.setObjectName("muted")
        self.lbl_phase_y.setVisible(False)
        plot_header.addWidget(self.lbl_phase_y)
        self.combo_phase_y = QComboBox()
        self.combo_phase_y.setFixedWidth(80)
        self.combo_phase_y.setFixedHeight(30)
        self.combo_phase_y.setVisible(False)
        self.combo_phase_y.currentIndexChanged.connect(self._on_phase_axis_changed)
        plot_header.addWidget(self.combo_phase_y)

        self.btn_markers = QPushButton("•")
        self.btn_markers.setObjectName("topBtn")
        self.btn_markers.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_markers.setToolTip("Show/hide grid points")
        self.btn_markers.setCheckable(True)
        self.btn_markers.setChecked(False)
        self.btn_markers.clicked.connect(self._toggle_markers)
        plot_header.addWidget(self.btn_markers)

        self.btn_colors = QPushButton("🎨")
        self.btn_colors.setObjectName("topBtn")
        self.btn_colors.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_colors.setToolTip("Colors")
        self.btn_colors.clicked.connect(self._show_color_menu)
        plot_header.addWidget(self.btn_colors)

        self.btn_axes = QPushButton("📏")
        self.btn_axes.setObjectName("topBtn")
        self.btn_axes.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_axes.setCheckable(True)
        self.btn_axes.setChecked(False)
        self.btn_axes.clicked.connect(self._toggle_axes_row)
        plot_header.addWidget(self.btn_axes)
        pv.addLayout(plot_header)

        # Axes range row (hidden by default)
        self.axes_row_widget = QWidget()
        axes_row = QHBoxLayout(self.axes_row_widget)
        axes_row.setContentsMargins(0, 0, 0, 0)
        axes_row.setSpacing(8)

        self.lbl_axes_x = QLabel("X:")
        self.lbl_axes_x.setObjectName("muted")
        axes_row.addWidget(self.lbl_axes_x)
        self.entry_xmin = QLineEdit()
        self.entry_xmin.setFixedWidth(80)
        self.entry_xmin.editingFinished.connect(self._on_axes_changed)
        axes_row.addWidget(self.entry_xmin)
        self.lbl_axes_dash_x = QLabel("—")
        self.lbl_axes_dash_x.setObjectName("muted")
        axes_row.addWidget(self.lbl_axes_dash_x)
        self.entry_xmax = QLineEdit()
        self.entry_xmax.setFixedWidth(80)
        self.entry_xmax.editingFinished.connect(self._on_axes_changed)
        axes_row.addWidget(self.entry_xmax)

        axes_row.addSpacing(16)

        self.lbl_axes_y = QLabel("Y:")
        self.lbl_axes_y.setObjectName("muted")
        axes_row.addWidget(self.lbl_axes_y)
        self.entry_ymin = QLineEdit()
        self.entry_ymin.setFixedWidth(80)
        self.entry_ymin.editingFinished.connect(self._on_axes_changed)
        axes_row.addWidget(self.entry_ymin)
        self.lbl_axes_dash_y = QLabel("—")
        self.lbl_axes_dash_y.setObjectName("muted")
        axes_row.addWidget(self.lbl_axes_dash_y)
        self.entry_ymax = QLineEdit()
        self.entry_ymax.setFixedWidth(80)
        self.entry_ymax.editingFinished.connect(self._on_axes_changed)
        axes_row.addWidget(self.entry_ymax)

        self.btn_axes_reset = QPushButton()
        self.btn_axes_reset.setObjectName("topBtn")
        self.btn_axes_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_axes_reset.clicked.connect(self._on_axes_reset)
        axes_row.addWidget(self.btn_axes_reset)

        axes_row.addStretch()
        self.axes_row_widget.setVisible(False)
        pv.addWidget(self.axes_row_widget)

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self._style_axes()
        self.fig.tight_layout(pad=1.5)

        self.canvas = FigureCanvasQTAgg(self.fig)
        pv.addWidget(self.canvas, stretch=1)
        v.addWidget(plot_card, stretch=2)

        # Table card
        tbl_card = self._card()
        tv = QVBoxLayout(tbl_card)
        tv.setContentsMargins(16, 14, 16, 14)
        tv.setSpacing(8)

        tbl_header = QHBoxLayout()
        self.lbl_table = QLabel()
        self.lbl_table.setObjectName("section")
        tbl_header.addWidget(self.lbl_table)
        tbl_header.addStretch()
        self.lbl_table_step = QLabel()
        self.lbl_table_step.setObjectName("muted")
        tbl_header.addWidget(self.lbl_table_step)
        self.entry_table_step = QLineEdit()
        self.entry_table_step.setFixedWidth(90)
        self.entry_table_step.editingFinished.connect(self._on_table_step_changed)
        tbl_header.addWidget(self.entry_table_step)
        tv.addLayout(tbl_header)

        self.table = QTableWidget(0, 1)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setAlternatingRowColors(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setMinimumHeight(160)
        tv.addWidget(self.table, stretch=1)
        v.addWidget(tbl_card, stretch=1)

        return panel

    def _style_axes(self):
        c = self._colors
        self.fig.set_facecolor(c["card"])
        self.ax.set_facecolor(c["card"])
        self.ax.tick_params(labelsize=10, colors=c["field_label"])
        for spine in self.ax.spines.values():
            spine.set_edgecolor(c["border"])
        self.ax.grid(True, color=c["grid_line"], linewidth=0.8)
        self.ax.axhline(0, color=c["muted"], linewidth=0.9, zorder=1)
        self.ax.axvline(0, color=c["muted"], linewidth=0.9, zorder=1)

    # ------------------------------------------------------------------ #
    #  Dynamic n-fields                                                    #
    # ------------------------------------------------------------------ #
    def _sync_n_fields(self, n=None):
        if n is None:
            n = self.spin_n.value()

        self._adjust_rows(self.eq_entries, self.eq_layout, n,
                          lambda i: f"x{i+1}' =", default="")
        self._adjust_rows(self.bc_entries, self.bc_layout, n,
                          lambda i: f"R{i+1} =", default="")
        self._adjust_rows(self.p0_entries, self.p0_layout, n,
                          lambda i: f"p{i+1}₀ =", default="0")
        self._setup_tab_order()

    def _setup_tab_order(self):
        """Set logical tab order: n → equations → boundary → a → b → t* → p0 → solve."""
        widgets = [self.spin_n]
        for _, entry in self.eq_entries:
            widgets.append(entry)
        for _, entry in self.bc_entries:
            widgets.append(entry)
        widgets.append(self.entry_a)
        widgets.append(self.entry_b)
        widgets.append(self.entry_tstar)
        for _, entry in self.p0_entries:
            widgets.append(entry)
        widgets.append(self.btn_solve)
        for i in range(len(widgets) - 1):
            QWidget.setTabOrder(widgets[i], widgets[i + 1])

    def _adjust_rows(self, entries, layout, n, label_fn, default):
        while len(entries) < n:
            i = len(entries)
            row_w = QWidget()
            row = QHBoxLayout(row_w)
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)

            lbl = QLabel(label_fn(i))
            lbl.setObjectName("muted")
            lbl.setFixedWidth(48)
            lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

            entry = QLineEdit()
            if default:
                entry.setText(default)

            row.addWidget(lbl)
            row.addWidget(entry, stretch=1)
            layout.addWidget(row_w)
            entries.append((row_w, entry))

        while len(entries) > n:
            row_w, _ = entries.pop()
            row_w.setParent(None)
            row_w.deleteLater()

    # ------------------------------------------------------------------ #
    #  Tab 2 — Parameters                                                  #
    # ------------------------------------------------------------------ #
    def _build_params_tab(self):
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        outer = QVBoxLayout(content)
        outer.setContentsMargins(40, 30, 40, 30)
        outer.setSpacing(20)

        # ---- Inner problem card ----
        inner_card = self._card()
        iv = QVBoxLayout(inner_card)
        iv.setContentsMargins(28, 22, 28, 22)
        iv.setSpacing(6)

        self.lbl_inner_title = QLabel()
        self.lbl_inner_title.setObjectName("section")
        iv.addWidget(self.lbl_inner_title)

        self.lbl_inner_desc = QLabel()
        self.lbl_inner_desc.setObjectName("muted")
        iv.addWidget(self.lbl_inner_desc)

        iv.addSpacing(10)

        ig = QGridLayout()
        ig.setHorizontalSpacing(24)
        ig.setVerticalSpacing(14)
        ig.setColumnMinimumWidth(0, 260)

        self.lbl_inner_method = QLabel()
        self.lbl_inner_method.setObjectName("fieldLabel")
        self.lbl_inner_method.setFixedWidth(260)
        self.combo_inner = QComboBox()
        self.combo_inner.setFixedWidth(280)
        self.combo_inner.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.combo_inner.currentIndexChanged.connect(
            lambda idx: self._on_method_changed("inner"))

        self.lbl_inner_tol = QLabel()
        self.lbl_inner_tol.setObjectName("fieldLabel")
        self.lbl_inner_tol.setFixedWidth(260)
        self.combo_inner_tol = QComboBox()
        self.combo_inner_tol.addItems(TOLERANCE_OPTIONS)
        self.combo_inner_tol.setCurrentText("1e-6")
        self.combo_inner_tol.setFixedWidth(280)

        ig.addWidget(self.lbl_inner_method, 0, 0, Qt.AlignmentFlag.AlignVCenter)
        ig.addWidget(self.combo_inner,      0, 1, Qt.AlignmentFlag.AlignVCenter)
        ig.addWidget(self.lbl_inner_tol,    1, 0, Qt.AlignmentFlag.AlignVCenter)
        ig.addWidget(self.combo_inner_tol,  1, 1, Qt.AlignmentFlag.AlignVCenter)
        ig.setColumnStretch(2, 1)

        iv.addLayout(ig)
        outer.addWidget(inner_card)

        # ---- Outer problem card ----
        outer_card = self._card()
        ov = QVBoxLayout(outer_card)
        ov.setContentsMargins(28, 22, 28, 22)
        ov.setSpacing(6)

        self.lbl_outer_title = QLabel()
        self.lbl_outer_title.setObjectName("section")
        ov.addWidget(self.lbl_outer_title)

        self.lbl_outer_desc = QLabel()
        self.lbl_outer_desc.setObjectName("muted")
        ov.addWidget(self.lbl_outer_desc)

        ov.addSpacing(10)

        og = QGridLayout()
        og.setHorizontalSpacing(24)
        og.setVerticalSpacing(14)
        og.setColumnMinimumWidth(0, 260)

        self.lbl_outer_method = QLabel()
        self.lbl_outer_method.setObjectName("fieldLabel")
        self.lbl_outer_method.setFixedWidth(260)
        self.combo_outer = QComboBox()
        self.combo_outer.setFixedWidth(280)
        self.combo_outer.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.combo_outer.currentIndexChanged.connect(
            lambda idx: self._on_method_changed("outer"))

        self.lbl_outer_tol = QLabel()
        self.lbl_outer_tol.setObjectName("fieldLabel")
        self.lbl_outer_tol.setFixedWidth(260)
        self.combo_outer_tol = QComboBox()
        self.combo_outer_tol.addItems(TOLERANCE_OPTIONS)
        self.combo_outer_tol.setCurrentText("1e-4")
        self.combo_outer_tol.setFixedWidth(280)

        self.lbl_max_iter = QLabel()
        self.lbl_max_iter.setObjectName("fieldLabel")
        self.lbl_max_iter.setFixedWidth(260)
        self.entry_max_iter = QLineEdit("10")
        self.entry_max_iter.setFixedWidth(280)

        og.addWidget(self.lbl_outer_method, 0, 0, Qt.AlignmentFlag.AlignVCenter)
        og.addWidget(self.combo_outer,      0, 1, Qt.AlignmentFlag.AlignVCenter)
        og.addWidget(self.lbl_outer_tol,    1, 0, Qt.AlignmentFlag.AlignVCenter)
        og.addWidget(self.combo_outer_tol,  1, 1, Qt.AlignmentFlag.AlignVCenter)
        og.addWidget(self.lbl_max_iter,     2, 0, Qt.AlignmentFlag.AlignVCenter)
        og.addWidget(self.entry_max_iter,   2, 1, Qt.AlignmentFlag.AlignVCenter)
        og.setColumnStretch(2, 1)

        ov.addLayout(og)
        outer.addWidget(outer_card)

        outer.addStretch()
        scroll.setWidget(content)

        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        return tab

    def _populate_method_combos(self):
        """Fill method combo boxes with localized display names and tooltips."""
        display = METHOD_DISPLAY[self.lang]
        tooltips = METHOD_TOOLTIPS[self.lang]
        for combo in (self.combo_inner, self.combo_outer):
            current_key = METHOD_KEYS[combo.currentIndex()] if combo.count() > 0 else "RK45"
            combo.blockSignals(True)
            combo.clear()
            for key in METHOD_KEYS:
                combo.addItem(display[key], key)
            combo.setCurrentIndex(METHOD_KEYS.index(current_key))
            combo.blockSignals(False)
            # Set tooltip for each item in the dropdown
            for i, key in enumerate(METHOD_KEYS):
                combo.setItemData(i, tooltips[key], Qt.ItemDataRole.ToolTipRole)
            # Set combo tooltip to current selection
            combo.setToolTip(tooltips[current_key])

    def _on_method_changed(self, which):
        """Apply smart defaults when method changes."""
        if which == "inner":
            combo = self.combo_inner
            tol_combo = self.combo_inner_tol
        else:
            combo = self.combo_outer
            tol_combo = self.combo_outer_tol

        key = combo.currentData()
        if key and key in METHOD_DEFAULTS:
            default_tol = METHOD_DEFAULTS[key]
            if default_tol in TOLERANCE_OPTIONS:
                tol_combo.setCurrentIndex(TOLERANCE_OPTIONS.index(default_tol))
        if key and key in METHOD_TOOLTIPS.get(self.lang, {}):
            combo.setToolTip(METHOD_TOOLTIPS[self.lang][key])

    # ------------------------------------------------------------------ #
    #  Tab 3 — Author                                                      #
    # ------------------------------------------------------------------ #
    def _build_author_tab(self):
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addStretch(1)

        center = QWidget()
        cl = QVBoxLayout(center)
        cl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        cl.setSpacing(14)

        photo_path = os.path.join(os.path.dirname(__file__), "..", "images", "IMG_2705 W.jpg")
        photo_lbl = QLabel()
        photo_lbl.setObjectName("photoBox")
        photo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_lbl.setFixedSize(240, 300)
        if os.path.exists(photo_path):
            pix = QPixmap(photo_path).scaled(
                240, 300,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            photo_lbl.setPixmap(pix)
            photo_lbl.setScaledContents(False)
        cl.addWidget(photo_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        name_lbl = QLabel("Дроздов Александр Юрьевич")
        name_lbl.setObjectName("authorName")
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cl.addWidget(name_lbl)

        group_lbl = QLabel("Группа 313")
        group_lbl.setObjectName("authorGroup")
        group_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cl.addWidget(group_lbl)

        outer.addWidget(center, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch(1)
        return tab

    # ------------------------------------------------------------------ #
    #  Tab 4 — Help                                                        #
    # ------------------------------------------------------------------ #
    def _build_help_tab(self):
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setContentsMargins(20, 20, 20, 20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        cv = QVBoxLayout(content)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(16)

        # We'll create multiple cards for each help section
        self._help_cards = []
        section_keys = [
            "help_intro", "help_input", "help_params",
            "help_methods", "help_plot", "help_example", "help_json", "help_shortcuts"
        ]
        for key in section_keys:
            card = self._card()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(24, 20, 24, 20)
            card_layout.setSpacing(8)

            title_lbl = QLabel()
            title_lbl.setObjectName("section")
            card_layout.addWidget(title_lbl)

            body_lbl = QLabel()
            body_lbl.setObjectName("fieldLabel")
            body_lbl.setWordWrap(True)
            body_lbl.setTextFormat(Qt.TextFormat.RichText)
            card_layout.addWidget(body_lbl)

            cv.addWidget(card)
            self._help_cards.append((key, title_lbl, body_lbl))

        cv.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)
        return tab

    # ------------------------------------------------------------------ #
    #  Input collection                                                    #
    # ------------------------------------------------------------------ #
    def _collect_input(self):
        a      = float(self.entry_a.text())
        b      = float(self.entry_b.text())
        t_star = float(self.entry_tstar.text()) if self.entry_tstar.text().strip() else a
        eqs    = [e.text().strip() for _, e in self.eq_entries]
        bcs    = [e.text().strip() for _, e in self.bc_entries]
        p0     = [float(e.text().strip()) for _, e in self.p0_entries]
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
            inner_method = self.combo_inner.currentData(),
            outer_method = self.combo_outer.currentData(),
            inner_rtol   = float(self.combo_inner_tol.currentText()),
            inner_atol   = float(self.combo_inner_tol.currentText()),
            outer_rtol   = float(self.combo_outer_tol.currentText()),
            outer_atol   = float(self.combo_outer_tol.currentText()),
            max_iter     = int(self.entry_max_iter.text()),
        ), vars_

    # ------------------------------------------------------------------ #
    #  Solve                                                               #
    # ------------------------------------------------------------------ #
    def _on_solve(self):
        try:
            params, var_names = self._collect_input()
        except ValueError as e:
            QMessageBox.critical(self, "", str(e))
            return

        self._set_status(self._t("status_solving"), "status", key="status_solving")
        self.btn_solve.setEnabled(False)

        def worker():
            try:
                _, t, x, sol_dense = solve_bvp(**params)
                self.solve_done.emit(t, x, var_names, sol_dense)
            except Exception as e:
                self.solve_error.emit(str(e))

        threading.Thread(target=worker, daemon=True).start()

    def _update_results(self, t, x, var_names, sol_dense):
        self._last_result = (t, x, var_names)
        self._last_dense = sol_dense
        self._update_phase_combos(var_names)
        self._draw_plot(t, x, var_names)
        self._fill_table(t, x, var_names)
        self._set_status(self._t("status_done"), "statusOk", key="status_done")
        self.btn_solve.setEnabled(True)

    def _draw_plot(self, t, x, var_names):
        c = self._colors
        self.ax.clear()
        self._style_axes()

        if self._phase_mode and len(var_names) >= 2:
            ix = min(self._phase_x_idx, len(var_names) - 1)
            iy = min(self._phase_y_idx, len(var_names) - 1)
            color = self._custom_colors[0]
            marker = 'o' if self._show_markers else None
            ms = 4 if self._show_markers else None
            self.ax.plot(x[ix], x[iy], color=color, linewidth=2,
                         marker=marker, markersize=ms,
                         markerfacecolor=color, markeredgecolor=color)
            self.ax.set_xlabel(var_names[ix], fontsize=11, color=c["field_label"])
            self.ax.set_ylabel(var_names[iy], fontsize=11, color=c["field_label"])
        else:
            for i, name in enumerate(var_names):
                color = self._custom_colors[i % len(self._custom_colors)]
                marker = 'o' if self._show_markers else None
                ms = 4 if self._show_markers else None
                self.ax.plot(t, x[i], color=color, linewidth=2, label=name,
                             marker=marker, markersize=ms, markerfacecolor=color,
                             markeredgecolor=color)

            legend = self.ax.legend(fontsize=10, frameon=False)
            if legend:
                for txt in legend.get_texts():
                    txt.set_color(c["text"])
            self.ax.set_xlabel("t", fontsize=11, color=c["field_label"])
            self.ax.set_ylabel("x(t)", fontsize=11, color=c["field_label"])
        self._apply_axes_limits()
        self.fig.tight_layout(pad=1.5)
        self.canvas.draw()

    def _apply_axes_limits(self):
        """Apply user-specified axes limits if any are set; otherwise leave autoscale."""
        def _parse(le):
            txt = le.text().strip().replace(",", ".")
            if not txt:
                return None
            try:
                return float(txt)
            except ValueError:
                return None

        xmin = _parse(self.entry_xmin)
        xmax = _parse(self.entry_xmax)
        ymin = _parse(self.entry_ymin)
        ymax = _parse(self.entry_ymax)

        cur_xmin, cur_xmax = self.ax.get_xlim()
        cur_ymin, cur_ymax = self.ax.get_ylim()
        new_xmin = xmin if xmin is not None else cur_xmin
        new_xmax = xmax if xmax is not None else cur_xmax
        new_ymin = ymin if ymin is not None else cur_ymin
        new_ymax = ymax if ymax is not None else cur_ymax
        if new_xmin < new_xmax:
            self.ax.set_xlim(new_xmin, new_xmax)
        if new_ymin < new_ymax:
            self.ax.set_ylim(new_ymin, new_ymax)

    def _toggle_axes_row(self):
        """Show/hide the axes range row."""
        self.axes_row_widget.setVisible(self.btn_axes.isChecked())

    def _on_axes_changed(self):
        """Re-render plot when any of the axes limit fields changes."""
        if self._last_result:
            self._draw_plot(*self._last_result)

    def _on_axes_reset(self):
        """Clear all axes limit fields and re-render with autoscale."""
        for le in (self.entry_xmin, self.entry_xmax,
                   self.entry_ymin, self.entry_ymax):
            le.clear()
        if self._last_result:
            self._draw_plot(*self._last_result)

    def _toggle_markers(self):
        """Toggle grid point markers on the plot."""
        self._show_markers = self.btn_markers.isChecked()
        if self._last_result:
            self._draw_plot(*self._last_result)

    def _toggle_phase(self):
        """Toggle phase plane mode."""
        self._phase_mode = self.btn_phase.isChecked()
        visible = self._phase_mode
        for w in (self.lbl_phase_x, self.combo_phase_x,
                  self.lbl_phase_y, self.combo_phase_y):
            w.setVisible(visible)
        self.lbl_plot.setText(
            self._t("result_phase") if self._phase_mode else self._t("result_plot"))
        if self._last_result:
            self._draw_plot(*self._last_result)

    def _on_phase_axis_changed(self):
        """Handle phase X/Y combo selection."""
        if self.combo_phase_x.count() > 0:
            self._phase_x_idx = self.combo_phase_x.currentIndex()
        if self.combo_phase_y.count() > 0:
            self._phase_y_idx = self.combo_phase_y.currentIndex()
        if self._phase_mode and self._last_result:
            self._draw_plot(*self._last_result)

    def _update_phase_combos(self, var_names):
        """Refill phase axis combo boxes for current variable names."""
        n = len(var_names)
        # Disable phase mode for n < 2
        if n < 2:
            self.btn_phase.setEnabled(False)
            if self._phase_mode:
                self.btn_phase.setChecked(False)
                self._toggle_phase()
        else:
            self.btn_phase.setEnabled(True)

        for combo, target_idx in (
            (self.combo_phase_x, self._phase_x_idx),
            (self.combo_phase_y, self._phase_y_idx),
        ):
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(var_names)
            combo.setCurrentIndex(min(target_idx, max(0, n - 1)))
            combo.blockSignals(False)
        # Defaults: x1, x2
        if n >= 2:
            self._phase_x_idx = self.combo_phase_x.currentIndex()
            self._phase_y_idx = self.combo_phase_y.currentIndex()

    def _on_table_step_changed(self):
        """Re-fill table when step value changes."""
        if self._last_result:
            t, x, var_names = self._last_result
            self._fill_table(t, x, var_names)

    # ------------------------------------------------------------------ #
    #  Library / Save / Load                                              #
    # ------------------------------------------------------------------ #
    def _show_library_menu(self):
        """Show menu with built-in examples grouped by category."""
        from PyQt6.QtWidgets import QMenu
        from examples.library import EXAMPLES

        menu = QMenu(self)
        name_key = "name_ru" if self.lang == "ru" else "name_en"
        source_key = "source_ru" if self.lang == "ru" else "source_en"

        categories = [
            ("tutorial", self._t("lib_tutorial")),
            ("article",  self._t("lib_article")),
        ]
        for cat_key, cat_label in categories:
            sub = menu.addMenu(cat_label)
            for ex in EXAMPLES:
                if ex["category"] != cat_key:
                    continue
                action = sub.addAction(ex[name_key])
                action.setToolTip(ex[source_key])
                action.triggered.connect(
                    lambda checked, eid=ex["id"]: self._apply_example(eid))

        menu.exec(self.btn_library.mapToGlobal(self.btn_library.rect().bottomLeft()))

    def _apply_example(self, example_id):
        """Load example by id into the form fields."""
        from examples.library import get_example
        ex = get_example(example_id)
        if ex is None:
            return
        self._load_state(ex)

    def _on_save(self):
        """Save current problem state to JSON file."""
        path, _ = QFileDialog.getSaveFileName(
            self, self._t("save_dialog"), "problem.json", self._t("json_filter"))
        if not path:
            return
        try:
            import json
            state = self._serialize_state()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "", self._t("save_error", msg=str(e)))

    def _on_load(self):
        """Load problem state from JSON file."""
        path, _ = QFileDialog.getOpenFileName(
            self, self._t("load_dialog"), "", self._t("json_filter"))
        if not path:
            return
        try:
            import json
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)
            self._load_state(state)
        except Exception as e:
            QMessageBox.critical(self, "", self._t("load_error", msg=str(e)))

    def _serialize_state(self):
        """Collect current form state into a JSON-serializable dict."""
        return {
            "n":             self.spin_n.value(),
            "equations":     [e.text() for _, e in self.eq_entries],
            "boundary":      [e.text() for _, e in self.bc_entries],
            "a":             float(self.entry_a.text()),
            "b":             float(self.entry_b.text()),
            "t_star":        float(self.entry_tstar.text()) if self.entry_tstar.text().strip() else 0.0,
            "p0":            [float(e.text()) for _, e in self.p0_entries],
            "inner_method":  self.combo_inner.currentData(),
            "outer_method":  self.combo_outer.currentData(),
            "inner_tol":     self.combo_inner_tol.currentText(),
            "outer_tol":     self.combo_outer_tol.currentText(),
            "max_iter":      int(self.entry_max_iter.text()),
        }

    def _load_state(self, state):
        """Apply a state dict to the form (used by both library and file load)."""
        n = int(state["n"])
        self.spin_n.setValue(n)
        self._sync_n_fields(n)

        for (_, entry), val in zip(self.eq_entries, state.get("equations", [])):
            entry.setText(str(val))
        for (_, entry), val in zip(self.bc_entries, state.get("boundary", [])):
            entry.setText(str(val))
        for (_, entry), val in zip(self.p0_entries, state.get("p0", [])):
            entry.setText(str(val))

        self.entry_a.setText(str(state.get("a", 0.0)))
        self.entry_b.setText(str(state.get("b", 1.0)))
        self.entry_tstar.setText(str(state.get("t_star", 0.0)))

        for combo, key in [(self.combo_inner, "inner_method"),
                           (self.combo_outer, "outer_method")]:
            method = state.get(key)
            if method:
                for i in range(combo.count()):
                    if combo.itemData(i) == method:
                        combo.setCurrentIndex(i)
                        break

        for combo, key in [(self.combo_inner_tol, "inner_tol"),
                           (self.combo_outer_tol, "outer_tol")]:
            tol = state.get(key)
            if tol is not None:
                tol_str = str(tol) if not isinstance(tol, str) else tol
                idx = combo.findText(tol_str)
                if idx >= 0:
                    combo.setCurrentIndex(idx)

        self.entry_max_iter.setText(str(state.get("max_iter", 10)))

    def _show_color_menu(self):
        """Show menu to pick color for each variable."""
        if not self._last_result:
            return
        _, _, var_names = self._last_result
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        for i, name in enumerate(var_names):
            action = menu.addAction(f"  {name}")
            color = self._custom_colors[i % len(self._custom_colors)]
            action.setIcon(self._color_icon(color))
            action.triggered.connect(lambda checked, idx=i: self._pick_color(idx))
        menu.exec(self.btn_colors.mapToGlobal(self.btn_colors.rect().bottomLeft()))

    def _pick_color(self, idx):
        """Open color dialog for variable at index."""
        current = QColor(self._custom_colors[idx % len(self._custom_colors)])
        color = QColorDialog.getColor(current, self, "")
        if color.isValid():
            while len(self._custom_colors) <= idx:
                self._custom_colors.append(COLORS[len(self._custom_colors) % len(COLORS)])
            self._custom_colors[idx] = color.name()
            if self._last_result:
                self._draw_plot(*self._last_result)

    def _color_icon(self, color_hex):
        """Create a small colored square icon with a contrasting border."""
        from PyQt6.QtGui import QPixmap, QIcon, QPainter, QPen
        size = 14
        pix = QPixmap(size, size)
        pix.fill(QColor(0, 0, 0, 0))  # transparent background
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        p.fillRect(1, 1, size - 2, size - 2, QColor(color_hex))
        pen = QPen(QColor(self._colors["text"]))
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(0, 0, size - 1, size - 1)
        p.end()
        return QIcon(pix)

    def _fill_table(self, t, x, var_names):
        import numpy as np
        cols = ["t"] + var_names

        step_text = self.entry_table_step.text().strip()
        t_grid = None
        x_grid = None
        if step_text and self._last_dense is not None:
            try:
                step = float(step_text.replace(",", "."))
            except ValueError:
                step = None
            a, b = float(t[0]), float(t[-1])
            span = b - a
            if step is not None and step > 0 and step <= span:
                # Build evenly spaced grid; include endpoint b explicitly
                n_steps = int(np.floor(span / step + 1e-9))
                t_grid = a + np.arange(n_steps + 1) * step
                if t_grid[-1] < b - 1e-12:
                    t_grid = np.append(t_grid, b)
                t_grid[-1] = min(t_grid[-1], b)
                x_grid = self._last_dense(t_grid)

        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)

        if t_grid is not None and x_grid is not None:
            self.table.setRowCount(len(t_grid))
            for r in range(len(t_grid)):
                self.table.setItem(r, 0, QTableWidgetItem(f"{t_grid[r]:.4f}"))
                for i in range(len(var_names)):
                    self.table.setItem(r, i + 1, QTableWidgetItem(f"{x_grid[i][r]:.6f}"))
        else:
            step_idx = max(1, len(t) // 50)
            rows = list(range(0, len(t), step_idx))
            self.table.setRowCount(len(rows))
            for r, j in enumerate(rows):
                self.table.setItem(r, 0, QTableWidgetItem(f"{t[j]:.4f}"))
                for i in range(len(var_names)):
                    self.table.setItem(r, i + 1, QTableWidgetItem(f"{x[i][j]:.6f}"))

        # Row numbering (1-based)
        self.table.setVerticalHeaderLabels(
            [str(r + 1) for r in range(self.table.rowCount())])

    def _on_error(self, msg):
        self._set_status(self._t("status_error", msg=msg), "statusErr", key="status_error", msg=msg)
        self.btn_solve.setEnabled(True)

    def _set_status(self, text, object_name, key=None, **kwargs):
        self._status_key = key
        self._status_kwargs = kwargs
        self._status_object_name = object_name
        self.lbl_status.setText(text)
        self.lbl_status.setObjectName(object_name)
        self.lbl_status.style().unpolish(self.lbl_status)
        self.lbl_status.style().polish(self.lbl_status)

    # ------------------------------------------------------------------ #
    #  Theme                                                               #
    # ------------------------------------------------------------------ #
    def _toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self._apply_theme()

    def _apply_theme(self):
        self._colors = LIGHT_COLORS if self.theme == "light" else DARK_COLORS
        self.setStyleSheet(_make_stylesheet(self._colors))
        self.theme_btn.setText("☀" if self.theme == "dark" else "🌙")
        self._apply_combo_palettes()
        if self._last_result:
            self._draw_plot(*self._last_result)
        else:
            self._style_axes()
            self.canvas.draw()

    def _apply_combo_palettes(self):
        """Fix combo dropdown colors and remove double-checkmark on macOS."""
        c = self._colors
        all_combos = [self.combo_inner, self.combo_outer,
                      self.combo_inner_tol, self.combo_outer_tol,
                      self.combo_phase_x, self.combo_phase_y]
        for combo in all_combos:
            # Replace view with plain QListView (no check indicators)
            lv = QListView()
            lv.setTextElideMode(Qt.TextElideMode.ElideRight)
            lv.setStyleSheet(f"""
                QListView {{
                    background-color: {c["card"]};
                    color: {c["text"]};
                    outline: none;
                    border: none;
                    border-radius: 8px;
                }}
                QListView::item {{
                    padding: 5px 10px;
                    border: none;
                    border-radius: 6px;
                    margin: 2px 4px;
                }}
                QListView::item:hover {{
                    background-color: {c["top_btn_hover"]};
                }}
                QListView::item:selected {{
                    background-color: {c["primary"]};
                    color: #ffffff;
                }}
            """)
            combo.setView(lv)
            # Force popup width to match the combo box
            w = combo.width() if combo.width() > 0 else 280
            lv.setMinimumWidth(w)
            popup = combo.view().parentWidget()
            if popup:
                popup.setMinimumWidth(w)
                popup.setMaximumWidth(w)
                popup.setStyleSheet(f"""
                    QWidget {{
                        background-color: {c["card"]};
                        border: 1px solid {c["border"]};
                        border-radius: 8px;
                    }}
                """)

    # ------------------------------------------------------------------ #
    #  Language                                                            #
    # ------------------------------------------------------------------ #
    def _toggle_lang(self):
        idx = LANGUAGES.index(self.lang)
        self.lang = LANGUAGES[(idx + 1) % len(LANGUAGES)]
        self._refresh_labels()

    def _refresh_labels(self):
        self.setWindowTitle(self._t("app_title"))
        self.lbl_app_title.setText(self._t("app_title"))
        self.tabs.setTabText(0, self._t("tab_solution"))
        self.tabs.setTabText(1, self._t("tab_parameters"))
        self.tabs.setTabText(2, self._t("tab_author"))
        self.tabs.setTabText(3, self._t("tab_help"))

        self.lang_btn.setText("EN" if self.lang == "ru" else "RU")

        self.lbl_dimension.setText(self._t("dimension"))
        self.lbl_interval.setText(self._t("interval"))
        self.lbl_tstar.setText(self._t("t_star"))
        self.lbl_equations.setText(self._t("equations"))
        self.lbl_boundary.setText(self._t("boundary"))
        self.lbl_p0.setText(self._t("p0"))
        self.btn_solve.setText(self._t("btn_solve"))
        self.btn_library.setText(self._t("btn_library"))
        self.btn_save.setText(self._t("btn_save"))
        self.btn_load.setText(self._t("btn_load"))
        self.lbl_plot.setText(
            self._t("result_phase") if self._phase_mode else self._t("result_plot"))
        self.lbl_table.setText(self._t("result_table"))
        self.lbl_table_step.setText(self._t("table_step"))
        self.entry_table_step.setPlaceholderText(self._t("table_step_placeholder"))
        self.entry_table_step.setToolTip(self._t("tip_table_step"))
        self.btn_markers.setToolTip(self._t("tip_markers"))
        self.btn_phase.setToolTip(self._t("tip_phase"))
        self.btn_colors.setToolTip(self._t("tip_colors"))
        self.btn_axes.setToolTip(self._t("tip_axes"))
        self.btn_axes_reset.setText(self._t("btn_axes_reset"))
        for le, ph in (
            (self.entry_xmin, "x min"), (self.entry_xmax, "x max"),
            (self.entry_ymin, "y min"), (self.entry_ymax, "y max"),
        ):
            le.setPlaceholderText(ph)
        self.lbl_phase_x.setText(self._t("phase_x"))
        self.lbl_phase_y.setText(self._t("phase_y"))

        # Parameters tab
        self.lbl_inner_title.setText(self._t("inner_card_title"))
        self.lbl_inner_desc.setText(self._t("inner_card_desc"))
        self.lbl_outer_title.setText(self._t("outer_card_title"))
        self.lbl_outer_desc.setText(self._t("outer_card_desc"))
        self.lbl_inner_method.setText(self._t("param_method"))
        self.lbl_outer_method.setText(self._t("param_method"))
        self.lbl_inner_tol.setText(self._t("param_tol"))
        self.lbl_outer_tol.setText(self._t("param_tol"))
        self.lbl_max_iter.setText(self._t("param_max_iter"))
        self._populate_method_combos()

        # Update help cards
        for key, title_lbl, body_lbl in self._help_cards:
            title_lbl.setText(self._t(key + "_title"))
            body_lbl.setText(self._t(key + "_body"))

        # Update status text on language change
        if self._status_key:
            self.lbl_status.setText(self._t(self._status_key, **self._status_kwargs))


class App:
    def __init__(self):
        self.qapp = QApplication.instance() or QApplication(sys.argv)
        self.window = MainWindow()

    def run(self):
        self.window.show()
        self.qapp.exec()
