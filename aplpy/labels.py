import matplotlib.pyplot as mpl
import wcs_util
import numpy as np
import string
import math_util
from matplotlib.font_manager import FontProperties

class Labels(object):
    
    def _initialize_labels(self):
        
        # Set font
        self.tick_font = FontProperties()
        self.axes_font = FontProperties()
        
        self.set_tick_labels_style('plain', refresh=False)
        
        self._ax2.yaxis.set_label_position('right')
        self._ax2.xaxis.set_label_position('top')
        
        self.xlabel = None
        self.ylabel = None
        
        system,equinox,units = wcs_util.system(self._wcs)
        
        # Set default label format
        if system == 'celestial':
            self.set_tick_labels_format(xformat="hh:mm:ss.ss", yformat="dd:mm:ss.s", refresh=False)
        else:
            self.set_tick_labels_format(xformat="ddd.dddd", yformat="dd.dddd", refresh=False)
        
        if system == 'celestial':
            if equinox == 'b1950':
                self.xlabel_default = 'RA (B1950)'
                self.ylabel_default = 'Dec (B1950)'
            else:
                self.xlabel_default = 'RA (J2000)'
                self.ylabel_default = 'Dec (J2000)'
        elif system == 'galactic':
            self.xlabel_default = 'Galactic Longitude'
            self.ylabel_default = 'Galactic Latitude'
        else:
            self.xlabel_default = 'Ecliptic Longitude'
            self.ylabel_default = 'Ecliptic Latitude'
        
        self.set_axis_labels()
        
        # Set major tick formatters
        fx1 = WCSFormatter(wcs=self._wcs,coord='x')
        fy1 = WCSFormatter(wcs=self._wcs,coord='y')
        self._ax1.xaxis.set_major_formatter(fx1)
        self._ax1.yaxis.set_major_formatter(fy1)
        
        fx2 = mpl.NullFormatter()
        fy2 = mpl.NullFormatter()
        self._ax2.xaxis.set_major_formatter(fx2)
        self._ax2.yaxis.set_major_formatter(fy2)
    
    def set_tick_labels_xformat(self,format,refresh=True):
        print "This method has been depracated. Please use the set_tick_labels_format() instead"
        return
    
    def set_tick_labels_yformat(self,format,refresh=True):
        print "This method has been depracated. Please use the set_tick_labels_format() instead"
        return
    
    def set_tick_labels_format(self,xformat=None,yformat=None,refresh=True):
        '''
        Set the format of the tick labels
        
        Optional Keyword Arguments:
            
            *xformat*: [ string ]
            
            *yformat*: [ string ]

                The x and y formats for the tick labels. These can be:
                    
                    * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
                    * ``hh`` or ``dd`` - hours (or degrees)
                    * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
                    * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
                    * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.
                
                If one of these arguments is not specified, the format for that axis
                is left unchanged.
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        '''
        
        if xformat: self._ax1.xaxis.apl_label_form = xformat
        if yformat: self._ax1.yaxis.apl_label_form = yformat
        if refresh: self.refresh()
    
    def set_tick_labels_style(self,style,refresh=True):
        """
        Set the format of the x-axis tick labels
        
        Required Arguments:
            
            *style*: [ 'colons' | 'plain' | 'latex' ]
                
                How to style the tick labels:
                
                'colons' uses colons as separators, for example
                31:41:59.26 +27:18:28.1
                
                'plain' uses plain letters as separators, for example
                31:41:59.26 +27:18:28.1
                
                'latex' uses superscripts, and typesets the labels
                with LaTeX. To decide whether to use the matplotlib
                internal LaTeX engine or a real LaTeX installation, use
                the set_labels_latex() method.
        
        Optional Keyword Arguments:
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        if not style in ['colons','plain','latex']:
            raise Exception("Label style should be one of colons/plain/latex")
        
        self._ax1.xaxis.apl_labels_style = style
        self._ax1.yaxis.apl_labels_style = style
        
        if refresh:
            self.refresh()
    
    def set_labels_latex(self, usetex, refresh=True):
        """
        Set whether to use a real LaTeX installation or the built-in matplotlib LaTeX
        
        Required Arguments:
            
            *usetex*: [ True | False ]
                Whether to use a real LaTex installation (True) or the built-in
                matplotlib LaTeX (False). Note that if the former is chosen, an
                installation of LaTex is required.
        
        Optional Keyword Arguments:
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        mpl.rc('text',usetex=usetex)
        
        if refresh:
            self.refresh()
    
    def set_tick_labels_size(self, size, refresh=True):
        print "This method has been depracated. Please use the set_tick_labels_font() instead"
        return
    
    def set_tick_labels_weight(self, weight, refresh=True):
        print "This method has been depracated. Please use the set_tick_labels_font() instead"
        return
    
    def set_tick_labels_family(self, family, refresh=True):
        print "This method has been depracated. Please use the set_tick_labels_font() instead"
        return
    
    def set_tick_labels_font(self,size=None,weight=None,family=None,refresh=True):
        """
        Set the size of the tick labels
        
        Optional Keyword Arguments:
            
            Default values for size/weight/family are set by matplotlib
            or previously set values if set_tick_labels_font has
            already been called. Global default values can be set by
            editing the matplotlibrc file.
            
            *size*: [ size in points | xx-small | x-small | small |
                      medium | large | x-large | xx-large ]
                
                The size of the numeric tick labels.
            
            *weight*: [ a numeric value in range 0-1000 | ultralight |
                      light | normal | regular | book | medium |
                      roman | semibold | demibold | demi | bold |
                      heavy | extra bold | black ]
                
                The weight of the numeric tick labels.
            
            *family*: [ serif | sans-serif | cursive | fantasy | monospace ]
                
                The font family of the numeric tick labels.
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        if size: self.tick_font.set_size(size)
        if weight: self.tick_font.set_weight(weight)
        if family: self.tick_font.set_family(family)
        
        self._update_tick_font()
        
        if refresh:
            self.refresh()
    
    def show_tick_labels(self,refresh=True):
        """
        Show the tick labels
        
        Optional Keyword Arguments:
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        for tick in self._ax1.get_xticklabels():
            tick.set_visible(True)
        for tick in self._ax1.get_yticklabels():
            tick.set_visible(True)
        
        if refresh: self.refresh()
    
    def hide_tick_labels(self,refresh=True):
        """
        Hide the tick labels
        
        Optional Keyword Arguments:
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        for tick in self._ax1.get_xticklabels():
            tick.set_visible(False)
        for tick in self._ax1.get_yticklabels():
            tick.set_visible(False)
        
        if refresh: self.refresh()
    
    def _update_tick_font(self):
        
        for tick in self._ax1.get_xticklabels():
            tick.set_fontproperties(self.tick_font)
        for tick in self._ax1.get_yticklabels():
            tick.set_fontproperties(self.tick_font)
    
    def set_axis_labels_xdisp(self,displacement,refresh=True):
        print "This method has been depracated. Please use the xpad= argument for set_axis_labels() instead"
        return
    
    def set_axis_labels_ydisp(self,displacement,refresh=True):
        print "This method has been depracated. Please use the ypad= argument for set_axis_labels() instead"
        return
    
    def set_axis_labels(self,xlabel='default',ylabel='default',xpad=0,ypad=0,refresh=True):
        """
        Set the axes labels
        
        Optional Keyword Arguments:
            
            *xlabel*: [ string ]
                The x-axis label. The default is chosen based on the WCS coordinate system.
            
            *ylabel*: [ string ]
                The y-axis label. The default is chosen based on the WCS coordinate system.
            
            *xpad*: [ integer ]
                Correction to the x label vertical position relative to default position, in points
            
            *ypad*: [ integer ]
                Correction to the y label horizontal position relative to default position, in points
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        if xlabel == 'default':
            xlabel = self.xlabel_default
        
        if xpad <> 0:
            try:
                self.xlabel = self._ax1.set_xlabel(xlabel,labelpad=xpad)
            except:
                print "WARNING: the version of matplotlib you are using does not support the labelpad= argument for set_xlabel. Ignoring the xpad= argument"
                self.xlabel = self._ax1.set_xlabel(xlabel)
        else:
            self.xlabel = self._ax1.set_xlabel(xlabel)
        
        if ylabel == 'default':
            ylabel = self.ylabel_default
        
        if ypad <> 0:
            try:
                self.ylabel = self._ax1.set_ylabel(ylabel,labelpad=ypad)
            except:
                print "WARNING: the version of matplotlib you are using does not support the labelpad= argument for set_ylabel. Ignoring the ypad= argument"
                self.ylabel = self._ax1.set_ylabel(ylabel)
        else:
            self.ylabel = self._ax1.set_ylabel(ylabel)
        
        if refresh:
            self.refresh()
    
    def set_axis_labels_size(self, size, refresh=True):
        print "This method has been depracated. Please use the set_axis_labels_font() instead"
        return
    
    def set_axis_labels_weight(self, weight, refresh=True):
        print "This method has been depracated. Please use the set_axis_labels_font() instead"
        return
    
    def set_axis_labels_family(self, family, refresh=True):
        print "This method has been depracated. Please use the set_axis_labels_font() instead"
        return
    
    def set_axis_labels_font(self,size=None,weight=None,family=None,refresh=True):
        """
        Set the size of the axis labels
        
        Default values for size/weight/family are set by matplotlib
        or previously set values if set_axis_labels_font has
        already been called. Global default values can be set by
        editing the matplotlibrc file.
        
        Optional Keyword Arguments:
            
            *size*: [ size in points | xx-small | x-small | small |
                      medium | large | x-large | xx-large ]
                
                The size of the axis labels
            
            *weight*: [ a numeric value in range 0-1000 | ultralight |
                      light | normal | regular | book | medium |
                      roman | semibold | demibold | demi | bold |
                      heavy | extra bold | black ]
                
                The weight of the axis labels
            
            *family*: [ serif | sans-serif | cursive | fantasy | monospace ]
                
                The font family of the axis labels.
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        if size: self.axes_font.set_size(size)
        if weight: self.axes_font.set_weight(weight)
        if family: self.axes_font.set_family(family)
        
        self._update_axes_font()
        
        if refresh:
            self.refresh()
    
    def show_axis_labels(self,refresh=True):
        """
        Show the axis labels
        
        Optional Keyword Arguments:
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        if self.xlabel:
            self.xlabel.set_visible(True)
        if self.ylabel:
            self.ylabel.set_visible(True)
        
        if refresh: self.refresh()
    
    def hide_axis_labels(self,refresh=True):
        """
        Hide the axis labels
        
        Optional Keyword Arguments:
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        if self.xlabel:
            self.xlabel.set_visible(False)
        if self.ylabel:
            self.ylabel.set_visible(False)
        
        if refresh: self.refresh()
    
    def _update_axes_font(self):
        
        self.xlabel.set_fontproperties(self.axes_font)
        self.ylabel.set_fontproperties(self.axes_font)

class WCSFormatter(mpl.Formatter):
    
    def __init__(self, wcs=False,coord='x'):
        self._wcs = wcs
        self.coord = coord
    
    def __call__(self,x,pos=None):
        'Return the format for tick val x at position pos; pos=None indicated unspecified'
        
        hours = 'h' in self.axis.apl_label_form
        
        if self.axis.apl_labels_style == 'plain':
            sep = ('d','m','s')
            if hours: sep = ('h','m','s')
        elif self.axis.apl_labels_style == 'colons':
            sep = (':',':','')
        elif self.axis.apl_labels_style == 'latex':
            if hours:
                sep = ('^{h}','^{m}','^{s}')
            else:
                sep = ('^{\circ}','^{\prime}','^{\prime\prime}')
        
        ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
        xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()
        
        ipos = math_util.minloc(np.abs(self.axis.apl_tick_positions_pix-x))
        
        label = self.axis.apl_tick_spacing * self.axis.apl_tick_positions_world[ipos]
        if hours: label = label.tohours()
        label = label.tostringlist(format=self.axis.apl_label_form,sep=sep)
        
        if self.coord == x or self.axis.apl_tick_positions_world[ipos] > 0:
            comp_ipos = ipos - 1
        else:
            comp_ipos = ipos + 1
        
        if comp_ipos >= 0 and comp_ipos <= len(self.axis.apl_tick_positions_pix)-1:
            
            comp_label = self.axis.apl_tick_spacing * self.axis.apl_tick_positions_world[comp_ipos]
            if hours: comp_label = comp_label.tohours()
            comp_label = comp_label.tostringlist(format=self.axis.apl_label_form,sep=sep)
            
            for iter in range(len(label)):
                if comp_label[0] == label[0]:
                    label.pop(0)
                    comp_label.pop(0)
                else:
                    break
        
        if self.axis.apl_labels_style == 'latex':
            return "$"+string.join(label,"")+"$"
        else:
            return string.join(label,"")
