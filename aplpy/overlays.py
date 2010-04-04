import warnings

from mpl_toolkits.axes_grid.anchored_artists \
    import AnchoredEllipse, AnchoredSizeBar

from matplotlib.patches import FancyArrowPatch
from matplotlib.font_manager import FontProperties
import wcs_util

import numpy as np

from decorators import auto_refresh

class Compass(object):

    def _initialize_compass(self):

        # Initialize compass holder
        self._compass = None

        self._compass_show = False

        # Set grid event handler
        self._ax1.callbacks.connect('xlim_changed', self.update_compass)
        self._ax1.callbacks.connect('ylim_changed', self.update_compass)

    @auto_refresh
    def show_compass(self, color='red', length = 0.1, corner=4, frame=True):
        '''
        Display a scalebar

        Required Arguments:

            *length*:[ float ]
                The length of the scalebar, in degrees

        Optional Keyword Arguments:

            *label*: [ string ]
                Label to place above the scalebar

            *corner*: [ integer ]
                Where to place the scalebar. Acceptable values are:
                1: top right
                2: top left
                3: bottom left (default)
                4: bottom right
                5: center right
                6: center left
                7: center right (same as 5)
                8: bottom center
                9: top center

            *frame*: [ True | False ]
                Whether to display a frame behind the scalebar (default is False)

            Additional keyword arguments can be used to control the appearance
            of the scalebar, which is made up of an instance of the matplotlib
            Rectangle class and a an instance of the Text class. For more
            information on available arguments, see

            `Rectangle <http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.patches.Rectangle>`_

            and

            `Text <http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.text.Text>`_`.

            In cases where the same argument exists for the two objects, the
            argument is passed to both the Text and Rectangle instance

        '''

        w = 2 * length

        pos = {1:(1-w, 1-w),
               2:(w, 1-w),
               3:(w, w),
               4:(1-w, w),
               5:(1-w, 0.5),
               6:(w, 0.5),
               7:(1-w, 0.5),
               8:(0.5, w),
               9:(0.5, 1-w)}

        self._compass_position = pos[corner]
        self._compass_length = length
        self._compass_color = color
        self._compass = None
        self._compass_show = True

        self.update_compass()

    @auto_refresh
    def update_compass(self, *args, **kwargs):

        if not self._compass_show:
            return

        rx, ry = self._compass_position
        length = self._compass_length
        color = self._compass_color

        xmin, xmax = self._ax1.get_xlim()
        ymin, ymax = self._ax1.get_ylim()

        x0 = rx * (xmax - xmin) + xmin
        y0 = ry * (ymax - ymin) + ymin

        xw, yw = self.pixel2world(x0, y0)

        len_pix = length * (ymax - ymin)

        degperpix = wcs_util.degperpix(self._wcs)

        len_deg = len_pix * degperpix

        # Should really only do tiny displacement then magnify the vectors - important if there is curvature

        x1, y1 = self.world2pixel(xw + len_deg / np.cos(np.radians(yw)), yw)
        x2, y2 = self.world2pixel(xw, yw + len_deg)

        if self._compass:
            self._compass[0].remove()
            self._compass[1].remove()

        arrow1 = FancyArrowPatch(posA=(x0, y0), posB=(x1, y1), arrowstyle='-|>', mutation_scale=20., fc=color, ec=color, shrinkA=0., shrinkB=0.)
        arrow2 = FancyArrowPatch(posA=(x0, y0), posB=(x2, y2), arrowstyle='-|>', mutation_scale=20., fc=color, ec=color, shrinkA=0., shrinkB=0.)

        self._compass = (arrow1, arrow2)

        self._ax1.add_patch(arrow1)
        self._ax1.add_patch(arrow2)

    @auto_refresh
    def hide_compass(self):
        pass

class ScaleBar(object):

    def __init__(self, parent):

        # Retrieve info from parent figure
        self._ax = parent._ax1
        self._wcs = parent._wcs
        self._figure = parent._figure

        # Initialize settings
        self._base_settings = {}
        self._scalebar_settings = {}
        self._label_settings = {}
        self._label_settings['fontproperties'] = FontProperties()

    @auto_refresh
    def show(self, length, label=None, corner=4, frame=False, **kwargs):
        '''
        Display a scalebar

        Required Arguments:

            *length*:[ float ]
                The length of the scalebar, in degrees

        Optional Keyword Arguments:

            *label*: [ string ]
                Label to place below the scalebar

            *corner*: [ integer ]
                Where to place the scalebar. Acceptable values are:
                1: top right
                2: top left
                3: bottom left (default)
                4: bottom right
                5: center right
                6: center left
                7: center right (same as 5)
                8: bottom center
                9: top center

            *frame*: [ True | False ]
                Whether to display a frame behind the scalebar (default is False)

            Additional keyword arguments can be used to control the appearance
            of the scalebar, which is made up of an instance of the matplotlib
            Rectangle class and a an instance of the Text class. For more
            information on available arguments, see

            `Rectangle <http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.patches.Rectangle>`_

            and

            `Text <http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.text.Text>`_`.

            In cases where the same argument exists for the two objects, the
            argument is passed to both the Text and Rectangle instance

        '''

        self._length = length
        self._base_settings['corner'] = corner
        self._base_settings['frame'] = frame

        degperpix = wcs_util.degperpix(self._wcs)

        length = length / degperpix

        try:
            self._scalebar.remove()
        except:
            pass

        self._scalebar = AnchoredSizeBar(self._ax.transData, length, label, corner, \
                              pad=0.5, borderpad=0.4, sep=5, frameon=frame)

        self._ax.add_artist(self._scalebar)

        self.set(**kwargs)

    @auto_refresh
    def _remove(self):
        self._scalebar.remove()

    @auto_refresh
    def hide(self):
        '''
        Hide the scalebar
        '''
        try:
            self._scalebar.remove()
        except:
            pass

    @auto_refresh
    def set_length(self, length):
        self.show(length, **self._base_settings)
        self._set_scalebar_properties(**self._scalebar_settings)
        self._set_label_properties(**self._scalebar_settings)

    @auto_refresh
    def set_label(self, label):
        self._set_label_properties(text=label)

    @auto_refresh
    def set_linewidth(self, linewidth):
        self._set_scalebar_properties(linewidth=linewidth)

    @auto_refresh
    def set_linestyle(self, linestyle):
        self._set_scalebar_properties(linestyle=linestyle)

    @auto_refresh
    def set_corner(self, corner):
        self._base_settings['corner'] = corner
        self.show(self._length, **self._base_settings)
        self._set_scalebar_properties(**self._scalebar_settings)
        self._set_label_properties(**self._scalebar_settings)

    @auto_refresh
    def set_frame(self, frame):
        self._base_settings['frame'] = frame
        self.show(self._length, **self._base_settings)
        self._set_scalebar_properties(**self._scalebar_settings)
        self._set_label_properties(**self._scalebar_settings)

    @auto_refresh
    def set_alpha(self, alpha):
        self._set_scalebar_properties(alpha=alpha)
        self._set_label_properties(alpha=alpha)

    @auto_refresh
    def set_color(self, color):
        self._set_scalebar_properties(color=color)
        self._set_label_properties(color=color)

    @auto_refresh
    def set_font_family(self, family):
        warnings.warn("scalebar.set_font_family is deprecated - use scalebar.set_font instead", DeprecationWarning)
        self.set_font(family=family)

    @auto_refresh
    def set_font_weight(self, weight):
        warnings.warn("scalebar.set_font_weight is deprecated - use scalebar.set_font instead", DeprecationWarning)
        self.set_font(weight=weight)

    def set_font_size(self, size):
        warnings.warn("scalebar.set_font_size is deprecated - use scalebar.set_font instead", DeprecationWarning)
        self.set_font(size=size)

    @auto_refresh
    def set_font_style(self, style):
        warnings.warn("scalebar.set_font_style is deprecated - use scalebar.set_font instead", DeprecationWarning)
        self.set_font(style=style)

    @auto_refresh
    def set_font(self, family=None, style=None, variant=None, stretch=None, weight=None, size=None, fontproperties=None):

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
        '''
        Modify the scalebar label properties. All arguments are passed to the
        matplotlib Text class. See the matplotlib documentation for more
        details.
        '''
        for kwarg in kwargs:
            self._label_settings[kwarg] = kwargs[kwarg]
        self._scalebar.txt_label.get_children()[0].set(**kwargs)

    @auto_refresh
    def _set_scalebar_properties(self, **kwargs):
        '''
        Modify the scalebar properties. All arguments are passed to the
        matplotlib Rectangle class. See the matplotlib documentation for more
        details.
        '''
        for kwarg in kwargs:
            self._scalebar_settings[kwarg] = kwargs[kwarg]
        self._scalebar.size_bar.get_children()[0].set(**kwargs)

    @auto_refresh
    def set(self, **kwargs):
        '''
        Modify the scalebar and scalebar properties. All arguments are passed
        to the matplotlib Rectangle and Text classes. See the matplotlib
        documentation for more details. In cases where the same argument
        exists for the two objects, the argument is passed to both the Text
        and Rectangle instance.
        '''
        for kwarg in kwargs:
            kwargs_single = {kwarg: kwargs[kwarg]}
            try:
                self._set_label_properties(**kwargs_single)
            except AttributeError:
                pass
            try:
                self._set_scalebar_properties(**kwargs_single)
            except AttributeError:
                pass


class Beam(object):

    def __init__(self, parent):

        # Retrieve info from parent figure
        self._figure = parent._figure
        self._hdu = parent._hdu
        self._ax = parent._ax1
        self._wcs = parent._wcs

        # Initialize settings
        self._base_settings = {}
        self._beam_settings = {}

    @auto_refresh
    def show(self, major='BMAJ', minor='BMIN', \
        angle='BPA', corner=3, frame=False, borderpad=0.4, pad=0.5, **kwargs):

        '''
        Display the beam shape and size for the primary image

        By default, this method will search for the BMAJ, BMIN, and BPA
        keywords in the FITS header to set the major and minor axes and the
        position angle on the sky.

        Optional Keyword Arguments:

            *major*: [ float ]
                Major axis of the beam in degrees (overrides BMAJ if present)

            *minor*: [ float ]
                Minor axis of the beam in degrees (overrides BMIN if present)

            *angle*: [ float ]
                Position angle of the beam on the sky in degrees (overrides
                BPA if present)

            *corner*: [ integer ]
                Where to place the beam. Acceptable values are:
                1: top right
                2: top left
                3: bottom left (default)
                4: bottom right
                5: center right
                6: center left
                7: center right (same as 5)
                8: bottom center
                9: top center

            *frame*: [ True | False ]
                Whether to display a frame behind the beam (default is False)

            Additional keyword arguments can be used to control the appearance
            of the beam, which is an instance of the matplotlib Ellipse class.
            For more information on available arguments, see `Ellipse
            <http://matplotlib.sourceforge.net/api/artist_api.html
            #matplotlib.patches.Ellipse>`_.

        '''

        if type(major) == str:
            major = self._hdu.header[major]

        if type(minor) == str:
            minor = self._hdu.header[minor]

        if type(angle) == str:
            angle = self._hdu.header[angle]

        degperpix = wcs_util.degperpix(self._wcs)

        self._base_settings['minor'] = minor
        self._base_settings['major'] = major
        self._base_settings['angle'] = angle
        self._base_settings['corner'] = corner
        self._base_settings['frame'] = frame
        self._base_settings['borderpad'] = borderpad
        self._base_settings['pad'] = pad

        minor /= degperpix
        major /= degperpix

        try:
            self._beam.remove()
        except:
            pass

        self._beam = AnchoredEllipse(self._ax.transData, \
            width=major, height=minor, angle=angle, \
            loc=corner, pad=pad, borderpad=borderpad, frameon=frame)

        self._ax.add_artist(self._beam)

        self.set(**kwargs)

    @auto_refresh
    def _remove(self):
        self._beam.remove()

    @auto_refresh
    def hide(self):
        '''
        Hide the beam
        '''
        try:
            self._beam.remove()
        except:
            pass

    @auto_refresh
    def set_major(self, major):
        self._base_settings['major'] = major
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_minor(self, minor):
        self._base_settings['minor'] = minor
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_angle(self, angle):
        self._base_settings['angle'] = angle
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_corner(self, corner):
        self._base_settings['corner'] = corner
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_frame(self, frame):
        self._base_settings['frame'] = frame
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_borderpad(self, borderpad):
        self._base_settings['borderpad'] = borderpad
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_pad(self, pad):
        self._base_settings['pad'] = pad
        self.show(**self._base_settings)
        self.set(**self._beam_settings)

    @auto_refresh
    def set_alpha(self, alpha):
        self.set(alpha=alpha)

    @auto_refresh
    def set_color(self, color):
        self.set(color=color)

    @auto_refresh
    def set_edgecolor(self, edgecolor):
        self.set(edgecolor=edgecolor)

    @auto_refresh
    def set_facecolor(self, facecolor):
        self.set(facecolor=facecolor)

    @auto_refresh
    def set_linestyle(self, linestyle):
        self.set(linestyle=linestyle)

    @auto_refresh
    def set_linewidth(self, linewidth):
        self.set(linewidth=linewidth)

    @auto_refresh
    def set_hatch(self, hatch):
        self.set(hatch=hatch)

    @auto_refresh
    def set(self, **kwargs):
        '''
        Modify the beam properties

        All arguments are passed to the beam, which is an instance of the
        matplotlib Ellipse class. For more information on available arguments,
        see `Ellipse <http://matplotlib.sourceforge.net/api/artist_api.html
        #matplotlib.patches.Ellipse>`_.
        '''
        for kwarg in kwargs:
            self._beam_settings[kwarg] = kwargs[kwarg]
        self._beam.ellipse.set(**kwargs)
