import matplotlib.pyplot as mpl
import wcs_util
import numpy as np
import string
import math_util
from matplotlib.font_manager import FontProperties

class Labels(object):
    
    def _initialize_labels(self):
        
        self._ax2.yaxis.set_label_position('right')
        self._ax2.xaxis.set_label_position('top')
        
        system,equinox,units = wcs_util.system(self._wcs)
        
        # Set default label format
        if system == 'celestial':
            self.set_labels_xformat("hh:mm:ss.ss")
            self.set_labels_yformat("dd:mm:ss.s")
        else:
            self.set_labels_xformat("ddd.dddd")
            self.set_labels_yformat("dd.dddd")
        
        if system == 'celestial':
            if equinox == 'b1950':
                self.set_axis_labels('RA (B1950)','Dec (B1950)', refresh=False)
            else:
                self.set_axis_labels('RA (J2000)','Dec (J2000)', refresh=False)
        elif system == 'galactic':
            self.set_axis_labels('Galactic Longitude','Galactic Latitude', refresh=False)
        else:
            self.set_axis_labels('Ecliptic Longitude','Ecliptic Latitude', refresh=False)
        
        # Set major tick formatters
        fx1 = WCSFormatter(wcs=self._wcs,axist='x')
        fy1 = WCSFormatter(wcs=self._wcs,axist='y')
        self._ax1.xaxis.set_major_formatter(fx1)
        self._ax1.yaxis.set_major_formatter(fy1)
        
        fx2 = mpl.NullFormatter()
        fy2 = mpl.NullFormatter()
        self._ax2.xaxis.set_major_formatter(fx2)
        self._ax2.yaxis.set_major_formatter(fy2)
        
        # Set font
        self.tick_font = FontProperties()
        self.axes_font = FontProperties()
        self._ax1.usetex = False
        self.set_tick_label_style('plain', refresh=False)
        self.set_tick_labels_size('small', refresh=False)
        
    def set_tick_labels_xformat(self,format,refresh=True):
        '''
        Set the format of the x-axis tick labels
        
        Required Arguments:
            
            *format*: [ string ]
                The format for the tick labels. This can be:
                    
                    * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
                    * ``hh`` or ``dd`` - hours (or degrees)
                    * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
                    * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
                    * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.
        
        Optional Keyword Arguments:
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        '''
        
        self._ax1.xaxis.apl_label_form = format
        if refresh: self.refresh()
    
    def set_tick_labels_yformat(self,format,refresh=True):
        '''
        Set the format of the x-axis tick labels
        
        Required Arguments:
            
            *format*: [ string ]
                The format for the tick labels. This can be:
                    
                    * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
                    * ``hh`` or ``dd`` - hours (or degrees)
                    * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
                    * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
                    * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.
        
        Optional Keyword Arguments:
            
            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        '''
        
        self._ax1.yaxis.apl_label_form = format
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
                the set_latex() method.
                
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        if not style in ['colons','plain','latex']:
            raise Exception("Label style should be one of colons/plain/latex")
        
        self._ax1.xaxis.apl_label_style = style
        self._ax1.yaxis.apl_label_style = style
    
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
        """
        Set the size of the tick labels
            
        Required Arguments:
        
            *size*: [ size in points | ‘xx-small’ | ‘x-small’ | ‘small’ |
                      ‘medium’ | ‘large’ | ‘x-large’ | ‘xx-large’ ]
                      
                The size of the numeric tick labels. Default is 'small'.
                                
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        self.tick_font.set_size(size)
        self._update_tick_font()

        if refresh:
            self.refresh()
            
    def set_tick_labels_weight(self, weight, refresh=True):
        """
        Set the weight of the tick labels
        
        Required Arguments:
        
            *weight*: [ a numeric value in range 0-1000 | ‘ultralight’ |
                        ‘light’ | ‘normal’ | ‘regular’ | ‘book’ | ‘medium’ |
                        ‘roman’ | ‘semibold’ | ‘demibold’ | ‘demi’ | ‘bold’ |
                        ‘heavy’ | ‘extra bold’ | ‘black’ ]
                      
                The weight of the numeric tick labels. Default is 'normal'.
                                
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """

        self.tick_font.set_weight(weight)
        self._update_tick_font()

        if refresh:
            self.refresh()
            
    def set_tick_labels_family(self, family, refresh=True):
        """
        Set the font family of the tick labels
        
        Required Arguments:
        
            *family*: [ ‘serif’ | ‘sans-serif’ | ‘cursive’ | ‘fantasy’ | ‘monospace’ ]
                      
                The font family of the numeric tick labels. Default is 'sans-serif'.
                                
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        self.tick_font.set_family(family)
        self._update_tick_font()

        if refresh:
            self.refresh()
            
    def _update_tick_font(self):
        
        for tick in self._ax1.get_xticklabels():
            tick.set_fontproperties(self.tick_font)
        for tick in self._ax1.get_yticklabels():
            tick.set_fontproperties(self.tick_font)
    
    def set_axis_labels(self,xlabel,ylabel, refresh=True):
        """
        Set the axes labels
            
        Required Arguments:
        
            *xlabel*: [ string ]
                The x-axis label.
                
            *ylabel*: [ string ]
                The y-axis label.
                                
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        self._ax1.set_xlabel(xlabel,fontdict=self.axes_font)
        self._ax1.set_ylabel(ylabel,fontdict=self.axes_font)
               
        if refresh:
            self.refresh()
                    
    def set_axis_labels_size(self, size, refresh=True):
        """
        Set the size of the axis labels
            
        Required Arguments:
        
            *size*: [ size in points | ‘xx-small’ | ‘x-small’ | ‘small’ |
                      ‘medium’ | ‘large’ | ‘x-large’ | ‘xx-large’ ]
                      
                The size of the axis labels. Default is 'small'.
                                
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        self.axes_font.set_size(size)
        self._update_axes_font()

        if refresh:
            self.refresh()

    def set_axis_labels_weight(self, weight, refresh=True):
        """
        Set the weight of the axis labels
        
        Required Arguments:
        
            *weight*: [ a numeric value in range 0-1000 | ‘ultralight’ |
                        ‘light’ | ‘normal’ | ‘regular’ | ‘book’ | ‘medium’ |
                        ‘roman’ | ‘semibold’ | ‘demibold’ | ‘demi’ | ‘bold’ |
                        ‘heavy’ | ‘extra bold’ | ‘black’ ]
                      
                The weight of the axis labels. Default is 'normal'.
                                
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """

        self.axes_font.set_weight(weight)
        self._update_axes_font()

        if refresh:
            self.refresh()

    def set_axis_labels_family(self, family, refresh=True):
        """
        Set the font family of the axis labels
        
        Required Arguments:
        
            *family*: [ ‘serif’ | ‘sans-serif’ | ‘cursive’ | ‘fantasy’ | ‘monospace’ ]
                      
                The font family of the axis labels. Default is 'sans-serif'.
                                
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.
        """
        
        self.axes_font.set_family(family)
        self._update_axes_font()

        if refresh:
            self.refresh()
            
    def _update_axes_font(self):

        xlabel = self._ax1.get_xlabel()
        ylabel = self._ax1.get_ylabel()

        self._ax1.set_xlabel(xlabel,fontproperties=self.axes_font)
        self._ax1.set_ylabel(ylabel,fontproperties=self.axes_font)

class WCSFormatter(mpl.Formatter):
    
    def __init__(self, wcs=False,axist='x'):
        self._wcs = wcs
        self.axist = axist
    
    def __call__(self,x,pos=None):
        'Return the format for tick val x at position pos; pos=None indicated unspecified'
        
        hours = 'h' in self.axis.apl_label_form
        
        if self.axis.apl_label_style == 'plain':
            sep = ('d','m','s')
            if hours: sep = ('h','m','s') 
        elif self.axis.apl_label_style == 'colons':
            sep = (':',':','')
        elif self.axis.apl_label_style == 'latex':
            if hours:
                sep = ('^{h}','^{m}','^{s}')
            else:
                sep = ('^{\circ}','^{\prime}','^{\prime\prime}')
        
        ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
        xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()
        
        ipos = math_util.minloc(np.abs(self.axis.apl_tick_positions_pix-x))
        
        c = self.axis.apl_tick_spacing * self.axis.apl_tick_positions_world[ipos]
        
        if hours:
            c = c.tohours()
        
        c = c.tostringlist(format=self.axis.apl_label_form,sep=sep)
        
        if ipos <> len(self.axis.apl_tick_positions_pix)-1:
            cnext = self.axis.apl_tick_spacing * self.axis.apl_tick_positions_world[ipos+1]
            if hours:
                cnext = cnext.tohours()
            cnext = cnext.tostringlist(format=self.axis.apl_label_form,sep=sep)
            for iter in range(len(c)):
                if cnext[0] == c[0]:
                    c.pop(0)
                    cnext.pop(0)
                else:
                    break
        
        if self.axis.apl_label_style == 'latex':
            return "$"+string.join(c,"")+"$"
        else:
            return string.join(c,"")
