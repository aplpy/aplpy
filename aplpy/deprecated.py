import warnings

from decorators import auto_refresh

class Deprecated(object):

    @auto_refresh
    def show_grid(self, *args, **kwargs):
        warnings.warn("show_grid is deprecated - use add_grid instead", DeprecationWarning)
        self.add_grid(*args, **kwargs)

    @auto_refresh
    def hide_grid(self, *args, **kwargs):
        warnings.warn("hide_grid is deprecated - use remove_grid instead", DeprecationWarning)
        self.add_grid(*args, **kwargs)
        
    @auto_refresh
    def show_beam(self, *args, **kwargs):
        warnings.warn("show_beam is deprecated - use add_beam instead", DeprecationWarning)
        self.add_beam(*args, **kwargs)
        
    @auto_refresh
    def hide_beam(self, *args, **kwargs):
        warnings.warn("hide_beam is deprecated - use remove_beam instead", DeprecationWarning)
        self.add_beam(*args, **kwargs)
        
    @auto_refresh
    def show_scalebar(self, *args, **kwargs):
        warnings.warn("show_scalebar is deprecated - use add_scalebar instead", DeprecationWarning)
        self.add_scalebar(*args, **kwargs)
        
    @auto_refresh
    def hide_scalebar(self, *args, **kwargs):
        warnings.warn("hide_scalebar is deprecated - use remove_scalebar instead", DeprecationWarning)
        self.add_scalebar(*args, **kwargs)
        
    @auto_refresh
    def show_colorbar(self, *args, **kwargs):
        warnings.warn("show_colorbar is deprecated - use add_colorbar instead", DeprecationWarning)
        self.add_colorbar(*args, **kwargs)
        
    @auto_refresh
    def hide_colorbar(self, *args, **kwargs):
        warnings.warn("hide_colorbar is deprecated - use remove_colorbar instead", DeprecationWarning)
        self.add_colorbar(*args, **kwargs)

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
