from __future__ import absolute_import, print_function, division

from matplotlib.font_manager import FontProperties

from . import wcs_util
from .decorators import auto_refresh, fixdocstring


class AxisLabels(object):

    def __init__(self,  axes, x, y, parameters):
        self._ax = axes
        self._wcs = self._ax.wcs
        self.x = x
        self.y = y

        # Save plotting parameters (required for @auto_refresh)
        self._parameters = parameters

        # Set font
        self._label_fontproperties = FontProperties()

        # TODO: Get rid of this part
        system, equinox, units = wcs_util.system(self._wcs, dimensions=[self.x, self.y])

        if system['name'] == 'equatorial':

            if equinox == 'b1950':
                xtext = 'RA (B1950)'
                ytext = 'Dec (B1950)'
            else:
                xtext = 'RA (J2000)'
                ytext = 'Dec (J2000)'

        elif system['name'] == 'galactic':

            xtext = 'Galactic Longitude'
            ytext = 'Galactic Latitude'

        elif system['name'] == 'ecliptic':

            xtext = 'Ecliptic Longitude'
            ytext = 'Ecliptic Latitude'

        elif system['name'] == 'unknown':

#            xunit = " (%s)" % self._wcs.cunit_x if self._wcs.cunit_x not in ["", None] else ""
#            yunit = " (%s)" % self._wcs.cunit_y if self._wcs.cunit_y not in ["", None] else ""
            xunit = " (%s)" % self._wcs.wcs.ctype[self.x] if self._wcs.wcs.ctype[self.x] not in ["", None] else ""
            yunit = " (%s)" % self._wcs.wcs.ctype[self.y] if self._wcs.wcs.ctype[self.y] not in ["", None] else ""

#            if len(self._wcs.cname_x) > 0:
#                xtext = self._wcs.cname_x + xunit
            if len(self._wcs.wcs.cname[self.x]) > 0:
                xtext = self._wcs.wcs.cname[self.x] + xunit
            else:
                if len(self._wcs.wcs.ctype[self.x]) == 8 and self._wcs.wcs.ctype[self.x] == '-':
                    xtext = self._wcs.wcs.ctype[self.x][:4].replace('-', '') + xunit
                else:
                    xtext = self._wcs.wcs.ctype[self.x] + xunit

            if len(self._wcs.wcs.cname[self.y]) > 0:
                ytext = self._wcs.wcs.cname[self.y] + yunit
            else:
                if len(self._wcs.wcs.ctype[self.y]) == 8 and self._wcs.wcs.ctype[self.y][4] == '-':
                    ytext = self._wcs.wcs.ctype[self.y][:4].replace('-', '') + yunit
                else:
                    ytext = self._wcs.wcs.ctype[self.y] + yunit

        if system['inverted']:
            xtext, ytext = ytext, xtext

        self.set_xtext(xtext)
        self.set_ytext(ytext)

        self.set_xposition('bottom')
        self.set_yposition('left')

    @auto_refresh
    def set_xtext(self, label):
        """
        Set the x-axis label text.
        """
        self._x_text = label
        self._ax.coords[self.x].set_axislabel(label)

    @auto_refresh
    def set_ytext(self, label):
        """
        Set the y-axis label text.
        """
        self._y_text = label
        self._ax.coords[self.y].set_axislabel(label)

    @auto_refresh
    def set_xpad(self, pad):
        """
        Set the x-axis label displacement, in points.
        """
        self._ax.coords[self.x].set_axislabel(self._x_text, minpad=pad)

    @auto_refresh
    def set_ypad(self, pad):
        """
        Set the y-axis label displacement, in points.
        """
        self._ax.coords[self.y].set_axislabel(self._y_text, minpad=pad)

    @auto_refresh
    @fixdocstring
    def set_font(self,  **kwargs):
        """
        Set the font of the axis labels.

        Parameters
        ----------

        common: family, style, variant, stretch, weight, size, fontproperties

        Notes
        -----

        Default values are set by matplotlib or previously set values if
        set_font has already been called. Global default values can be set by
        editing the matplotlibrc file.
        """
        self._ax.coords[self.x].set_axislabel(self._x_text, **kwargs)
        self._ax.coords[self.y].set_axislabel(self._y_text, **kwargs)

    @auto_refresh
    def show(self):
        """
        Show the x- and y-axis labels.
        """
        self.show_x()
        self.show_y()

    @auto_refresh
    def hide(self):
        """
        Hide the x- and y-axis labels.
        """
        self.hide_x()
        self.hide_y()

    @auto_refresh
    def show_x(self):
        """
        Show the x-axis label.
        """
        if self._xposition == 'bottom':
            self._ax.coords[self.x].set_axislabel_position('b')
        else:
            self._ax.coords[self.x].set_axislabel_position('t')

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis label.
        """
        self._ax.coords[self.x].set_axislabel_position('')

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis label.
        """
        if self._yposition == 'left':
            self._ax.coords[self.y].set_axislabel_position('l')
        else:
            self._ax.coords[self.y].set_axislabel_position('r')

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis label.
        """
        self._ax.coords[self.y].set_axislabel_position('')

    @auto_refresh
    def set_xposition(self, position):
        "Set the position of the x-axis label ('top' or 'bottom')"
        if position == 'bottom':
            self._ax.coords[self.x].set_axislabel_position('b')
        elif position == 'top':
            self._ax.coords[self.x].set_axislabel_position('t')
        else:
            raise ValueError("position should be one of 'top' or 'bottom'")
        self._xposition = position

    @auto_refresh
    def set_yposition(self, position):
        "Set the position of the y-axis label ('left' or 'right')"
        if position == 'left':
            self._ax.coords[self.y].set_axislabel_position('l')
        elif position == 'right':
            self._ax.coords[self.y].set_axislabel_position('r')
        else:
            raise ValueError("position should be one of 'left' or 'right'")
        self._yposition = position
