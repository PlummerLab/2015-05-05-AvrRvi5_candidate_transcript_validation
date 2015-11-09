""" Shapes for drawing genes and gene features. """

from matplotlib.path import Path
import numpy as np
from math import sin
from math import radians


class Shape(object):

    """ Base class for drawing genomic features. """

    def __init__(
            self,
            angle=0,
            x_offset=0,
            y_offset=0,
            width=1,
            **kwargs
            ):
        """ . """
        self.angle = angle
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.properties = kwargs
        return

    def __call__(
            self,
            x,
            y,
            length
            ):
        """ . """
        return self._draw(x, y, length)

    def _rotate(self):
        """ . """
        return


class Rectangle(Shape):

    """ Rectangle. """

    def _draw(
            self,
            x,
            y,
            length
            ):
        """ . """
        x += self.x_offset
        y += self.y_offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        path = np.array([
            [x, y],  # bottom left
            [x + length, y],  # bottom right
            [x + length, y + self.width],  # top right
            [x, y + self.width],  # top left
            [x, y]  # bottom left
            ])
        return path, codes


class Arrow(Shape):

    """ Arrow. """

    def __init__(
            self,
            tail_width=0.8,
            tip_angle=90,
            **kwargs
            ):
        """ . """
        super().__init__(**kwargs)
        self.tail_width = tail_width
        self.tip_angle = tip_angle
        self.head_length = (sin(radians(90 - (self.tip_angle/2))) * self.width/2) / sin(radians(self.tip_angle/2))
        return

    def _draw(
            self,
            x,
            y,
            length
            ):
        """ . """
        x += self.x_offset
        y += self.y_offset

        tail_offset = (self.width - (self.width * self.tail_width)) / 2

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])
        # TODO: add conditional formatting for case head_length > length
        path = np.array([
            [x, y + tail_offset],
            [x, y + self.width - tail_offset],
            [x + length - self.head_length, y + self.width - tail_offset],
            [x + length - self.head_length, y + self.width],
            [x + length, y + (self.width / 2)],
            [x + length - self.head_length, y],
            [x + length - self.head_length, y + tail_offset],
            [x, y + tail_offset]
            ])

        return path, codes


class Hexagon(Shape):

    """ Hexagon. """

    def __init__(self):
        return


class Ellipse(Shape):

    """ Ellipse. """

    def __init__(self):
        return


class Triangle(Shape):

    """ Triangle. """

    def __init__(
            self,
            **kwargs
            ):
        """ . """
        super().__init__(**kwargs)
        return

    def _draw(
            self,
            x,
            y,
            length
            ):
        """ . """
        x += self.x_offset
        y += self.y_offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])
        # TODO: add conditional formatting for case head_length > length
        path = np.array([
            [x, y],
            [x, y + self.width],
            [x + length, y + (self.width / 2)],
            [x, y]
            ])
        return path, codes


class Trapeziod(Shape):

    """ Trapeziod. """

    def __init__(self):
        return


class OpenTriangle(Shape):

    """ . """

    def _draw(
            self,
            x,
            y,
            length
            ):
        """ . """
        x += self.x_offset
        y += self.y_offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO
            ])

        path = np.array([
            [x, y],
            [x + length / 2, y + self.width],
            [x + length, y]
            ])

        return path, codes


class OpenRectangle(Shape):

    """ . """

    def _draw(
            self,
            x,
            y,
            length
            ):
        """ . """
        x += self.x_offset
        y += self.y_offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        path = np.array([
            [x, y],
            [x, y + self.width],
            [x + length, y],
            [x, y]
            ])

        return path, codes


class SineWave(Shape):

    """ . """

    def __init__(self):
        return


class SawtoothWave(Shape):

    """ . """

    def __init__(self):
        return


class SquareWave(Shape):

    """ . """

    def __init__(self):
        return


class TriangleWave(Shape):

    """ . """

    def __init__(self):
        return


class Helix(Shape):

    """ . """

    def __init__(self):
        return


class DoubleHelix(Shape):

    """ . """

    def __init__(self):
        return
