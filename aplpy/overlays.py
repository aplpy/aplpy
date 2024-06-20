import warnings

from mpl_toolkits.axes_grid1.anchored_artists import (AnchoredEllipse,
                                                      AnchoredSizeBar)

import numpy as np
from matplotlib.font_manager import FontProperties

from astropy import units as u
from astropy.wcs.utils import proj_plane_pixel_scales

from .decorators import auto_refresh

corners = {}
corners['top right'] = 1
corners['top left'] = 2
corners['bottom left'] = 3
corners['bottom right'] = 4
corners['right'] = 5
corners['left'] = 6
corners['bottom'] = 8
corners['top'] = 9


class Scalebar(object):

    def __init__(self, parent):

        # Retrieve info from parent figure
        self._ax = parent.ax
        self._wcs = parent._wcs
        self._figure = parent._figure
        self._dimensions = [parent.x, parent.y]

        # Initialize settings
        self._base_settings = {}
        self._scalebar_settings = {}
        self._label_settings = {}
        self._label_settings['fontproperties'] = FontProperties()

    # LAYOUT

    @auto_refresh
    def show(self, length, label=None, corner='bottom right', frame=False,
             borderpad=0.4, pad=0.5, **kwargs):
        """
        Overlay a scale bar on the image.

        Parameters
        ----------

        length : float, or quantity
            The length of the scalebar in degrees, an angular quantity, or angular unit

        label : str, optional
            Label to place below the scalebar

        corner : int, optional
            Where to place the scalebar. Acceptable values are:, 'left',
            'right', 'top', 'bottom', 'top left', 'top right', 'bottom
            left' (default), 'bottom right'

        frame : str, optional
            Whether to display a frame behind the scalebar (default is False)

        kwargs
            Additional arguments are passed to the matplotlib Rectangle and
            Text classes. See the matplotlib documentation for more details.
            In cases where the same argument exists for the two objects, the
            argument is passed to both the Text and Rectangle instance.
        """

        self._length = length
        self._base_settings['corner'] = corner
        self._base_settings['frame'] = frame
        self._base_settings['borderpad'] = borderpad
        self._base_settings['pad'] = pad

        if isinstance(length, u.Quantity):
            length = length.to(u.degree).value
        elif isinstance(length, u.Unit):
            length = length.to(u.degree)

        if self._wcs.is_celestial:
            pix_scale = proj_plane_pixel_scales(self._wcs)
            sx = pix_scale[self._dimensions[0]]
            sy = pix_scale[self._dimensions[1]]
            degrees_per_pixel = np.sqrt(sx * sy)
        else:
            raise ValueError("Cannot show scalebar when WCS is not celestial")

        length = length / degrees_per_pixel

        try:
            self._scalebar.remove()
        except Exception:
            pass

        if isinstance(corner, str):
            corner = corners[corner]

        self._scalebar = AnchoredSizeBar(self._ax.transData, length, label,
                                         corner, pad=pad, borderpad=borderpad,
                                         sep=5, frameon=frame)

        self._ax.add_artist(self._scalebar)

        self.set(**kwargs)

    @auto_refresh
    def _remove(self):
        self._scalebar.remove()

    @auto_refresh
    def hide(self):
        """
        Hide the scalebar.
        """
        try:
            self._scalebar.remove()
        except Exception:
            pass

    @auto_refresh
    def set_length(self, length):
        """
        Set the length of the scale bar.
        """
        self.show(length, **self._base_settings)
        self._set_scalebar_properties(**self._scalebar_settings)
        self._set_label_properties(**self._scalebar_settings)

    @auto_refresh
    def set_label(self, label):
        """
        Set the label of the scale bar.
        """
        self._set_label_properties(text=label)

    @auto_refresh
    def set_corner(self, corner):
        """
        Set where to place the scalebar.

        Acceptable values are 'left', 'right', 'top', 'bottom', 'top left',
        'top right', 'bottom left' (default), and 'bottom right'.
        """
        self._base_settings['corner'] = corner
        self.show(self._length, **self._base_settings)
        self._set_scalebar_properties(**self._scalebar_settings)
        self._set_label_properties(**self._scalebar_settings)

    @auto_refresh
    def set_frame(self, frame):
        """
        Set whether to display a frame around the scalebar.
        """
        self._base_settings['frame'] = frame
        self.show(self._length, **self._base_settings)
        self._set_scalebar_properties(**self._scalebar_settings)
        self._set_label_properties(**self._scalebar_settings)

    # APPEARANCE

    @auto_refresh
    def set_linewidth(self, linewidth):
        """
        Set the linewidth of the scalebar, in points.
        """
        self._set_scalebar_properties(linewidth=linewidth)

    @auto_refresh
    def set_linestyle(self, linestyle):
        """
        Set the linestyle of the scalebar.

        Should be one of 'solid', 'dashed', 'dashdot', or 'dotted'.
        """
        self._set_scalebar_properties(linestyle=linestyle)

    @auto_refresh
    def set_alpha(self, alpha):
        """
        Set the alpha value (transparency).

        This should be a floating point value between 0 and 1.
        """
        self._set_scalebar_properties(alpha=alpha)
        self._set_label_properties(alpha=alpha)

    @auto_refresh
    def set_color(self, color):
        """
        Set the label and scalebar color.
        """
        self._set_scalebar_properties(color=color)
        self._set_label_properties(color=color)

    @auto_refresh
    def set_font(self, family=None, style=None, variant=None, stretch=None,
                 weight=None, size=None, fontproperties=None):
        """
        Set the font of the tick labels

        Parameters
        ----------

        common: family, style, variant, stretch, weight, size, fontproperties

        Notes
        -----

        Default values are set by matplotlib or previously set values if
        set_font has already been called. Global default values can be set by
        editing the matplotlibrc file.
        """

        if family:
            self._label_settings['fontproperties'].set_family(family)

        if style:
            self._label_settings['fontproperties'].set_style(style)

        if variant:
            self._label_settings['fontproperties'].set_variant(variant)

        if stretch:
            self._label_settings['fontproperties'].set_stretch(stretch)

        if weight:
            self._label_settings['fontproperties'].set_weight(weight)

        if size:
            self._label_settings['fontproperties'].set_size(size)

        if fontproperties:
            self._label_settings['fontproperties'] = fontproperties

        self._set_label_properties(fontproperties=self._label_settings['fontproperties'])

    @auto_refresh
    def _set_label_properties(self, **kwargs):
        """
        Modify the scalebar label properties.

        All arguments are passed to the matplotlib Text class. See the
        matplotlib documentation for more details.
        """
        for kwarg, val in kwargs.items():
            try:
                # Only set attributes that exist
                kvpair = {kwarg: val}
                self._scalebar.txt_label.get_children()[0].set(**kvpair)
                self._label_settings[kwarg] = val
            except AttributeError:
                warnings.warn("Text labels do not have attribute {0}. Skipping.".format(kwarg))

    @auto_refresh
    def _set_scalebar_properties(self, **kwargs):
        """
        Modify the scalebar properties.

        All arguments are passed to the matplotlib Rectangle class. See the
        matplotlib documentation for more details.
        """
        for kwarg, val in kwargs.items():
            try:
                kvpair = {kwarg: val}
                self._scalebar.size_bar.get_children()[0].set(**kvpair)
                self._scalebar_settings[kwarg] = val
            except AttributeError:
                warnings.warn("Scalebar does not have attribute {0}. Skipping.".format(kwarg))

    @auto_refresh
    def set(self, **kwargs):
        """
        Modify the scalebar and scalebar properties.

        All arguments are passed to the matplotlib Rectangle and Text classes.
        See the matplotlib documentation for more details. In cases where the
        same argument exists for the two objects, the argument is passed to
        both the Text and Rectangle instance.
        """
        for kwarg in kwargs:
            kwargs_single = {kwarg: kwargs[kwarg]}
            try:
                self._set_label_properties(**kwargs_single)
            except (AttributeError, TypeError):
                pass
            try:
                self._set_scalebar_properties(**kwargs_single)
            except (AttributeError, TypeError):
                pass

    # DEPRECATED

    @auto_refresh
    def set_font_family(self, family):
        warnings.warn("scalebar.set_font_family is deprecated - use scalebar.set_font instead", DeprecationWarning)
        self.set_font(family=family)

    @auto_refresh
    def set_font_weight(self, weight):
        warnings.warn("scalebar.set_font_weight is deprecated - use scalebar.set_font instead", DeprecationWarning)
        self.set_font(weight=weight)

    @auto_refresh
    def set_font_size(self, size):
        warnings.warn("scalebar.set_font_size is deprecated - use scalebar.set_font instead", DeprecationWarning)
        self.set_font(size=size)

    @auto_refresh
    def set_font_style(self, style):
        warnings.warn("scalebar.set_font_style is deprecated - use scalebar.set_font instead", DeprecationWarning)
        self.set_font(style=style)


# For backward-compatibility
ScaleBar = Scalebar


class Beam(object):

    def __init__(self, parent):

        # Retrieve info from parent figure
        self._figure = parent._figure
        self._header = parent._header
        self._ax = parent.ax
        self._wcs = parent._wcs
        self._dimensions = [parent.x, parent.y]

        # Initialize settings
        self._base_settings = {}
        self._beam_settings = {}

    # LAYOUT

    @auto_refresh
    def show(self, major='BMAJ', minor='BMIN', angle='BPA',
             corner='bottom left', frame=False, borderpad=0.4, pad=0.5,
             **kwargs):
        """
        Display the beam shape and size for the primary image.

        By default, this method will search for the BMAJ, BMIN, and BPA
        keywords in the FITS header to set the major and minor axes and the
        position angle on the sky.

        Parameters
        ----------

        major : float, quantity or unit, optional
            Major axis of the beam in degrees or an angular quantity (overrides
            BMAJ if present)

        minor : float, quantity or unit, optional
            Minor axis of the beam in degrees or an angular quantity (overrides
            BMIN if present)

        angle : float, quantity or unit, optional
            Position angle of the beam on the sky in degrees or an angular
            quantity (overrides BPA if present) in the anticlockwise direction.

        corner : int, optional
            The beam location. Acceptable values are 'left', 'right',
            'top', 'bottom', 'top left', 'top right', 'bottom left'
            (default), and 'bottom right'.

        frame : str, optional
            Whether to display a frame behind the beam (default is False)

        kwargs
            Additional arguments are passed to the matplotlib Ellipse class.
            See the matplotlib documentation for more details.
        """

        if isinstance(major, str):
            major = self._header[major]

        if isinstance(minor, str):
            minor = self._header[minor]

        if isinstance(angle, str):
            angle = self._header[angle]

        if isinstance(major, u.Quantity):
            major = major.to(u.degree).value
        elif isinstance(major, u.Unit):
            major = major.to(u.degree)

        if isinstance(minor, u.Quantity):
            minor = minor.to(u.degree).value
        elif isinstance(minor, u.Unit):
            minor = minor.to(u.degree)

        if isinstance(angle, u.Quantity):
            angle = angle.to(u.degree).value
        elif isinstance(angle, u.Unit):
            angle = angle.to(u.degree)

        if self._wcs.has_celestial:   # fix for #444 "beam not shown for cubes"
            pix_scale = proj_plane_pixel_scales(self._wcs)
            sx = pix_scale[self._dimensions[0]]
            sy = pix_scale[self._dimensions[1]]
            degrees_per_pixel = np.sqrt(sx * sy)
        else:
            raise ValueError("Cannot show beam when WCS is not celestial")

        self._base_settings['minor'] = minor
        self._base_settings['major'] = major
        self._base_settings['angle'] = angle
        self._base_settings['corner'] = corner
        self._base_settings['frame'] = frame
        self._base_settings['borderpad'] = borderpad
        self._base_settings['pad'] = pad

        minor /= degrees_per_pixel
        major /= degrees_per_pixel

        try:
            self._beam.remove()
        except Exception:
            pass

        if isinstance(corner, str):
            corner = corners[corner]

        self._beam = AnchoredEllipse(self._ax.transData, width=minor,
                                     height=major, angle=angle, loc=corner,
                                     pad=pad, borderpad=borderpad,
                                     frameon=frame)

        self._ax.add_artist(self._beam)

        self.set(**kwargs)

    @auto_refresh
    def _remove(self):
        self._beam.remove()

    @auto_refresh
    def hide(self):
        """
        Hide the beam
        """
        try:
            self._beam.remove()
        except Exception:
            pass

    @auto_refresh
    def set_major(self, major):
        """
        Set the major axis of the beam, in degrees.
        """
        self._base_settings['major'] = major
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_minor(self, minor):
        """
        Set the minor axis of the beam, in degrees.
        """
        self._base_settings['minor'] = minor
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_angle(self, angle):
        """
        Set the position angle of the beam on the sky, in degrees.
        """
        self._base_settings['angle'] = angle
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_corner(self, corner):
        """
        Set the beam location.

        Acceptable values are 'left', 'right', 'top', 'bottom', 'top left',
        'top right', 'bottom left' (default), and 'bottom right'.
        """
        self._base_settings['corner'] = corner
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_frame(self, frame):
        """
        Set whether to display a frame around the beam.
        """
        self._base_settings['frame'] = frame
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_borderpad(self, borderpad):
        """
        Set the amount of padding within the beam object, relative to the
        canvas size.
        """
        self._base_settings['borderpad'] = borderpad
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_pad(self, pad):
        """
        Set the amount of padding between the beam object and the image
        corner/edge, relative to the canvas size.
        """
        self._base_settings['pad'] = pad
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    # APPEARANCE

    @auto_refresh
    def set_alpha(self, alpha):
        """
        Set the alpha value (transparency).

        This should be a floating point value between 0 and 1.
        """
        self.set(alpha=alpha)

    @auto_refresh
    def set_color(self, color):
        """
        Set the beam color.
        """
        self.set(color=color)

    @auto_refresh
    def set_edgecolor(self, edgecolor):
        """
        Set the color for the edge of the beam.
        """
        self.set(edgecolor=edgecolor)

    @auto_refresh
    def set_facecolor(self, facecolor):
        """
        Set the color for the interior of the beam.
        """
        self.set(facecolor=facecolor)

    @auto_refresh
    def set_linestyle(self, linestyle):
        """
        Set the line style for the edge of the beam.

        This should be one of 'solid', 'dashed', 'dashdot', or 'dotted'.
        """
        self.set(linestyle=linestyle)

    @auto_refresh
    def set_linewidth(self, linewidth):
        """
        Set the line width for the edge of the beam, in points.
        """
        self.set(linewidth=linewidth)

    @auto_refresh
    def set_hatch(self, hatch):
        """
        Set the hatch pattern.

        This should be one of '/', '\', '|', '-', '+', 'x', 'o', 'O', '.', or
        '*'.
        """
        self.set(hatch=hatch)

    @auto_refresh
    def set(self, **kwargs):
        """
        Modify the beam properties. All arguments are passed to the matplotlib
        Ellipse class. See the matplotlib documentation for more details.
        """
        for kwarg in kwargs:
            self._beam_settings[kwarg] = kwargs[kwarg]
        self._beam.ellipse.set(**kwargs)
