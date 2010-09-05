# Module that looks after plotting a coordinate grid on images

# To improve, create array with e.g. all declination values, insert values which occur at intersections then
# remove all array sections with out of bounds pixel values

from ticks import tick_positions
import numpy as np
from matplotlib.collections import LineCollection

import math_util

import wcs_util
from ticks import default_spacing

import angle_util as au

from decorators import auto_refresh

# can do coarse search to check if any longitude lines are completely contained inside box.
# if not, then has to intersect axis, and so can just do the ones that intersect

class Grid(object):

    @auto_refresh
    def __init__(self, parent):

        # Save axes and wcs information
        self.ax = parent._ax1
        self.wcs = parent._wcs
        self._figure = parent._figure

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
                The spacing in the longitudinal direction, in degrees.
                To set the spacing to be the same as the ticks, set this
                to 'tick'
        '''

        if xspacing == 'tick':
            self.x_auto_spacing = True
        else:
            self.x_auto_spacing = False
            self.x_grid_spacing = au.Angle(degrees = xspacing)

        self._update()

    @auto_refresh
    def set_yspacing(self, yspacing):
        '''
        Set the grid line spacing in the latitudinal direction

        Required Arguments:

            *yspacing*: [ float | 'tick' ]
                The spacing in the latitudinal direction, in degrees.
                To set the spacing to be the same as the ticks, set this
                to 'tick'
        '''

        if yspacing == 'tick':
            self.y_auto_spacing = True
        else:
            self.y_auto_spacing = False
            self.y_grid_spacing = au.Angle(degrees = yspacing)

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
            if id(self.ax) <> id(args[0]):
                raise Exception("ax ids should match")

        lines = []

        if self.x_auto_spacing:
            if self.ax.xaxis.apl_auto_tick_spacing:
                xspacing = default_spacing(self.ax, 'x', self.ax.xaxis.apl_label_form).todegrees()
            else:
                xspacing = self.ax.xaxis.apl_tick_spacing.todegrees()
        else:
            xspacing = self.x_grid_spacing.todegrees()

        if self.y_auto_spacing:
            if self.ax.yaxis.apl_auto_tick_spacing:
                yspacing = default_spacing(self.ax, 'y', self.ax.yaxis.apl_label_form).todegrees()
            else:
                yspacing = self.ax.yaxis.apl_tick_spacing.todegrees()
        else:
            yspacing = self.y_grid_spacing.todegrees()

        # Find longitude lines that intersect with axes
        lon_i, lat_i = find_intersections(self.wcs, 'x', xspacing)

        lon_i_unique = np.array(list(set(lon_i)))

        # Plot those lines
        for l in lon_i_unique:
            for line in plot_longitude(self.wcs, lon_i, lat_i, l):
                lines.append(line)

        # Find longitude lines that don't intersect with axes
        lon_all = math_util.complete_range(0.0, 360.0, xspacing)
        lon_ni = np.sort(np.array(list(set(lon_all)-set(lon_i_unique))))
        lat_ni = np.ones(np.size(lon_ni)) # doesn't matter what value is, is either in or outside

        if np.size(lon_ni) > 0:

            xpix, ypix = wcs_util.world2pix(self.wcs, lon_ni, lat_ni)

            # Plot those lines
            # for i in range(0, np.size(lon_ni)):
            #     if(in_plot(wcs, xpix[i], ypix[i])):
            #         print "Inside longitude : "+str(lon_ni[i])
            #         plot_longitude(wcs, np.array([]), np.array([]), lon_ni[i])

            # Find latitude lines that intersect with axes
        lon_i, lat_i = find_intersections(self.wcs, 'y', yspacing)

        lat_i_unique = np.array(list(set(lat_i)))

        # Plot those lines
        for l in lat_i_unique:
            for line in plot_latitude(self.wcs, lon_i, lat_i, l):
                lines.append(line)

        # Find latitude lines that don't intersect with axes
        lat_all = math_util.complete_range(-90.0, 90.0, yspacing)
        lat_ni = np.sort(np.array(list(set(lat_all)-set(lat_i_unique))))
        lon_ni = np.ones(np.size(lat_ni)) # doesn't matter what value is, is either in or outside

        if np.size(lat_ni) > 0:

            xpix, ypix = wcs_util.world2pix(self.wcs, lon_ni, lat_ni)

            # Plot those lines
            # for i in range(0, np.size(lat_ni)):
            #     if(in_plot(wcs, xpix[i], ypix[i])):
            #         print "Inside latitude : "+str(lat_ni[i])
            #         plot_latitude(wcs, np.array([]), np.array([]), lat_ni[i])

        if self._grid:
            self._grid.set_verts(lines)
        else:
            self._grid = LineCollection(lines, transOffset=self.ax.transData)
            self.ax.add_collection(self._grid, False)

        return self.ax

##########################################################
# plot_latitude: plot a single latitude line
##########################################################

def plot_latitude(wcs, lon, lat, lat0, alpha=0.5):

    lines_out = []

    # Check if the point with coordinates (0, lat0) is inside the viewport
    xpix, ypix = wcs_util.world2pix(wcs, 0., lat0)

    if in_plot(wcs, xpix, ypix):
        lon_min = 0.
        inside = True
    else:
        inside = False

    # Find intersections that correspond to latitude lat0
    index = np.where(lat==lat0)

    # Produce sorted array of the longitudes of all intersections
    lonnew = np.sort(lon[index])

    # Cycle through intersections
    for l in lonnew:

        # If inside, then current intersection closes arc - plot it
        if(inside):
            lon_max = l
            x_world = math_util.complete_range(lon_min, lon_max, 360) # Plotting every degree, make more general
            y_world = np.ones(len(x_world)) * lat0
            x_pix, y_pix = wcs_util.world2pix(wcs, x_world, y_world)
            lines_out.append(zip(x_pix, y_pix))
            inside = False
        else:
            lon_min = l
            inside = True

    # If still inside when finished going through intersections, then close at longitude 360
    if(inside):
        lon_max = 360.
        x_world = math_util.complete_range(lon_min, lon_max, 360)
        y_world = np.ones(len(x_world)) * lat0
        x_pix, y_pix = wcs_util.world2pix(wcs, x_world, y_world)
        lines_out.append(zip(x_pix, y_pix))
        inside = False

    return lines_out

##########################################################
# plot_longitude: plot a single longitude line
##########################################################

def plot_longitude(wcs, lon, lat, lon0, alpha=0.5):

    lines_out = []

    # Check if the point with coordinates (10., -90.) is inside the viewport
    xpix, ypix = wcs_util.world2pix(wcs, 10., -90.)

    if in_plot(wcs, xpix, ypix):
        lat_min = -90.
        inside = True
    else:
        inside = False
    # Find intersections that correspond to longitude lon0
    index = np.where(lon==lon0)

    # Produce sorted array of the latitudes of all intersections
    latnew = np.sort(lat[index])

    # Cycle through intersections
    for l in latnew:
        if(inside):
            lat_max = l
            y_world = math_util.complete_range(lat_min, lat_max, 360)
            x_world = np.ones(len(y_world)) * lon0
            x_pix, y_pix = wcs_util.world2pix(wcs, x_world, y_world)
            lines_out.append(zip(x_pix, y_pix))
            inside = False
        else:
            lat_min = l
            inside = True

    if(inside):
        lat_max = 90.
        y_world = math_util.complete_range(lat_min, lat_max, 360)
        x_world = np.ones(len(y_world)) * lon0
        x_pix, y_pix = wcs_util.world2pix(wcs, x_world, y_world)
        lines_out.append(zip(x_pix, y_pix))
        inside = False

    return lines_out

##########################################################
# in_plot: whether a given point is in a plot
##########################################################

def in_plot(wcs, x_pix, y_pix):
    return x_pix > +0.5 and x_pix < wcs.naxis1+0.5 and y_pix > +0.5 and y_pix < wcs.naxis2+0.5

##########################################################
# find_intersections: find intersections of a given
#                     coordinate with a all axes.
##########################################################

def find_intersections(wcs, coord, spacing):

    # Initialize arrays
    x = []
    y = []

    # Bottom X axis
    (labels_x, labels_y, world_x, world_y) = tick_positions(wcs, spacing, 'x', coord, farside=False)
    for i in range(0, len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])

    # Top X axis
    (labels_x, labels_y, world_x, world_y) = tick_positions(wcs, spacing, 'x', coord, farside=True)
    for i in range(0, len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])

    # Left Y axis
    (labels_x, labels_y, world_x, world_y) = tick_positions(wcs, spacing, 'y', coord, farside=False)
    for i in range(0, len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])

    # Right Y axis
    (labels_x, labels_y, world_x, world_y) = tick_positions(wcs, spacing, 'y', coord, farside=True)
    for i in range(0, len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])

    return np.array(x), np.array(y)

    ##########################################################
