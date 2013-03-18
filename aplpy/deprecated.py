from __future__ import absolute_import, print_function, division

import warnings

from .decorators import auto_refresh


class Deprecated(object):

    @auto_refresh
    def set_tick_xspacing(self, *args, **kwargs):
        warnings.warn("set_tick_xspacing is deprecated - use ticks.set_xspacing instead", DeprecationWarning)
        self.ticks.set_xspacing(*args, **kwargs)

    @auto_refresh
    def set_tick_yspacing(self, *args, **kwargs):
        warnings.warn("set_tick_yspacing is deprecated - use ticks.set_yspacing instead", DeprecationWarning)
        self.ticks.set_yspacing(*args, **kwargs)

    @auto_refresh
    def set_tick_size(self, *args, **kwargs):
        warnings.warn("set_tick_size is deprecated - use ticks.set_length instead", DeprecationWarning)
        self.ticks.set_length(*args, **kwargs)

    @auto_refresh
    def set_tick_color(self, *args, **kwargs):
        warnings.warn("set_tick_color is deprecated - use ticks.set_color instead", DeprecationWarning)
        self.ticks.set_color(*args, **kwargs)

    @auto_refresh
    def show_grid(self, *args, **kwargs):
        warnings.warn("show_grid is deprecated - use add_grid instead", DeprecationWarning)
        self.add_grid(*args, **kwargs)

    @auto_refresh
    def hide_grid(self, *args, **kwargs):
        warnings.warn("hide_grid is deprecated - use remove_grid instead", DeprecationWarning)
        self.remove_grid(*args, **kwargs)

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
        warnings.warn("set_scalebar_properties is deprecated - use scalebar.set instead", DeprecationWarning)
        self.scalebar._set_scalebar_properties(*args, **kwargs)

    @auto_refresh
    def set_label_properties(self, *args, **kwargs):
        warnings.warn("set_label_properties is deprecated - use scalebar.set instead", DeprecationWarning)
        self.scalebar._set_label_properties(*args, **kwargs)

    @auto_refresh
    def set_beam_properties(self, *args, **kwargs):
        warnings.warn("set_beam_properties is deprecated - use beam.set instead", DeprecationWarning)
        self.beam.set(*args, **kwargs)

    @auto_refresh
    def set_labels_latex(self, usetex):
        warnings.warn("set_labels_latex has been deprecated - use set_system_latex instead", DeprecationWarning)
        self.set_system_latex(usetex)

    # TICK LABELS

    @auto_refresh
    def set_tick_labels_format(self, xformat=None, yformat=None):
        warnings.warn("set_tick_labels_format has been deprecated - use tick_labels.set_xformat() and tick_labels.set_yformat instead", DeprecationWarning)
        if xformat:
            self.tick_labels.set_xformat(xformat)
        if yformat:
            self.tick_labels.set_yformat(yformat)

    @auto_refresh
    def set_tick_labels_xformat(self, format):
        warnings.warn("set_tick_labels_xformat has been deprecated - use tick_labels.set_xformat() instead", DeprecationWarning)
        self.tick_labels.set_xformat(format)

    @auto_refresh
    def set_tick_labels_yformat(self, format):
        warnings.warn("set_tick_labels_yformat has been deprecated - use tick_labels.set_yformat() instead", DeprecationWarning)
        self.tick_labels.set_yformat(format)

    @auto_refresh
    def set_tick_labels_style(self, style):
        warnings.warn("set_tick_labels_style has been deprecated - use tick_labels.set_style instead", DeprecationWarning)
        self.tick_labels.set_style(style)

    @auto_refresh
    def set_tick_labels_size(self, size):
        warnings.warn("set_tick_labels_size has been deprecated - use tick_labels.set_font instead", DeprecationWarning)
        self.tick_labels.set_font(size=size)

    @auto_refresh
    def set_tick_labels_weight(self, weight):
        warnings.warn("set_tick_labels_weight has been deprecated - use tick_labels.set_font instead", DeprecationWarning)
        self.tick_labels.set_font(weight=weight)

    @auto_refresh
    def set_tick_labels_family(self, family):
        warnings.warn("set_tick_labels_family has been deprecated - use tick_labels.set_font instead", DeprecationWarning)
        self.tick_labels.set_font(family=family)

    @auto_refresh
    def set_tick_labels_font(self, *args, **kwargs):
        warnings.warn("set_tick_labels_font has been deprecated - use tick_labels.set_font instead", DeprecationWarning)
        self.tick_labels.set_font(*args, **kwargs)

    @auto_refresh
    def show_tick_labels(self):
        warnings.warn("show_tick_labels has been deprecated - use tick_labels.show instead", DeprecationWarning)
        self.tick_labels.show()

    @auto_refresh
    def hide_tick_labels(self):
        warnings.warn("hide_tick_labels has been deprecated - use tick_labels.hide instead", DeprecationWarning)
        self.tick_labels.hide()

    @auto_refresh
    def show_xtick_labels(self):
        warnings.warn("show_xtick_labels has been deprecated - use tick_labels.show_x instead", DeprecationWarning)
        self.tick_labels.show_x()

    @auto_refresh
    def hide_xtick_labels(self):
        warnings.warn("hide_xtick_labels has been deprecated - use tick_labels.hide_x instead", DeprecationWarning)
        self.tick_labels.hide_x()

    @auto_refresh
    def show_ytick_labels(self):
        warnings.warn("show_ytick_labels has been deprecated - use tick_labels.show_y instead", DeprecationWarning)
        self.tick_labels.show_y()

    @auto_refresh
    def hide_ytick_labels(self):
        warnings.warn("hide_ytick_labels has been deprecated - use tick_labels.hide_y instead", DeprecationWarning)
        self.tick_labels.hide_y()

    # AXIS LABELS

    @auto_refresh
    def set_axis_labels(self, xlabel='default', ylabel='default', xpad='default', ypad='default'):
        warnings.warn("set_axis_labels has been deprecated - use axis_labels.set_xtext, axis_labels.set_ytext, axis_labels.set_xpad, and axis_labels.set_ypad instead", DeprecationWarning)
        if xlabel != 'default':
            self.axis_labels.set_xtext(xlabel)
        if xpad != 'default':
            self.axis_labels.set_xpad(xpad)
        if ylabel != 'default':
            self.axis_labels.set_ytext(ylabel)
        if ypad != 'default':
            self.axis_labels.set_ypad(ypad)

    @auto_refresh
    def set_axis_labels_xdisp(self, xpad):
        warnings.warn("set_axis_labels_xdisk has been deprecated - use axis_labels.set_xpad instead", DeprecationWarning)
        self.axis_labels.set_xpad(xpad)

    @auto_refresh
    def set_axis_labels_ydisp(self, ypad):
        warnings.warn("set_axis_labels_xdisp has been deprecated - use axis_labels.set_ypad instead", DeprecationWarning)
        self.axis_labels.set_ypad(ypad)

    @auto_refresh
    def set_axis_labels_size(self, size):
        warnings.warn("set_axis_labels_size has been deprecated - use axis_labels.set_font instead", DeprecationWarning)
        self.axis_labels.set_font(size=size)

    @auto_refresh
    def set_axis_labels_weight(self, weight):
        warnings.warn("set_axis_labels_weight has been deprecated - use axis_labels.set_font instead", DeprecationWarning)
        self.axis_labels.set_font(weight=weight)

    @auto_refresh
    def set_axis_labels_family(self, family):
        warnings.warn("set_axis_labels_family has been deprecated - use axis_labels.set_font instead", DeprecationWarning)
        self.axis_labels.set_font(family=family)

    @auto_refresh
    def set_axis_labels_font(self, *args, **kwargs):
        warnings.warn("set_axis_labels_font has been deprecated - use axis_labels.set_font instead", DeprecationWarning)
        self.axis_labels.set_font(*args, **kwargs)

    @auto_refresh
    def show_axis_labels(self):
        warnings.warn("show_axis_labels has been deprecated - use axis_labels.show instead", DeprecationWarning)
        self.axis_labels.show()

    @auto_refresh
    def hide_axis_labels(self):
        warnings.warn("hide_axis_labels has been deprecated - use axis_labels.hide instead", DeprecationWarning)
        self.axis_labels.hide()

    @auto_refresh
    def show_xaxis_label(self):
        warnings.warn("show_xaxis_label has been deprecated - use axis_labels.show_x instead", DeprecationWarning)
        self.axis_labels.show_x()

    @auto_refresh
    def hide_xaxis_label(self):
        warnings.warn("hide_xaxis_label has been deprecated - use axis_labels.hide_x instead", DeprecationWarning)
        self.axis_labels.hide_x()

    @auto_refresh
    def show_yaxis_label(self):
        warnings.warn("show_yaxis_label has been deprecated - use axis_labels.show_y instead", DeprecationWarning)
        self.axis_labels.show_y()

    @auto_refresh
    def hide_yaxis_label(self):
        warnings.warn("hide_yaxis_label has been deprecated - use axis_labels.hide_y instead", DeprecationWarning)
        self.axis_labels.hide_y()

    # FRAME

    @auto_refresh
    def set_frame_color(self, *args, **kwargs):
        warnings.warn("set_frame_color has been deprecated - use frame.set_color instead", DeprecationWarning)
        self.frame.set_color(*args, **kwargs)

    @auto_refresh
    def set_frame_linewidth(self, *args, **kwargs):
        warnings.warn("set_frame_linewidth has been deprecated - use frame.set_linewidth instead", DeprecationWarning)
        self.frame.set_linewidth(*args, **kwargs)
