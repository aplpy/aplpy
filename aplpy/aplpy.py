from distutils import version
import os
import warnings

try:
    import matplotlib
    import matplotlib.pyplot as mpl
    import mpl_toolkits.axes_grid.parasite_axes as mpltk
except ImportError:
    raise Exception("matplotlib 0.99.0 or later is required for APLpy")

if version.LooseVersion(matplotlib.__version__) < version.LooseVersion('0.99.0'):
    raise Exception("matplotlib 0.99.0 or later is required for APLpy")

try:
    import pyfits
except ImportError:
    raise Exception("pyfits is required for APLpy")

try:
    import pywcs
except ImportError:
    raise Exception("pywcs is required for APLpy")

try:
    import numpy as np
except ImportError:
    raise Exception("numpy is required for APLpy")

from matplotlib.patches import Circle, Rectangle, Ellipse, Polygon
from matplotlib.collections import PatchCollection

import contour_util

import convolve_util

import montage
import image_util
import header
import wcs_util
import slicer

from layers import Layers
from grid import Grid
from ticks import Ticks
from labels import TickLabels
from axis_labels import AxisLabels
from overlays import Beam, ScaleBar
from regions import Regions
from colorbar import Colorbar
from normalize import APLpyNormalize
from frame import Frame

from decorators import auto_refresh, fixdocstring

from deprecated import Deprecated


class FITSFigure(Layers, Regions, Deprecated):

    "A class for plotting FITS files."

    @auto_refresh
    def __init__(self, data, hdu=0, figure=None, subplot=None, downsample=False, north=False, convention=None, slices=[], auto_refresh=True, **kwargs):
        '''
        Create a FITSFigure instance

        Required arguments:

            *data*: [ string | pyfits PrimaryHDU | pyfits ImageHDU ]
                Either the filename of the FITS file to open, or a pyfits
                PrimaryHDU or ImageHDU instance.

        Optional Keyword Arguments:

            *hdu*: [ integer ]
                By default, the image in the primary HDU is read in. If a
                different HDU is required, use this argument.

            *figure*: [ matplotlib figure() instance ]
                If specified, a subplot will be added to this existing
                matplotlib figure() instance, rather than a new figure
                being created from scratch.

            *subplot*: [ list of four floats ]
                If specified, a subplot will be added at this position. The
                list should contain [xmin, ymin, dx, dy] where xmin and ymin
                are the position of the bottom left corner of the subplot, and
                dx and dy are the width and height of the subplot respectively.
                These should all be given in units of the figure width and
                height. For example, [0.1, 0.1, 0.8, 0.8] will almost fill the
                entire figure, leaving a 10 percent margin on all sides.

            *downsample*: [ integer ]
                If this option is specified, the image will be downsampled
                by a factor *downsample* when reading in the data.

            *north*: [ True | False ]
                Whether to rotate the image so that the North Celestial
                Pole is up. Note that this option requires Montage to be
                installed.

            *convention*: [ string ]
                This is used in cases where a FITS header can be interpreted
                in multiple ways. For example, for files with a -CAR
                projection and CRVAL2=0, this can be set to 'wells' or
                'calabretta' to choose the appropriate convention.

            *slices*: [ tuple or list ]
                If a FITS file with more than two dimensions is specified,
                then these are the slices to extract. If all extra dimensions
                only have size 1, then this is not required.

            *auto_refresh*: [ True | False ]
                Whether to refresh the figure automatically every time a
                plotting method is called. This can also be set using the
                set_auto_refresh method.

        Any additional arguments are passed on to matplotlib's Figure() class.
        For example, to set the figure size, use the figsize=(xsize, ysize)
        argument (where xsize and ysize are in inches). For more information
        on these additional arguments, see the *Optional keyword arguments*
        section in the documentation for `Figure
        <http://matplotlib.sourceforge.net/api/figure_api.html?
        #matplotlib.figure.Figure>`_
        '''

        if not 'figsize' in kwargs:
            kwargs['figsize'] = (10, 9)

        if north and not montage._installed():
            raise Exception("Montage needs to be installed and in the $PATH in order to use the north= option")

        self._hdu, self._wcs = self._get_hdu(data, hdu, north, \
            convention=convention, slices=slices)

        # Downsample if requested
        if downsample:
            naxis1_new = self._wcs.naxis1 - np.mod(self._wcs.naxis1, downsample)
            naxis2_new = self._wcs.naxis2 - np.mod(self._wcs.naxis2, downsample)
            self._hdu.data = self._hdu.data[0:naxis2_new, 0:naxis1_new]
            self._hdu.data = image_util.resample(self._hdu.data, downsample)
            self._wcs.naxis1, self._wcs.naxis2 = naxis1_new, naxis2_new

        # Open the figure
        if figure:
            self._figure = figure
        else:
            self._figure = mpl.figure(**kwargs)

        # Create first axis instance
        if subplot:
            self._ax1 = mpltk.HostAxes(self._figure, subplot, adjustable='datalim')
        else:
            self._ax1 = mpltk.SubplotHost(self._figure, 1, 1, 1)

        self._ax1.toggle_axisline(False)

        self._figure.add_axes(self._ax1)

        # Create second axis instance
        self._ax2 = self._ax1.twin()
        self._ax2.set_frame_on(False)

        self._ax2.toggle_axisline(False)

        # Turn off autoscaling
        self._ax1.set_autoscale_on(False)
        self._ax2.set_autoscale_on(False)

        # Force zorder of parasite axes
        self._ax2.xaxis.set_zorder(2.5)
        self._ax2.yaxis.set_zorder(2.5)

        # Store WCS in axes
        self._ax1.apl_wcs = self._wcs
        self._ax2.apl_wcs = self._wcs

        self.set_auto_refresh(auto_refresh)

        # Set view to whole FITS file
        self._initialize_view()

        # Initialize ticks
        self.ticks = Ticks(self)

        # Initialize labels
        self.axis_labels = AxisLabels(self)
        self.tick_labels = TickLabels(self)

        self.frame = Frame(self)

        self._ax1.format_coord = self.tick_labels._cursor_position

        # Initialize layers list
        self._initialize_layers()

        # Find generating function for vmin/vmax
        self._auto_v = image_util.percentile_function(self._hdu.data)

        # Set image holder to be empty
        self.image = None

        # Set default theme
        self.set_theme(theme='pretty')

    def _get_hdu(self, data, hdu, north, convention=None, slices=[]):

        if type(data) == str:

            filename = data

            # Check file exists
            if not os.path.exists(filename):
                raise Exception("File not found: "+filename)

            # Read in FITS file
            try:
                hdu = pyfits.open(filename)[hdu]
            except:
                raise Exception("An error occured while reading the FITS file")

        elif isinstance(data, pyfits.PrimaryHDU) or isinstance(data, pyfits.ImageHDU):

            hdu = data

        elif isinstance(data, pyfits.HDUList):

            hdu = data[hdu]

        else:

            raise Exception("data argument should either be a filename, or an HDU instance from pyfits.")

        # Extract slices
        hdu = slicer.slice(hdu, slices=slices)

        # Reproject to face north if requested
        if north:
            hdu = montage.reproject_north(hdu)

        # Check header
        hdu.header = header.check(hdu.header, convention=convention)

        # Parse WCS info
        try:
            wcs = pywcs.WCS(hdu.header)
        except:
            raise Exception("An error occured while parsing the WCS information")

        return hdu, wcs

    @auto_refresh
    def set_system_latex(self, usetex):
        '''
        Set whether to use a real LaTeX installation or the built-in matplotlib LaTeX

        Required Arguments:

            *usetex*: [ True | False ]
                Whether to use a real LaTex installation (True) or the built-in
                matplotlib LaTeX (False). Note that if the former is chosen, an
                installation of LaTex is required.
        '''
        mpl.rc('text', usetex=usetex)

    @auto_refresh
    def recenter(self, x, y, radius=None, width=None, height=None):
        '''
        Center the image on a given position and with a given radius

        Required Arguments:

            *x*: [ float ]
                Longitude of the position to center on (degrees)

            *y*: [ float ]
                Latitude of the position to center on (degrees)

        Optional Keyword Arguments:

            Either the radius or width/heigh arguments should be specified.

            *radius*: [ float ]
                Radius of the region to view (degrees). This produces a square plot.

            *width*: [ float ]
                Width of the region to view (degrees). This should be given in
                conjunction with the height argument.

            *height*: [ float ]
                Height of the region to view (degrees). This should be given in
                conjunction with the width argument.
        '''

        xpix, ypix = wcs_util.world2pix(self._wcs, x, y)

        degperpix = wcs_util.degperpix(self._wcs)

        if radius:
            dx_pix = radius / degperpix
            dy_pix = radius / degperpix
        elif width and height:
            dx_pix = width / degperpix / 2.
            dy_pix = height / degperpix / 2.
        else:
            raise Exception("Need to specify either radius= or width= and height= arguments")

        if xpix + dx_pix < self._extent[0] or \
           xpix - dx_pix > self._extent[1] or \
           ypix + dy_pix < self._extent[2] or \
           ypix - dy_pix > self._extent[3]:

            raise Exception("Zoom region falls outside the image")

        self._ax1.set_xlim(xpix-dx_pix, xpix+dx_pix)
        self._ax1.set_ylim(ypix-dy_pix, ypix+dy_pix)

    @auto_refresh
    def show_grayscale(self, vmin=None, vmid=None, vmax=None, \
                            pmin=0.25, pmax=99.75, \
                            stretch='linear', exponent=2, invert='default', smooth=None, kernel='gauss'):
        '''
        Show a grayscale image of the FITS file

        Optional Keyword Arguments:

            *vmin*: [ None | float ]
                Minimum pixel value to use for the grayscale. If set to None,
                the minimum pixel value is determined using pmin (default).

            *vmax*: [ None | float ]
                Maximum pixel value to use for the grayscale. If set to None,
                the maximum pixel value is determined using pmax (default).

            *pmin*: [ float ]
                Percentile value used to determine the minimum pixel value to
                use for the grayscale if vmin is set to None. The default
                value is 0.25%.

            *pmax*: [ float ]
                Percentile value used to determine the maximum pixel value to
                use for the grayscale if vmax is set to None. The default
                value is 99.75%.

            *stretch*: [ 'linear' | 'log' | 'sqrt' | 'arcsinh' | 'power' ]
                The stretch function to use

            *vmid*: [ None | float ]
                Mid-pixel value used for the log and arcsinh stretches. If
                set to None, this is set to a sensible value.

            *exponent*: [ float ]
                If stretch is set to 'power', this is the exponent to use

            *invert*: [ True | False ]
                Whether to invert the grayscale or not. The default is False,
                unless set_theme is used, in which case the default depends on
                the theme.

            *smooth*: [ integer | tuple ]
                Default smoothing scale is 3 pixels across. User can define
                whether they want an NxN kernel (integer), or NxM kernel
                (tuple). This argument corresponds to the 'gauss' and 'box'
                smoothing kernels.

            *kernel*: [ 'gauss' | 'box' | numpy.array]
                Default kernel used for smoothing is 'gauss'. The user can
                specify if they would prefer 'gauss', 'box', or a custom
                kernel. All kernels are normalized to ensure flux retention.
        '''

        if invert=='default':
            invert = self._get_invert_default()

        if invert:
            cmap = 'gist_yarg'
        else:
            cmap = 'gray'

        self.show_colorscale(vmin=vmin, vmid=vmid, vmax=vmax, stretch=stretch, exponent=exponent, cmap=cmap, pmin=pmin, pmax=pmax, smooth=smooth, kernel=kernel)

    @auto_refresh
    def hide_grayscale(self, *args, **kwargs):
        self.hide_colorscale(*args, **kwargs)

    @auto_refresh
    def show_colorscale(self, vmin=None, vmid=None, vmax=None, \
                             pmin=0.25, pmax=99.75,
                             stretch='linear', exponent=2, cmap='default', smooth=None, kernel='gauss'):
        '''
        Show a colorscale image of the FITS file

        Optional Keyword Arguments:

            *vmin*: [ None | float ]
                Minimum pixel value to use for the colorscale. If set to None,
                the minimum pixel value is determined using pmin (default).

            *vmax*: [ None | float ]
                Maximum pixel value to use for the colorscale. If set to None,
                the maximum pixel value is determined using pmax (default).

            *pmin*: [ float ]
                Percentile value used to determine the minimum pixel value to
                use for the colorscale if vmin is set to None. The default
                value is 0.25%.

            *pmax*: [ float ]
                Percentile value used to determine the maximum pixel value to
                use for the colorscale if vmax is set to None. The default
                value is 99.75%.

            *stretch*: [ 'linear' | 'log' | 'sqrt' | 'arcsinh' | 'power' ]
                The stretch function to use

            *vmid*: [ None | float ]
                Mid-pixel value used for the log and arcsinh stretches. If
                set to None, this is set to a sensible value.

            *exponent*: [ float ]
                If stretch is set to 'power', this is the exponent to use

            *cmap*: [ string ]
                The name of the colormap to use

            *smooth*: [ integer | tuple ]
                Default smoothing scale is 3 pixels across. User can define
                whether they want an NxN kernel (integer), or NxM kernel
                (tuple). This argument corresponds to the 'gauss' and 'box'
                smoothing kernels.

            *kernel*: [ 'gauss' | 'box' | numpy.array]
                Default kernel used for smoothing is 'gauss'. The user can
                specify if they would prefer 'gauss', 'box', or a custom
                kernel. All kernels are normalized to ensure flux retention.
        '''

        if cmap=='default':
            cmap = self._get_colormap_default()

        min_auto = np.equal(vmin, None)
        max_auto = np.equal(vmax, None)

        # The set of available functions
        cmap = mpl.cm.get_cmap(cmap, 1000)

        if min_auto:
            vmin = self._auto_v(pmin)

        if max_auto:
            vmax = self._auto_v(pmax)

        # Prepare normalizer object
        normalizer = APLpyNormalize(stretch=stretch, exponent=exponent,
                                    vmid=vmid, vmin=vmin, vmax=vmax)

        # Adjust vmin/vmax if auto
        if min_auto:
            if stretch <> 'linear':
                warnings.warn("Auto-scaling for non-linear stretches may produce slightly different results compared to APLpy 0.9.4")
            else:
                vmin = -0.1 * (vmax - vmin) + vmin
            print "Auto-setting vmin to %10.3e" % vmin

        if max_auto:
            if stretch <> 'linear':
                warnings.warn("Auto-scaling for non-linear stretches may produce slightly different results compared to APLpy 0.9.4")
            else:
                vmax = 0.1 * (vmax - vmin) + vmax
            print "Auto-setting vmax to %10.3e" % vmax

        # Update normalizer object
        normalizer.vmin = vmin
        normalizer.vmax = vmax

        if self.image:
            self.image.set_visible(True)
            self.image.set_norm(normalizer)
            self.image.set_cmap(cmap=cmap)
            self.image.origin='lower'
            self.image.set_data(convolve_util.convolve(self._hdu.data,smooth=smooth,kernel=kernel))
        else:
            self.image = self._ax1.imshow(convolve_util.convolve(self._hdu.data,smooth=smooth,kernel=kernel), cmap=cmap, interpolation='nearest', origin='lower', extent=self._extent, norm=normalizer)

        xmin, xmax = self._ax1.get_xbound()
        if xmin == 0.0:
            self._ax1.set_xlim(0.5, xmax)

        ymin, ymax = self._ax1.get_ybound()
        if ymin == 0.0:
            self._ax1.set_ylim(0.5, ymax)

        if hasattr(self, 'colorbar'):
            self.colorbar.update()

    @auto_refresh
    def hide_colorscale(self):
        self.image.set_visible(False)

    @auto_refresh
    def set_nan_color(self, color):
        '''
        Set the color for NaN pixels

        Required Arguments:

            *color*: [ string | matplotlib color ]
        '''
        cm = self.image.get_cmap()
        cm.set_bad(color)
        self.image.set_cmap(cm)

    @auto_refresh
    def show_rgb(self, filename, interpolation='nearest', flip=False):
        '''
        Show a 3-color image instead of the FITS file data

        Required Arguments:

            *filename*
                The 3-color image should have exactly the same dimensions as the FITS file, and
                will be shown with exactly the same projection.

        Optional Arguments:

            *flip*: [ True | False ]
                Whether to vertically flip the RGB image in case it is the
                wrong way around.
        '''

        img = mpl.imread(filename)

        if flip:
            img = np.flipud(img)

        self.image = self._ax1.imshow(img, extent=self._extent, interpolation=interpolation, origin='upper')

    @auto_refresh
    def show_contour(self, data, hdu=0, layer=None, levels=5, filled=False, cmap=None, colors=None, returnlevels=False, convention=None, slices=[], smooth=None, kernel='gauss', **kwargs):
        '''
        Overlay contours on the current plot

        Required Arguments:

            *data*: [ string | pyfits PrimaryHDU | pyfits ImageHDU ]
                Either the filename of the FITS file to open, or a pyfits
                PrimaryHDU or ImageHDU instance.

        Optional Keyword Arguments:

            *hdu*: [ integer ]
                By default, the image in the primary HDU is read in. If a
                different HDU is required, use this argument.

            *layer*: [ string ]
                The name of the contour layer. This is useful for giving
                custom names to layers (instead of contour_set_n) and for
                replacing existing layers.

            *levels*: [ int | list ]
                This can either be the number of contour levels to compute
                (if an integer is provided) or the actual list of contours
                to show (if a list of floats is provided)

            *filled*: [ True | False ]
                Whether to show filled or line contours

            *cmap*: [ string ]
                The colormap to use for the contours

            *colors*: [ string | tuple of strings ]
                If a single string is provided, all contour levels will be
                shown in this color. If a tuple of strings is provided,
                each contour will be colored according to the corresponding
                tuple element.

            *returnlevels*: [ True | False ]
                Whether to return the list of contours to the caller.

            *convention*: [ string ]
                This is used in cases where a FITS header can be interpreted
                in multiple ways. For example, for files with a -CAR
                projection and CRVAL2=0, this can be set to 'wells' or
                'calabretta' to choose the appropriate convention.

            *slices*: [ tuple or list ]
                If a FITS file with more than two dimensions is specified,
                then these are the slices to extract. If all extra dimensions
                only have size 1, then this is not required.

            *smooth*: [ integer | tuple ]
                Default smoothing scale is 3 pixels across. User can define
                whether they want an NxN kernel (integer), or NxM kernel
                (tuple). This argument corresponds to the 'gauss' and 'box'
                smoothing kernels.

            *kernel*: [ 'gauss' | 'box' | numpy.array]
                Default kernel used for smoothing is 'gauss'. The user can
                specify if they would prefer 'gauss', 'box', or a custom
                kernel. All kernels are normalized to ensure flux retention.

            Additional keyword arguments (such as alpha, linewidths, or
            linestyles) will be passed on directly to matplotlib's contour or
            contourf methods. For more information on these additional
            arguments, see the *Optional keyword arguments* sections in the
            documentation for `contour
            <http://matplotlib.sourceforge.net/api/axes_api.html?
            #matplotlib.axes.Axes.contour>`_ and `contourf
            <http://matplotlib.sourceforge.net/api/axes_api.html?
            #matplotlib.axes.Axes.contourf>`_.
        '''
        if layer:
            self.remove_layer(layer, raise_exception=False)

        if cmap:
            cmap = mpl.cm.get_cmap(cmap, 1000)
        elif not colors:
            cmap = mpl.cm.get_cmap('jet', 1000)

        hdu_contour, wcs_contour = self._get_hdu(data, hdu, False, \
            convention=convention, slices=slices)

        image_contour = convolve_util.convolve(hdu_contour.data,smooth=smooth,kernel=kernel)
        extent_contour = (0.5, wcs_contour.naxis1+0.5, 0.5, wcs_contour.naxis2+0.5)

        if type(levels) == int:
            auto_levels = image_util.percentile_function(image_contour)
            vmin = auto_levels(0.25)
            vmax = auto_levels(99.75)
            levels = np.linspace(vmin, vmax, levels)

        if filled:
            c = self._ax1.contourf(image_contour, levels, extent=extent_contour, cmap=cmap, colors=colors, **kwargs)
        else:
            c = self._ax1.contour(image_contour, levels, extent=extent_contour, cmap=cmap, colors=colors, **kwargs)

        if layer:
            contour_set_name = layer
        else:
            self._contour_counter += 1
            contour_set_name = 'contour_set_'+str(self._contour_counter)

        contour_util.transform(c, wcs_contour, self._wcs, filled=filled)

        self._layers[contour_set_name] = c

        if returnlevels:
            return levels

    # This method plots markers. The input should be an Nx2 array with WCS coordinates
    # in degree format.

    @auto_refresh
    def show_markers(self, xw, yw, layer=False, **kwargs):
        '''
        Overlay markers on the current plot.

        Required arguments:

            *xw*: [ list | numpy.ndarray ]
                The x postions of the markers (in world coordinates)

            *yw*: [ list | numpy.ndarray ]
                The y positions of the markers (in world coordinates)

        Optional Keyword Arguments:

            *layer*: [ string ]
                The name of the scatter layer. This is useful for giving
                custom names to layers (instead of marker_set_n) and for
                replacing existing layers.

        Additional keyword arguments (such as marker, facecolor, edgecolor,
        alpha, or linewidth) will be passed on directly to matplotlib's
        scatter method. For more information on these additional arguments,
        see the *Optional keyword arguments* sections in the documentation for
        `scatter <http://matplotlib.sourceforge.net/api/
        axes_api.html?#matplotlib.axes.Axes.scatter>`_.

        '''

        if not 'c' in kwargs:
            kwargs.setdefault('edgecolor', 'red')
            kwargs.setdefault('facecolor', 'none')

        kwargs.setdefault('s', 30)

        if layer:
            self.remove_layer(layer, raise_exception=False)

        xp, yp = wcs_util.world2pix(self._wcs, xw, yw)
        s = self._ax1.scatter(xp, yp, **kwargs)

        if layer:
            marker_set_name = layer
        else:
            self._scatter_counter += 1
            marker_set_name = 'marker_set_'+str(self._scatter_counter)

        self._layers[marker_set_name] = s

    # Show circles. Different from markers as this method allows more definitions
    # for the circles.
    @auto_refresh
    def show_circles(self, xw, yw, radius, layer=False, **kwargs):
        '''
        Overlay circles on the current plot.

        Required arguments:

            *xw*: [ list | numpy.ndarray ]
                The x postions of the circles (in world coordinates)

            *yw*: [ list | numpy.ndarray ]
                The y positions of the circles (in world coordinates)

            *radius*: [integer | float | list | numpy.ndarray ]
                The radii of the circles in degrees

        Optional Keyword Arguments:

            *layer*: [ string ]
                The name of the circle layer. This is useful for giving
                custom names to layers (instead of circle_set_n) and for
                replacing existing layers.

        Additional keyword arguments (such as facecolor, edgecolor, alpha,
        or linewidth) can be used to control the appearance of the circles,
        which are instances of the matplotlib Circle class. For more
        information on available arguments, see `Circle
        <http://matplotlib.sourceforge.net/api/
        artist_api.html#matplotlib.patches.Circle>`_.
        '''

        if np.isscalar(xw):
            xw = np.array([xw])
        else:
            xw = np.array(xw)

        if np.isscalar(yw):
            yw = np.array([yw])
        else:
            yw = np.array(yw)

        if np.isscalar(radius):
            radius = np.repeat(radius, len(xw))
        else:
            radius = np.array(radius)

        if not 'facecolor' in kwargs:
            kwargs.setdefault('facecolor', 'none')

        if layer:
            self.remove_layer(layer, raise_exception=False)

        xp, yp = wcs_util.world2pix(self._wcs, xw, yw)
        rp = 3600.0*radius/wcs_util.arcperpix(self._wcs)

        patches = []
        for i in range(len(xp)):
            patches.append(Circle((xp[i], yp[i]), radius=rp[i], **kwargs))

        c = self._ax1.add_collection(PatchCollection(patches, match_original=True))

        if layer:
            circle_set_name = layer
        else:
            self._circle_counter += 1
            circle_set_name = 'circle_set_'+str(self._circle_counter)

        self._layers[circle_set_name] = c

    @auto_refresh
    def show_ellipses(self, xw, yw, width, height, layer=False, **kwargs):
        '''
       Overlay ellipses on the current plot.

       Required arguments:

           *xw*: [ list | numpy.ndarray ]
               The x postions of the ellipses (in world coordinates)

           *yw*: [ list | numpy.ndarray ]
               The y positions of the ellipses (in world coordinates)

           *width*: [integer | float | list | numpy.ndarray ]
               The width of the ellipse in degrees

           *height*: [integer | float | list | numpy.ndarray ]
               The height of the ellipse in degrees

       Optional Keyword Arguments:

           *angle*: [integer | float | list | numpy.ndarray ]
               rotation in degrees (anti-clockwise). Default
               angle is 0.0.

           *layer*: [ string ]
               The name of the ellipse layer. This is useful for giving
               custom names to layers (instead of ellipse_set_n) and for
               replacing existing layers.

       Additional keyword arguments (such as facecolor, edgecolor, alpha,
       or linewidth) can be used to control the appearance of the ellipses,
       which are instances of the matplotlib Ellipse class. For more
       information on available arguments, see `Ellipse
       <http://matplotlib.sourceforge.net/api/
       artist_api.html#matplotlib.patches.Ellipse>`_.
       '''

        if np.isscalar(xw):
            xw = np.array([xw])
        else:
            xw = np.array(xw)

        if np.isscalar(yw):
            yw = np.array([yw])
        else:
            yw = np.array(yw)

        if np.isscalar(width):
            width = np.repeat(width, len(xw))
        else:
            width = np.array(width)

        if np.isscalar(height):
            height = np.repeat(height, len(xw))
        else:
            height = np.array(height)

        if not 'facecolor' in kwargs:
            kwargs.setdefault('facecolor', 'none')

        if layer:
            self.remove_layer(layer, raise_exception=False)

        xp, yp = wcs_util.world2pix(self._wcs, xw, yw)
        wp = 3600.0*width/wcs_util.arcperpix(self._wcs)
        hp = 3600.0*height/wcs_util.arcperpix(self._wcs)

        patches = []
        for i in range(len(xp)):
            patches.append(Ellipse((xp[i], yp[i]), width=wp[i], height=hp[i], **kwargs))

        c = self._ax1.add_collection(PatchCollection(patches, match_original=True))

        if layer:
            ellipse_set_name = layer
        else:
            self._ellipse_counter += 1
            ellipse_set_name = 'ellipse_set_'+str(self._ellipse_counter)

        self._layers[ellipse_set_name] = c

    @auto_refresh
    def show_rectangles(self, xw, yw, width, height, layer=False, **kwargs):
        '''
       Overlay rectangles on the current plot.

       Required arguments:

           *xw*: [ list | numpy.ndarray ]
               The x postions of the rectangles (in world coordinates)

           *yw*: [ list | numpy.ndarray ]
               The y positions of the rectangles (in world coordinates)

           *width*: [integer | float | list | numpy.ndarray ]
               The width of the rectangle in degrees

           *height*: [integer | float | list | numpy.ndarray ]
               The height of the rectangle in degrees

       Optional Keyword Arguments:

           *layer*: [ string ]
               The name of the rectangle layer. This is useful for giving
               custom names to layers (instead of rectangle_set_n) and for
               replacing existing layers.

       Additional keyword arguments (such as facecolor, edgecolor, alpha,
       or linewidth) can be used to control the appearance of the
       rectangles, which are instances of the matplotlib Rectangle class.
       For more information on available arguments, see `Rectangle
       <http://matplotlib.sourceforge.net/api/
       artist_api.html#matplotlib.patches.Rectangle>`_.
       '''

        if np.isscalar(xw):
            xw = np.array([xw])
        else:
            xw = np.array(xw)

        if np.isscalar(yw):
            yw = np.array([yw])
        else:
            yw = np.array(yw)

        if np.isscalar(width):
            width = np.repeat(width, len(xw))
        else:
            width = np.array(width)

        if np.isscalar(height):
            height = np.repeat(height, len(xw))
        else:
            height = np.array(height)

        if not 'facecolor' in kwargs:
            kwargs.setdefault('facecolor', 'none')

        if layer:
            self.remove_layer(layer, raise_exception=False)

        xp, yp = wcs_util.world2pix(self._wcs, xw, yw)
        wp = 3600.0*width/wcs_util.arcperpix(self._wcs)
        hp = 3600.0*height/wcs_util.arcperpix(self._wcs)

        patches = []
        xp = xp - wp/2.
        yp = yp - hp/2.
        for i in range(len(xp)):
            patches.append(Rectangle((xp[i], yp[i]), width=wp[i], height=hp[i], **kwargs))

        c = self._ax1.add_collection(PatchCollection(patches, match_original=True))

        if layer:
            rectangle_set_name = layer
        else:
            self._rectangle_counter += 1
            rectangle_set_name = 'rectangle_set_'+str(self._rectangle_counter)

        self._layers[rectangle_set_name] = c

    @auto_refresh
    def show_polygons(self, polygon_list, layer=False, **kwargs):
        '''
        Overlay polygons on the current plot.

        Required arguments:

            *polygon_list*: [ list ]
                A list of one or more 2xN numpy arrays which contain
                the [x,y] positions of the vertices in world coordinates.

        Optional Keyword Arguments:

            *layer*: [ string ]
                The name of the circle layer. This is useful for giving
                custom names to layers (instead of circle_set_n) and for
                replacing existing layers.

        Additional keyword arguments (such as facecolor, edgecolor, alpha,
        or linewidth) can be used to control the appearance of the circles,
        which are instances of the matplotlib Polygon class. For more
        information on available arguments, see `Polygon
        <http://matplotlib.sourceforge.net/api/
        artist_api.html#matplotlib.patches.Polygon>`_.
        '''

        if not kwargs.has_key('facecolor'):
            kwargs.setdefault('facecolor', 'none')

        if layer:
            self.remove_layer(layer, raise_exception=False)

        pix_polygon_list = []
        for i in range(len(polygon_list)):
            xw = polygon_list[i][:,0]
            yw = polygon_list[i][:,1]
            xp, yp = wcs_util.world2pix(self._wcs, xw, yw)
            pix_polygon_list.append(np.column_stack((xp,yp)))

        patches = []
        for i in range(len(pix_polygon_list)):
            patches.append(Polygon(pix_polygon_list[i], **kwargs))

        c = self._ax1.add_collection(PatchCollection(patches, match_original=True))

        if layer:
            poly_set_name = layer
        else:
            self._poly_counter += 1
            poly_set_name = 'poly_set_'+str(self._poly_counter)

        self._layers[poly_set_name] = c

    @auto_refresh
    @fixdocstring
    def add_label(self, x, y, text, relative=False, color='black',
                  family=None, style=None, variant=None, stretch=None,
                  weight=None, size=None, fontproperties=None,
                  horizontalalignment='center', verticalalignment='center',
                  layer=None, **kwargs):
        '''
        Add a text label

        Required Arguments:

            *x, y*: [ float ]
                Coordinates of the text label

            *text*: [ string ]
                The label

        Optional Keyword Arguments:

            *relative*: [ True | False ]
                Whether the coordinates are to be interpreted as world
                coordinates (e.g. RA/Dec or longitude/latitude), or
                coordinates relative to the axes (where 0.0 is left or bottom
                and 1.0 is right or top).

        common: color, family, style, variant, stretch, weight, size, fontproperties, horizontalalignment, verticalalignment
        '''

        if layer:
            self.remove_layer(layer, raise_exception=False)

        # Can't pass fontproperties=None to text. Only pass it if it is not None.
        if fontproperties:
            kwargs['fontproperties'] = fontproperties

        if relative:
            l = self._ax1.text(x, y, text, color=color,
                               family=family, style=style, variant=variant,
                               stretch=stretch, weight=weight, size=size,
                               horizontalalignment=horizontalalignment,
                               verticalalignment=verticalalignment,
                               transform=self._ax1.transAxes, **kwargs)
        else:
            xp, yp = wcs_util.world2pix(self._wcs, x, y)
            l = self._ax1.text(xp, yp, text, color=color,
                               family=family, style=style, variant=variant,
                               stretch=stretch, weight=weight, size=size,
                               horizontalalignment=horizontalalignment,
                               verticalalignment=verticalalignment, **kwargs)

        if layer:
            label_name = layer
        else:
            self._label_counter += 1
            label_name = 'label_'+str(self._label_counter)

        self._layers[label_name] = l

    def set_auto_refresh(self, refresh):
        '''
        Set whether the display should refresh after each method call

        Required Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display every time a FITSFigure
                method is called. The default is True. If set to false,
                the display can be refreshed manually using the refresh()
                method
        '''
        self._figure._auto_refresh = refresh

    def refresh(self, force=True):
        '''
        Refresh the display

        Optional Keyword Arguments:

            *force*: [ True | False ]
                If set to False, refresh() will only have an effect if
                auto refresh is on. If set to True, the display will be
                refreshed whatever the auto refresh setting is set to.
                The default is True.
        '''
        if self._figure._auto_refresh or force:
            self._figure.canvas.draw()

    def save(self, filename, dpi=None, transparent=False, adjust_bbox=True, max_dpi=300):
        '''
        Save the current figure to a file

        Required arguments:

            *filename*: [ string ]
                The name of the file to save the plot to. This can be
                for example a PS, EPS, PDF, PNG, JPEG, or SVG file.

        Optional Keyword Arguments:

            *dpi*: [ float ]
                The output resolution, in dots per inch. If the output file
                is a vector graphics format (such as PS, EPS, PDF or SVG) only
                the image itself will be rasterized. If the output is a PS or
                EPS file and no dpi is specified, the dpi is automatically
                calculated to match the resolution of the image. If this value is
                larger than max_dpi, then dpi is set to max_dpi.

            *transparent*: [ True | False ]
                Whether to preserve transparency

            *adjust_bbox*: [ True | False ]
                Auto-adjust the bounding box for the output

            *max_dpi*: [ float ]
                The maximum resolution to output images at. If no maximum is
                wanted, enter None or 0.
        '''

        if dpi == None and os.path.splitext(filename)[1].lower() in ['.eps', '.ps', '.pdf']:
            width = self._ax1.get_position().width * self._figure.get_figwidth()
            interval = self._ax1.xaxis.get_view_interval()
            nx = interval[1] - interval[0]
            if max_dpi:
                dpi = np.minimum(nx / width, max_dpi)
            else:
                dpi = nx / width
            print "Auto-setting resolution to ", dpi, " dpi"

        artists = []
        if adjust_bbox:
            for artist in self._layers.values():
                if hasattr(artist, 'get_window_extent'):
                    artists.append(artist)
            self._figure.savefig(filename, dpi=dpi, transparent=transparent, bbox_inches='tight', bbox_extra_artists=artists)
        else:
            self._figure.savefig(filename, dpi=dpi, transparent=transparent)

    def _initialize_view(self):

        self._ax1.xaxis.set_view_interval(+0.5, self._wcs.naxis1+0.5)
        self._ax1.yaxis.set_view_interval(+0.5, self._wcs.naxis2+0.5)
        self._ax2.xaxis.set_view_interval(+0.5, self._wcs.naxis1+0.5)
        self._ax2.yaxis.set_view_interval(+0.5, self._wcs.naxis2+0.5)

        # set the image extent to FITS pixel coordinates
        self._extent = (0.5, self._wcs.naxis1+0.5, 0.5, self._wcs.naxis2+0.5)

    def _get_invert_default(self):
        return self._figure.apl_grayscale_invert_default

    def _get_colormap_default(self):
        return self._figure.apl_colorscale_cmap_default

    @auto_refresh
    def set_theme(self, theme):
        '''
        Set the axes, ticks, grid, and image colors to a certain style (experimental)

        Required Arguments:

            *theme*: [ string ]
                The theme to use. At the moment, this can be 'pretty' (for
                viewing on-screen) and 'publication' (which makes the ticks
                and grid black, and displays the image in inverted grayscale)
       '''

        if theme=='pretty':
            self.frame.set_color('white')
            self.frame.set_linewidth(0.5)
            self.ticks.set_color('white')
            self.ticks.set_length(7)
            self._figure.apl_grayscale_invert_default = False
            self._figure.apl_colorscale_cmap_default = 'jet'
            if self.image:
                self.image.set_cmap(cmap=mpl.cm.get_cmap('jet', 1000))
        elif theme=='publication':
            self.frame.set_color('black')
            self.frame.set_linewidth(0.5)
            self.ticks.set_color('black')
            self.ticks.set_length(7)
            self._figure.apl_grayscale_invert_default = True
            self._figure.apl_colorscale_cmap_default = 'gist_heat'
            if self.image:
                self.image.set_cmap(cmap=mpl.cm.get_cmap('gist_yarg', 1000))

    def world2pixel(self, xw, yw):
        '''
        Convert world to pixel coordinates

        Required arguments:

            *xw*: [ scalar | list | numpy array ]
                x world coordinate

            *yw*: [ scalar | list | numpy array ]
                y world coordinate

        Returns the pixel coordinates as a tuple of scalars, lists, or numpy arrays depending on the input
        '''

        return wcs_util.world2pix(self._wcs, xw, yw)

    def pixel2world(self, xp, yp):
        '''
        Convert pixel to world coordinates

        Required arguments:

            *xp*: [ scalar | list | numpy array ]
                x pixel coordinate

            *yp*: [ scalar | list | numpy array ]
                y pixel coordinate

        Returns the world coordinates as a tuple of scalars, lists, or numpy arrays depending on the input
        '''

        return wcs_util.pix2world(self._wcs, xp, yp)


    @auto_refresh
    def add_grid(self, *args, **kwargs):
        '''
        Add a coordinate to the current figure

        Once this method has been run, a grid attribute becomes available,
        and can be used to control the aspect of the grid::

            >>> f = aplpy.FITSFigure(...)
            >>> ...
            >>> f.add_grid()
            >>> f.grid.set_color('white')
            >>> f.grid.set_alpha(0.5)
            >>> ...
        '''
        if hasattr(self, 'grid'):
            raise Exception("Grid already exists")
        try:
            self.grid = Grid(self)
            self.grid.show(*args, **kwargs)
        except:
            del self.grid
            raise

    @auto_refresh
    def remove_grid(self):
        '''
        Removes the grid from the current figure
        '''
        self.grid._remove()
        del self.grid

    @auto_refresh
    def add_beam(self, *args, **kwargs):
        '''
        Add a beam to the current figure

        Once this method has been run, a beam attribute becomes available,
        and can be used to control the aspect of the beam::

            >>> f = aplpy.FITSFigure(...)
            >>> ...
            >>> f.add_beam()
            >>> f.beam.set_color('white')
            >>> f.beam.set_hatch('+')
            >>> ...
        '''
        if hasattr(self, 'beam'):
            raise Exception("Beam already exists")
        try:
            self.beam = Beam(self)
            self.beam.show(*args, **kwargs)
        except:
            del self.beam
            raise

    @auto_refresh
    def remove_beam(self):
        '''
        Removes the beam from the current figure
        '''
        self.beam._remove()
        del self.beam

    @auto_refresh
    def add_scalebar(self, *args, **kwargs):
        '''
        Add a scalebar to the current figure

        Once this method has been run, a scalebar attribute becomes
        available, and can be used to control the aspect of the scalebar::

            >>> f = aplpy.FITSFigure(...)
            >>> ...
            >>> f.add_scalebar(0.01) # length has to be specified
            >>> f.scalebar.set_label('100 AU')
            >>> ...
        '''
        if hasattr(self, 'scalebar'):
            raise Exception("Scalebar already exists")
        try:
            self.scalebar = ScaleBar(self)
            self.scalebar.show(*args, **kwargs)
        except:
            del self.scalebar
            raise

    @auto_refresh
    def remove_scalebar(self):
        '''
        Removes the scalebar from the current figure
        '''
        self.scalebar._remove()
        del self.scalebar

    @auto_refresh
    def add_colorbar(self, *args, **kwargs):
        '''
        Add a colorbar to the current figure

        Once this method has been run, a colorbar attribute becomes
        available, and can be used to control the aspect of the colorbar::

            >>> f = aplpy.FITSFigure(...)
            >>> ...
            >>> f.add_colorbar()
            >>> f.colorbar.set_width(0.3)
            >>> f.colorbar.set_location('top')
            >>> ...
        '''
        if hasattr(self, 'colorbar'):
            raise Exception("Colorbar already exists")
        if self.image is None:
            raise Exception("No image is shown, so a colorbar cannot be displayed")
        try:
            self.colorbar = Colorbar(self)
            self.colorbar.show(*args, **kwargs)
        except:
            del self.colorbar
            raise

    @auto_refresh
    def remove_colorbar(self):
        '''
        Removes the colorbar from the current figure
        '''
        self.colorbar._remove()
        del self.colorbar
