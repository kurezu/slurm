from  PyQt5.QtCore import QPointF, QPoint
from PyQt5.QtGui import QPolygonF

from knot import Knot

from typing import List


class Spline:
    def __init__(self) -> None:
        self.knots: List[Knot] = []
        self.curve = None
        self.subdivs = 40
        self.uStep = 1.0 / self.subdivs


    def get_knots(self) -> List[Knot]:
        return self.knots

    def set_current_knot(self, index: int, value: Knot):
        if not self.knots:
            return        
        self.knots[index] = value
        self.curve = None

    def get_curve(self) -> QPolygonF:
        if self.curve is None:
            self._interpolate()
        return self.curve or QPolygonF()

    def add_knot(self, pos) -> None:
        self.knots.append(Knot(QPointF(pos)))
        self.curve = None

    def get_knot_by_pos(self, pos: QPoint) -> int:
        for index, knot in enumerate(self.knots):
            if (knot.pos - pos).manhattanLength() < 8:
                return index

    def _interpolate(self) -> QPolygonF:
        if len(self.knots) < 2:
            return

        self.curve = QPolygonF()

        for k in range(len(self.knots) - 1):
            prev: Knot = self.knots[k] if k == 0 else self.knots[k - 1]
            cur: Knot = self.knots[k]
            next1: Knot = self.knots[k + 1]
            next2: Knot = (
                self.knots[k + 1] if k + 2 >= len(self.knots) else self.knots[k + 2]
            )

            t = cur.tension
            b = cur.bias
            c = cur.continuity

            d0 = (
                0.5
                * (1 - t)
                * (
                    (1 + b) * (1 - c) * (cur.pos - prev.pos)
                    + (1 - b) * (1 + c) * (next1.pos - cur.pos)
                )
            )

            t = next1.tension
            b = next1.bias
            c = next1.continuity

            d1 = (
                0.5
                * (1 - t)
                * (
                    (1 + b) * (1 + c) * (next1.pos - cur.pos)
                    + (1 - b) * (1 - c) * (next2.pos - next1.pos)
                )
            )

            u = 0.0
            for _ in range(self.subdivs):
                u2 = u * u
                u3 = u * u * u
                
                self.curve.append(
                    (2 * u3 - 3 * u2 + 1) * cur.pos
                    + (-2 * u3 + 3 * u2) * next1.pos
                    + (u3 - 2 * u2 + u) * d0
                    + (u3 - u2) * d1
                )
                u += self.uStep

        self.curve.append(self.knots[-1].pos)