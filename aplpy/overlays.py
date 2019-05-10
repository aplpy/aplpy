from __future__ import absolute_import, print_function, division

import warnings

from mpl_toolkits.axes_grid1.anchored_artists import (AnchoredEllipse,
                                                      AnchoredSizeBar)

import matplotlib
MPL_VERSION = int(matplotlib.__version__[0])
if MPL_VERSION >= 3:
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredDirectionArrows
else:
    from astropy.coordinates import SkyCoord
    from astropy.wcs.utils import wcs_to_celestial_frame
    from matplotlib.patches import FancyArrowPatch
    from matplotlib.patches import Rectangle
    from matplotlib.text import Text

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


class Compass(object):

    def __init__(self, parent):

        # Retrieve info from parent figure
        self._figure = parent._figure
        self._header = parent._header
        self._ax = parent.ax
        self._wcs = parent._wcs
        self._dimensions = [parent.x, parent.y]

        # Initialize settings
        self._base_settings = {}
        self._arrow_settings = {}
        self._label_settings = {}
        self._label_settings['fontproperties'] = FontProperties()

    # LAYOUT

    @auto_refresh
    def show(self, length=0.15, corner='top right', frame=False, borderpad=0.4,
             pad=0.5, sep_x=0.01, sep_y=0.03, fontproperties=None, **kwargs):
        """
        Overlay a compass on the image.

        Parameters
        ----------

        length : float or quantity, optional
            The length of the compass arrows in degrees, an angular quantity,
            or angular unit

        corner : str, optional
            Where to place the compass. Acceptable values are: 'left',
            'right', 'top', 'bottom', 'top left', 'top right' (default),
            'bottom left', 'bottom right'

        frame : bool, optional
            Whether to display a frame behind the compass (default is False)

        sep_x, sep_y : float or quantity, optional
            Separation between the arrows and labels in degrees, an angular
            quantity, or angular unit (defaults are 0.01 and 0.03)

        fontproperties : matplotlib FontProperties, optional
            Font properties for the label text

        kwargs
            Additional arguments are passed to the matplotlib Text (mpl 2),
            TextPath (mpl 3), and FancyArrowPatch classes. See the matplotlib
            documentation for more details.
        """

        if MPL_VERSION == 3:
            length *= -1
        self._base_settings['length'] = length
        self._base_settings['corner'] = corner
        self._base_settings['frame'] = frame
        self._base_settings['borderpad'] = borderpad
        self._base_settings['pad'] = pad
        self._base_settings['sep_x'] = sep_x
        self._base_settings['sep_y'] = sep_y
        if not fontproperties:
            self._label_settings['fontproperties'] = FontProperties()

        if isinstance(length, u.Quantity):
            length = length.to(u.degree).value
        elif isinstance(length, u.Unit):
            length = length.to(u.degree)

        if isinstance(sep_x, u.Quantity):
            sep_x = sep_x.to(u.degree).value
        elif isinstance(sep_x, u.Unit):
            sep_x = sep_x.to(u.degree)

        if isinstance(sep_y, u.Quantity):
            sep_y = sep_y.to(u.degree).value
        elif isinstance(sep_y, u.Unit):
            sep_y = sep_y.to(u.degree)

        if self._wcs.is_celestial:
            pix_scale = proj_plane_pixel_scales(self._wcs)
            pix_units = self._wcs.wcs.cunit
            sy = pix_scale[1]*u.Unit(pix_units[1])
            sy = sy.to('deg').value
        else:
            raise ValueError("Cannot show compass when WCS is not celestial")

        try:
            self._compass.remove()
        except Exception:
            pass

        if isinstance(corner, str):
            corner = corners[corner]

        if MPL_VERSION >= 3:
            compass = AnchoredDirectionArrows(self._ax.transAxes, length=length,
                                              label_x='E', label_y='N',
                                              loc=corner, aspect_ratio=-1,
                                              frameon=True, fontproperties=self._label_settings['fontproperties'])
            self._ax.add_artist(compass)
            self._figure.canvas.draw()
            frame_bl = compass.patch.get_bbox().min
            frame_tr = compass.patch.get_bbox().max
            frame_bl = self._ax.transData.inverted().transform(frame_bl)
            frame_tr = self._ax.transData.inverted().transform(frame_tr)
            frame_center = np.array([frame_bl[0] + (frame_tr[0] - frame_bl[0]) / 2,
                                     frame_bl[1] + (frame_tr[1] - frame_bl[1]) / 2])
            compass.remove()

            p1 = np.array(self._wcs.all_pix2world(frame_center[0], frame_center[1], 1))
            p2 = np.array([p1[0], p1[1] + sy])
            p2 = np.array(self._wcs.all_world2pix(p2[0], p2[1], 1))
            p1 = frame_center
            angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
            angle = np.rad2deg(angle) - 90

            self._compass = AnchoredDirectionArrows(self._ax.transAxes,
                                                    length=length, label_x='E',
                                                    label_y='N', loc=corner,
                                                    angle=angle,
                                                    aspect_ratio=-1,
                                                    frameon=frame, sep_x=sep_x,
                                                    sep_y=sep_y,
                                                    fontproperties=self._label_settings['fontproperties'])

            self._ax.add_artist(self._compass)

        else:
            xmin, xmax = self._ax.get_xlim()
            ymin, ymax = self._ax.get_ylim()
            pos_min = self._wcs.all_pix2world(xmin, ymin, 1)
            pos_max = self._wcs.all_pix2world(xmax, ymax, 1)

            extent_x = [pos_max[0], pos_min[1]]
            extent_y = [pos_min[0], pos_max[1]]

            # trying to be insensitive to frame, RA/dec vs. galactic, etc.
            pos_min = self._wcs.all_world2pix(*pos_min, 1)
            extent_x = self._wcs.all_world2pix(*extent_x, 1)
            extent_y = self._wcs.all_world2pix(*extent_y, 1)
            pos_min = SkyCoord.from_pixel(*pos_min, self._wcs, origin=1)
            extent_x = SkyCoord.from_pixel(*extent_x, self._wcs, origin=1)
            extent_y = SkyCoord.from_pixel(*extent_y, self._wcs, origin=1)
            extent_x = pos_min.separation(extent_x)
            extent_y = pos_min.separation(extent_y)
            if hasattr(pos_min, 'dec'):
                extent_x /= np.cos(pos_min.dec.to('radian'))

            w = 2 * length / np.max([extent_x.degree, extent_y.degree])

            pos = {1: (1 - w, 1 - w),
                   2: (w, 1 - w),
                   3: (w, w),
                   4: (1 - w, w),
                   5: (1 - w, 0.5),
                   6: (w, 0.5),
                   7: (1 - w, 0.5),
                   8: (0.5, w),
                   9: (0.5, 1 - w)}

            rx, ry = pos[corner]

            x0 = rx * (xmax - xmin) + xmin
            y0 = ry * (ymax - ymin) + ymin
            pos0 = self._wcs.all_pix2world(x0, y0, 1)

            pos1 = [pos0[0] + length / np.cos(np.radians(pos0[1])), pos0[1]]
            pos2 = [pos0[0], pos0[1] + length]

            pos0 = self._wcs.all_world2pix(*pos0, 1)
            pos1 = self._wcs.all_world2pix(*pos1, 1)
            pos2 = self._wcs.all_world2pix(*pos2, 1)

            arrow1 = FancyArrowPatch(posA=pos0, posB=pos1, arrowstyle='-|>',
                                     mutation_scale=20.,
                                     shrinkA=0., shrinkB=0.,
                                     zorder=self._ax.zorder + 4)
            arrow2 = FancyArrowPatch(posA=pos0, posB=pos2, arrowstyle='-|>',
                                     mutation_scale=20.,
                                     shrinkA=0., shrinkB=0.,
                                     zorder=self._ax.zorder + 4)

            self._ax.add_patch(arrow1)
            self._ax.add_patch(arrow2)

            label1 = Text(pos2[0] + (sep_x / sy), pos2[1] + (sep_y / sy), 'N',
                          fontproperties=self._label_settings['fontproperties'],
                          zorder=self._ax.zorder + 4)
            label2 = Text(pos1[0] + (sep_x / sy), pos1[1] + (sep_y / sy) * 2,
                          'E', fontproperties=self._label_settings['fontproperties'],
                          zorder=self._ax.zorder + 4)

            self._ax.add_artist(label1)
            self._ax.add_artist(label2)

            self._compass = [arrow1, arrow2, label1, label2]

            if frame:
                arrow_corners = np.vstack([pos0, pos1, pos2, [pos1[0], pos2[1]]])

                frame_origin = np.min(arrow_corners, axis=0)
                frame_origin -= [sep_x / sy, 2 * sep_y / sy]

                frame_limit = np.max(arrow_corners, axis=0)
                frame_limit += [5 * sep_x / sy, 6 * sep_y / sy]

                frame_w = frame_limit[0] - frame_origin[0]
                frame_h = frame_limit[1] - frame_origin[1]

                rect = Rectangle(frame_origin, frame_w, frame_h,
                                 zorder=self._ax.zorder + 3, facecolor='white',
                                 edgecolor='black')
                self._ax.add_patch(rect)

                self._compass.append(rect)

        self.set(**kwargs)

    @auto_refresh
    def _remove(self):
        if MPL_VERSION == 3:
            self._compass.remove()
        else:
            print(self._compass, len(self._compass))
            for i in range(len(self._compass)):
                self._compass[i].remove()

    @auto_refresh
    def hide(self):
        """
        Hide the compass.
        """
        if MPL_VERSION == 3:
            try:
                self._compass.remove()
            except Exception:
                pass
        else:
            for i in range(len(self._compass)):
                try:
                    self._compass[i].remove()
                except Exception:
                    pass

    @auto_refresh
    def set_length(self, length):
        """
        Set the length of the compass arrows.
        """
        if MPL_VERSION == 3:
            self._base_settings['length'] = -length
        else:
            self._base_settings['length'] = length
        print(self._base_settings)
        self.show(**self._base_settings)
        self._set_arrow_properties(**self._arrow_settings)
        self._set_label_properties(**self._label_settings)

    @auto_refresh
    def set_corner(self, corner):
        """
        Set where to place the compass.

        Acceptable values are 'left', 'right', 'top', 'bottom', 'top left',
        'top right', 'bottom left', and 'bottom right'.
        """
        self._base_settings['corner'] = corner
        self.show(**self._base_settings)
        self._set_arrow_properties(**self._arrow_settings)
        self._set_label_properties(**self._label_settings)

    @auto_refresh
    def set_frame(self, frame):
        """
        Set whether to display a frame around the compass.
        """
        self._base_settings['frame'] = frame
        self.show(**self._base_settings)
        self._set_arrow_properties(**self._arrow_settings)
        self._set_label_properties(**self._label_settings)

    @auto_refresh
    def set_sep_x(self, sep):
        """
        Set x-direction separation between arrows and labels.
        """
        self._base_settings['sep_x'] = sep
        self.show(**self._base_settings)
        self._set_arrow_properties(**self._arrow_settings)
        self._set_label_properties(**self._label_settings)

    @auto_refresh
    def set_sep_y(self, sep):
        """
        Set y-direction separation between arrows and labels.
        """
        self._base_settings['sep_y'] = sep
        self.show(**self._base_settings)
        self._set_arrow_properties(**self._arrow_settings)
        self._set_label_properties(**self._label_settings)

    # APPEARANCE

    @auto_refresh
    def set_linewidth(self, linewidth):
        """
        Set the linewidth of the compass arrows, in points.
        """
        self._set_arrow_properties(linewidth=linewidth)

    @auto_refresh
    def set_linestyle(self, linestyle):
        """
        Set the linestyle of the compass arrows.

        Should be one of 'solid', 'dashed', 'dashdot', or 'dotted'.
        """
        self._set_arrow_properties(linestyle=linestyle)

    @auto_refresh
    def set_alpha(self, alpha):
        """
        Set the alpha value (transparency).

        This should be a floating point value between 0 and 1.
        """
        self._set_arrow_properties(alpha=alpha)
        self._set_label_properties(alpha=alpha)

    @auto_refresh
    def set_color(self, color):
        """
        Set the compass color.
        """
        self._set_arrow_properties(color=color)
        self._set_label_properties(color=color)

    @auto_refresh
    def set_font(self, family=None, style=None, variant=None, stretch=None,
                 weight=None, size=None, fontproperties=None):
        """
        Set the font of the label text.

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

        self.show(fontproperties=self._label_settings['fontproperties'],
                  **self._base_settings)
        self._set_arrow_properties(**self._arrow_settings)
        self._set_label_properties(**self._label_settings)

    @auto_refresh
    def _set_label_properties(self, **kwargs):
        """
        Modify the compass label properties.

        All arguments are passed to the matplotlib Text (mpl 2) or TextPath
        mpl 3) class. See the matplotlib documentation for more details.
        """
        for kwarg, val in kwargs.items():
            kvpair = {kwarg: val}
            if MPL_VERSION == 3:
                try:
                    # TextPath does not take fontproperties, always handled by show
                    if kwarg == 'fontproperties':
                        continue
                    self._compass.box.get_children()[2].set(**kvpair)
                    self._compass.box.get_children()[3].set(**kvpair)
                    self._label_settings[kwarg] = val
                except AttributeError:
                    warnings.warn("TextPath labels do not have attribute {0}. Skipping.".format(kwarg))
            else:
                try:
                    self._compass[2].set(**kvpair)
                    self._compass[3].set(**kvpair)
                    self._label_settings[kwarg] = val
                except AttributeError:
                    warnings.warn("Text labels do not have attribute {0}. Skipping.".format(kwarg))

    @auto_refresh
    def _set_arrow_properties(self, **kwargs):
        """
        Modify the arrow properties.

        All arguments are passed to the matplotlib FancyArrowPatch class. See
        the matplotlib documentation for more details.
        """
        for kwarg, val in kwargs.items():
            kvpair = {kwarg: val}
            try:
                if MPL_VERSION == 3:
                    self._compass.arrow_x.set(**kvpair)
                    self._compass.arrow_y.set(**kvpair)
                else:
                    self._compass[0].set(**kvpair)
                    self._compass[1].set(**kvpair)
                self._arrow_settings[kwarg] = val
            except AttributeError:
                warnings.warn("FancyArrowPatch does not have attribute {0}. Skipping.".format(kwarg))

    @auto_refresh
    def set(self, **kwargs):
        """
        Modify the compass and compass properties.

        All arguments are passed to the matplotlib TextPath and
        FancyArrowPatch classes. See the matplotlib documentation for more
        details.
        """
        for kwarg in kwargs:
            kwargs_single = {kwarg: kwargs[kwarg]}
            try:
                self._set_label_properties(**kwargs_single)
            except (AttributeError, TypeError):
                pass
            try:
                self._set_arrow_properties(**kwargs_single)
            except (AttributeError, TypeError):
                pass


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

        if self._wcs.is_celestial:
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
