import warnings

from mpl_toolkits.axes_grid import make_axes_locatable


class Colorbar(object):

    def _initialize_colorbar(self):
        self._colorbar_axes = None

    def show_colorbar(self, location='right', size="5%", pad=0.05):

        if self.image:

            if self._colorbar_axes:
                self._figure.delaxes(self._colorbar_axes)

            divider = make_axes_locatable(self._ax1)

            if location=='right':
                self._colorbar_axes = divider.new_horizontal(size=size, pad=pad)
                self.orientation='vertical'
                self._colorbar_axes.axis["left"].toggle(ticklabels=False, ticks=True)
                self._colorbar_axes.axis["right"].toggle(ticklabels=True, ticks=True)
            elif location=='top':
                self._colorbar_axes = divider.new_vertical(size=size, pad=pad)
                self.orientation='horizontal'
                self._colorbar_axes.axis["bottom"].toggle(ticklabels=False, ticks=True)
                self._colorbar_axes.axis["top"].toggle(ticklabels=True, ticks=True)
            elif location=='left':
                warnings.warn("Left colorbar not fully implemented")
                self._colorbar_axes = divider.new_horizontal(size=size, pad=pad, pack_start=True)
                locator = divider.new_locator(nx=0, ny=0)
                self._colorbar_axes.set_axes_locator(locator)
                self.orientation='vertical'
                self._colorbar_axes.axis["left"].toggle(ticklabels=True, ticks=True)
                self._colorbar_axes.axis["right"].toggle(ticklabels=False, ticks=True)
            elif location=='bottom':
                warnings.warn("Bottom colorbar not fully implemented")
                self._colorbar_axes = divider.new_vertical(size=size, pad=pad, pack_start=True)
                locator = divider.new_locator(nx=0, ny=0)
                self._colorbar_axes.set_axes_locator(locator)
                self.orientation='horizontal'
                self._colorbar_axes.axis["bottom"].toggle(ticklabels=True, ticks=True)
                self._colorbar_axes.axis["top"].toggle(ticklabels=False, ticks=True)
            else:
                raise Exception("Location should be one of: right/top")

            self._figure.add_axes(self._colorbar_axes)

            self._colorbar = self._figure.colorbar(self.image, cax=self._colorbar_axes, orientation=self.orientation)

        else:

            warnings.warn("No image is shown, therefore, no colorbar will be plotted")

        self.refresh()

    def hide_colorbar(self):

        self._figure.delaxes(self._colorbar_axes)
        self._colorbar_axes = None
