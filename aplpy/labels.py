# -*- coding: utf-8 -*-

import warnings
import matplotlib.pyplot as mpl
import wcs_util
import numpy as np
import string
from matplotlib.font_manager import FontProperties
import angle_util as au
from decorators import auto_refresh, fixdocstring


class TickLabels(object):

    def __init__(self, parent):

        # Store references to axes
        self._ax1 = parent._ax1
        self._ax2 = parent._ax2
        self._wcs = parent._wcs
        self._figure = parent._figure

        # Set font
        self._label_fontproperties = FontProperties()

        self.set_style('plain')

        system, equinox, units = wcs_util.system(self._wcs)

        # Set default label format
        if system == 'celestial':
            self.set_xformat("hh:mm:ss.ss")
            self.set_yformat("dd:mm:ss.s")
        else:
            self.set_xformat("ddd.dddd")
            self.set_yformat("dd.dddd")

        # Set major tick formatters
        fx1 = WCSFormatter(wcs=self._wcs, coord='x')
        fy1 = WCSFormatter(wcs=self._wcs, coord='y')
        self._ax1.xaxis.set_major_formatter(fx1)
        self._ax1.yaxis.set_major_formatter(fy1)

        fx2 = mpl.NullFormatter()
        fy2 = mpl.NullFormatter()
        self._ax2.xaxis.set_major_formatter(fx2)
        self._ax2.yaxis.set_major_formatter(fy2)

    @auto_refresh
    def set_xformat(self, format):
        '''
        Set the format of the x-axis tick labels:

            * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
            * ``hh`` or ``dd`` - hours (or degrees)
            * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
            * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
            * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.

        If one of these arguments is not specified, the format for that axis is left unchanged.
        '''
        try:
            if not self._ax1.xaxis.apl_auto_tick_spacing:
                au._check_format_spacing_consistency(format, self._ax1.xaxis.apl_tick_spacing)
        except au.InconsistentSpacing:
            warnings.warn("WARNING: Requested label format is not accurate enough to display ticks. The label format will not be changed.")
            return

        self._ax1.xaxis.apl_label_form = format
        self._ax2.xaxis.apl_label_form = format

    @auto_refresh
    def set_yformat(self, format):
        '''
        Set the format of the y-axis tick labels:

            * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
            * ``hh`` or ``dd`` - hours (or degrees)
            * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
            * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
            * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.

        If one of these arguments is not specified, the format for that axis is left unchanged.
        '''
        try:
            if not self._ax1.yaxis.apl_auto_tick_spacing:
                au._check_format_spacing_consistency(format, self._ax1.yaxis.apl_tick_spacing)
        except au.InconsistentSpacing:
            warnings.warn("WARNING: Requested label format is not accurate enough to display ticks. The label format will not be changed.")
            return
        
        self._ax1.yaxis.apl_label_form = format
        self._ax2.yaxis.apl_label_form = format

    @auto_refresh
    def set_style(self, style):
        """
        Set the format of the x-axis tick labels. This can be 'colons' or 'plain':

            * 'colons' uses colons as separators, for example 31:41:59.26 +27:18:28.1
            * 'plain' uses letters and symbols as separators, for example 31h41m59.26s +27º18'28.1"
        """

        if style is 'latex':
            warnings.warn("latex has now been merged with plain - whether or not to use LaTeX is controled through set_system_latex")
            style = 'plain'

        if not style in ['colons', 'plain']:
            raise Exception("Label style should be one of colons/plain")

        self._ax1.xaxis.apl_labels_style = style
        self._ax1.yaxis.apl_labels_style = style

    @auto_refresh
    @fixdocstring
    def set_font(self, family=None, style=None, variant=None, stretch=None, weight=None, size=None, fontproperties=None):
        """
        Set the font of the tick labels

        Optional Keyword Arguments:

        common: family, style, variant, stretch, weight, size, fontproperties

        Default values are set by matplotlib or previously set values if
        set_font has already been called. Global default values can be set by
        editing the matplotlibrc file.
        """

        if family:
            self._label_fontproperties.set_family(family)

        if style:
            self._label_fontproperties.set_style(style)

        if variant:
            self._label_fontproperties.set_variant(variant)

        if stretch:
            self._label_fontproperties.set_stretch(stretch)

        if weight:
            self._label_fontproperties.set_weight(weight)

        if size:
            self._label_fontproperties.set_size(size)

        if fontproperties:
            self._label_fontproperties = fontproperties

        for tick in self._ax1.get_xticklabels():
            tick.set_fontproperties(self._label_fontproperties)
        for tick in self._ax1.get_yticklabels():
            tick.set_fontproperties(self._label_fontproperties)

    @auto_refresh
    def show(self):
        """
        Show the x- and y-axis tick labels
        """

        for tick in self._ax1.get_xticklabels():
            tick.set_visible(True)
        for tick in self._ax1.get_yticklabels():
            tick.set_visible(True)

    @auto_refresh
    def hide(self):
        """
        Hide the x- and y-axis tick labels
        """

        for tick in self._ax1.get_xticklabels():
            tick.set_visible(False)
        for tick in self._ax1.get_yticklabels():
            tick.set_visible(False)

    @auto_refresh
    def show_x(self):
        """
        Show the x-axis tick labels
        """

        for tick in self._ax1.get_xticklabels():
            tick.set_visible(True)

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis tick labels
        """

        for tick in self._ax1.get_xticklabels():
            tick.set_visible(False)

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis tick labels
        """

        for tick in self._ax1.get_yticklabels():
            tick.set_visible(True)

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis tick labels
        """

        for tick in self._ax1.get_yticklabels():
            tick.set_visible(False)

    def _cursor_position(self, x, y):

        xaxis = self._ax1.xaxis
        yaxis = self._ax1.yaxis

        xw, yw = wcs_util.pix2world(self._wcs, x, y)

        xw = au.Angle(degrees=xw, latitude=False)
        yw = au.Angle(degrees=yw, latitude=True)

        hours = 'h' in xaxis.apl_label_form

        if hours:
            xw = xw.tohours()

        if xaxis.apl_labels_style in ['plain', 'latex']:
            sep = ('d', 'm', 's')
            if hours:
                sep = ('h', 'm', 's')
        elif xaxis.apl_labels_style == 'colons':
            sep = (':', ':', '')

        xlabel = xw.tostringlist(format=xaxis.apl_label_form, sep=sep)

        if yaxis.apl_labels_style in ['plain', 'latex']:
            sep = ('d', 'm', 's')
            if hours:
                sep = ('h', 'm', 's')
        elif yaxis.apl_labels_style == 'colons':
            sep = (':', ':', '')

        ylabel = yw.tostringlist(format=yaxis.apl_label_form, sep=sep)

        return string.join(xlabel, "") + " " + string.join(ylabel, "")


class WCSFormatter(mpl.Formatter):

    def __init__(self, wcs=False, coord='x'):
        self._wcs = wcs
        self.coord = coord

    def __call__(self, x, pos=None):
        'Return the format for tick val x at position pos; pos=None indicated unspecified'

        au._check_format_spacing_consistency(self.axis.apl_label_form, self.axis.apl_tick_spacing)

        hours = 'h' in self.axis.apl_label_form

        if self.axis.apl_labels_style == 'plain':
            if mpl.rcParams['text.usetex']:
                label_style = 'plain_tex'
            else:
                label_style = 'plain_notex'
        else:
            label_style = self.axis.apl_labels_style

        if label_style == 'plain_notex':
            sep = (u'\u00b0', u"'", u'"')
            if hours:
                sep = ('h', 'm', 's')
        elif label_style == 'colons':
            sep = (':', ':', '')
        elif label_style == 'plain_tex':
            if hours:
                sep = ('^{h}', '^{m}', '^{s}')
            else:
                sep = ('^{\circ}', '^{\prime}', '^{\prime\prime}')

        ipos = np.argmin(np.abs(self.axis.apl_tick_positions_pix-x))

        label = self.axis.apl_tick_spacing * self.axis.apl_tick_positions_world[ipos]
        if hours:
            label = label.tohours()
        label = label.tostringlist(format=self.axis.apl_label_form, sep=sep)

        if self.coord == x or self.axis.apl_tick_positions_world[ipos] > 0:
            comp_ipos = ipos - 1
        else:
            comp_ipos = ipos + 1

        if comp_ipos >= 0 and comp_ipos <= len(self.axis.apl_tick_positions_pix)-1:

            comp_label = self.axis.apl_tick_spacing * self.axis.apl_tick_positions_world[comp_ipos]
            if hours:
                comp_label = comp_label.tohours()
            comp_label = comp_label.tostringlist(format=self.axis.apl_label_form, sep=sep)

            for iter in range(len(label)):
                if comp_label[0] == label[0]:
                    label.pop(0)
                    comp_label.pop(0)
                else:
                    break

        if mpl.rcParams['text.usetex']:
            return "$"+string.join(label, "")+"$"
        else:
            return string.join(label, "")
