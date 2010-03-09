import warnings

from mpl_toolkits.axes_grid import make_axes_locatable
import matplotlib.axes as maxes

import numpy as np

class Colorbar(object):

    def _initialize_colorbar(self):
        self._colorbar_axes = None
        self.location = 'right'
        self.size = "5%"
        self.pad = 0.05

    def reset_colorbar(self):
        self.location = 'right'
        self.size = "5%"
        self.pad = 0.05
        self.update_colorbar()

    def show_colorbar(self, location=None, size=None, pad=None):

        if type(location) == str:
            self.location = location

        if type(size) == str:
            self.size = size

        if not np.equal(pad, None):
            self.pad = pad

        if self.image:

            if self._colorbar_axes:
                self._figure.delaxes(self._colorbar_axes)

            divider = make_axes_locatable(self._ax1)

            if self.location=='right':
                self._colorbar_axes = divider.new_horizontal(size=self.size, pad=self.pad, axes_class=maxes.Axes)
                self.orientation='vertical'
            elif self.location=='top':
                self._colorbar_axes = divider.new_vertical(size=self.size, pad=self.pad, axes_class=maxes.Axes)
                self.orientation='horizontal'
            elif self.location=='left':
                warnings.warn("Left colorbar not fully implemented")
                self._colorbar_axes = divider.new_horizontal(size=self.size, pad=self.pad, pack_start=True, axes_class=maxes.Axes)
                locator = divider.new_locator(nx=0, ny=0)
                self._colorbar_axes.set_axes_locator(locator)
                self.orientation='vertical'
            elif self.location=='bottom':
                warnings.warn("Bottom colorbar not fully implemented")
                self._colorbar_axes = divider.new_vertical(size=self.size, pad=self.pad, pack_start=True, axes_class=maxes.Axes)
                locator = divider.new_locator(nx=0, ny=0)
                self._colorbar_axes.set_axes_locator(locator)
                self.orientation='horizontal'
            else:
                raise Exception("location should be one of: right/top")

            self._figure.add_axes(self._colorbar_axes)

            self._colorbar = self._figure.colorbar(self.image, cax=self._colorbar_axes, orientation=self.orientation)

            if self.location=='right':
                for tick in self._colorbar_axes.yaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = False
                    tick.label2On = True
            if self.location=='top':
                for tick in self._colorbar_axes.xaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = False
                    tick.label2On = True
            if self.location=='left':
                for tick in self._colorbar_axes.yaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = True
                    tick.label2On = False
            if self.location=='bottom':
                for tick in self._colorbar_axes.xaxis.get_major_ticks():
                    tick.tick1On = True
                    tick.tick2On = True
                    tick.label1On = True
                    tick.label2On = False

        else:

            warnings.warn("No image is shown, therefore, no colorbar will be plotted")

        self.refresh()

    def update_colorbar(self):
        if self._colorbar_axes:
            self.show_colorbar()

    def hide_colorbar(self):
        self._figure.delaxes(self._colorbar_axes)
        self._colorbar_axes = None
