from __future__ import absolute_import, print_function, division

from .decorators import auto_refresh


class Frame(object):

    @auto_refresh
    def __init__(self, parent):
        self.ax = parent.ax

    @auto_refresh
    def set_linewidth(self, linewidth):
        """
        Set line width of the frame.

        Parameters
        ----------
        linewidth:
            The linewidth to use for the frame.
        """
        self.ax.coords.frame.set_linewidth(linewidth)

    @auto_refresh
    def set_color(self, color):
        """
        Set color of the frame.

        Parameters
        ----------
        color:
            The color to use for the frame.
        """
        self.ax.coords.frame.set_color(color)
