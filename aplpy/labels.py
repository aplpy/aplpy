# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

import warnings

import numpy as np
import matplotlib.pyplot as mpl
from matplotlib.font_manager import FontProperties

from . import wcs_util
from . import angle_util as au
from .decorators import auto_refresh, fixdocstring


class TickLabels(object):

    def __init__(self, parent):
        self._ax = parent.ax
        self._wcs = parent.ax.wcs
        self.x = parent.x
        self.y = parent.y
        self._figure = parent._figure

        # Save plotting parameters (required for @auto_refresh)
        self._parameters = parent._parameters

        # Set font
        self._label_fontproperties = FontProperties()

        self.set_style('plain')

        system, equinox = wcs_util.system(self._wcs)

        # Set default label format
        if self._ax.coords[self.x].coord_type in ['longitude', 'latitude']:

            if system['name'] == 'equatorial':
                if self._ax.coords[self.x].coord_type == 'longitude':
                    self.set_xformat("hh:mm:ss.ss")
                else:
                    self.set_xformat("dd:mm:ss.s")
            else:
                self.set_xformat("d.dddd")
        else:
            self.set_xformat('%g')

        if self._ax.coords[self.y].coord_type in ['longitude', 'latitude']:
            if system['name'] == 'equatorial':
                if self._ax.coords[self.y].coord_type == 'longitude':
                    self.set_yformat("hh:mm:ss.ss")
                else:
                    self.set_yformat("dd:mm:ss.s")
            else:
                self.set_yformat("d.dddd")
        else:
            self.set_yformat('%g')

        # Cursor display
        self._ax._cursor_world = True
        self._figure.canvas.mpl_connect('key_press_event', self._set_cursor_prefs)

    @auto_refresh
    def set_xformat(self, format):
        '''
        Set the format of the x-axis tick labels.

        If the x-axis type is ``longitude`` or ``latitude``, then the options
        are:

            * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
            * ``hh`` or ``dd`` - hours (or degrees)
            * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
            * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
            * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.

        If the x-axis type is ``scalar``, then the format should be a valid
        python string format beginning with a ``%``.

        If one of these arguments is not specified, the format for that axis
        is left unchanged.
        '''
        coord_type = self._ax.coords[self.x].coord_type
        if coord_type in ['longitude', 'latitude']:
            if format.startswith('%'):
                raise Exception("Cannot specify Python format for longitude or latitude")
            try:
                spacing = self._ax.coords[self.x]._formatter_locator.spacing
                if spacing is not None:
                    spacing = au.Angle(degrees=spacing.value, latitude=coord_type == 'latitude')
                    au._check_format_spacing_consistency(format, spacing)
            except au.InconsistentSpacing:
                warnings.warn("WARNING: Requested label format is not accurate enough to display ticks. The label format will not be changed.")
                return
        else:
            if not format.startswith('%'):
                raise Exception("For scalar tick labels, format should be a Python format beginning with %")
        self._ax.coords[self.x].set_major_formatter(format)

    @auto_refresh
    def set_yformat(self, format):
        '''
        Set the format of the y-axis tick labels.

        If the y-axis type is ``longitude`` or ``latitude``, then the options
        are:

            * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
            * ``hh`` or ``dd`` - hours (or degrees)
            * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
            * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
            * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.

        If the y-axis type is ``scalar``, then the format should be a valid
        python string format beginning with a ``%``.

        If one of these arguments is not specified, the format for that axis
        is left unchanged.
        '''
        coord_type = self._ax.coords[self.y].coord_type
        if coord_type in ['longitude', 'latitude']:
            if format.startswith('%'):
                raise Exception("Cannot specify Python format for longitude or latitude")
            try:
                spacing = self._ax.coords[self.y]._formatter_locator.spacing
                if spacing is not None:
                    spacing = au.Angle(degrees=spacing.value, latitude=coord_type == 'latitude')
                    au._check_format_spacing_consistency(format, spacing)
            except au.InconsistentSpacing:
                warnings.warn("WARNING: Requested label format is not accurate enough to display ticks. The label format will not be changed.")
                return
        else:
            if not format.startswith('%'):
                raise Exception("For scalar tick labels, format should be a Python format beginning with %")

        self._ax.coords[self.y].set_major_formatter(format)

    @auto_refresh
    def set_style(self, style):
        """
        Set the format of the x-axis tick labels.

        This can be 'colons' or 'plain':

            * 'colons' uses colons as separators, for example 31:41:59.26 +27:18:28.1
            * 'plain' uses letters and symbols as separators, for example 31h41m59.26s +27º18'28.1"
        """
        if style == 'latex':
            warnings.warn("latex has now been merged with plain - whether or not to use LaTeX is controlled through set_system_latex")
            style = 'plain'
        if style not in ['colons', 'plain']:
            raise Exception("Label style should be one of colons/plain")

        self.style = style
        coords = [self.x, self.y]
        for coord in coords:
            coord_type = self._ax.coords[coord].coord_type
            if coord_type in ['longitude', 'latitude']:
                if style == 'colons':
                    sep = (':', ':', '')
                else:
                    sep = ('d', 'm', 's')
                    format = self._ax.coords[coord]._formatter_locator.format
                    if (format is not None) and 'h' in format:
                        sep = ('h', 'm', 's')

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
        self._ax.coords[self.x].set_ticklabel_position('b')

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis tick labels.
        """
        self._ax.coords[self.x].set_ticklabel_position('')

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis tick labels.
        """
        self._ax.coords[self.y].set_ticklabel_position('l')

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis tick labels.
        """
        self._ax.coords[self.y].set_ticklabel_position('')

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

    def _set_cursor_prefs(self, event, **kwargs):
        if event.key == 'c':
            self._ax._cursor_world = not self._ax._cursor_world

    def _cursor_position(self, x, y):

        if self._ax._cursor_world:

            xw, yw = wcs_util.pix2world(self._wcs, x, y)

            if self._ax.coords[self.x].coord_type in ['longitude', 'latitude']:

                xw = au.Angle(degrees=xw, latitude=self._ax.coords[self.x].coord_type == 'latitude')
                x_format = self._ax.coords[self.x]._formatter_locator.format

                hours = 'h' in x_format

                if hours:
                    xw = xw.tohours()

                if self.style in ['plain', 'latex']:
                    sep = ('d', 'm', 's')
                    if hours:
                        sep = ('h', 'm', 's')
                elif self.style == 'colons':
                    sep = (':', ':', '')

                xlabel = xw.tostringlist(format=x_format, sep=sep)
                xlabel = "".join(xlabel)

            else:

                xlabel = x_format % xw

            if self._ax.coords[self.y].coord_type in ['longitude', 'latitude']:

                y_format = self._ax.coords[self.y]._formatter_locator.format

                yw = au.Angle(degrees=yw, latitude=self._ax.coords[self.y].coord_type == 'latitude')

                hours = 'h' in y_format

                if hours:
                    yw = yw.tohours()

                if self.style in ['plain', 'latex']:
                    sep = ('d', 'm', 's')
                    if hours:
                        sep = ('h', 'm', 's')
                elif self.style == 'colons':
                    sep = (':', ':', '')

                ylabel = yw.tostringlist(format=y_format, sep=sep)
                ylabel = "".join(ylabel)

            else:

                ylabel = y_format % yw

            return "%s %s (world)" % (xlabel, ylabel)

        else:

            return "%g %g (pixel)" % (x, y)
