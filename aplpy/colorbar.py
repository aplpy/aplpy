import warnings

from mpl_toolkits.axes_grid import make_axes_locatable
import matplotlib.axes as maxes

from matplotlib.font_manager import FontProperties

from decorators import auto_refresh

# As of matplotlib 0.99.1.1, any time a colorbar property is updated, the axes
# need to be removed and re-created. This has been fixed in svn r8213 but we
# should wait until we up the required version of matplotlib before changing the
# code here

class Colorbar(object):

    def __init__(self, parent):
        self._figure = parent._figure
        self._colorbar_axes = None
        self._parent = parent
        self._base_settings = {}
        self._label_fontproperties = FontProperties()

    @auto_refresh
    def show(self, location='right', size='5%', pad=0.05, ticks=None, labels=True):

        self._base_settings['location'] = location
        self._base_settings['size'] = size
        self._base_settings['pad'] = pad

        if self._parent.image:

            if self._colorbar_axes:
                self._parent._figure.delaxes(self._colorbar_axes)

            divider = make_axes_locatable(self._parent._ax1)

            if location=='right':
                self._colorbar_axes = divider.new_horizontal(size=size, pad=pad, axes_class=maxes.Axes)
                orientation='vertical'
            elif location=='top':
                self._colorbar_axes = divider.new_vertical(size=size, pad=pad, axes_class=maxes.Axes)
                orientation='horizontal'
            elif location=='left':
                warnings.warn("Left colorbar not fully implemented")
                self._colorbar_axes = divider.new_horizontal(size=size, pad=pad, pack_start=True, axes_class=maxes.Axes)
                locator = divider.new_locator(nx=0, ny=0)
                self._colorbar_axes.set_axes_locator(locator)
                orientation='vertical'
            elif location=='bottom':
                warnings.warn("Bottom colorbar not fully implemented")
                self._colorbar_axes = divider.new_vertical(size=size, pad=pad, pack_start=True, axes_class=maxes.Axes)
                locator = divider.new_locator(nx=0, ny=0)
                self._colorbar_axes.set_axes_locator(locator)
                orientation='horizontal'
            else:
                raise Exception("location should be one of: right/top")

            self._parent._figure.add_axes(self._colorbar_axes)

            self._colorbar = self._parent._figure.colorbar(self._parent.image, cax=self._colorbar_axes, orientation=orientation, ticks=ticks)

            if location=='right':
                for tick in self._colorbar_axes.yaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = False
                    tick.label2On = labels
            if location=='top':
                for tick in self._colorbar_axes.xaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = False
                    tick.label2On = labels
            if location=='left':
                for tick in self._colorbar_axes.yaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = labels
                    tick.label2On = False
            if location=='bottom':
                for tick in self._colorbar_axes.xaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = labels
                    tick.label2On = False

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
        self._base_settings['location'] = location
        self.show(**self._base_settings)
        self.set_font_properties(fontproperties=self._label_fontproperties)

    @auto_refresh
    def set_size(self, size):
        self._base_settings['size'] = size
        self.show(**self._base_settings)
        self.set_font_properties(fontproperties=self._label_fontproperties)

    @auto_refresh
    def set_pad(self, pad):
        self._base_settings['pad'] = pad
        self.show(**self._base_settings)
        self.set_font_properties(fontproperties=self._label_fontproperties)

    # FONT PROPERTIES

    @auto_refresh
    def set_font_family(self, family):
        self.set_font_properties(family=family)

    @auto_refresh
    def set_font_style(self, style):
        self.set_font_properties(style=style)

    @auto_refresh
    def set_font_variant(self, variant):
        self.set_font_properties(variant=variant)

    @auto_refresh
    def set_font_stretch(self, stretch):
        self.set_font_properties(stretch=stretch)

    @auto_refresh
    def set_font_weight(self, weight):
        self.set_font_properties(weight=weight)

    @auto_refresh
    def set_font_size(self, size):
        self.set_font_properties(size=size)

    @auto_refresh
    def set_label_properties(self, *args, **kwargs):
        warnings.warn("set_label_properties is deprecated - use set_font_properties instead", DeprecationWarning)
        self.set_font_properties(*args, **kwargs)

    @auto_refresh
    def set_font_properties(self, family=None, style=None, variant=None, stretch=None, weight=None, size=None, fontproperties=None):

        if family:
            self._label_fontproperties.set_family(family)

        if style:
            self._label_fontproperties.set_style(style)

        if variant:
            self._label_fontproperties.set_variant(variant)

        if stretch:
            self._label_fontproperties.set_stretch(stretch)

        if weight:
            self._label_fontproperties.set_weight(weight)

        if size:
            self._label_fontproperties.set_size(size)

        if fontproperties:
            self._label_fontproperties = fontproperties

        for label in self._colorbar_axes.get_xticklabels():
            label.set_fontproperties(self._label_fontproperties)
        for label in self._colorbar_axes.get_yticklabels():
            label.set_fontproperties(self._label_fontproperties)

    # FRAME PROPERTIES

    @auto_refresh
    def set_frame_linewidth(self, linewidth):
        for key in self._colorbar_axes.spines:
            self._colorbar_axes.spines[key].set_linewidth(linewidth)

    @auto_refresh
    def set_frame_color(self, color):
        for key in self._colorbar_axes.spines:
            self._colorbar_axes.spines[key].set_edgecolor(color)
