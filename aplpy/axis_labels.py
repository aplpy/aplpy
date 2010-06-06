import wcs_util
from matplotlib.font_manager import FontProperties
from decorators import auto_refresh, fixdocstring

class AxisLabels(object):

    def __init__(self, parent):

        # Store references to axes
        self._ax1 = parent._ax1
        self._ax2 = parent._ax2
        self._wcs = parent._wcs
        self._figure = parent._figure

        # Set font
        self._label_fontproperties = FontProperties()

        self._ax2.yaxis.set_label_position('right')
        self._ax2.xaxis.set_label_position('top')

        system, equinox, units = wcs_util.system(self._wcs)

        if system == 'celestial':
            if equinox == 'b1950':
                self.set_xtext('RA (B1950)')
                self.set_ytext('Dec (B1950)')
            else:
                self.set_xtext('RA (J2000)')
                self.set_ytext('Dec (J2000)')
        elif system == 'galactic':
            self.set_xtext('Galactic Longitude')
            self.set_ytext('Galactic Latitude')
        else:
            self.set_xtext('Ecliptic Longitude')
            self.set_ytext('Ecliptic Latitude')

    @auto_refresh
    def set_xtext(self, label):
        """
        Set the x-axis label text
        """
        self.xlabel = self._ax1.set_xlabel(label)

    @auto_refresh
    def set_ytext(self, label):
        """
        Set the y-axis label text
        """
        self.ylabel = self._ax1.set_ylabel(label)

    @auto_refresh
    def set_xpad(self, pad):
        """
        Set the x-axis label displacement, in points
        """
        self.xlabel = self._ax1.set_xlabel(self.xlabel.get_text(), labelpad=pad)

    @auto_refresh
    def set_ypad(self, pad):
        """
        Set the x-axis label displacement, in points
        """
        self.ylabel = self._ax1.set_ylabel(self.ylabel.get_text(), labelpad=pad)

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

        self.xlabel.set_fontproperties(self._label_fontproperties)
        self.ylabel.set_fontproperties(self._label_fontproperties)

    @auto_refresh
    def show(self):
        """
        Show the x- and y-axis labels
        """

        if self.xlabel:
            self.xlabel.set_visible(True)
        if self.ylabel:
            self.ylabel.set_visible(True)

    @auto_refresh
    def hide(self):
        """
        Hide the x- and y-axis labels
        """

        if self.xlabel:
            self.xlabel.set_visible(False)
        if self.ylabel:
            self.ylabel.set_visible(False)

    @auto_refresh
    def show_x(self):
        """
        Show the x-axis label
        """

        if self.xlabel:
            self.xlabel.set_visible(True)

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis label
        """

        if self.xlabel:
            self.xlabel.set_visible(False)

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis label
        """

        if self.ylabel:
            self.ylabel.set_visible(True)

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis label
        """

        if self.ylabel:
            self.ylabel.set_visible(False)
