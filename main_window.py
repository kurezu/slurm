from PyQt5.QtWidgets import QMainWindow, QAction, QComboBox
from PyQt5.QtGui import QKeySequence

from spline_view import SplineView
from control_panel import ControlPanel
from sub_window import Sub_window


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        menubar = self.menuBar()
        self.spline_view = SplineView()
        file_menu = menubar.addMenu('File')
        new_action = file_menu.addAction('New')
        new_action.triggered.connect(self.spline_view.NewDialog)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        open_action = file_menu.addAction('Open')
        open_action.triggered.connect(self.spline_view.OpenDialog)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        save_action = file_menu.addAction('Save')
        save_action.triggered.connect(self.spline_view.SaveDialog)
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
        
        about_menu = menubar.addAction('About')
        about_menu.triggered.connect(Sub_window.about)

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
        # print(self.combo_type)
        if idx == 1:
            self.spline_view.set_type(1)  
        else:
            self.spline_view.set_type(0)