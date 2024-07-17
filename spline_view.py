from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter,  QPalette, QPen, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
import pickle

from spline import Spline
from knot import Knot
from spline_history import SplineHistory

class SplineView(QWidget):
    current_knot_changed = pyqtSignal(Knot)

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.spline = Spline()
        self.spline_history = SplineHistory()
        self.cur_knot_index = None
        self.spline_history.add_spline(self.spline.knots, self.cur_knot_index)

    def paintEvent(self, event) -> None:
        bg_color = self.palette().color(QPalette.Base)
        curve_color = self.palette().color(QPalette.Foreground)
        painter = QPainter(self)
        painter.fillRect(self.rect(), bg_color)

        painter.setPen(QPen(curve_color, 2, Qt.SolidLine))
        painter.setRenderHints(QPainter.HighQualityAntialiasing)

        painter.drawPolyline(self.spline.get_curve())

        painter.setBrush(QBrush(curve_color, Qt.SolidPattern))
        for index, knot in enumerate(self.spline.get_knots()):
            radius = 6 if self.cur_knot_index == index else 4
            painter.drawEllipse(knot.pos, radius, radius)
        
        return super().paintEvent(event)

    def mousePressEvent(self, event) -> None:
        button = event.button()
        index = self.spline.get_knot_by_pos(event.pos())
        if button == Qt.LeftButton:
            if index is not None:
                self.cur_knot_index = index
            elif (self.cur_knot_index != len(self.spline.get_knots()) - 1) and (self.cur_knot_index is not None):
                self.spline.add_knot(event.pos(), self.cur_knot_index+1)
                self.cur_knot_index = self.cur_knot_index + 1
            else:
                self.spline.add_knot(event.pos(), None)
                self.cur_knot_index = len(self.spline.get_knots()) - 1
            self.spline_history.add_spline(self.spline.knots, self.cur_knot_index)
            
        self.current_knot_changed.emit(self.spline.get_knots()[self.cur_knot_index])
        self.update()
        return super().mousePressEvent(event)

    def undo_spline_view(self):
        if self.spline_history.actual_index > 0:
            self.spline_history.actual_index -= 1
        self.spline.knots = self.spline_history.copy_spline(self.spline_history.actual_index)
        self.cur_knot_index = self.spline_history.copy_cur_knot_ind(self.spline_history.actual_index)

        if len(self.spline.knots) > 0:
            self.current_knot_changed.emit(self.spline.knots[self.cur_knot_index])
        self.spline.curve = None
        self.update()

    def redo_spline_view(self):
        if self.spline_history.actual_index < len(self.spline_history.spline_list) - 1:
            self.spline_history.actual_index += 1
            
            self.spline.knots = self.spline_history.copy_spline(self.spline_history.actual_index)
            self.cur_knot_index = self.spline_history.copy_cur_knot_ind(self.spline_history.actual_index)

            if len(self.spline.knots) == 0:
                self.cur_knot_index = 0
            else:
                self.current_knot_changed.emit(self.spline.knots[self.cur_knot_index])

            self.spline.curve = None
            self.update()

    def set_current_knot(self, value: Knot):
        self.spline.set_current_knot(self.cur_knot_index, value)
        self.update()

    def OpenDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '', "Spl Files (*.spl)")[0]
        if fname != '':
            with open(fname, 'rb') as pickle_file:
                self.spline.knots = pickle.load(pickle_file)
                self.spline.curve = None
                self.update()
                
    def SaveDialog(self):

        fname = QFileDialog.getSaveFileName(self, 'Save file', '', "Spl Files (*.spl)")[0]
        if fname != '':
            with open(fname, 'wb') as pickle_file:
                pickle.dump(self.spline.knots, pickle_file)
                
    def NewDialog(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("New")
        dlg.setText("Сбросить все точки?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            print("Yes!")
            self.spline.knots = []
            self.spline.curve = None
            self.update()