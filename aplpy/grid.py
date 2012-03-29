import warnings

import numpy as np
from matplotlib.collections import LineCollection

from . import math_util
from . import wcs_util
from . import angle_util as au
from .ticks import tick_positions, default_spacing
from .decorators import auto_refresh


class Grid(object):

    @auto_refresh
    def __init__(self, parent):

        # Save axes and wcs information
        self.ax = parent._ax1
        self._wcs = parent._wcs
        self._figure = parent._figure

        # Save plotting parameters (required for @auto_refresh)
        self._parameters = parent._parameters

        # Initialize grid container
        self._grid = None
        self._active = False

        # Set defaults
        self.x_auto_spacing = True
        self.y_auto_spacing = True
        self.default_color = 'white'
        self.default_alpha = 0.5

        # Set grid event handler
        self.ax.callbacks.connect('xlim_changed', self._update_norefresh)
        self.ax.callbacks.connect('ylim_changed', self._update_norefresh)

    @auto_refresh
    def _remove(self):
        self._grid.remove()

    @auto_refresh
    def set_xspacing(self, xspacing):
        '''
        Set the grid line spacing in the longitudinal direction

        Required Arguments:

            *xspacing*: [ float | 'tick' ]
                The spacing in the longitudinal direction. To set the spacing
                to be the same as the ticks, set this to 'tick'
        '''
        if xspacing == 'tick':
            self.x_auto_spacing = True
        elif np.isreal(xspacing):
            self.x_auto_spacing = False
            if self._wcs.xaxis_coord_type in ['longitude', 'latitude']:
                self.x_grid_spacing = au.Angle(degrees=xspacing, latitude=self._wcs.xaxis_coord_type == 'latitude')
            else:
                self.x_grid_spacing = xspacing
        else:
            raise ValueError("Grid spacing should be a scalar or 'tick'")

        self._update()

    @auto_refresh
    def set_yspacing(self, yspacing):
        '''
        Set the grid line spacing in the latitudinal direction

        Required Arguments:

            *yspacing*: [ float | 'tick' ]
                The spacing in the latitudinal direction. To set the spacing
                to be the same as the ticks, set this to 'tick'
        '''

        if yspacing == 'tick':
            self.y_auto_spacing = True
        elif np.isreal(yspacing):
            self.y_auto_spacing = False
            if self._wcs.yaxis_coord_type in ['longitude', 'latitude']:
                self.y_grid_spacing = au.Angle(degrees=yspacing, latitude=self._wcs.yaxis_coord_type == 'latitude')
            else:
                self.y_grid_spacing = yspacing
        else:
            raise ValueError("Grid spacing should be a scalar or 'tick'")

        self._update()

    @auto_refresh
    def set_color(self, color):
        '''
        Set the color of the grid lines

        Required Arguments:

            *color*: [ string ]
                The color of the grid lines
        '''
        if self._grid:
            self._grid.set_edgecolor(color)
        else:
            self.default_color = color

    @auto_refresh
    def set_alpha(self, alpha):
        '''
        Set the alpha (transparency) of the grid lines

        Required Arguments:

            *alpha*: [ float ]
                The alpha value of the grid. This should be a floating
                point value between 0 and 1, where 0 is completely
                transparent, and 1 is completely opaque.
        '''
        if self._grid:
            self._grid.set_alpha(alpha)
        else:
            self.default_alpha = alpha

    @auto_refresh
    def set_linewidth(self, linewidth):
        self._grid.set_linewidth(linewidth)

    @auto_refresh
    def set_linestyle(self, linestyle):
        self._grid.set_linestyle(linestyle)

    @auto_refresh
    def show(self):
        if self._grid:
            self._grid.set_visible(True)
        else:
            self._active = True
            self._update()
            self.set_color(self.default_color)
            self.set_alpha(self.default_alpha)

    @auto_refresh
    def hide(self):
        self._grid.set_visible(False)

    @auto_refresh
    def _update(self, *args):
        self._update_norefresh(*args)

    def _update_norefresh(self, *args):

        if not self._active:
            return self.ax

        if len(args) == 1:
            if id(self.ax) != id(args[0]):
                raise Exception("ax ids should match")

        lines = []

        # Set x grid spacing
        if self.x_auto_spacing:
            if self.ax.xaxis.apl_auto_tick_spacing:
                xspacing = default_spacing(self.ax, 'x', self.ax.xaxis.apl_label_form)
            else:
                xspacing = self.ax.xaxis.apl_tick_spacing
        else:
            xspacing = self.x_grid_spacing

        if xspacing is None:
            warnings.warn("Could not determine x tick spacing - grid cannot be drawn")
            return

        if self._wcs.xaxis_coord_type in ['longitude', 'latitude']:
            xspacing = xspacing.todegrees()

        # Set y grid spacing
        if self.y_auto_spacing:
            if self.ax.yaxis.apl_auto_tick_spacing:
                yspacing = default_spacing(self.ax, 'y', self.ax.yaxis.apl_label_form)
            else:
                yspacing = self.ax.yaxis.apl_tick_spacing
        else:
            yspacing = self.y_grid_spacing

        if yspacing is None:
            warnings.warn("Could not determine y tick spacing - grid cannot be drawn")
            return

        if self._wcs.yaxis_coord_type in ['longitude', 'latitude']:
            yspacing = yspacing.todegrees()

        # Find x lines that intersect with axes
        grid_x_i, grid_y_i = find_intersections(self._wcs, 'x', xspacing)

        # Ensure that longitudes are between 0 and 360, and latitudes between
        # -90 and 90
        if self._wcs.xaxis_coord_type == 'longitude':
            grid_x_i = np.mod(grid_x_i, 360.)
        elif self._wcs.xaxis_coord_type == 'latitude':
            grid_x_i = np.mod(grid_x_i + 90., 180.) - 90.

        if self._wcs.yaxis_coord_type == 'longitude':
            grid_y_i = np.mod(grid_y_i, 360.)
        elif self._wcs.yaxis_coord_type == 'latitude':
            grid_y_i = np.mod(grid_y_i + 90., 180.) - 90.

        # If we are dealing with longitude/latitude then can search all
        # neighboring grid lines to see if there are any closed longitude
        # lines
        if self._wcs.xaxis_coord_type == 'latitude' and self._wcs.yaxis_coord_type == 'longitude' and len(grid_x_i) > 0:

            gx = grid_x_i.min()

            while True:
                gx -= xspacing
                xpix, ypix = wcs_util.world2pix(self._wcs, gx, 0.)
                if in_plot(self._wcs, xpix, ypix) and gx >= -90.:
                    grid_x_i = np.hstack([grid_x_i, gx, gx])
                    grid_y_i = np.hstack([grid_y_i, 0., 360.])
                else:
                    break

            gx = grid_x_i.max()

            while True:
                gx += xspacing
                xpix, ypix = wcs_util.world2pix(self._wcs, gx, 0.)
                if in_plot(self._wcs, xpix, ypix) and gx <= +90.:
                    grid_x_i = np.hstack([grid_x_i, gx, gx])
                    grid_y_i = np.hstack([grid_y_i, 0., 360.])
                else:
                    break

        # Plot those lines
        for gx in np.unique(grid_x_i):
            for line in plot_grid_x(self._wcs, grid_x_i, grid_y_i, gx):
                lines.append(line)

        # Find y lines that intersect with axes
        grid_x_i, grid_y_i = find_intersections(self._wcs, 'y', yspacing)

        if self._wcs.xaxis_coord_type == 'longitude':
            grid_x_i = np.mod(grid_x_i, 360.)
        elif self._wcs.xaxis_coord_type == 'latitude':
            grid_x_i = np.mod(grid_x_i + 90., 180.) - 90.

        if self._wcs.yaxis_coord_type == 'longitude':
            grid_y_i = np.mod(grid_y_i, 360.)
        elif self._wcs.yaxis_coord_type == 'latitude':
            grid_y_i = np.mod(grid_y_i + 90., 180.) - 90.

        # If we are dealing with longitude/latitude then can search all
        # neighboring grid lines to see if there are any closed longitude
        # lines
        if self._wcs.xaxis_coord_type == 'longitude' and self._wcs.yaxis_coord_type == 'latitude' and len(grid_y_i) > 0:

            gy = grid_y_i.min()

            while True:
                gy -= yspacing
                xpix, ypix = wcs_util.world2pix(self._wcs, 0., gy)
                if in_plot(self._wcs, xpix, ypix) and gy >= -90.:
                    grid_x_i = np.hstack([grid_x_i, 0., 360.])
                    grid_y_i = np.hstack([grid_y_i, gy, gy])
                else:
                    break

            gy = grid_y_i.max()

            while True:
                gy += yspacing
                xpix, ypix = wcs_util.world2pix(self._wcs, 0., gy)
                if in_plot(self._wcs, xpix, ypix) and gy <= +90.:
                    grid_x_i = np.hstack([grid_x_i, 0., 360.])
                    grid_y_i = np.hstack([grid_y_i, gy, gy])
                else:
                    break

        # Plot those lines
        for gy in np.unique(grid_y_i):
            for line in plot_grid_y(self._wcs, grid_x_i, grid_y_i, gy):
                lines.append(line)

        if self._grid:
            self._grid.set_verts(lines)
        else:
            self._grid = LineCollection(lines, transOffset=self.ax.transData)
            self.ax.add_collection(self._grid, False)

        return self.ax


def plot_grid_y(wcs, grid_x, grid_y, gy, alpha=0.5):
    '''Plot a single grid line in the y direction'''

    lines_out = []

    # Find intersections that correspond to latitude lat0
    index = np.where(grid_y == gy)

    # Produce sorted array of the longitudes of all intersections
    grid_x_sorted = np.sort(grid_x[index])

    # If coordinate type is a latitude or longitude, also need to check if
    # end-points fall inside the plot
    if wcs.xaxis_coord_type == 'latitude':
        if not np.any(grid_x_sorted == -90):
            xpix, ypix = wcs_util.world2pix(wcs, max(grid_x_sorted[0] - 1., -90.), gy)
            if in_plot(wcs, xpix, ypix):
                grid_x_sorted = np.hstack([-90., grid_x_sorted])
        if not np.any(grid_x_sorted == +90):
            xpix, ypix = wcs_util.world2pix(wcs, min(grid_x_sorted[-1] + 1., +90.), gy)
            if in_plot(wcs, xpix, ypix):
                grid_x_sorted = np.hstack([grid_x_sorted, +90.])
    elif wcs.xaxis_coord_type == 'longitude':
        if not np.any(grid_x_sorted == 0.):
            xpix, ypix = wcs_util.world2pix(wcs, max(grid_x_sorted[0] - 1., 0.), gy)
            if in_plot(wcs, xpix, ypix):
                grid_x_sorted = np.hstack([0., grid_x_sorted])
        if not np.any(grid_x_sorted == 360.):
            xpix, ypix = wcs_util.world2pix(wcs, min(grid_x_sorted[-1] + 1., 360.), gy)
            if in_plot(wcs, xpix, ypix):
                grid_x_sorted = np.hstack([grid_x_sorted, 360.])
    # Check that number of grid points is even
    if len(grid_x_sorted) % 2 == 1:
        warnings.warn("Unexpected number of grid points - x grid lines cannot be drawn")
        return []

    # Cycle through intersections
    for i in range(0, len(grid_x_sorted), 2):

        grid_x_min = grid_x_sorted[i]
        grid_x_max = grid_x_sorted[i + 1]

        x_world = math_util.complete_range(grid_x_min, grid_x_max, 100)
        y_world = np.repeat(gy, len(x_world))
        x_pix, y_pix = wcs_util.world2pix(wcs, x_world, y_world)
        lines_out.append(zip(x_pix, y_pix))

    return lines_out


def plot_grid_x(wcs, grid_x, grid_y, gx, alpha=0.5):
    '''Plot a single longitude line'''

    lines_out = []

    # Find intersections that correspond to longitude gx
    index = np.where(grid_x == gx)

    # Produce sorted array of the latitudes of all intersections
    grid_y_sorted = np.sort(grid_y[index])

    # If coordinate type is a latitude or longitude, also need to check if
    # end-points fall inside the plot
    if wcs.yaxis_coord_type == 'latitude':
        if not np.any(grid_y_sorted == -90):
            xpix, ypix = wcs_util.world2pix(wcs, gx, max(grid_y_sorted[0] - 1., -90.))
            if in_plot(wcs, xpix, ypix):
                grid_y_sorted = np.hstack([-90., grid_y_sorted])
        if not np.any(grid_y_sorted == +90):
            xpix, ypix = wcs_util.world2pix(wcs, gx, min(grid_y_sorted[-1] + 1., +90.))
            if in_plot(wcs, xpix, ypix):
                grid_y_sorted = np.hstack([grid_y_sorted, +90.])
    elif wcs.yaxis_coord_type == 'longitude':
        if not np.any(grid_y_sorted == 0.):
            xpix, ypix = wcs_util.world2pix(wcs, gx, max(grid_y_sorted[0] - 1., 0.))
            if in_plot(wcs, xpix, ypix):
                grid_y_sorted = np.hstack([0., grid_y_sorted])
        if not np.any(grid_y_sorted == 360.):
            xpix, ypix = wcs_util.world2pix(wcs, gx, min(grid_y_sorted[-1] + 1., 360.))
            if in_plot(wcs, xpix, ypix):
                grid_y_sorted = np.hstack([grid_y_sorted, 360.])

    # Check if the first mid-point with coordinates is inside the viewport
    xpix, ypix = wcs_util.world2pix(wcs, gx, (grid_y_sorted[0] + grid_y_sorted[1]) / 2.)

    if not in_plot(wcs, xpix, ypix):
        grid_y_sorted = np.roll(grid_y_sorted, 1)

    # Check that number of grid points is even
    if len(grid_y_sorted) % 2 == 1:
        warnings.warn("Unexpected number of grid points - y grid lines cannot be drawn")
        return []

    # Cycle through intersections
    for i in range(0, len(grid_y_sorted), 2):

        grid_y_min = grid_y_sorted[i]
        grid_y_max = grid_y_sorted[i + 1]

        y_world = math_util.complete_range(grid_y_min, grid_y_max, 100)
        x_world = np.repeat(gx, len(y_world))
        x_pix, y_pix = wcs_util.world2pix(wcs, x_world, y_world)
        lines_out.append(zip(x_pix, y_pix))

    return lines_out


def in_plot(wcs, x_pix, y_pix):
    '''Check whether a given point is in a plot'''
    return x_pix > +0.5 and x_pix < wcs.nx + 0.5 and y_pix > +0.5 and y_pix < wcs.ny + 0.5


def find_intersections(wcs, coord, spacing):
    '''Find intersections of a given coordinate with a all axes'''

    # Initialize arrays
    x = []
    y = []

    # Bottom X axis
    (labels_x, labels_y, world_x, world_y) = tick_positions(wcs, spacing, 'x', coord, farside=False, mode='xy')
    for i in range(0, len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])

    # Top X axis
    (labels_x, labels_y, world_x, world_y) = tick_positions(wcs, spacing, 'x', coord, farside=True, mode='xy')
    for i in range(0, len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])

    # Left Y axis
    (labels_x, labels_y, world_x, world_y) = tick_positions(wcs, spacing, 'y', coord, farside=False, mode='xy')
    for i in range(0, len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])

    # Right Y axis
    (labels_x, labels_y, world_x, world_y) = tick_positions(wcs, spacing, 'y', coord, farside=True, mode='xy')
    for i in range(0, len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])

    return np.array(x), np.array(y)
