from __future__ import absolute_import, print_function, division

from distutils import version
import os
import operator
from functools import reduce

import matplotlib

if version.LooseVersion(matplotlib.__version__) < version.LooseVersion('1.0.0'):
    raise Exception("matplotlib 1.0.0 or later is required for APLpy")

import matplotlib.pyplot as mpl
import mpl_toolkits.axes_grid.parasite_axes as mpltk
from astropy.extern import six

WCS_TYPES = []
HDU_TYPES = []
HDULIST_TYPES = []

# We need to be able to accept PyFITS objects if users have old scripts that
# are reading FITS files with this instead of Astropy
try:
    import pyfits
    HDU_TYPES.append(pyfits.PrimaryHDU)
    HDU_TYPES.append(pyfits.ImageHDU)
    HDU_TYPES.append(pyfits.CompImageHDU)
    HDULIST_TYPES.append(pyfits.HDUList)
    del pyfits
except ImportError:
    pass

# Similarly, we need to accept PyWCS objects
try:
    import pywcs
    WCS_TYPES.append(pywcs.WCS)
    del pywcs
except ImportError:
    pass

from astropy.io import fits
HDU_TYPES.append(fits.PrimaryHDU)
HDU_TYPES.append(fits.ImageHDU)
HDU_TYPES.append(fits.CompImageHDU)
HDULIST_TYPES.append(fits.HDUList)

from astropy.wcs import WCS
WCS_TYPES.append(WCS)
del WCS

# Convert to tuples so that these work when calling isinstance()
HDU_TYPES = tuple(HDU_TYPES)
HDULIST_TYPES = tuple(HDULIST_TYPES)
WCS_TYPES = tuple(WCS_TYPES)

import numpy as np

from matplotlib.patches import Circle, Rectangle, Ellipse, Polygon, FancyArrow
from matplotlib.collections import PatchCollection, LineCollection

from astropy import log
import astropy.utils.exceptions as aue

from . import contour_util
from . import convolve_util
from . import image_util
from . import header as header_util
from . import wcs_util
from . import slicer

from .layers import Layers
from .grid import Grid
from .ticks import Ticks
from .labels import TickLabels
from .axis_labels import AxisLabels
from .overlays import Beam, Scalebar
from .regions import Regions
from .colorbar import Colorbar
from .normalize import APLpyNormalize
from .frame import Frame

from .decorators import auto_refresh, fixdocstring

from .deprecated import Deprecated

class Parameters():
    '''
    A class to contain the current plotting parameters
    '''
    pass


class FITSFigure(Layers, Regions, Deprecated):

    "A class for plotting FITS files."

    _parameters = Parameters()

    @auto_refresh
    def __init__(self, data, hdu=0, figure=None, subplot=(1, 1, 1),
                 downsample=False, north=False, convention=None,
                 dimensions=[0, 1], slices=[], auto_refresh=None,
                 **kwargs):
        '''
        Create a FITSFigure instance.

        Parameters
        ----------

        data : see below

            The FITS file to open. The following data types can be passed:

                 string
                 astropy.io.fits.PrimaryHDU
                 astropy.io.fits.ImageHDU
                 pyfits.PrimaryHDU
                 pyfits.ImageHDU
                 astropy.wcs.WCS
                 np.ndarray
                 RGB image with AVM meta-data

        hdu : int, optional
            By default, the image in the primary HDU is read in. If a
            different HDU is required, use this argument.

        figure : ~matplotlib.figure.Figure, optional
            If specified, a subplot will be added to this existing
            matplotlib figure() instance, rather than a new figure
            being created from scratch.

        subplot : tuple or list, optional
            If specified, a subplot will be added at this position. If a tuple
            of three values, the tuple should contain the standard matplotlib
            subplot parameters, i.e. (ny, nx, subplot). If a list of four
            values, the list should contain [xmin, ymin, dx, dy] where xmin
            and ymin are the position of the bottom left corner of the
            subplot, and dx and dy are the width and height of the subplot
            respectively. These should all be given in units of the figure
            width and height. For example, [0.1, 0.1, 0.8, 0.8] will almost
            fill the entire figure, leaving a 10 percent margin on all sides.

        downsample : int, optional
            If this option is specified, the image will be downsampled
            by a factor *downsample* when reading in the data.

        north : str, optional
            Whether to rotate the image so that the North Celestial
            Pole is up. Note that this option requires Montage to be
            installed.

        convention : str, optional
            This is used in cases where a FITS header can be interpreted
            in multiple ways. For example, for files with a -CAR
            projection and CRVAL2=0, this can be set to 'wells' or
            'calabretta' to choose the appropriate convention.

        dimensions : tuple or list, optional
            The index of the axes to use if the data has more than three
            dimensions.

        slices : tuple or list, optional
            If a FITS file with more than two dimensions is specified,
            then these are the slices to extract. If all extra dimensions
            only have size 1, then this is not required.

        auto_refresh : bool, optional
            Whether to refresh the figure automatically every time a
            plotting method is called. This can also be set using the
            set_auto_refresh method. This defaults to `True` if and only if
            APLpy is being used from IPython and the Matplotlib backend is
            interactive.

        kwargs
            Any additional arguments are passed on to matplotlib's Figure() class.
            For example, to set the figure size, use the figsize=(xsize, ysize)
            argument (where xsize and ysize are in inches). For more information
            on these additional arguments, see the *Optional keyword arguments*
            section in the documentation for `Figure
            <http://matplotlib.org/api/figure_api.html?#matplotlib.figure.Figure>`_
        '''

        # Set whether to automatically refresh the display
        self.set_auto_refresh(auto_refresh)

        if not 'figsize' in kwargs:
            kwargs['figsize'] = (10, 9)

        if isinstance(data, six.string_types) and data.split('.')[-1].lower() in ['png', 'jpg', 'tif']:

            try:
                from PIL import Image
            except ImportError:
                try:
                    import Image
                except ImportError:
                    raise ImportError("The Python Imaging Library (PIL) is required to read in RGB images")

            try:
                import pyavm
            except ImportError:
                raise ImportError("PyAVM is required to read in AVM meta-data from RGB images")

            if version.LooseVersion(pyavm.__version__) < version.LooseVersion('0.9.1'):
                raise ImportError("PyAVM installation is not recent enough "
                                  "(version 0.9.1 or later is required).")

            from pyavm import AVM

            # Remember image filename
            self._rgb_image = data

            # Find image size
            nx, ny = Image.open(data).size

            # Now convert AVM information to WCS
            data = AVM.from_image(data).to_wcs()

            # Need to scale CDELT values sometimes the AVM meta-data is only really valid for the full-resolution image
            data.wcs.cdelt = [data.wcs.cdelt[0] * nx / float(nx), data.wcs.cdelt[1] * ny / float(ny)]
            data.wcs.crpix = [data.wcs.crpix[0] / nx * float(nx), data.wcs.crpix[1] / ny * float(ny)]

            # Update the NAXIS values with the true dimensions of the RGB image
            data.nx = nx
            data.ny = ny

        if isinstance(data, WCS_TYPES):
            wcs = data
            if not hasattr(wcs, 'naxis1'):
                raise aue.AstropyDeprecationWarning('WCS no longer stores information about NAXISn '
                                                    'so it is not possibly to instantiate a FITSFigure '
                                                    'from WCS alone')

            if wcs.naxis != 2:
                raise ValueError("FITSFigure initialization via WCS objects can only be done with 2-dimensional WCS objects")
            header = wcs.to_header()
            header['NAXIS1'] = wcs.naxis1
            header['NAXIS2'] = wcs.naxis2
            nx = header['NAXIS%i' % (dimensions[0] + 1)]
            ny = header['NAXIS%i' % (dimensions[1] + 1)]
            self._data = np.zeros((ny, nx), dtype=float)
            self._header = header
            self._wcs = wcs_util.WCS(header, dimensions=dimensions, slices=slices, relax=True)
            self._wcs.nx = nx
            self._wcs.ny = ny
            if downsample:
                log.warning("downsample argument is ignored if data passed is a WCS object")
                downsample = False
            if north:
                log.warning("north argument is ignored if data passed is a WCS object")
                north = False
        else:
            self._data, self._header, self._wcs = self._get_hdu(data, hdu, north, \
                convention=convention, dimensions=dimensions, slices=slices)
            self._wcs.nx = self._header['NAXIS%i' % (dimensions[0] + 1)]
            self._wcs.ny = self._header['NAXIS%i' % (dimensions[1] + 1)]

        # Downsample if requested
        if downsample:
            nx_new = self._wcs.nx - np.mod(self._wcs.nx, downsample)
            ny_new = self._wcs.ny - np.mod(self._wcs.ny, downsample)
            self._data = self._data[0:ny_new, 0:nx_new]
            self._data = image_util.resample(self._data, downsample)
            self._wcs.nx, self._wcs.ny = nx_new, ny_new

        # Open the figure
        if figure:
            self._figure = figure
        else:
            self._figure = mpl.figure(**kwargs)

        # Create first axis instance
        if type(subplot) == list and len(subplot) == 4:
            self._ax1 = mpltk.HostAxes(self._figure, subplot, adjustable='datalim')
        elif type(subplot) == tuple and len(subplot) == 3:
            self._ax1 = mpltk.SubplotHost(self._figure, *subplot)
        else:
            raise ValueError("subplot= should be either a tuple of three values, or a list of four values")

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
        self._ax1._wcs = self._wcs
        self._ax2._wcs = self._wcs

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
        self._auto_v = image_util.percentile_function(self._data)

        # Set image holder to be empty
        self.image = None

        # Set default theme
        self.set_theme(theme='pretty')

    def _get_hdu(self, data, hdu, north, convention=None, dimensions=[0, 1], slices=[]):

        if isinstance(data, six.string_types):

            filename = data

            # Check file exists
            if not os.path.exists(filename):
                raise IOError("File not found: " + filename)

            # Read in FITS file
            try:
                hdulist = fits.open(filename)
            except:
                raise IOError("An error occurred while reading the FITS file")

            # Check whether the HDU specified contains any data, otherwise
            # cycle through all HDUs to find one that contains valid image data
            if hdulist[hdu].data is None:
                found = False
                for alt_hdu in range(len(hdulist)):
                    if isinstance(hdulist[alt_hdu], HDU_TYPES):
                        if hdulist[alt_hdu].data is not None:
                            log.warning("hdu=%i does not contain any data, using hdu=%i instead" % (hdu, alt_hdu))
                            hdu = hdulist[alt_hdu]
                            found = True
                            break
                if not found:
                    raise Exception("FITS file does not contain any image data")

            else:
                hdu = hdulist[hdu]

        elif type(data) == np.ndarray:

            hdu = fits.ImageHDU(data)

        elif isinstance(data, HDU_TYPES):

            hdu = data

        elif isinstance(data, HDULIST_TYPES):

            hdu = data[hdu]

        else:

            raise Exception("data argument should either be a filename, an HDU object from astropy.io.fits or pyfits, a WCS object from astropy.wcs or pywcs, or a Numpy array.")

        # Check that we have at least 2-dimensional data
        if hdu.header['NAXIS'] < 2:
            raise ValueError("Data should have at least two dimensions")

        # Check dimensions= argument
        if type(dimensions) not in [list, tuple]:
            raise ValueError('dimensions= should be a list or a tuple')
        if len(set(dimensions)) != 2 or len(dimensions) != 2:
            raise ValueError("dimensions= should be a tuple of two different values")
        if dimensions[0] < 0 or dimensions[0] > hdu.header['NAXIS'] - 1:
            raise ValueError('values of dimensions= should be between %i and %i' % (0, hdu.header['NAXIS'] - 1))
        if dimensions[1] < 0 or dimensions[1] > hdu.header['NAXIS'] - 1:
            raise ValueError('values of dimensions= should be between %i and %i' % (0, hdu.header['NAXIS'] - 1))

        # Reproject to face north if requested
        if north:
            try:
                import montage_wrapper as montage
            except ImportError:
                raise Exception("Both the Montage command-line tools and the"
                                " montage-wrapper Python module are required"
                                " to use the north= argument")
            hdu = montage.reproject_hdu(hdu, north_aligned=True)

        # Now copy the data and header to new objects, since in PyFITS the two
        # attributes are linked, which can lead to confusing behavior. We just
        # need to copy the header to avoid memory issues - as long as one item
        # is copied, the two variables are decoupled.
        data = hdu.data
        header = hdu.header.copy()
        del hdu

        # If slices wasn't specified, check if we can guess
        shape = data.shape
        if len(shape) > 2:
            n_total = reduce(operator.mul, shape)
            n_image = shape[len(shape) - 1 - dimensions[0]] \
                    * shape[len(shape) - 1 - dimensions[1]]
            if n_total == n_image:
                slices = [0 for i in range(1, len(shape) - 1)]
                log.info("Setting slices=%s" % str(slices))

        # Extract slices
        data = slicer.slice_hypercube(data, header, dimensions=dimensions, slices=slices)

        # Check header
        header = header_util.check(header, convention=convention, dimensions=dimensions)

        # Parse WCS info
        wcs = wcs_util.WCS(header, dimensions=dimensions, slices=slices, relax=True)

        return data, header, wcs

    @auto_refresh
    def set_title(self, title, **kwargs):
        '''
        Set the figure title
        '''
        self._ax1.set_title(title, **kwargs)

    @auto_refresh
    def set_xaxis_coord_type(self, coord_type):
        '''
        Set the type of x coordinate.

        Options are:

        * ``scalar``: treat the values are normal decimal scalar values
        * ``longitude``: treat the values as a longitude in the 0 to 360 range
        * ``latitude``: treat the values as a latitude in the -90 to 90 range
        '''
        self._wcs.set_xaxis_coord_type(coord_type)

    @auto_refresh
    def set_yaxis_coord_type(self, coord_type):
        '''
        Set the type of y coordinate.

        Options are:

        * ``scalar``: treat the values are normal decimal scalar values
        * ``longitude``: treat the values as a longitude in the 0 to 360 range
        * ``latitude``: treat the values as a latitude in the -90 to 90 range
        '''
        self._wcs.set_yaxis_coord_type(coord_type)

    @auto_refresh
    def set_system_latex(self, usetex):
        '''
        Set whether to use a real LaTeX installation or the built-in matplotlib LaTeX.

        Parameters
        ----------

        usetex : str
            Whether to use a real LaTex installation (True) or the built-in
            matplotlib LaTeX (False). Note that if the former is chosen, an
            installation of LaTex is required.
        '''
        mpl.rc('text', usetex=usetex)

    @auto_refresh
    def recenter(self, x, y, radius=None, width=None, height=None):
        '''
        Center the image on a given position and with a given radius.

        Either the radius or width/height arguments should be specified. The
        units of the radius or width/height should be the same as the world
        coordinates in the WCS. For images of the sky, this is often (but not
        always) degrees.

        Parameters
        ----------

        x, y : float
            Coordinates to center on

        radius : float, optional
            Radius of the region to view in degrees. This produces a square plot.

        width : float, optional
            Width of the region to view. This should be given in
            conjunction with the height argument.

        height : float, optional
            Height of the region to view. This should be given in
            conjunction with the width argument.
        '''

        xpix, ypix = wcs_util.world2pix(self._wcs, x, y)

        if self._wcs.is_celestial:
            sx = sy = wcs_util.celestial_pixel_scale(self._wcs)
        else:
            sx, sy = wcs_util.non_celestial_pixel_scales(self._wcs)

        if radius:
            dx_pix = radius / sx
            dy_pix = radius / sy
        elif width and height:
            dx_pix = width / sx * 0.5
            dy_pix = height / sy * 0.5
        else:
            raise Exception("Need to specify either radius= or width= and height= arguments")

        if xpix + dx_pix < self._extent[0] or \
           xpix - dx_pix > self._extent[1] or \
           ypix + dy_pix < self._extent[2] or \
           ypix - dy_pix > self._extent[3]:

            raise Exception("Zoom region falls outside the image")

        self._ax1.set_xlim(xpix - dx_pix, xpix + dx_pix)
        self._ax1.set_ylim(ypix - dy_pix, ypix + dy_pix)

    @auto_refresh
    def show_grayscale(self, vmin=None, vmid=None, vmax=None,
                       pmin=0.25, pmax=99.75,
                       stretch='linear', exponent=2, invert='default',
                       smooth=None, kernel='gauss', aspect='equal',
                       interpolation='nearest'):
        '''
        Show a grayscale image of the FITS file.

        Parameters
        ----------

        vmin : None or float, optional
            Minimum pixel value to use for the grayscale. If set to None,
            the minimum pixel value is determined using pmin (default).

        vmax : None or float, optional
            Maximum pixel value to use for the grayscale. If set to None,
            the maximum pixel value is determined using pmax (default).

        pmin : float, optional
            Percentile value used to determine the minimum pixel value to
            use for the grayscale if vmin is set to None. The default
            value is 0.25%.

        pmax : float, optional
            Percentile value used to determine the maximum pixel value to
            use for the grayscale if vmax is set to None. The default
            value is 99.75%.

        stretch : { 'linear', 'log', 'sqrt', 'arcsinh', 'power' }, optional
            The stretch function to use

        vmid : None or float, optional
            Baseline value used for the log and arcsinh stretches. If
            set to None, this is set to zero for log stretches and to
            vmin - (vmax - vmin) / 30. for arcsinh stretches

        exponent : float, optional
            If stretch is set to 'power', this is the exponent to use

        invert : str, optional
            Whether to invert the grayscale or not. The default is False,
            unless set_theme is used, in which case the default depends on
            the theme.

        smooth : int or tuple, optional
            Default smoothing scale is 3 pixels across. User can define
            whether they want an NxN kernel (integer), or NxM kernel
            (tuple). This argument corresponds to the 'gauss' and 'box'
            smoothing kernels.

        kernel : { 'gauss', 'box', numpy.array }, optional
            Default kernel used for smoothing is 'gauss'. The user can
            specify if they would prefer 'gauss', 'box', or a custom
            kernel. All kernels are normalized to ensure flux retention.

        aspect : { 'auto', 'equal' }, optional
            Whether to change the aspect ratio of the image to match that
            of the axes ('auto') or to change the aspect ratio of the axes
            to match that of the data ('equal'; default)

        interpolation : str, optional
            The type of interpolation to use for the image. The default is
            'nearest'. Other options include 'none' (no interpolation,
            meaning that if exported to a postscript file, the grayscale
            will be output at native resolution irrespective of the dpi
            setting), 'bilinear', 'bicubic', and many more (see the
            matplotlib documentation for imshow).
        '''

        if invert == 'default':
            invert = self._get_invert_default()

        if invert:
            cmap = 'gist_yarg'
        else:
            cmap = 'gray'

        self.show_colorscale(vmin=vmin, vmid=vmid, vmax=vmax,
                             pmin=pmin, pmax=pmax,
                             stretch=stretch, exponent=exponent, cmap=cmap,
                             smooth=smooth, kernel=kernel, aspect=aspect,
                             interpolation=interpolation)

    @auto_refresh
    def hide_grayscale(self, *args, **kwargs):
        self.hide_colorscale(*args, **kwargs)

    @auto_refresh
    def show_colorscale(self, vmin=None, vmid=None, vmax=None, \
                             pmin=0.25, pmax=99.75,
                             stretch='linear', exponent=2, cmap='default',
                             smooth=None, kernel='gauss', aspect='equal',
                             interpolation='nearest'):
        '''
        Show a colorscale image of the FITS file.

        Parameters
        ----------

        vmin : None or float, optional
            Minimum pixel value to use for the colorscale. If set to None,
            the minimum pixel value is determined using pmin (default).

        vmax : None or float, optional
            Maximum pixel value to use for the colorscale. If set to None,
            the maximum pixel value is determined using pmax (default).

        pmin : float, optional
            Percentile value used to determine the minimum pixel value to
            use for the colorscale if vmin is set to None. The default
            value is 0.25%.

        pmax : float, optional
            Percentile value used to determine the maximum pixel value to
            use for the colorscale if vmax is set to None. The default
            value is 99.75%.

        stretch : { 'linear', 'log', 'sqrt', 'arcsinh', 'power' }, optional
            The stretch function to use

        vmid : None or float, optional
            Baseline value used for the log and arcsinh stretches. If
            set to None, this is set to zero for log stretches and to
            vmin - (vmax - vmin) / 30. for arcsinh stretches

        exponent : float, optional
            If stretch is set to 'power', this is the exponent to use

        cmap : str, optional
            The name of the colormap to use

        smooth : int or tuple, optional
            Default smoothing scale is 3 pixels across. User can define
            whether they want an NxN kernel (integer), or NxM kernel
            (tuple). This argument corresponds to the 'gauss' and 'box'
            smoothing kernels.

        kernel : { 'gauss', 'box', numpy.array }, optional
            Default kernel used for smoothing is 'gauss'. The user can
            specify if they would prefer 'gauss', 'box', or a custom
            kernel. All kernels are normalized to ensure flux retention.

        aspect : { 'auto', 'equal' }, optional
            Whether to change the aspect ratio of the image to match that
            of the axes ('auto') or to change the aspect ratio of the axes
            to match that of the data ('equal'; default)

        interpolation : str, optional
            The type of interpolation to use for the image. The default is
            'nearest'. Other options include 'none' (no interpolation,
            meaning that if exported to a postscript file, the colorscale
            will be output at native resolution irrespective of the dpi
            setting), 'bilinear', 'bicubic', and many more (see the
            matplotlib documentation for imshow).
        '''

        if cmap == 'default':
            cmap = self._get_colormap_default()

        min_auto = np.equal(vmin, None)
        max_auto = np.equal(vmax, None)

        # The set of available functions
        cmap = mpl.cm.get_cmap(cmap)

        if min_auto:
            vmin = self._auto_v(pmin)

        if max_auto:
            vmax = self._auto_v(pmax)

        # Prepare normalizer object
        normalizer = APLpyNormalize(stretch=stretch, exponent=exponent,
                                    vmid=vmid, vmin=vmin, vmax=vmax)

        # Adjust vmin/vmax if auto
        if min_auto:
            if stretch == 'linear':
                vmin = -0.1 * (vmax - vmin) + vmin
            log.info("Auto-setting vmin to %10.3e" % vmin)

        if max_auto:
            if stretch == 'linear':
                vmax = 0.1 * (vmax - vmin) + vmax
            log.info("Auto-setting vmax to %10.3e" % vmax)

        # Update normalizer object
        normalizer.vmin = vmin
        normalizer.vmax = vmax

        if self.image:
            self.image.set_visible(True)
            self.image.set_norm(normalizer)
            self.image.set_cmap(cmap=cmap)
            self.image.origin = 'lower'
            self.image.set_interpolation(interpolation)
            self.image.set_data(convolve_util.convolve(self._data,
                                                       smooth=smooth,
                                                       kernel=kernel))
        else:
            self.image = self._ax1.imshow(
                convolve_util.convolve(self._data, smooth=smooth, kernel=kernel),
                cmap=cmap, interpolation=interpolation, origin='lower',
                extent=self._extent, norm=normalizer, aspect=aspect)

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
        Set the color for NaN pixels.

        Parameters
        ----------
        color : str
            This can be any valid matplotlib color
        '''
        from copy import deepcopy
        cm = deepcopy(self.image.get_cmap())
        cm.set_bad(color)
        self.image.set_cmap(cm)

    @auto_refresh
    def show_rgb(self, filename=None, interpolation='nearest', vertical_flip=False, horizontal_flip=False, flip=False):
        '''
        Show a 3-color image instead of the FITS file data.

        Parameters
        ----------

        filename, optional
            The 3-color image should have exactly the same dimensions
            as the FITS file, and will be shown with exactly the same
            projection. If FITSFigure was initialized with an
            AVM-tagged RGB image, the filename is not needed here.

        vertical_flip : str, optional
            Whether to vertically flip the RGB image

        horizontal_flip : str, optional
            Whether to horizontally flip the RGB image
        '''

        try:
            from PIL import Image
        except ImportError:
            try:
                import Image
            except ImportError:
                raise ImportError("The Python Imaging Library (PIL) is required to read in RGB images")

        if flip:
            log.warning("Note that show_rgb should now correctly flip RGB images, so the flip= argument is now deprecated. If you still need to flip an image vertically or horizontally, you can use the vertical_flip= and horizontal_flip arguments instead.")

        if filename is None:
            if hasattr(self, '_rgb_image'):
                image = Image.open(self._rgb_image)
            else:
                raise Exception("Need to specify the filename of an RGB image")
        else:
            image = Image.open(filename)

        if image_util._matplotlib_pil_bug_present():
            vertical_flip = True

        if vertical_flip:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        if horizontal_flip:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # Elsewhere in APLpy we assume that we are using origin='lower' so here
        # we flip the image by default (since RGB images usually would require
        # origin='upper') then we use origin='lower'
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        self.image = self._ax1.imshow(image, extent=self._extent, interpolation=interpolation, origin='lower')

    @auto_refresh
    def show_contour(self, data=None, hdu=0, layer=None, levels=5, filled=False, cmap=None, colors=None, returnlevels=False, convention=None, dimensions=[0, 1], slices=[], smooth=None, kernel='gauss', overlap=False, **kwargs):
        '''
        Overlay contours on the current plot.

        Parameters
        ----------

        data : see below

            The FITS file to plot contours for. The following data types can be passed:

                 string
                 astropy.io.fits.PrimaryHDU
                 astropy.io.fits.ImageHDU
                 pyfits.PrimaryHDU
                 pyfits.ImageHDU
                 astropy.wcs.WCS
                 np.ndarray

        hdu : int, optional
            By default, the image in the primary HDU is read in. If a
            different HDU is required, use this argument.

        layer : str, optional
            The name of the contour layer. This is useful for giving
            custom names to layers (instead of contour_set_n) and for
            replacing existing layers.

        levels : int or list, optional
            This can either be the number of contour levels to compute
            (if an integer is provided) or the actual list of contours
            to show (if a list of floats is provided)

        filled : str, optional
            Whether to show filled or line contours

        cmap : str, optional
            The colormap to use for the contours

        colors : str or tuple, optional
            If a single string is provided, all contour levels will be
            shown in this color. If a tuple of strings is provided,
            each contour will be colored according to the corresponding
            tuple element.

        returnlevels : str, optional
            Whether to return the list of contours to the caller.

        convention : str, optional
            This is used in cases where a FITS header can be interpreted
            in multiple ways. For example, for files with a -CAR
            projection and CRVAL2=0, this can be set to 'wells' or
            'calabretta' to choose the appropriate convention.

        dimensions : tuple or list, optional
            The index of the axes to use if the data has more than three
            dimensions.

        slices : tuple or list, optional
            If a FITS file with more than two dimensions is specified,
            then these are the slices to extract. If all extra dimensions
            only have size 1, then this is not required.

        smooth : int or tuple, optional
            Default smoothing scale is 3 pixels across. User can define
            whether they want an NxN kernel (integer), or NxM kernel
            (tuple). This argument corresponds to the 'gauss' and 'box'
            smoothing kernels.

        kernel : { 'gauss' , 'box' , numpy.array }, optional
            Default kernel used for smoothing is 'gauss'. The user can
            specify if they would prefer 'gauss', 'box', or a custom
            kernel. All kernels are normalized to ensure flux retention.

        overlap str, optional
            Whether to include only contours that overlap with the image
            area. This significantly speeds up the drawing of contours and
            reduces file size when using a file for the contours covering
            a much larger area than the image.

        kwargs
            Additional keyword arguments (such as alpha, linewidths, or
            linestyles) will be passed on directly to Matplotlib's
            :meth:`~matplotlib.axes.Axes.contour` or
            :meth:`~matplotlib.axes.Axes.contourf` methods. For more
            information on these additional arguments, see the *Optional
            keyword arguments* sections in the documentation for those
            methods.
        '''
        if layer:
            self.remove_layer(layer, raise_exception=False)

        if cmap:
            cmap = mpl.cm.get_cmap(cmap)
        elif not colors:
            cmap = mpl.cm.get_cmap('jet')

        if data is not None:
            data_contour, header_contour, wcs_contour = self._get_hdu(data, \
                    hdu, False, convention=convention, dimensions=dimensions, \
                    slices=slices)
        else:
            data_contour = self._data
            header_contour = self._header
            wcs_contour = self._wcs

        wcs_contour.nx = header_contour['NAXIS%i' % (dimensions[0] + 1)]
        wcs_contour.ny = header_contour['NAXIS%i' % (dimensions[1] + 1)]

        image_contour = convolve_util.convolve(data_contour, smooth=smooth, kernel=kernel)
        extent_contour = (0.5, wcs_contour.nx + 0.5, 0.5, wcs_contour.ny + 0.5)

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
            contour_set_name = 'contour_set_' + str(self._contour_counter)

        contour_util.transform(c, wcs_contour, self._wcs, filled=filled, overlap=overlap)

        self._layers[contour_set_name] = c

        if returnlevels:
            return levels

    @auto_refresh
    def show_vectors(self, pdata, adata, phdu=0, ahdu=0, step=1, scale=1,
                     rotate=0, cutoff=0, units='degrees', layer=None,
                     convention=None, dimensions=[0, 1], slices=[], **kwargs):
        '''
        Overlay vectors on the current plot.

        Parameters
        ----------

        pdata : see below

            The FITS file specifying the magnitude of vectors. The following data types can be passed:

                 string
                 astropy.io.fits.PrimaryHDU
                 astropy.io.fits.ImageHDU
                 pyfits.PrimaryHDU
                 pyfits.ImageHDU
                 astropy.wcs.WCS
                 np.ndarray

        adata : see below

            The FITS file specifying the angle of vectors. The following data types can be passed:

                 string
                 astropy.io.fits.PrimaryHDU
                 astropy.io.fits.ImageHDU
                 pyfits.PrimaryHDU
                 pyfits.ImageHDU
                 astropy.wcs.WCS
                 np.ndarray

        phdu : int, optional
            By default, the image in the primary HDU is read in. If a
            different HDU is required for pdata, use this argument.

        ahdu : int, optional
            By default, the image in the primary HDU is read in. If a
            different HDU is required for adata, use this argument.

        step : int, optional
            Derive a vector only from every 'step' pixels. You will
            normally want this to be >1 to get sensible vector spacing.

        scale : int, optional
            The length, in pixels, of a vector with magnitude 1 in the image
            specified by pdata. If pdata specifies fractional polarization,
            make this comparable to step.

        rotate : float, optional
            An angle to rotate by, in units the same as those of the angle map.

        cutoff : float, optional
            The value of magnitude below which no
            vectors should be plotted. The default value, zero,
            excludes negative-length and NaN-masked data.

        units : str, optional
            Units to assume for the angle map. Valid values are 'degrees'
            (the default) or 'radians' (or anything else), which will not
            apply a scaling factor of pi/180 to the angle data.

        layer : str, optional
            The name of the vector layer. This is useful for giving
            custom names to layers (instead of vector_set_n) and for
            replacing existing layers.

        convention : str, optional
            This is used in cases where a FITS header can be interpreted
            in multiple ways. For example, for files with a -CAR
            projection and CRVAL2=0, this can be set to 'wells' or
            'calabretta' to choose the appropriate convention.

        dimensions : tuple or list, optional
            The index of the axes to use if the data has more than three
            dimensions.

        slices : tuple or list, optional
            If a FITS file with more than two dimensions is specified,
            then these are the slices to extract. If all extra dimensions
            only have size 1, then this is not required.

        kwargs
            Additional keyword arguments (such as alpha, linewidths, or color)
            which are passed to Matplotlib's
            :class:`~matplotlib.collections.LineCollection` class, and can be used to
            control the appearance of the lines. For more
            information on these additional arguments, see the *Optional
            keyword arguments* sections in the documentation for those
            methods.

        '''

        # over-ride default color (none) that will otherwise be set by
        #show_lines()
        if not 'color' in kwargs:
            kwargs.setdefault('color', 'black')

        if layer:
            self.remove_layer(layer, raise_exception=False)

        data_p, header_p, wcs_p = self._get_hdu(pdata, phdu, False, \
            convention=convention, dimensions=dimensions, slices=slices)
        data_a, header_a, wcs_a = self._get_hdu(adata, ahdu, False, \
            convention=convention, dimensions=dimensions, slices=slices)

        wcs_p.nx = header_p['NAXIS%i' % (dimensions[0] + 1)]
        wcs_p.ny = header_p['NAXIS%i' % (dimensions[1] + 1)]
        wcs_a.nx = header_a['NAXIS%i' % (dimensions[0] + 1)]
        wcs_a.ny = header_a['NAXIS%i' % (dimensions[1] + 1)]

        if (wcs_p.nx!=wcs_a.nx or wcs_p.ny!=wcs_a.ny):
            raise Exception("Angle and magnitude images must be same size")

        angle = data_a + rotate
        if units == 'degrees':
            angle = np.radians(angle)

        linelist=[]
        for y in range(0,wcs_p.ny,step):
            for x in range(0,wcs_p.nx,step):
                if data_p[y,x]>cutoff and np.isfinite(angle[y,x]):
                    r=data_p[y,x]*0.5*scale
                    a=angle[y,x]
                    x1=1 + x + r*np.sin(a)
                    y1=1 + y - r*np.cos(a)
                    x2=1 + x - r*np.sin(a)
                    y2=1 + y + r*np.cos(a)

                    x_world,y_world=wcs_util.pix2world(wcs_p, [x1,x2],[y1,y2] )
                    line=np.array([x_world,y_world])
                    linelist.append(line)

        if layer:
            vector_set_name = layer
        else:
            self._vector_counter += 1
            vector_set_name = 'vector_set_' + str(self._vector_counter)

        # Use show_lines to finish the process off
        self.show_lines(linelist,layer=vector_set_name,**kwargs)

    # This method plots markers. The input should be an Nx2 array with WCS coordinates
    # in degree format.

    @auto_refresh
    def show_markers(self, xw, yw, layer=False, **kwargs):
        '''
        Overlay markers on the current plot.

        Parameters
        ----------

        xw : list or `~numpy.ndarray`
            The x positions of the markers (in world coordinates)

        yw : list or `~numpy.ndarray`
            The y positions of the markers (in world coordinates)

        layer : str, optional
            The name of the scatter layer. This is useful for giving
            custom names to layers (instead of marker_set_n) and for
            replacing existing layers.

        kwargs
            Additional keyword arguments (such as marker, facecolor,
            edgecolor, alpha, or linewidth) will be passed on directly to
            Matplotlib's :meth:`~matplotlib.axes.Axes.scatter` method (in
            particular, have a look at the *Optional keyword arguments* in the
            documentation for that method).
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
            marker_set_name = 'marker_set_' + str(self._scatter_counter)

        self._layers[marker_set_name] = s

    # Show circles. Different from markers as this method allows more definitions
    # for the circles.
    @auto_refresh
    def show_circles(self, xw, yw, radius, layer=False, zorder=None, **kwargs):
        '''
        Overlay circles on the current plot.

        Parameters
        ----------

        xw : list or `~numpy.ndarray`
            The x positions of the centers of the circles (in world coordinates)

        yw : list or `~numpy.ndarray`
            The y positions of the centers of the circles (in world coordinates)

        radius : int or float or list or `~numpy.ndarray`
            The radii of the circles (in world coordinates)

        layer : str, optional
            The name of the circle layer. This is useful for giving
            custom names to layers (instead of circle_set_n) and for
            replacing existing layers.

        kwargs
            Additional keyword arguments (such as facecolor, edgecolor, alpha,
            or linewidth) are passed to Matplotlib
            :class:`~matplotlib.collections.PatchCollection` class, and can be
            used to control the appearance of the circles.
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
        rp = radius / wcs_util.celestial_pixel_scale(self._wcs)

        patches = []
        for i in range(len(xp)):
            patches.append(Circle((xp[i], yp[i]), radius=rp[i]))

        # Due to bugs in matplotlib, we need to pass the patch properties
        # directly to the PatchCollection rather than use match_original.
        p = PatchCollection(patches, **kwargs)

        if zorder is not None:
            p.zorder = zorder
        c = self._ax1.add_collection(p)

        if layer:
            circle_set_name = layer
        else:
            self._circle_counter += 1
            circle_set_name = 'circle_set_' + str(self._circle_counter)

        self._layers[circle_set_name] = c

    @auto_refresh
    def show_ellipses(self, xw, yw, width, height, angle=0, layer=False, zorder=None, **kwargs):
        '''
        Overlay ellipses on the current plot.

        Parameters
        ----------

        xw : list or `~numpy.ndarray`
            The x positions of the centers of the ellipses (in world coordinates)

        yw : list or `~numpy.ndarray`
            The y positions of the centers of the ellipses (in world coordinates)

        width : int or float or list or `~numpy.ndarray`
            The width of the ellipse (in world coordinates)

        height : int or float or list or `~numpy.ndarray`
            The height of the ellipse (in world coordinates)

        angle : int or float or list or `~numpy.ndarray`, optional
            rotation in degrees (anti-clockwise). Default
            angle is 0.0.

        layer : str, optional
            The name of the ellipse layer. This is useful for giving
            custom names to layers (instead of ellipse_set_n) and for
            replacing existing layers.

        kwargs
            Additional keyword arguments (such as facecolor, edgecolor, alpha,
            or linewidth) are passed to Matplotlib
            :class:`~matplotlib.collections.PatchCollection` class, and can be
            used to control the appearance of the ellipses.
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

        if np.isscalar(angle):
            angle = np.repeat(angle, len(xw))
        else:
            angle = np.array(angle)

        if np.isscalar(height):
            height = np.repeat(height, len(xw))
        else:
            height = np.array(height)

        if not 'facecolor' in kwargs:
            kwargs.setdefault('facecolor', 'none')

        if layer:
            self.remove_layer(layer, raise_exception=False)

        xp, yp = wcs_util.world2pix(self._wcs, xw, yw)
        wp = width / wcs_util.celestial_pixel_scale(self._wcs)
        hp = height / wcs_util.celestial_pixel_scale(self._wcs)
        ap = angle

        patches = []
        for i in range(len(xp)):
            patches.append(Ellipse((xp[i], yp[i]), width=wp[i], height=hp[i], angle=ap[i]))

        # Due to bugs in matplotlib, we need to pass the patch properties
        # directly to the PatchCollection rather than use match_original.
        p = PatchCollection(patches, **kwargs)

        if zorder is not None:
            p.zorder = zorder
        c = self._ax1.add_collection(p)

        if layer:
            ellipse_set_name = layer
        else:
            self._ellipse_counter += 1
            ellipse_set_name = 'ellipse_set_' + str(self._ellipse_counter)

        self._layers[ellipse_set_name] = c

    @auto_refresh
    def show_rectangles(self, xw, yw, width, height, layer=False, zorder=None, **kwargs):
        '''
        Overlay rectangles on the current plot.

        Parameters
        ----------

        xw : list or `~numpy.ndarray`
            The x positions of the centers of the rectangles (in world coordinates)

        yw : list or `~numpy.ndarray`
            The y positions of the centers of the rectangles (in world coordinates)

        width : int or float or list or `~numpy.ndarray`
            The width of the rectangle (in world coordinates)

        height : int or float or list or `~numpy.ndarray`
            The height of the rectangle (in world coordinates)

        layer : str, optional
            The name of the rectangle layer. This is useful for giving
            custom names to layers (instead of rectangle_set_n) and for
            replacing existing layers.

        kwargs
            Additional keyword arguments (such as facecolor, edgecolor, alpha,
            or linewidth) are passed to Matplotlib
            :class:`~matplotlib.collections.PatchCollection` class, and can be
            used to control the appearance of the rectangles.
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
        wp = width / wcs_util.celestial_pixel_scale(self._wcs)
        hp = height / wcs_util.celestial_pixel_scale(self._wcs)

        patches = []
        xp = xp - wp / 2.
        yp = yp - hp / 2.
        for i in range(len(xp)):
            patches.append(Rectangle((xp[i], yp[i]), width=wp[i], height=hp[i]))

        # Due to bugs in matplotlib, we need to pass the patch properties
        # directly to the PatchCollection rather than use match_original.
        p = PatchCollection(patches, **kwargs)

        if zorder is not None:
            p.zorder = zorder
        c = self._ax1.add_collection(p)

        if layer:
            rectangle_set_name = layer
        else:
            self._rectangle_counter += 1
            rectangle_set_name = 'rectangle_set_' + str(self._rectangle_counter)

        self._layers[rectangle_set_name] = c

    @auto_refresh
    def show_lines(self, line_list, layer=False, zorder=None, **kwargs):
        '''
        Overlay lines on the current plot.

        Parameters
        ----------

        line_list : list
             A list of one or more 2xN numpy arrays which contain
             the [x, y] positions of the vertices in world coordinates.

        layer : str, optional
            The name of the line(s) layer. This is useful for giving
            custom names to layers (instead of line_set_n) and for
            replacing existing layers.

        kwargs
            Additional keyword arguments (such as color, offsets, linestyle,
            or linewidth) are passed to Matplotlib
            :class:`~matplotlib.collections.LineCollection` class, and can be used to
            control the appearance of the lines.
        '''

        if not 'color' in kwargs:
            kwargs.setdefault('color', 'none')

        if layer:
            self.remove_layer(layer, raise_exception=False)

        lines = []

        for line in line_list:
            xp, yp = wcs_util.world2pix(self._wcs, line[0, :], line[1, :])
            lines.append(np.column_stack((xp, yp)))

        l = LineCollection(lines, **kwargs)
        if zorder is not None:
            l.zorder = zorder
        c = self._ax1.add_collection(l)

        if layer:
            line_set_name = layer
        else:
            self._linelist_counter += 1
            line_set_name = 'line_set_' + str(self._linelist_counter)

        self._layers[line_set_name] = c

    @auto_refresh
    def show_arrows(self, x, y, dx, dy, width='auto', head_width='auto',
                    head_length='auto', length_includes_head=True, layer=False, zorder=None, **kwargs):
        '''
        Overlay arrows on the current plot.

        Parameters
        ----------

        x, y, dx, dy : float or list or `~numpy.ndarray`
            Origin and displacement of the arrows in world coordinates.
            These can either be scalars to plot a single arrow, or lists or
            arrays to plot multiple arrows.

        width : float, optional
            The width of the arrow body, in pixels (default: 2% of the
            arrow length)

        head_width : float, optional
            The width of the arrow head, in pixels (default: 5% of the
            arrow length)

        head_length : float, optional
            The length of the arrow head, in pixels (default: 5% of the
            arrow length)

        length_includes_head : bool, optional
            Whether the head includes the length

        layer : str, optional
            The name of the arrow(s) layer. This is useful for giving
            custom names to layers (instead of line_set_n) and for
            replacing existing layers.

        kwargs
            Additional keyword arguments (such as facecolor, edgecolor, alpha,
            or linewidth) are passed to Matplotlib
            :class:`~matplotlib.collections.PatchCollection` class, and can be
            used to control the appearance of the arrows.
        '''

        if layer:
            self.remove_layer(layer, raise_exception=False)

        arrows = []

        if np.isscalar(x):
            x, y, dx, dy = [x], [y], [dx], [dy]

        for i in range(len(x)):

            xp1, yp1 = wcs_util.world2pix(self._wcs, x[i], y[i])
            xp2, yp2 = wcs_util.world2pix(self._wcs, x[i] + dx[i], y[i] + dy[i])

            if width == 'auto':
                width = 0.02 * np.sqrt((xp2 - xp1) ** 2 + (yp2 - yp1) ** 2)

            if head_width == 'auto':
                head_width = 0.1 * np.sqrt((xp2 - xp1) ** 2 + (yp2 - yp1) ** 2)

            if head_length == 'auto':
                head_length = 0.1 * np.sqrt((xp2 - xp1) ** 2 + (yp2 - yp1) ** 2)

            arrows.append(FancyArrow(xp1, yp1, xp2 - xp1, yp2 - yp1,
                                     width=width, head_width=head_width,
                                     head_length=head_length,
                                     length_includes_head=length_includes_head)
                                     )

        # Due to bugs in matplotlib, we need to pass the patch properties
        # directly to the PatchCollection rather than use match_original.
        p = PatchCollection(arrows, **kwargs)

        if zorder is not None:
            p.zorder = zorder
        c = self._ax1.add_collection(p)

        if layer:
            line_set_name = layer
        else:
            self._linelist_counter += 1
            line_set_name = 'arrow_set_' + str(self._linelist_counter)

        self._layers[line_set_name] = c

    @auto_refresh
    def show_polygons(self, polygon_list, layer=False, zorder=None, **kwargs):
        '''
        Overlay polygons on the current plot.

        Parameters
        ----------

        polygon_list : list or tuple
            A list of one or more 2xN or Nx2 Numpy arrays which contain
            the [x, y] positions of the vertices in world coordinates.
            Note that N should be greater than 2.

        layer : str, optional
            The name of the circle layer. This is useful for giving
            custom names to layers (instead of circle_set_n) and for
            replacing existing layers.

        kwargs
            Additional keyword arguments (such as facecolor, edgecolor, alpha,
            or linewidth) are passed to Matplotlib
            :class:`~matplotlib.collections.PatchCollection` class, and can be
            used to control the appearance of the polygons.
        '''

        if not 'facecolor' in kwargs:
            kwargs.setdefault('facecolor', 'none')

        if layer:
            self.remove_layer(layer, raise_exception=False)

        if type(polygon_list) not in [list, tuple]:
            raise Exception("polygon_list should be a list or tuple of Numpy arrays")

        pix_polygon_list = []
        for polygon in polygon_list:

            if type(polygon) is not np.ndarray:
                raise Exception("Polygon should be given as a Numpy array")

            if polygon.shape[0] == 2 and polygon.shape[1] > 2:
                xw = polygon[0, :]
                yw = polygon[1, :]
            elif polygon.shape[0] > 2 and polygon.shape[1] == 2:
                xw = polygon[:, 0]
                yw = polygon[:, 1]
            else:
                raise Exception("Polygon should have dimensions 2xN or Nx2 with N>2")

            xp, yp = wcs_util.world2pix(self._wcs, xw, yw)
            pix_polygon_list.append(np.column_stack((xp, yp)))

        patches = []
        for i in range(len(pix_polygon_list)):
            patches.append(Polygon(pix_polygon_list[i], **kwargs))

        # Due to bugs in matplotlib, we need to pass the patch properties
        # directly to the PatchCollection rather than use match_original.
        p = PatchCollection(patches, **kwargs)

        if zorder is not None:
            p.zorder = zorder
        c = self._ax1.add_collection(p)

        if layer:
            poly_set_name = layer
        else:
            self._poly_counter += 1
            poly_set_name = 'poly_set_' + str(self._poly_counter)

        self._layers[poly_set_name] = c

    @auto_refresh
    @fixdocstring
    def add_label(self, x, y, text, relative=False, color='black',
                  family=None, style=None, variant=None, stretch=None,
                  weight=None, size=None, fontproperties=None,
                  horizontalalignment='center', verticalalignment='center',
                  layer=None, **kwargs):
        '''
        Add a text label.

        Parameters
        ----------

        x, y : float
            Coordinates of the text label

        text : str
            The label

        relative : str, optional
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

        if not np.isscalar(x):
            raise Exception("x should be a single value")

        if not np.isscalar(y):
            raise Exception("y should be a single value")

        if not np.isscalar(text):
            raise Exception("text should be a single value")

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
            label_name = 'label_' + str(self._label_counter)

        self._layers[label_name] = l

    def set_auto_refresh(self, refresh):
        '''
        Set whether the display should refresh after each method call.

        Parameters
        ----------
        refresh : bool
            Whether to refresh the display every time a FITSFigure method is
            called. This defaults to `True` if and only if APLpy is being used
            from IPython and the Matplotlib backend is interactive.
        '''

        if refresh is None:
            if matplotlib.is_interactive():
                try:
                    get_ipython()
                except NameError:
                    refresh = False
                else:
                    refresh = True
            else:
                refresh = False
        elif not isinstance(refresh, bool):
            raise TypeError("refresh argument should be boolean or `None`")

        self._parameters.auto_refresh = refresh

    def refresh(self, force=True):
        '''
        Refresh the display.

        Parameters
        ----------
        force : str, optional
            If set to False, refresh() will only have an effect if
            auto refresh is on. If set to True, the display will be
            refreshed whatever the auto refresh setting is set to.
            The default is True.
        '''
        if self._parameters.auto_refresh or force:
            self._figure.canvas.draw()

    def save(self, filename, dpi=None, transparent=False, adjust_bbox=True, max_dpi=300, format=None):
        '''
        Save the current figure to a file.

        Parameters
        ----------

        filename : str or fileobj
            The name of the file to save the plot to. This can be for
            example a PS, EPS, PDF, PNG, JPEG, or SVG file. Note that it
            is also possible to pass file-like object.

        dpi : float, optional
            The output resolution, in dots per inch. If the output file
            is a vector graphics format (such as PS, EPS, PDF or SVG) only
            the image itself will be rasterized. If the output is a PS or
            EPS file and no dpi is specified, the dpi is automatically
            calculated to match the resolution of the image. If this value is
            larger than max_dpi, then dpi is set to max_dpi.

        transparent : str, optional
            Whether to preserve transparency

        adjust_bbox : str, optional
            Auto-adjust the bounding box for the output

        max_dpi : float, optional
            The maximum resolution to output images at. If no maximum is
            wanted, enter None or 0.

        format : str, optional
            By default, APLpy tries to guess the file format based on the
            file extension, but the format can also be specified
            explicitly. Should be one of 'eps', 'ps', 'pdf', 'svg', 'png'.
        '''

        if isinstance(filename, six.string_types) and format is None:
            format = os.path.splitext(filename)[1].lower()[1:]

        if dpi is None and format in ['eps', 'ps', 'pdf']:
            width = self._ax1.get_position().width * self._figure.get_figwidth()
            interval = self._ax1.xaxis.get_view_interval()
            nx = interval[1] - interval[0]
            if max_dpi:
                dpi = np.minimum(nx / width, max_dpi)
            else:
                dpi = nx / width
            log.info("Auto-setting resolution to %g dpi" % dpi)

        artists = []
        if adjust_bbox:
            for artist in self._layers.values():
                if isinstance(artist, matplotlib.text.Text):
                    artists.append(artist)
            self._figure.savefig(filename, dpi=dpi, transparent=transparent, bbox_inches='tight', bbox_extra_artists=artists, format=format)
        else:
            self._figure.savefig(filename, dpi=dpi, transparent=transparent, format=format)

    def _initialize_view(self):

        self._ax1.xaxis.set_view_interval(+0.5, self._wcs.nx + 0.5, ignore=True)
        self._ax1.yaxis.set_view_interval(+0.5, self._wcs.ny + 0.5, ignore=True)
        self._ax2.xaxis.set_view_interval(+0.5, self._wcs.nx + 0.5, ignore=True)
        self._ax2.yaxis.set_view_interval(+0.5, self._wcs.ny + 0.5, ignore=True)

        # set the image extent to FITS pixel coordinates
        self._extent = (0.5, self._wcs.nx + 0.5, 0.5, self._wcs.ny + 0.5)

    def _get_invert_default(self):
        return self._figure.apl_grayscale_invert_default

    def _get_colormap_default(self):
        return self._figure.apl_colorscale_cmap_default

    @auto_refresh
    def set_theme(self, theme):
        '''
        Set the axes, ticks, grid, and image colors to a certain style (experimental).

        Parameters
        ----------

        theme : str
            The theme to use. At the moment, this can be 'pretty' (for
            viewing on-screen) and 'publication' (which makes the ticks
            and grid black, and displays the image in inverted grayscale)
       '''

        if theme == 'pretty':
            self.frame.set_color('black')
            self.frame.set_linewidth(1.0)
            self.ticks.set_color('white')
            self.ticks.set_length(7)
            self._figure.apl_grayscale_invert_default = False
            self._figure.apl_colorscale_cmap_default = 'jet'
            if self.image:
                self.image.set_cmap(cmap=mpl.cm.get_cmap('jet'))
        elif theme == 'publication':
            self.frame.set_color('black')
            self.frame.set_linewidth(1.0)
            self.ticks.set_color('black')
            self.ticks.set_length(7)
            self._figure.apl_grayscale_invert_default = True
            self._figure.apl_colorscale_cmap_default = 'gist_heat'
            if self.image:
                self.image.set_cmap(cmap=mpl.cm.get_cmap('gist_yarg'))

    def world2pixel(self, xw, yw):
        '''
        Convert world to pixel coordinates.

        Parameters
        ----------
        xw : float or list or `~numpy.ndarray`
            x world coordinate
        yw : float or list or `~numpy.ndarray`
            y world coordinate

        Returns
        -------
        xp : float or list or `~numpy.ndarray`
            x pixel coordinate
        yp : float or list or `~numpy.ndarray`
            y pixel coordinate
        '''

        return wcs_util.world2pix(self._wcs, xw, yw)

    def pixel2world(self, xp, yp):
        '''
        Convert pixel to world coordinates.

        Parameters
        ----------
        xp : float or list or `~numpy.ndarray`
            x pixel coordinate
        yp : float or list or `~numpy.ndarray`
            y pixel coordinate

        Returns
        -------
        xw : float or list or `~numpy.ndarray`
            x world coordinate
        yw : float or list or `~numpy.ndarray`
            y world coordinate
        '''

        return wcs_util.pix2world(self._wcs, xp, yp)

    @auto_refresh
    def add_grid(self, *args, **kwargs):
        '''
        Add a coordinate to the current figure.

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
        Removes the grid from the current figure.
        '''
        self.grid._remove()
        del self.grid

    @auto_refresh
    def add_beam(self, *args, **kwargs):
        '''
        Add a beam to the current figure.

        Once this method has been run, a beam attribute becomes available,
        and can be used to control the aspect of the beam::

            >>> f = aplpy.FITSFigure(...)
            >>> ...
            >>> f.add_beam()
            >>> f.beam.set_color('white')
            >>> f.beam.set_hatch('+')
            >>> ...

        If more than one beam is added, the beam object becomes a list. In
        this case, to control the aspect of one of the beams, you will need to
        specify the beam index::

            >>> ...
            >>> f.beam[2].set_hatch('/')
            >>> ...
        '''

        # Initalize the beam and set parameters
        b = Beam(self)
        b.show(*args, **kwargs)

        if hasattr(self, 'beam'):
            if type(self.beam) is list:
                self.beam.append(b)
            else:
                self.beam = [self.beam, b]
        else:
            self.beam = b

    @auto_refresh
    def remove_beam(self, beam_index=None):
        '''
        Removes the beam from the current figure.

        If more than one beam is present, the index of the beam should be
        specified using beam_index=
        '''

        if type(self.beam) is list:

            if beam_index is None:
                raise Exception("More than one beam present - use beam_index= to specify which one to remove")
            else:
                b = self.beam.pop(beam_index)
                b._remove()
                del b

            # If only one beam is present, remove containing list
            if len(self.beam) == 1:
                self.beam = self.beam[0]

        else:

            self.beam._remove()
            del self.beam

    @auto_refresh
    def add_scalebar(self, length, *args, **kwargs):
        '''
        Add a scalebar to the current figure.

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
            self.scalebar = Scalebar(self)
            self.scalebar.show(length, *args, **kwargs)
        except:
            del self.scalebar
            raise

    @auto_refresh
    def remove_scalebar(self):
        '''
        Removes the scalebar from the current figure.
        '''
        self.scalebar._remove()
        del self.scalebar

    @auto_refresh
    def add_colorbar(self, *args, **kwargs):
        '''
        Add a colorbar to the current figure.

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
        Removes the colorbar from the current figure.
        '''
        self.colorbar._remove()
        del self.colorbar

    def close(self):
        '''
        Close the figure and free up the memory.
        '''
        mpl.close(self._figure)
