from PyQt5.QtWidgets import QMainWindow

from spline_view import SplineView
from control_panel import ControlPanel
from sub_window import Sub_window


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        close_action = file_menu.addAction('Close')
        close_action.triggered.connect(self.close)

        spline_view = SplineView()
        edit_menu = menubar.addMenu('Edit')
        undo_action = edit_menu.addAction('Undo')
        undo_action.triggered.connect(spline_view.undo_spline_view)
        redo_action = edit_menu.addAction('Redo')
        redo_action.triggered.connect(spline_view.redo_spline_view)
        
        self.setCentralWidget(spline_view)
        
        about_menu = menubar.addAction('About')
        about_menu.triggered.connect(Sub_window.about)
        
        control_panel = ControlPanel(spline_view.maximumWidth(), spline_view.maximumHeight())
        self.statusBar().addWidget(control_panel)

        control_panel.state_changed.connect(spline_view.set_current_knot)
        spline_view.current_knot_changed.connect(control_panel.set_state)
