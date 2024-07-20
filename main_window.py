from PyQt5.QtWidgets import QMainWindow, QAction, QComboBox, QActionGroup
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import Qt, QEvent

from spline_view import SplineView
from control_panel import ControlPanel
from sub_window import Sub_window
from style import AppStyle

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.main_style = AppStyle()
        with open(self.main_style.style, 'r', encoding='utf-8') as style_sheet_file:
            self.setStyleSheet(style_sheet_file.read())
        
        spline_icon = QIcon("icons/vector-spline.svg")
        self.setWindowIcon(spline_icon)
        menubar = self.menuBar()
        self.spline_view = SplineView()
        file_menu = menubar.addMenu('File')
        new_action = file_menu.addAction('New')
        new_action.triggered.connect(self.spline_view.newDialog)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        open_action = file_menu.addAction('Open')
        open_action.triggered.connect(self.spline_view.openDialog)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        save_action = file_menu.addAction('Save')
        save_action.triggered.connect(self.spline_view.saveDialog)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        close_action = file_menu.addAction('Close')
        close_action.triggered.connect(self.close)

        edit_menu = menubar.addMenu('Edit')
        
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.spline_view.undo_spline_view)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.spline_view.redo_spline_view)
        redo_action.setShortcut(QKeySequence("Shift+Ctrl+Z"))
        edit_menu.addAction(redo_action)
        
        settings_menu = menubar.addMenu('Settings')
        style_menu = settings_menu.addMenu("Style")
        group = QActionGroup(self)
        
        style_action_dark = QAction("dark", self, checkable=True)
        if self.main_style.style == 'style/dark.qss':
            style_action_dark.setChecked(True)
        style_action_dark.triggered.connect(self.changeStyleDark)
        style_menu.addAction(style_action_dark)
        
        style_action_perstfic = QAction("perstfic", self, checkable=True)
        if self.main_style.style == 'style/Perstfic.qss':
            style_action_perstfic.setChecked(True)
        style_action_perstfic.triggered.connect(self.changeStylePerstfic)
        style_menu.addAction(style_action_perstfic)

        style_action_geoo = QAction("geoo", self, checkable=True)
        if self.main_style.style == 'style/Geoo.qss':
            style_action_geoo.setChecked(True)
        style_action_geoo.triggered.connect(self.changeStyleGeoo)
        style_menu.addAction(style_action_geoo)

        group.addAction(style_action_dark)
        group.addAction(style_action_perstfic)
        group.addAction(style_action_geoo)
        
        self.about_window = Sub_window()
        about_menu = menubar.addAction('About')
        about_menu.triggered.connect(self.about_window.about)

        combo = QComboBox(self)
        combo.addItem("Kochanek–Bartels")
        combo.addItem("Polyline")
        combo.activated.connect(self.onActivated)
        
        self.setCentralWidget(self.spline_view)
        
        control_panel = ControlPanel(self.spline_view.maximumWidth(), self.spline_view.maximumHeight())
        self.statusBar().addWidget(control_panel)
        self.statusBar().addWidget(combo)

        control_panel.state_changed.connect(self.spline_view.set_current_knot)
        self.spline_view.current_knot_changed.connect(control_panel.set_state)


    def onActivated(self, idx):
        if idx == 1:
            self.spline_view.set_type(1)  
        else:
            self.spline_view.set_type(0)
            
    def event(self, event):
        if (event.type() == QEvent.ShortcutOverride) and (event.key() == Qt.Key_Shift):
            self.spline_view.shift = True
        if (event.type() == QEvent.KeyRelease) and (event.key() == Qt.Key_Shift):
            self.spline_view.shift = False
        return super().event(event)
    
    def changeStylePerstfic(self):
        self.main_style.setStyle('style/Perstfic.qss')
        with open(self.main_style.style, 'r', encoding='utf-8') as style_sheet_file:
            self.setStyleSheet(style_sheet_file.read())
    
    def changeStyleDark(self):
        self.main_style.setStyle('style/dark.qss')
        with open(self.main_style.style, 'r', encoding='utf-8') as style_sheet_file:
            self.setStyleSheet(style_sheet_file.read())
    
    def changeStyleGeoo(self):
        self.main_style.setStyle('style/Geoo.qss')
        with open(self.main_style.style, 'r', encoding='utf-8') as style_sheet_file:
            self.setStyleSheet(style_sheet_file.read())
        