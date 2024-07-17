from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtGui import QKeySequence

from spline_view import SplineView
from control_panel import ControlPanel
from sub_window import Sub_window


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        menubar = self.menuBar()
        spline_view = SplineView()
        file_menu = menubar.addMenu('File')
        new_action = file_menu.addAction('New')
        new_action.triggered.connect(spline_view.NewDialog)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        open_action = file_menu.addAction('Open')
        open_action.triggered.connect(spline_view.OpenDialog)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        save_action = file_menu.addAction('Save')
        save_action.triggered.connect(spline_view.SaveDialog)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        close_action = file_menu.addAction('Close')
        close_action.triggered.connect(self.close)

        edit_menu = menubar.addMenu('Edit')
        
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(spline_view.undo_spline_view)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(spline_view.redo_spline_view)
        redo_action.setShortcut(QKeySequence("Shift+Ctrl+Z"))
        edit_menu.addAction(redo_action)
        
        self.setCentralWidget(spline_view)
        
        about_menu = menubar.addAction('About')
        about_menu.triggered.connect(Sub_window.about)
        
        control_panel = ControlPanel(spline_view.maximumWidth(), spline_view.maximumHeight())
        self.statusBar().addWidget(control_panel)

        control_panel.state_changed.connect(spline_view.set_current_knot)
        spline_view.current_knot_changed.connect(control_panel.set_state)
