from __future__ import absolute_import, print_function, division

import warnings

import numpy as np
from matplotlib.pyplot import Locator

from . import wcs_util
from . import angle_util as au
from . import scalar_util as su
from . import math_util
from .decorators import auto_refresh


class Ticks(object):

    @auto_refresh
    def __init__(self, parent):

        # Store references to axes
        self._ax1 = parent._ax1
        self._ax2 = parent._ax2
        self._wcs = parent._wcs
        self._figure = parent._figure
        self._parent = parent

        # Save plotting parameters (required for @auto_refresh)
        self._parameters = parent._parameters

        # Set tick positions
        self._ax1.yaxis.tick_left()
        self._ax1.xaxis.tick_bottom()
        self._ax2.yaxis.tick_right()
        self._ax2.xaxis.tick_top()

        # Set tick spacing to default
        self.set_xspacing('auto')
        self.set_yspacing('auto')

        # Set major tick locators
        lx = WCSLocator(wcs=self._wcs, coord='x')
        self._ax1.xaxis.set_major_locator(lx)
        ly = WCSLocator(wcs=self._wcs, coord='y')
        self._ax1.yaxis.set_major_locator(ly)
        lxt = WCSLocator(wcs=self._wcs, coord='x', farside=True)
        self._ax2.xaxis.set_major_locator(lxt)
        lyt = WCSLocator(wcs=self._wcs, coord='y', farside=True)
        self._ax2.yaxis.set_major_locator(lyt)

        # Set minor tick locators
        lx = WCSLocator(wcs=self._wcs, coord='x', minor=True)
        self._ax1.xaxis.set_minor_locator(lx)
        ly = WCSLocator(wcs=self._wcs, coord='y', minor=True)
        self._ax1.yaxis.set_minor_locator(ly)
        lxt = WCSLocator(wcs=self._wcs, coord='x', farside=True, minor=True)
        self._ax2.xaxis.set_minor_locator(lxt)
        lyt = WCSLocator(wcs=self._wcs, coord='y', farside=True, minor=True)
        self._ax2.yaxis.set_minor_locator(lyt)

    @auto_refresh
    def set_xspacing(self, spacing):
        '''
        Set the x-axis tick spacing, in degrees. To set the tick spacing to be
        automatically determined, set this to 'auto'.
        '''

        if spacing == 'auto':
            self._ax1.xaxis.apl_auto_tick_spacing = True
            self._ax2.xaxis.apl_auto_tick_spacing = True
        else:

            self._ax1.xaxis.apl_auto_tick_spacing = False
            self._ax2.xaxis.apl_auto_tick_spacing = False

            if self._wcs.xaxis_coord_type in ['longitude', 'latitude']:
                try:
                    au._check_format_spacing_consistency(self._ax1.xaxis.apl_label_form, au.Angle(degrees=spacing, latitude=self._wcs.xaxis_coord_type == 'latitude'))
                except au.InconsistentSpacing:
                    warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                    return
                self._ax1.xaxis.apl_tick_spacing = au.Angle(degrees=spacing, latitude=self._wcs.xaxis_coord_type == 'latitude')
                self._ax2.xaxis.apl_tick_spacing = au.Angle(degrees=spacing, latitude=self._wcs.xaxis_coord_type == 'latitude')
            else:
                try:
                    su._check_format_spacing_consistency(self._ax1.xaxis.apl_label_form, spacing)
                except au.InconsistentSpacing:
                    warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                    return
                self._ax1.xaxis.apl_tick_spacing = spacing
                self._ax2.xaxis.apl_tick_spacing = spacing

        if hasattr(self._parent, 'grid'):
            self._parent.grid._update()

    @auto_refresh
    def set_yspacing(self, spacing):
        '''
        Set the y-axis tick spacing, in degrees. To set the tick spacing to be
        automatically determined, set this to 'auto'.
        '''

        if spacing == 'auto':
            self._ax1.yaxis.apl_auto_tick_spacing = True
            self._ax2.yaxis.apl_auto_tick_spacing = True
        else:

            self._ax1.yaxis.apl_auto_tick_spacing = False
            self._ax2.yaxis.apl_auto_tick_spacing = False

            if self._wcs.yaxis_coord_type in ['longitude', 'latitude']:
                try:
                    au._check_format_spacing_consistency(self._ax1.yaxis.apl_label_form, au.Angle(degrees=spacing, latitude=self._wcs.yaxis_coord_type == 'latitude'))
                except au.InconsistentSpacing:
                    warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                    return
                self._ax1.yaxis.apl_tick_spacing = au.Angle(degrees=spacing, latitude=self._wcs.yaxis_coord_type == 'latitude')
                self._ax2.yaxis.apl_tick_spacing = au.Angle(degrees=spacing, latitude=self._wcs.yaxis_coord_type == 'latitude')
            else:
                try:
                    su._check_format_spacing_consistency(self._ax1.yaxis.apl_label_form, spacing)
                except au.InconsistentSpacing:
                    warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                    return
                self._ax1.yaxis.apl_tick_spacing = spacing
                self._ax2.yaxis.apl_tick_spacing = spacing

        if hasattr(self._parent, 'grid'):
            self._parent.grid._update()

    @auto_refresh
    def set_color(self, color):
        '''
        Set the color of the ticks
        '''

        # Major ticks
        for line in self._ax1.xaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax1.yaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_color(color)

        # Minor ticks
        for line in self._ax1.xaxis.get_minorticklines():
            line.set_color(color)
        for line in self._ax1.yaxis.get_minorticklines():
            line.set_color(color)
        for line in self._ax2.xaxis.get_minorticklines():
            line.set_color(color)
        for line in self._ax2.yaxis.get_minorticklines():
            line.set_color(color)

    @auto_refresh
    def set_length(self, length, minor_factor=0.5):
        '''
        Set the length of the ticks (in points)
        '''

        # Major ticks
        for line in self._ax1.xaxis.get_ticklines():
            line.set_markersize(length)
        for line in self._ax1.yaxis.get_ticklines():
            line.set_markersize(length)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_markersize(length)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_markersize(length)

        # Minor ticks
        for line in self._ax1.xaxis.get_minorticklines():
            line.set_markersize(length * minor_factor)
        for line in self._ax1.yaxis.get_minorticklines():
            line.set_markersize(length * minor_factor)
        for line in self._ax2.xaxis.get_minorticklines():
            line.set_markersize(length * minor_factor)
        for line in self._ax2.yaxis.get_minorticklines():
            line.set_markersize(length * minor_factor)

    @auto_refresh
    def set_linewidth(self, linewidth):
        '''
        Set the linewidth of the ticks (in points)
        '''

        # Major ticks
        for line in self._ax1.xaxis.get_ticklines():
            line.set_mew(linewidth)
        for line in self._ax1.yaxis.get_ticklines():
            line.set_mew(linewidth)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_mew(linewidth)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_mew(linewidth)

        # Minor ticks
        for line in self._ax1.xaxis.get_minorticklines():
            line.set_mew(linewidth)
        for line in self._ax1.yaxis.get_minorticklines():
            line.set_mew(linewidth)
        for line in self._ax2.xaxis.get_minorticklines():
            line.set_mew(linewidth)
        for line in self._ax2.yaxis.get_minorticklines():
            line.set_mew(linewidth)

    @auto_refresh
    def set_minor_frequency(self, frequency):
        '''
        Set the number of subticks per major tick. Set to one to hide minor
        ticks.
        '''
        self._ax1.xaxis.get_minor_locator().subticks = frequency
        self._ax1.yaxis.get_minor_locator().subticks = frequency
        self._ax2.xaxis.get_minor_locator().subticks = frequency
        self._ax2.yaxis.get_minor_locator().subticks = frequency

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
        for line in self._ax1.xaxis.get_ticklines():
            line.set_visible(True)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_visible(True)
        for line in self._ax1.xaxis.get_minorticklines():
            line.set_visible(True)
        for line in self._ax2.xaxis.get_minorticklines():
            line.set_visible(True)

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis ticks
        """
        for line in self._ax1.xaxis.get_ticklines():
            line.set_visible(False)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_visible(False)
        for line in self._ax1.xaxis.get_minorticklines():
            line.set_visible(False)
        for line in self._ax2.xaxis.get_minorticklines():
            line.set_visible(False)

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis ticks
        """
        for line in self._ax1.yaxis.get_ticklines():
            line.set_visible(True)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_visible(True)
        for line in self._ax1.yaxis.get_minorticklines():
            line.set_visible(True)
        for line in self._ax2.yaxis.get_minorticklines():
            line.set_visible(True)

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis ticks
        """
        for line in self._ax1.yaxis.get_ticklines():
            line.set_visible(False)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_visible(False)
        for line in self._ax1.yaxis.get_minorticklines():
            line.set_visible(False)
        for line in self._ax2.yaxis.get_minorticklines():
            line.set_visible(False)


class WCSLocator(Locator):

    def __init__(self, presets=None, wcs=False, coord='x', farside=False, minor=False, subticks=5):
        if presets is None:
            self.presets = {}
        else:
            self.presets = presets
        self._wcs = wcs
        self.coord = coord
        self.farside = farside
        self.minor = minor
        self.subticks = subticks

    def __call__(self):

        self.coord_type = self._wcs.xaxis_coord_type if self.coord == 'x' else self._wcs.yaxis_coord_type

        ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
        xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()

        if self.axis.apl_auto_tick_spacing:
            self.axis.apl_tick_spacing = default_spacing(self.axis.get_axes(), self.coord, self.axis.apl_label_form)
            if self.axis.apl_tick_spacing is None:
                self.axis.apl_tick_positions_pix = []
                self.axis.apl_tick_positions_world = []
                return []

        if self.coord_type in ['longitude', 'latitude']:
            tick_spacing = self.axis.apl_tick_spacing.todegrees()
        else:
            tick_spacing = self.axis.apl_tick_spacing

        if self.minor:
            tick_spacing /= float(self.subticks)

        px, py, wx = tick_positions(self._wcs, tick_spacing, self.coord, self.coord, farside=self.farside, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, mode='xscaled')
        px, py, wx = np.array(px, float), np.array(py, float), np.array(wx, int)

        if self.minor:
            keep = np.mod(wx, self.subticks) > 0
            px, py, wx = px[keep], py[keep], wx[keep] / float(self.subticks)

        self.axis.apl_tick_positions_world = np.array(wx, int)

        if self.coord == 'x':
            self.axis.apl_tick_positions_pix = px
        else:
            self.axis.apl_tick_positions_pix = py

        return self.axis.apl_tick_positions_pix


def default_spacing(ax, coord, format):

    wcs = ax._wcs

    xmin, xmax = ax.xaxis.get_view_interval()
    ymin, ymax = ax.yaxis.get_view_interval()

    px, py, wx, wy = axis_positions(wcs, coord, False, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    # Keep only pixels that fall inside the sky. This will only really work
    # for PyWCS 0.11 or more recent
    keep = ~np.isnan(wx) & ~np.isnan(wy)

    if np.sum(keep) == 0:
        return None
    else:
        px = px[keep]
        py = py[keep]
        wx = wx[keep]
        wy = wy[keep]

    coord_type = wcs.xaxis_coord_type if coord == 'x' else wcs.yaxis_coord_type

    if coord == 'x':

        # The following is required because PyWCS 0.10 and earlier did not return
        # NaNs for positions outside the sky, but instead returned an array with
        # all the same world coordinates regardless of input pixel coordinates.
        if len(wx) > 1 and len(np.unique(wx)) == 1:
            return None

        if coord_type in ['longitude', 'latitude']:
            if coord_type == 'longitude':
                wxmin, wxmax = math_util.smart_range(wx)
            else:
                wxmin, wxmax = min(wx), max(wx)
            if 'd.' in format:
                spacing = au.smart_round_angle_decimal((wxmax - wxmin) / 5., latitude=coord_type == 'latitude')
            else:
                spacing = au.smart_round_angle_sexagesimal((wxmax - wxmin) / 5., latitude=coord_type == 'latitude', hours='hh' in format)
        else:
            wxmin, wxmax = np.min(wx), np.max(wx)
            spacing = su.smart_round_angle_decimal((wxmax - wxmin) / 5.)
    else:

        # The following is required because PyWCS 0.10 and earlier did not return
        # NaNs for positions outside the sky, but instead returned an array with
        # all the same world coordinates regardless of input pixel coordinates.
        if len(wy) > 1 and len(np.unique(wy)) == 1:
            return None

        if coord_type in ['longitude', 'latitude']:
            if coord_type == 'longitude':
                wymin, wymax = math_util.smart_range(wy)
            else:
                wymin, wymax = min(wy), max(wy)
            if 'd.' in format:
                spacing = au.smart_round_angle_decimal((wymax - wymin) / 5., latitude=coord_type == 'latitude')
            else:
                spacing = au.smart_round_angle_sexagesimal((wymax - wymin) / 5., latitude=coord_type == 'latitude', hours='hh' in format)
        else:
            wymin, wymax = np.min(wy), np.max(wy)
            spacing = su.smart_round_angle_decimal((wymax - wymin) / 5.)

    # Find minimum spacing allowed by labels
    if coord_type in ['longitude', 'latitude']:
        min_spacing = au._get_label_precision(format, latitude=coord_type == 'latitude')
        if min_spacing.todegrees() > spacing.todegrees():
            return min_spacing
        else:
            return spacing
    else:
        min_spacing = su._get_label_precision(format)
        if min_spacing is not None and min_spacing > spacing:
            return min_spacing
        else:
            return spacing


def tick_positions(wcs, spacing, axis, coord, farside=False,
                   xmin=False, xmax=False, ymin=False, ymax=False,
                   mode='xscaled'):
    '''
    Find positions of ticks along a given axis.

    Parameters
    ----------

    wcs : ~aplpy.wcs_util.WCS
       The WCS instance for the image.

    spacing : float
       The spacing along the axis.

    axis : { 'x', 'y' }
       The axis along which we are looking for ticks.

    coord : { 'x', 'y' }
       The coordinate for which we are looking for ticks.

    farside : bool, optional
       Whether we are looking on the left or bottom axes (False) or the
       right or top axes (True).

    xmin, xmax, ymin, ymax : float, optional
       The range of pixel values covered by the image.

    mode : { 'xy', 'xscaled' }, optional
       If set to 'xy' the function returns the world coordinates of the
       ticks. If 'xscaled', then only the coordinate requested is
       returned, in units of the tick spacing.
    '''

    (px, py, wx, wy) = axis_positions(wcs, axis, farside, xmin, xmax, ymin, ymax)

    if coord == 'x':
        warr, walt = wx, wy
    else:
        warr, walt = wy, wx

    # Check for 360 degree transition, and if encountered,
    # change the values so that there is continuity

    if (coord == 'x' and wcs.xaxis_coord_type == 'longitude') or \
       (coord == 'y' and wcs.yaxis_coord_type == 'longitude'):
        for i in range(0, len(warr) - 1):
            if(abs(warr[i] - warr[i + 1]) > 180.):
                if(warr[i] > warr[i + 1]):
                    warr[i + 1:] = warr[i + 1:] + 360.
                else:
                    warr[i + 1:] = warr[i + 1:] - 360.

    # Convert warr to units of the spacing, then ticks are at integer values
    warr = warr / spacing

    # Create empty arrays for tick positions
    iall = []
    wall = []

    # Loop over ticks which lie in the range covered by the axis
    for w in np.arange(np.floor(min(warr)), np.ceil(max(warr)), 1.):

        # Find all the positions at which to interpolate
        inter = np.where(((warr[:-1] <= w) & (warr[1:] > w)) | ((warr[:-1] > w) & (warr[1:] <= w)))[0]

        # If there are any intersections, keep the indices, and the position
        # of the interpolation
        if len(inter) > 0:
            iall.append(inter.astype(int))
            wall.append(np.repeat(w, len(inter)).astype(float))

    if len(iall) > 0:
        iall = np.hstack(iall)
        wall = np.hstack(wall)
    else:
        if mode == 'xscaled':
            return [], [], []
        else:
            return [], [], [], []

    # Now we can interpolate as needed
    dwarr = warr[1:] - warr[:-1]
    px_out = px[:-1][iall] + (px[1:][iall] - px[:-1][iall]) * (wall - warr[:-1][iall]) / dwarr[iall]
    py_out = py[:-1][iall] + (py[1:][iall] - py[:-1][iall]) * (wall - warr[:-1][iall]) / dwarr[iall]

    if mode == 'xscaled':
        warr_out = wall
        return px_out, py_out, warr_out
    elif mode == 'xy':
        warr_out = wall * spacing
        walt_out = walt[:-1][iall] + (walt[1:][iall] - walt[:-1][iall]) * (wall - warr[:-1][iall]) / dwarr[iall]
        if coord == 'x':
            return px_out, py_out, warr_out, walt_out
        else:
            return px_out, py_out, walt_out, warr_out


def axis_positions(wcs, axis, farside, xmin=False, xmax=False,
                                       ymin=False, ymax=False):
    '''
    Find the world coordinates of all pixels along an axis.

    Parameters
    ----------

    wcs : ~aplpy.wcs_util.WCS
       The WCS instance for the image.

    axis : { 'x', 'y' }
       The axis along which we are computing world coordinates.

    farside : bool
       Whether we are looking on the left or bottom axes (False) or the
       right or top axes (True).

    xmin, xmax, ymin, ymax : float, optional
       The range of pixel values covered by the image
    '''

    if not xmin:
        xmin = 0.5
    if not xmax:
        xmax = 0.5 + wcs.nx
    if not ymin:
        ymin = 0.5
    if not ymax:
        ymax = 0.5 + wcs.ny

    # Check options
    assert axis == 'x' or axis == 'y', "The axis= argument should be set to x or y"

    # Generate an array of pixel values for the x-axis
    if axis == 'x':
        x_pix = np.linspace(xmin, xmax, 512)
        y_pix = np.ones(np.shape(x_pix))
        if(farside):
            y_pix = y_pix * ymax
        else:
            y_pix = y_pix * ymin
    else:
        y_pix = np.linspace(ymin, ymax, 512)
        x_pix = np.ones(np.shape(y_pix))
        if(farside):
            x_pix = x_pix * xmax
        else:
            x_pix = x_pix * xmin

    # Convert these to world coordinates
    x_world, y_world = wcs_util.pix2world(wcs, x_pix, y_pix)

    return x_pix, y_pix, x_world, y_world


def coord_range(wcs):
    '''
    Find the range of coordinates that intersect the axes.

    Parameters
    ----------

    wcs : ~aplpy.wcs_util.WCS
        The WCS instance for the image.
    '''

    x_pix, y_pix, x_world_1, y_world_1 = axis_positions(wcs, 'x', farside=False)
    x_pix, y_pix, x_world_2, y_world_2 = axis_positions(wcs, 'x', farside=True)
    x_pix, y_pix, x_world_3, y_world_3 = axis_positions(wcs, 'y', farside=False)
    x_pix, y_pix, x_world_4, y_world_4 = axis_positions(wcs, 'y', farside=True)

    x_world = np.hstack([x_world_1, x_world_2, x_world_3, x_world_4])
    y_world = np.hstack([y_world_1, y_world_2, y_world_3, y_world_4])

    x_min = min(x_world)
    x_max = max(x_world)
    y_min = min(y_world)
    y_max = max(y_world)

    return x_min, x_max, y_min, y_max
