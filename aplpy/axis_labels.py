from __future__ import absolute_import, print_function, division

from .decorators import auto_refresh, fixdocstring


class AxisLabels(object):

    def __init__(self, parent):

        self._ax = parent.ax
        self._wcs = parent.ax.wcs
        self.x = parent.x
        self.y = parent.y

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
