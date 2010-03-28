import warnings

from decorators import auto_refresh

class Deprecated(object):

    @auto_refresh
    def set_grid_alpha(self, *args, **kwargs):
        warnings.warn("set_grid_alpha is deprecated - use grid.set_alpha instead", DeprecationWarning)
        self.grid.set_alpha(*args, **kwargs)

    @auto_refresh
    def set_grid_color(self, *args, **kwargs):
        warnings.warn("set_grid_color is deprecated - use grid.set_color instead", DeprecationWarning)
        self.grid.set_color(*args, **kwargs)

    @auto_refresh
    def set_grid_xspacing(self, *args, **kwargs):
        warnings.warn("set_grid_xspacing is deprecated - use grid.set_xspacing instead", DeprecationWarning)
        self.grid.set_xspacing(*args, **kwargs)

    @auto_refresh
    def set_grid_yspacing(self, *args, **kwargs):
        warnings.warn("set_grid_yspacing is deprecated - use grid.set_yspacing instead", DeprecationWarning)
        self.grid.set_yspacing(*args, **kwargs)

    @auto_refresh
    def set_scalebar_properties(self, *args, **kwargs):
        warnings.warn("set_scalebar_properties is deprecated - use scalebar.set_properties instead", DeprecationWarning)
        self.scalebar.set_properties(*args, **kwargs)

    @auto_refresh
    def set_beam_properties(self, *args, **kwargs):
        warnings.warn("set_beam_properties is deprecated - use beam.set_properties instead", DeprecationWarning)
        self.beam.set_properties(*args, **kwargs)

    @auto_refresh
    def set_tick_labels_xformat(self, format):
        warnings.warn("set_tick_labels_xformat has been deprecated - use set_tick_labels_format() instead", DeprecationWarning)
        self.set_tick_labels_format(xformat=format)

    @auto_refresh
    def set_tick_labels_yformat(self, format):
        warnings.warn("set_tick_labels_yformat has been deprecated - use set_tick_labels_format() instead", DeprecationWarning)
        self.set_tick_labels_format(yformat=format)

    @auto_refresh
    def set_labels_latex(self, usetex):
        warnings.warn("set_labels_latex has been deprecated - use set_system_latex instead", DeprecationWarning)
        self.set_system_latex(usetex)

    @auto_refresh
    def set_tick_labels_size(self, size):
        warnings.warn("set_tick_labels_size has been deprecated - use set_tick_labels_font instead", DeprecationWarning)
        self.set_tick_labels_font(size=size)

    @auto_refresh
    def set_tick_labels_weight(self, weight):
        warnings.warn("set_tick_labels_weight has been deprecated - use set_tick_labels_weight instead", DeprecationWarning)
        self.set_tick_labels_font(weight=weight)

    @auto_refresh
    def set_tick_labels_family(self, family):
        warnings.warn("set_tick_labels_family has been deprecated - use set_tick_labels_family instead", DeprecationWarning)
        self.set_tick_labels_font(family=family)

    def set_axis_labels_xdisp(self, displacement):
        warnings.warn("set_axis_labels_xdisk has been deprecated - use the xpad= argument for set_axis_labels instead", DeprecationWarning)
        return

    def set_axis_labels_ydisp(self, displacement):
        warnings.warn("set_axis_labels_xdisp has been deprecated - use the ypad= argument for set_axis_labels() instead", DeprecationWarning)
        return

    def set_axis_labels_size(self, size):
        warnings.warn("set_axis_labels_size has been deprecated -use set_axis_labels_font instead", DeprecationWarning)
        self.set_axis_labels_font(size=size)

    def set_axis_labels_weight(self, weight):
        warnings.warn("set_axis_labels_weight has been deprecated - use set_axis_labels_font instead", DeprecationWarning)
        self.set_axis_labels_font(weight=weight)

    def set_axis_labels_family(self, family):
        warnings.warn("set_axis_labels_family has been deprecated - use set_axis_labels_font instead", DeprecationWarning)
        self.set_axis_labels_font(family=family)
