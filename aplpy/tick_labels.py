# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

from .decorators import auto_refresh, fixdocstring

__all__ = ['TickLabels']


class TickLabels(object):

    def __init__(self, parent):
        self._figure = parent._figure
        self._ax = parent.ax
        self._wcs = parent.ax.wcs
        self.x = parent.x
        self.y = parent.y
        self.set_style('plain')

    @auto_refresh
    def set_xformat(self, xformat):
        """
        Set the format of the x-axis tick labels.

        If the x-axis type is ``longitude`` or ``latitude``, then the options
        are:

            * ``d.ddddd`` - decimal degrees, where the number of decimal places can be varied
            * ``hh`` or ``dd`` - hours (or degrees)
            * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
            * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
            * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.

        If the x-axis type is ``scalar``, then the format should be a valid
        python string format beginning with a ``%``.

        If one of these arguments is not specified, the format for that axis
        is left unchanged.
        """
        if 'dd.' in xformat:
            xformat = xformat.replace('ddd.', 'd.').replace('dd.', 'd.')
        self._ax.coords[self.x].set_major_formatter(xformat)

    @auto_refresh
    def set_yformat(self, yformat):
        """
        Set the format of the y-axis tick labels.

        If the y-axis type is ``longitude`` or ``latitude``, then the options
        are:

            * ``d.ddddd`` - decimal degrees, where the number of decimal places can be varied
            * ``hh`` or ``dd`` - hours (or degrees)
            * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
            * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
            * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.

        If the y-axis type is ``scalar``, then the format should be a valid
        python string format beginning with a ``%``.

        If one of these arguments is not specified, the format for that axis
        is left unchanged.
        """
        if 'dd.' in yformat:
            yformat = yformat.replace('ddd.', 'd.').replace('dd.', 'd.')
        self._ax.coords[self.y].set_major_formatter(yformat)

    @auto_refresh
    def set_style(self, style):
        """
        Set the format of the x-axis tick labels.

        This can be 'colons' or 'plain':

            * 'colons' uses colons as separators, for example 31:41:59.26 +27:18:28.1
            * 'plain' uses letters and symbols as separators, for example 31h41m59.26s +27º18'28.1"
        """

        if style not in ['colons', 'plain']:
            raise Exception("Label style should be one of colons/plain")

        self.style = style
        for coord in [self.x, self.y]:
            coord_type = self._ax.coords[coord].coord_type
            if coord_type in ['longitude', 'latitude']:
                if style == 'colons':
                    sep = (':', ':', '')
                else:
                    sep = None

                self._ax.coords[coord].set_separator(sep)

    @auto_refresh
    @fixdocstring
    def set_font(self, **kwargs):
        """
        Set the font of the tick labels.

        Parameters
        ----------

        common: family, style, variant, stretch, weight, size, fontproperties

        Notes
        -----

        Default values are set by matplotlib or previously set values if
        set_font has already been called. Global default values can be set by
        editing the matplotlibrc file.
        """
        self._ax.coords[self.x].set_ticklabel(**kwargs)
        self._ax.coords[self.y].set_ticklabel(**kwargs)

    @auto_refresh
    def show(self):
        """
        Show the x- and y-axis tick labels.
        """
        self.show_x()
        self.show_y()

    @auto_refresh
    def hide(self):
        """
        Hide the x- and y-axis tick labels.
        """
        self.hide_x()
        self.hide_y()

    @auto_refresh
    def show_x(self):
        """
        Show the x-axis tick labels.
        """
        self._ax.coords[self.x].set_ticklabel_visible(True)

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis tick labels.
        """
        self._ax.coords[self.x].set_ticklabel_visible(False)

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis tick labels.
        """
        self._ax.coords[self.y].set_ticklabel_visible(True)

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis tick labels.
        """
        self._ax.coords[self.y].set_ticklabel_visible(False)

    @auto_refresh
    def set_xposition(self, position):
        """
        Set the position of the x-axis tick labels ('top' or 'bottom')
        """
        if position == 'bottom':
            self._ax.coords[self.x].set_ticklabel_position('b')
        elif position == 'top':
            self._ax.coords[self.x].set_ticklabel_position('t')
        else:
            raise ValueError("position should be one of 'top' or 'bottom'")

    @auto_refresh
    def set_yposition(self, position):
        """
        Set the position of the y-axis tick labels ('left' or 'right')
        """
        if position == 'left':
            self._ax.coords[self.y].set_ticklabel_position('l')
        elif position == 'right':
            self._ax.coords[self.y].set_ticklabel_position('r')
        else:
            raise ValueError("position should be one of 'left' or 'right'")
