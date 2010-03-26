import warnings

from mpl_toolkits.axes_grid import make_axes_locatable
import matplotlib.axes as maxes


class Colorbar(object):

    def __init__(self, parent):
        self._colorbar_axes = None
        self._parent = parent
        self._base_settings = {}
        self._label_settings = {}

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

        self._parent.refresh()

    def set_location(self, location):
        self._base_settings['location'] = location
        self.show(**self._base_settings)
        self.set_label_properties(**self._label_settings)

    def set_size(self, size):
        self._base_settings['size'] = size
        self.show(**self._base_settings)
        self.set_label_properties(**self._label_settings)

    def set_pad(self, pad):
        self._base_settings['pad'] = pad
        self.show(**self._base_settings)
        self.set_label_properties(**self._label_settings)

    def set_font_family(self, family):
        self.set_label_properties(family=family)

    def set_font_size(self, size):
        self.set_label_properties(size=size)

    def set_font_weight(self, weight):
        self.set_label_properties(weight=weight)

    def set_label_properties(self, family=None, size=None, weight=None):

        if family:
            self._label_settings['family'] = family
            for label in self._colorbar_axes.get_xticklabels():
                label.set_family(family)
            for label in self._colorbar_axes.get_yticklabels():
                label.set_family(family)

        if size:
            self._label_settings['size'] = size
            for label in self._colorbar_axes.get_xticklabels():
                label.set_size(size)
            for label in self._colorbar_axes.get_yticklabels():
                label.set_size(size)

        if weight:
            self._label_settings['weight'] = weight
            for label in self._colorbar_axes.get_xticklabels():
                label.set_weight(weight)
            for label in self._colorbar_axes.get_yticklabels():
                label.set_weight(weight)

        self._parent.refresh()

    def update(self):
        if self._colorbar_axes:
            self.show(**self._base_settings)

    def hide(self):
        self._parent._figure.delaxes(self._colorbar_axes)
        self._colorbar_axes = None
