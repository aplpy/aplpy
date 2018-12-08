from __future__ import absolute_import, print_function, division

from astropy.wcs.utils import wcs_to_celestial_frame
from astropy.coordinates import (ICRS, FK5, FK4, Galactic,
                                 HeliocentricTrueEcliptic,
                                 BarycentricTrueEcliptic)

from .decorators import auto_refresh, fixdocstring

__all__ = ['AxisLabels']


class AxisLabels(object):

    def __init__(self, parent):

        self._ax = parent.ax
        self._wcs = parent.ax.wcs
        self.x = parent.x
        self.y = parent.y

        self._ax.coords[self.x].set_axislabel_visibility_rule('always')
        self._ax.coords[self.y].set_axislabel_visibility_rule('always')

        xcoord_type = self._ax.coords[self.x].coord_type
        ycoord_type = self._ax.coords[self.y].coord_type

        if xcoord_type == 'longitude' and ycoord_type == 'latitude':
            celestial = True
            inverted = False
        elif xcoord_type == 'latitude' and ycoord_type == 'longitude':
            celestial = True
            inverted = True
        else:
            celestial = inverted = False

        if celestial:
            frame = wcs_to_celestial_frame(self._wcs)
        else:
            frame = None

        if isinstance(frame, ICRS):

            xtext = 'RA (ICRS)'
            ytext = 'Dec (ICRS)'

        elif isinstance(frame, FK5):

            equinox = "{:g}".format(FK5.equinox.jyear)
            xtext = 'RA (J{0})'.format(equinox)
            ytext = 'Dec (J{0})'.format(equinox)

        elif isinstance(frame, FK4):

            equinox = "{:g}".format(FK4.equinox.byear)
            xtext = 'RA (B{0})'.format(equinox)
            ytext = 'Dec (B{0})'.format(equinox)

        elif isinstance(frame, Galactic):

            xtext = 'Galactic Longitude'
            ytext = 'Galactic Latitude'

        elif isinstance(frame, (HeliocentricTrueEcliptic, BarycentricTrueEcliptic)):

            # NOTE: once we support only Astropy 2.0+, we can use BaseEclipticFrame

            xtext = 'Ecliptic Longitude'
            ytext = 'Ecliptic Latitude'

        else:

            cunit_x = self._wcs.wcs.cunit[self.x]
            cunit_y = self._wcs.wcs.cunit[self.y]

            cname_x = self._wcs.wcs.cname[self.x]
            cname_y = self._wcs.wcs.cname[self.y]

            ctype_x = self._wcs.wcs.ctype[self.x]
            ctype_y = self._wcs.wcs.ctype[self.y]

            xunit = " (%s)" % cunit_x if cunit_x not in ["", None] else ""
            yunit = " (%s)" % cunit_y if cunit_y not in ["", None] else ""

            if len(cname_x) > 0:
                xtext = cname_x + xunit
            else:
                if len(ctype_x) == 8 and ctype_x[4] == '-':
                    xtext = ctype_x[:4].replace('-', '') + xunit
                else:
                    xtext = ctype_x + xunit

            if len(cname_y) > 0:
                ytext = cname_y + yunit
            else:
                if len(ctype_y) == 8 and ctype_y[4] == '-':
                    ytext = ctype_y[:4].replace('-', '') + yunit
                else:
                    ytext = ctype_y + yunit

        if inverted:
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
        Set the x-axis label displacement in terms of the axis label font size.
        """
        self._ax.coords[self.x].axislabels.set_minpad(pad)

    @auto_refresh
    def set_ypad(self, pad):
        """
        Set the y-axis label displacement in terms of the axis label font size.
        """
        self._ax.coords[self.y].axislabels.set_minpad(pad)

    @auto_refresh
    @fixdocstring
    def set_font(self, **kwargs):
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
        self._ax.coords[self.x].axislabels.set(**kwargs)
        self._ax.coords[self.y].axislabels.set(**kwargs)

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
        """
        Set the position of the x-axis label ('top' or 'bottom')
        """
        if position == 'bottom':
            self._ax.coords[self.x].set_axislabel_position('b')
        elif position == 'top':
            self._ax.coords[self.x].set_axislabel_position('t')
        else:
            raise ValueError("position should be one of 'top' or 'bottom'")
        self._xposition = position

    @auto_refresh
    def set_yposition(self, position):
        """
        Set the position of the y-axis label ('left' or 'right')
        """
        if position == 'left':
            self._ax.coords[self.y].set_axislabel_position('l')
        elif position == 'right':
            self._ax.coords[self.y].set_axislabel_position('r')
        else:
            raise ValueError("position should be one of 'left' or 'right'")
        self._yposition = position
