from __future__ import absolute_import, print_function, division

import warnings

import matplotlib.axes as maxes
from mpl_toolkits.axes_grid import make_axes_locatable
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import LogFormatterMathtext

from .decorators import auto_refresh, fixdocstring

# As of matplotlib 0.99.1.1, any time a colorbar property is updated, the axes
# need to be removed and re-created. This has been fixed in svn r8213 but we
# should wait until we up the required version of matplotlib before changing the
# code here


class Colorbar(object):

    def __init__(self, parent):
        self._figure = parent._figure
        self._colorbar_axes = None
        self._parent = parent

        # Save plotting parameters (required for @auto_refresh)
        self._parameters = parent._parameters

        self._base_settings = {}
        self._ticklabel_fontproperties = FontProperties()
        self._axislabel_fontproperties = FontProperties()

    @auto_refresh
    def show(self, location='right', width=0.2, pad=0.05, ticks=None, labels=True, log_format=False,
             box=None, box_orientation='vertical', axis_label_text=None, axis_label_rotation=None,
             axis_label_pad=5):
        '''
        Show a colorbar on the side of the image.

        Parameters
        ----------

        location : str, optional
            Where to place the colorbar. Should be one of 'left', 'right', 'top', 'bottom'.

        width : float, optional
            The width of the colorbar relative to the canvas size.

        pad : float, optional
            The spacing between the colorbar and the image relative to the canvas size.

        ticks : list, optional
            The position of the ticks on the colorbar.

        labels : bool, optional
            Whether to show numerical labels.

        log_format : bool, optional
            Whether to format ticks in exponential notation

        box : list, optional
            A custom box within which to place the colorbar. This should
            be in the form [xmin, ymin, dx, dy] and be in relative figure
            units. This overrides the location argument.

        box_orientation str, optional
            The orientation of the colorbar within the box. Can be
            'horizontal' or 'vertical'

        axis_label_text str, optional
            Optional text label of the colorbar.
        '''

        self._base_settings['location'] = location
        self._base_settings['width'] = width
        self._base_settings['pad'] = pad
        self._base_settings['ticks'] = ticks
        self._base_settings['labels'] = labels
        self._base_settings['log_format'] = log_format
        self._base_settings['box'] = box
        self._base_settings['box_orientation'] = box_orientation
        self._base_settings['axis_label_text'] = axis_label_text
        self._base_settings['axis_label_rotation'] = axis_label_rotation
        self._base_settings['axis_label_pad'] = axis_label_pad

        if self._parent.image:

            if self._colorbar_axes:
                self._parent._figure.delaxes(self._colorbar_axes)

            if box is None:

                divider = make_axes_locatable(self._parent._ax1)

                if location == 'right':
                    self._colorbar_axes = divider.new_horizontal(size=width, pad=pad, axes_class=maxes.Axes)
                    orientation = 'vertical'
                elif location == 'top':
                    self._colorbar_axes = divider.new_vertical(size=width, pad=pad, axes_class=maxes.Axes)
                    orientation = 'horizontal'
                elif location == 'left':
                    warnings.warn("Left colorbar not fully implemented")
                    self._colorbar_axes = divider.new_horizontal(size=width, pad=pad, pack_start=True, axes_class=maxes.Axes)
                    locator = divider.new_locator(nx=0, ny=0)
                    self._colorbar_axes.set_axes_locator(locator)
                    orientation = 'vertical'
                elif location == 'bottom':
                    warnings.warn("Bottom colorbar not fully implemented")
                    self._colorbar_axes = divider.new_vertical(size=width, pad=pad, pack_start=True, axes_class=maxes.Axes)
                    locator = divider.new_locator(nx=0, ny=0)
                    self._colorbar_axes.set_axes_locator(locator)
                    orientation = 'horizontal'
                else:
                    raise Exception("location should be one of: right/top")

                self._parent._figure.add_axes(self._colorbar_axes)

            else:

                self._colorbar_axes = self._parent._figure.add_axes(box)
                orientation = box_orientation

            if log_format:
                format=LogFormatterMathtext()
            else:
                format=None

            self._colorbar = self._parent._figure.colorbar(self._parent.image, cax=self._colorbar_axes,
                                                           orientation=orientation, format=format,
                                                           ticks=ticks)
            if axis_label_text:
                if axis_label_rotation:
                    self._colorbar.set_label(axis_label_text, rotation=axis_label_rotation)
                else:
                    self._colorbar.set_label(axis_label_text)

            if location == 'right':
                for tick in self._colorbar_axes.yaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = False
                    tick.label2On = labels
                self._colorbar_axes.yaxis.set_label_position('right')
                self._colorbar_axes.yaxis.labelpad = axis_label_pad
            elif location == 'top':
                for tick in self._colorbar_axes.xaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = False
                    tick.label2On = labels
                self._colorbar_axes.xaxis.set_label_position('top')
                self._colorbar_axes.xaxis.labelpad = axis_label_pad
            elif location == 'left':
                for tick in self._colorbar_axes.yaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = labels
                    tick.label2On = False
                self._colorbar_axes.yaxis.set_label_position('left')
                self._colorbar_axes.yaxis.labelpad = axis_label_pad
            elif location == 'bottom':
                for tick in self._colorbar_axes.xaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = labels
                    tick.label2On = False
                self._colorbar_axes.xaxis.set_label_position('bottom')
                self._colorbar_axes.xaxis.labelpad = axis_label_pad

        else:

            warnings.warn("No image is shown, therefore, no colorbar will be plotted")

    @auto_refresh
    def update(self):
        if self._colorbar_axes:
            self.show(**self._base_settings)

    @auto_refresh
    def hide(self):
        self._parent._figure.delaxes(self._colorbar_axes)
        self._colorbar_axes = None

    @auto_refresh
    def _remove(self):
        self._parent._figure.delaxes(self._colorbar_axes)

    # LOCATION AND SIZE

    @auto_refresh
    def set_location(self, location):
        '''
        Set the location of the colorbar.

        Should be one of 'left', 'right', 'top', 'bottom'.
        '''
        self._base_settings['location'] = location
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    @auto_refresh
    def set_width(self, width):
        '''
        Set the width of the colorbar relative to the canvas size.
        '''
        self._base_settings['width'] = width
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    @auto_refresh
    def set_pad(self, pad):
        '''
        Set the spacing between the colorbar and the image relative to the canvas size.
        '''
        self._base_settings['pad'] = pad
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    @auto_refresh
    def set_ticks(self, ticks):
        '''
        Set the position of the ticks on the colorbar.
        '''
        self._base_settings['ticks'] = ticks
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    @auto_refresh
    def set_labels(self, labels):
        '''
        Set whether to show numerical labels.
        '''
        self._base_settings['labels'] = labels
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    @auto_refresh
    def set_box(self, box, box_orientation='vertical'):
        '''
        Set the box within which to place the colorbar.

        This should be in the form [xmin, ymin, dx, dy] and be in relative
        figure units. The orientation of the colorbar within the box can be
        controlled with the box_orientation argument.
        '''
        self._base_settings['box'] = box
        self._base_settings['box_orientation'] = box_orientation
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    @auto_refresh
    def set_axis_label_text(self, axis_label_text):
        '''
        Set the colorbar label text.
        '''
        self._base_settings['axis_label_text'] = axis_label_text
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    @auto_refresh
    def set_axis_label_rotation(self, axis_label_rotation):
        '''
        Set the colorbar label rotation.
        '''
        self._base_settings['axis_label_rotation'] = axis_label_rotation
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    @auto_refresh
    def set_axis_label_pad(self, axis_label_pad):
        '''
        Set the colorbar label displacement, in points.
        '''
        self._base_settings['axis_label_pad'] = axis_label_pad
        self.show(**self._base_settings)
        self.set_font(fontproperties=self._ticklabel_fontproperties)
        self.set_axis_label_font(fontproperties=self._axislabel_fontproperties)

    # FONT PROPERTIES

    @auto_refresh
    def set_label_properties(self, *args, **kwargs):
        warnings.warn("set_label_properties is deprecated - use set_font instead", DeprecationWarning)
        self.set_font(*args, **kwargs)

    @auto_refresh
    @fixdocstring
    def set_font(self, family=None, style=None, variant=None, stretch=None, weight=None, size=None, fontproperties=None):
        '''
        Set the font of the tick labels.

        Parameters
        ----------

        common: family, style, variant, stretch, weight, size, fontproperties

        Notes
        -----

        Default values are set by matplotlib or previously set values if
        set_font has already been called. Global default values can be set by
        editing the matplotlibrc file.
        '''

        if family:
            self._ticklabel_fontproperties.set_family(family)

        if style:
            self._ticklabel_fontproperties.set_style(style)

        if variant:
            self._ticklabel_fontproperties.set_variant(variant)

        if stretch:
            self._ticklabel_fontproperties.set_stretch(stretch)

        if weight:
            self._ticklabel_fontproperties.set_weight(weight)

        if size:
            self._ticklabel_fontproperties.set_size(size)

        if fontproperties:
            self._ticklabel_fontproperties = fontproperties

        # Update the tick label font properties
        for label in self._colorbar_axes.get_xticklabels():
            label.set_fontproperties(self._ticklabel_fontproperties)
        for label in self._colorbar_axes.get_yticklabels():
            label.set_fontproperties(self._ticklabel_fontproperties)

        # Also update the offset text font properties
        label = self._colorbar_axes.xaxis.get_offset_text()
        label.set_fontproperties(self._ticklabel_fontproperties)
        label = self._colorbar_axes.yaxis.get_offset_text()
        label.set_fontproperties(self._ticklabel_fontproperties)

    @auto_refresh
    @fixdocstring
    def set_axis_label_font(self, family=None, style=None, variant=None,
                            stretch=None, weight=None, size=None, fontproperties=None):
        '''
        Set the font of the tick labels.

        Parameters
        ----------

        common: family, style, variant, stretch, weight, size, fontproperties

        Notes
        -----

        Default values are set by matplotlib or previously set values if
        set_font has already been called. Global default values can be set by
        editing the matplotlibrc file.
        '''

        if family:
            self._axislabel_fontproperties.set_family(family)

        if style:
            self._axislabel_fontproperties.set_style(style)

        if variant:
            self._axislabel_fontproperties.set_variant(variant)

        if stretch:
            self._axislabel_fontproperties.set_stretch(stretch)

        if weight:
            self._axislabel_fontproperties.set_weight(weight)

        if size:
            self._axislabel_fontproperties.set_size(size)

        if fontproperties:
            self._axislabel_fontproperties = fontproperties

        # Update the label font properties
        label = self._colorbar_axes.xaxis.get_label()
        label.set_fontproperties(self._axislabel_fontproperties)
        label = self._colorbar_axes.yaxis.get_label()
        label.set_fontproperties(self._axislabel_fontproperties)

    # FRAME PROPERTIES

    @auto_refresh
    def set_frame_linewidth(self, linewidth):
        '''
        Set the linewidth of the colorbar frame, in points.
        '''
        warnings.warn("This method is not functional at this time")
        for key in self._colorbar_axes.spines:
            self._colorbar_axes.spines[key].set_linewidth(linewidth)

    @auto_refresh
    def set_frame_color(self, color):
        '''
        Set the color of the colorbar frame, in points.
        '''
        warnings.warn("This method is not functional at this time")
        for key in self._colorbar_axes.spines:
            self._colorbar_axes.spines[key].set_edgecolor(color)
