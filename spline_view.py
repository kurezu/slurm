from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter,  QPalette, QPen, QBrush
from PyQt5.QtCore import Qt, pyqtSignal

from spline import Spline
from knot import Knot


class SplineView(QWidget):
    current_knot_changed = pyqtSignal(Knot)

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.spline = Spline()
        self.cur_knot_index = None

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
        index = self.spline.get_knot_by_pos(event.pos())
        if index is not None:
            self.cur_knot_index = index
        else:
            self.spline.add_knot(event.pos())
            self.cur_knot_index = len(self.spline.get_knots()) - 1
            
        self.current_knot_changed.emit(self.spline.get_knots()[self.cur_knot_index])
        self.update()
        return super().mousePressEvent(event)

    def set_current_knot(self, value: Knot):
        self.spline.set_current_knot(self.cur_knot_index, value)
        self.update()

    