from __future__ import absolute_import, print_function, division

import warnings
import numbers

import numpy as np
from matplotlib.collections import LineCollection

from .decorators import auto_refresh


class Grid(object):

    @auto_refresh
    def __init__(self, parent):

        # Save axes and wcs information
        self.ax = parent.ax
        self._wcs = parent._wcs
        self._figure = parent._figure
        self.x = parent.x
        self.y = parent.y
        self.x_unit = self._wcs.wcs.cunit[self.x]
        self.y_unit = self._wcs.wcs.cunit[self.y]
        self.grid_type = parent.grid_type

        # Save plotting parameters (required for @auto_refresh)
        self._parameters = parent._parameters

        # TODO: What to do about this?
        # Set grid event handler
        # self.ax.callbacks.connect('xlim_changed', self._update_norefresh)
        # self.ax.callbacks.connect('ylim_changed', self._update_norefresh)

        # Set defaults
        self.default_color = 'white'
        self.default_alpha = 0.5

    @auto_refresh
    def set_xspacing(self, xspacing):
        '''
        Set the grid line spacing in the longitudinal direction

        Parameters
        ----------
        xspacing : { float, str }
            The spacing in the longitudinal direction. To set the spacing
            to be the same as the ticks, set this to 'tick'
        '''
        if xspacing == 'tick':
            self.ax.coords[self.x].grid(grid_type=self.grid_type)
        elif isinstance(xspacing, (numbers.Integral, numbers.Real)):
            self.ax.coords[self.x].set_ticks(spacing=xspacing * self.x_unit)
        else:
            raise ValueError("Grid spacing should be a scalar or 'tick'")

    @auto_refresh
    def set_yspacing(self, yspacing):
        '''
        Set the grid line spacing in the latitudinal direction

        Parameters
        ----------
        yspacing : { float, str }
            The spacing in the latitudinal direction. To set the spacing
            to be the same as the ticks, set this to 'tick'
        '''
        if yspacing == 'tick':
            self.ax.coords[self.y].grid(grid_type=self.grid_type)
        elif isinstance(yspacing, (numbers.Integral, numbers.Real)):
            self.ax.coords[self.y].set_ticks(spacing=yspacing * self.y_unit)
        else:
            raise ValueError("Grid spacing should be a scalar or 'tick'")

    @auto_refresh
    def set_color(self, color):
        '''
        Set the color of the grid lines

        Parameters
        ----------
        color : str
            The color of the grid lines
        '''
        self.default_color = color
        self.ax.coords[self.x].grid(color=color, grid_type=self.grid_type)
        self.ax.coords[self.y].grid(color=color, grid_type=self.grid_type)

    @auto_refresh
    def set_alpha(self, alpha):
        '''
        Set the alpha (transparency) of the grid lines

        Parameters
        ----------
        alpha : float
            The alpha value of the grid. This should be a floating
            point value between 0 and 1, where 0 is completely
            transparent, and 1 is completely opaque.
        '''
        self.default_alpha = alpha
        self.ax.coords[self.x].grid(alpha=alpha, grid_type=self.grid_type)
        self.ax.coords[self.y].grid(alpha=alpha, grid_type=self.grid_type)

    @auto_refresh
    def set_linewidth(self, linewidth):
        self.ax.coords[self.x].grid(linewidth=linewidth, grid_type=self.grid_type)
        self.ax.coords[self.y].grid(linewidth=linewidth, grid_type=self.grid_type)

    @auto_refresh
    def set_linestyle(self, linestyle):
        self.ax.coords[self.x].grid(linestyle=linestyle, grid_type=self.grid_type)
        self.ax.coords[self.y].grid(linestyle=linestyle, grid_type=self.grid_type)

    @auto_refresh
    def show(self):
        self.ax.coords[self.x].grid(grid_type=self.grid_type,
                                    color=self.default_color,
                                    alpha=self.default_alpha)
        self.ax.coords[self.y].grid(grid_type=self.grid_type,
                                    color=self.default_color,
                                    alpha=self.default_alpha)

    @auto_refresh
    def hide(self):
        self.ax.coords[self.x].grid(grid_type=self.grid_type, draw_grid=False)
        self.ax.coords[self.y].grid(grid_type=self.grid_type, draw_grid=False)
