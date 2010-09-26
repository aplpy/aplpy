import warnings
import numpy as np
from matplotlib.pyplot import Locator
import wcs_util
import angle_util as au
import math_util
from decorators import auto_refresh


class Ticks(object):

    @auto_refresh
    def __init__(self, parent):

        # Store references to axes
        self._ax1 = parent._ax1
        self._ax2 = parent._ax2
        self._wcs = parent._wcs
        self._figure = parent._figure
        self._parent = parent

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
            try:
                au._check_format_spacing_consistency(self._ax1.xaxis.apl_label_form, au.Angle(degrees = spacing, latitude=False))
            except au.InconsistentSpacing:
                warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                return
            self._ax1.xaxis.apl_auto_tick_spacing = False
            self._ax2.xaxis.apl_auto_tick_spacing = False
            self._ax1.xaxis.apl_tick_spacing = au.Angle(degrees = spacing, latitude=False)
            self._ax2.xaxis.apl_tick_spacing = au.Angle(degrees = spacing, latitude=False)

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
            try:
                au._check_format_spacing_consistency(self._ax1.yaxis.apl_label_form, au.Angle(degrees = spacing, latitude=True))
            except au.InconsistentSpacing:
                warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                return
            self._ax1.yaxis.apl_auto_tick_spacing = False
            self._ax2.yaxis.apl_auto_tick_spacing = False
            self._ax1.yaxis.apl_tick_spacing = au.Angle(degrees = spacing, latitude=True)
            self._ax2.yaxis.apl_tick_spacing = au.Angle(degrees = spacing, latitude=True)

        if hasattr(self._parent, 'grid'):
            self._parent.grid._update()

    @auto_refresh
    def set_color(self, color):
        '''
        Set the color of the ticks
        '''

        for line in self._ax1.xaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax1.yaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_color(color)

    @auto_refresh
    def set_length(self, length):
        '''
        Set the length of the ticks (in points)
        '''

        for line in self._ax1.xaxis.get_ticklines():
            line.set_markersize(length)
        for line in self._ax1.yaxis.get_ticklines():
            line.set_markersize(length)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_markersize(length)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_markersize(length)

    @auto_refresh
    def set_linewidth(self, linewidth):
        '''
        Set the linewidth of the ticks (in points)
        '''

        for line in self._ax1.xaxis.get_ticklines():
            line.set_mew(linewidth)
        for line in self._ax1.yaxis.get_ticklines():
            line.set_mew(linewidth)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_mew(linewidth)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_mew(linewidth)


class WCSLocator(Locator):

    def __init__(self, presets=None, wcs=False, coord='x', farside=False, minor=False):
        if presets is None:
            self.presets = {}
        else:
            self.presets = presets
        self._wcs = wcs
        self.coord = coord
        self.farside = farside

    def __call__(self):

        ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
        xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()

        if self.axis.apl_auto_tick_spacing:
            self.axis.apl_tick_spacing = default_spacing(self.axis.get_axes(), self.coord, self.axis.apl_label_form)

        px, py, wx = tick_positions_v2(self._wcs, self.axis.apl_tick_spacing.todegrees(), self.coord, self.coord, farside=self.farside, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

        self.axis.apl_tick_positions_world = np.array(wx, int)

        if self.coord=='x':
            self.axis.apl_tick_positions_pix = px
        else:
            self.axis.apl_tick_positions_pix = py

        return self.axis.apl_tick_positions_pix


def default_spacing(ax, coord, format):

    wcs = ax.apl_wcs

    xmin, xmax = ax.xaxis.get_view_interval()
    ymin, ymax = ax.yaxis.get_view_interval()

    px, py, wx, wy = axis_positions(wcs, coord, False, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    if coord == 'x':
        wxmin, wxmax = math_util.smart_range(wx)
        if 'd.' in format:
            spacing = au.smart_round_angle_decimal((wxmax-wxmin)/5., latitude=False)
        else:
            spacing = au.smart_round_angle_sexagesimal((wxmax-wxmin)/5., latitude=False, hours='hh' in format)
    else:
        wymin, wymax = min(wy), max(wy)
        if 'd.' in format:
            spacing = au.smart_round_angle_decimal((wymax-wymin)/5., latitude=True)
        else:
            spacing = au.smart_round_angle_sexagesimal((wymax-wymin)/5., latitude=True, hours='hh' in format)

    # Find minimum spacing allowed by labels
    min_spacing = au._get_label_precision(format)

    if min_spacing.todegrees() > spacing.todegrees():
        return min_spacing
    else:
        return spacing

###############################################################
# find_ticks:      Find positions of ticks along a given axis
#                  axes. This function takes one argument:
#
#             wcs: wcs header of FITS file (pywcs class)
#
#                  the function returns:
#     x_min, x_max: range of x values along all axes
#     y_min, y_max: range of y values along all axes
###############################################################

# Find wx in units of spacing, then search for pixel position of integer wx/spacing
# To plot labels, convert to an int and multiply by spacing in sexagesimal space

def tick_positions_v2(wcs, spacing, axis, coord, farside=False, xmin=False, xmax=False, ymin=False, ymax=False):

    (px, py, wx, wy) = axis_positions(wcs, axis, farside, xmin, xmax, ymin, ymax)

    if coord=='x':
        warr = wx
    else:
        warr = wy

    # Check for 360 degree transition, and if encountered,
    # change the values so that there is continuity

    for i in range(0, len(warr)-1):
        if(abs(warr[i]-warr[i+1])>180.):
            if(warr[i] > warr[i+1]):
                warr[i+1:] = warr[i+1:] + 360.
            else:
                warr[i+1:] = warr[i+1:] - 360.

    # Convert warr to units of the spacing, then ticks are at integer values
    warr = warr / spacing

    # Create empty arrays for tick positions
    px_out = []
    py_out = []
    warr_out = []

    for w in np.arange(np.floor(min(warr)), np.ceil(max(warr)), 1.):
        for i in range(len(px)-1):
            if (warr[i] <= w and warr[i+1] > w) or (warr[i] > w and warr[i+1] <= w):
                px_out.append(px[i] + (px[i+1]-px[i]) * (w - warr[i]) / (warr[i+1]-warr[i]))
                py_out.append(py[i] + (py[i+1]-py[i]) * (w - warr[i]) / (warr[i+1]-warr[i]))
                warr_out.append(w)


    return px_out, py_out, warr_out


def tick_positions(wcs, spacing, axis, coord, farside=False, xmin=False, xmax=False, ymin=False, ymax=False):

    (px, py, wx, wy) = axis_positions(wcs, axis, farside, xmin, xmax, ymin, ymax)

    if coord=='y':
        wx, wy = wy, wx

    # Check for 360 degree transition, and if encountered,
    # change the values so that there is continuity

    for i in range(0, len(wx)-1):
        if(abs(wx[i]-wx[i+1])>180.):
            if(wx[i] > wx[i+1]):
                wx[i+1:] = wx[i+1:] + 360.
            else:
                wx[i+1:] = wx[i+1:] - 360.

    # Convert wx to units of the spacing, then ticks are at integer values
    wx = wx / spacing

    # Create empty arrays for tick positions
    px_out = []
    py_out = []
    wx_out = []
    wy_out = []

    for w in np.arange(np.floor(min(wx)), np.ceil(max(wx)), 1.):
        for i in range(len(px)-1):
            if (wx[i] <= w and wx[i+1] > w) or (wx[i] > w and wx[i+1] <= w):
                px_out.append(px[i] + (px[i+1]-px[i]) * (w - wx[i]) / (wx[i+1]-wx[i]))
                py_out.append(py[i] + (py[i+1]-py[i]) * (w - wx[i]) / (wx[i+1]-wx[i]))
                wx_tick = w*spacing % 360.
                wy_tick = (wy[i] + (wy[i+1]-wy[i]) * (w - wx[i]) / (wx[i+1]-wx[i])) % 360
                wx_out.append(wx_tick)
                wy_out.append(wy_tick)

    if coord=='y':
        wx_out, wy_out = wy_out, wx_out

    for i in range(0, np.size(wy_out)):
        if wy_out[i] > 90.:
            wy_out[i] = wy_out[i] - 360.

    return px_out, py_out, wx_out, wy_out

###############################################################
# axis_positions:  pixel and world positions of all pixels
#                  along a given axis. This function takes
#                  three arguments:
#
#             wcs: wcs header of FITS file (pywcs class)
#            axis: x or y axis
#         farside: if true, use top instead of bottom
#                  axis, or right instead of left.
#
#                  the function returns:
#     x_pix, y_pix: pixel coordinates of pixels along axis
# x_world, y_world: world coordinates of pixels along axis
###############################################################

def axis_positions(wcs, axis, farside, xmin=False, xmax=False, ymin=False, \
    ymax=False):

    if not xmin:
        xmin = 0.5
    if not xmax:
        xmax = 0.5+wcs.naxis1
    if not ymin:
        ymin = 0.5
    if not ymax:
        ymax = 0.5+wcs.naxis2

    # Check options
    assert axis=='x' or axis=='y', "The axis= argument should be set to x or y"

    # Generate an array of pixel values for the x-axis
    if axis=='x':
        x_pix = math_util.arange2(xmin, xmax, 1.)
        y_pix = np.ones(np.shape(x_pix))
        if(farside):
            y_pix = y_pix * ymax
        else:
            y_pix = y_pix * ymin
    else:
        y_pix = math_util.arange2(ymin, ymax, 1.)
        x_pix = np.ones(np.shape(y_pix))
        if(farside):
            x_pix = x_pix * xmax
        else:
            x_pix = x_pix * xmin

    # Convert these to world coordinates
    x_world, y_world = wcs_util.pix2world(wcs, x_pix, y_pix)

    return x_pix, y_pix, x_world, y_world

###############################################################
# coord_range:     Range of coordinates that intersect the
#                  axes. This function takes one argument:
#
#             wcs: wcs header of FITS file (pywcs class)
#
#                  the function returns:
#     x_min, x_max: range of x values along all axes
#     y_min, y_max: range of y values along all axes
###############################################################

def coord_range(wcs):

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
