from .decorators import auto_refresh


class Ticks(object):

    @auto_refresh
    def __init__(self, parent):
        self._figure = parent._figure
        self._ax = parent.ax
        self.x = parent.x
        self.y = parent.y
        self._wcs = self._ax.wcs

    def set_tick_direction(self, direction):
        """
        Set the direction of the ticks to be facing out of the axes (``out``)
        or into the axes (``in``).
        """
        if direction in ('in', 'out'):
            self._ax.coords[self.x].ticks.set_tick_out(direction == 'out')
            self._ax.coords[self.y].ticks.set_tick_out(direction == 'out')
        else:
            raise ValueError("direction should be 'in' or 'out'")

    @auto_refresh
    def set_xspacing(self, spacing):
        """
        Set the x-axis tick spacing, in degrees. To set the tick spacing to be
        automatically determined, set this to 'auto'.
        """
        self._set_spacing(self.x, spacing)

    @auto_refresh
    def set_yspacing(self, spacing):
        """
        Set the y-axis tick spacing, in degrees. To set the tick spacing to be
        automatically determined, set this to 'auto'.
        """
        self._set_spacing(self.y, spacing)

    @auto_refresh
    def _set_spacing(self, coord, spacing):
        if spacing == 'auto':
            self._ax.coords[coord].set_ticks(spacing=None)
        else:
            coord_unit = self._wcs.wcs.cunit[coord]
            self._ax.coords[coord].set_ticks(spacing=spacing * coord_unit)

    @auto_refresh
    def set_color(self, color):
        """
        Set the color of the ticks
        """
        self._ax.coords[self.x].set_ticks(color=color)
        self._ax.coords[self.y].set_ticks(color=color)

    @auto_refresh
    def set_length(self, length, minor_factor=0.5):
        """
        Set the length of the ticks (in points)
        """
        # TODO: Can't set minor ticksize. Should we just remove that?
        # Not mentioned in the APLpy in docs either
        self._ax.coords[self.x].set_ticks(size=length)
        self._ax.coords[self.y].set_ticks(size=length)

    @auto_refresh
    def set_linewidth(self, linewidth):
        """
        Set the linewidth of the ticks (in points)
        """
        self._ax.coords[self.x].set_ticks(width=linewidth)
        self._ax.coords[self.y].set_ticks(width=linewidth)

    @auto_refresh
    def set_minor_frequency(self, xfrequency, yfrequency=None):
        '''
        Set the number of subticks per major tick.

        Set to one to hide minor ticks. If not yfrequency given, frequency is
        the same in both axis. Otherwise, xfrequency represents the frequency in
        the xaxis and yfrequency the one in the yaxis.
        '''

        if yfrequency is None:
            yfrequency = xfrequency

        self._ax.coords[self.x].set_minor_frequency(xfrequency)
        self._ax.coords[self.y].set_minor_frequency(yfrequency)

    @auto_refresh
    def show(self):
        """
        Show the x- and y-axis ticks
        """
        self.show_x()
        self.show_y()

    @auto_refresh
    def hide(self):
        """
        Hide the x- and y-axis ticks
        """
        self.hide_x()
        self.hide_y()

    @auto_refresh
    def show_x(self):
        """
        Show the x-axis ticks
        """
        self._ax.coords[self.x].set_ticks_visible(True)

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis ticks
        """
        self._ax.coords[self.x].set_ticks_visible(False)

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis ticks
        """
        self._ax.coords[self.y].set_ticks_visible(True)

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis ticks
        """
        self._ax.coords[self.y].set_ticks_visible(False)
