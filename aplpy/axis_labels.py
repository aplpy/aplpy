import wcs_util
from matplotlib.font_manager import FontProperties
from decorators import auto_refresh, fixdocstring


class AxisLabels(object):

    def __init__(self, parent, userwcs=False):

        # Store references to axes
        self._ax1 = parent._ax1
        self._ax2 = parent._ax2
        self._wcs = parent._wcs
        self._figure = parent._figure

        # Set font
        self._label_fontproperties = FontProperties()

        self._ax2.yaxis.set_label_position('right')
        self._ax2.xaxis.set_label_position('top')

        system, equinox, units = wcs_util.system(self._wcs,userwcs=userwcs)

        if system == 'equatorial':
            if equinox == 'b1950':
                self.set_xtext('RA (B1950)')
                self.set_ytext('Dec (B1950)')
            else:
                self.set_xtext('RA (J2000)')
                self.set_ytext('Dec (J2000)')
        elif system == 'galactic':
            self.set_xtext('Galactic Longitude')
            self.set_ytext('Galactic Latitude')
        elif userwcs:
            header = parent._hdu.header
            xunit = " (%s)" % header.get('CUNIT1') if header.has_key('CUNIT1') else ''
            yunit = " (%s)" % header.get('CUNIT2') if header.has_key('CUNIT2') else ''
            if header.has_key('CNAME1') and header.has_key('CNAME2'):
                self.set_xtext(header.get('CNAME1')+xunit)
                self.set_ytext(header.get('CNAME2')+yunit)
            else: 
                self.set_xtext('User Coordinate 1'+xunit)
                self.set_ytext('User Coordinate 2'+yunit)
        else:
            self.set_xtext('Ecliptic Longitude')
            self.set_ytext('Ecliptic Latitude')

        self.set_xposition('bottom')
        self.set_yposition('left')

    @auto_refresh
    def set_xtext(self, label):
        """
        Set the x-axis label text
        """
        self._xlabel1 = self._ax1.set_xlabel(label)
        self._xlabel2 = self._ax2.set_xlabel(label)

    @auto_refresh
    def set_ytext(self, label):
        """
        Set the y-axis label text
        """
        self._ylabel1 = self._ax1.set_ylabel(label)
        self._ylabel2 = self._ax2.set_ylabel(label)

    @auto_refresh
    def set_xpad(self, pad):
        """
        Set the x-axis label displacement, in points
        """
        self._xlabel1 = self._ax1.set_xlabel(self._xlabel1.get_text(), labelpad=pad)
        self._xlabel2 = self._ax2.set_xlabel(self._xlabel2.get_text(), labelpad=pad)

    @auto_refresh
    def set_ypad(self, pad):
        """
        Set the y-axis label displacement, in points
        """
        self._ylabel1 = self._ax1.set_ylabel(self._ylabel1.get_text(), labelpad=pad)
        self._ylabel2 = self._ax2.set_ylabel(self._ylabel2.get_text(), labelpad=pad)

    @auto_refresh
    @fixdocstring
    def set_font(self, family=None, style=None, variant=None, stretch=None, weight=None, size=None, fontproperties=None):
        """
        Set the font of the axis labels

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

        self._xlabel1.set_fontproperties(self._label_fontproperties)
        self._xlabel2.set_fontproperties(self._label_fontproperties)
        self._ylabel1.set_fontproperties(self._label_fontproperties)
        self._ylabel2.set_fontproperties(self._label_fontproperties)

    @auto_refresh
    def show(self):
        """
        Show the x- and y-axis labels
        """
        self.show_x()
        self.show_y()

    @auto_refresh
    def hide(self):
        """
        Hide the x- and y-axis labels
        """
        self.hide_x()
        self.hide_y()

    @auto_refresh
    def show_x(self):
        """
        Show the x-axis label
        """
        if self._xposition == 'bottom':
            self._xlabel1.set_visible(True)
        else:
            self._xlabel2.set_visible(True)

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis label
        """
        if self._xposition == 'bottom':
            self._xlabel1.set_visible(False)
        else:
            self._xlabel2.set_visible(False)

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis label
        """
        if self._yposition == 'left':
            self._ylabel1.set_visible(True)
        else:
            self._ylabel2.set_visible(True)

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis label
        """
        if self._yposition == 'left':
            self._ylabel1.set_visible(False)
        else:
            self._ylabel2.set_visible(False)

    @auto_refresh
    def set_xposition(self, position):
        "Set the position of the x-axis label ('top' or 'bottom')"
        if position == 'bottom':
            self._xlabel1.set_visible(True)
            self._xlabel2.set_visible(False)
        elif position == 'top':
            self._xlabel1.set_visible(False)
            self._xlabel2.set_visible(True)
        else:
            raise Exception("position should be one of 'top' or 'bottom'")
        self._xposition = position

    @auto_refresh
    def set_yposition(self, position):
        "Set the position of the y-axis label ('left' or 'right')"
        if position == 'left':
            self._ylabel1.set_visible(True)
            self._ylabel2.set_visible(False)
        elif position == 'right':
            self._ylabel1.set_visible(False)
            self._ylabel2.set_visible(True)
        else:
            raise Exception("position should be one of 'left' or 'right'")
        self._yposition = position
