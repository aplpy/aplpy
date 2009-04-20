import matplotlib.pyplot as mpl
import math

import wcs_util

class Labels(object):
    
    def _initialize_labels(self):
        
        self._ax2.yaxis.set_label_position('right')
        self._ax2.xaxis.set_label_position('top')
        
        system,equinox,units = wcs_util.system(self._wcs)
        
        # Set default label format
        if system == 'celestial':
            self._ax1.xaxis.apl_label_form = "hh:mm:ss."
            self._ax1.yaxis.apl_label_form = "dd:mm:ss."
        else:
            self._ax1.xaxis.apl_label_form = "ddd.dddd"
            self._ax1.yaxis.apl_label_form = "dd.dddd"
        
        if system == 'celestial':
            if equinox == 'b1950':
                self._ax1.set_xlabel('RA (B1950)')
                self._ax1.set_ylabel('Dec (B1950)')
            else:
                self._ax1.set_xlabel('RA (J2000)')
                self._ax1.set_ylabel('Dec (J2000)')
        elif system == 'galactic':
            self._ax1.set_xlabel('Galactic Longitude')
            self._ax1.set_ylabel('Galactic Latitude')
        else:
            self._ax1.set_xlabel('Ecliptic Longitude')
            self._ax1.set_ylabel('Ecliptic Latitude')
        
        # Set major tick formatters
        fx1 = WCSFormatter(wcs=self._wcs,axist='x')
        fy1 = WCSFormatter(wcs=self._wcs,axist='y')
        self._ax1.xaxis.set_major_formatter(fx1)
        self._ax1.yaxis.set_major_formatter(fy1)
        
        fx2 = mpl.NullFormatter()
        fy2 = mpl.NullFormatter()
        self._ax2.xaxis.set_major_formatter(fx2)
        self._ax2.yaxis.set_major_formatter(fy2)
    
    def set_xlabels_format(self,format,refresh=True):
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
    
    def set_ylabels_format(self,format,refresh=True):
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
    
    def set_axis_labels(self,refresh=True,family='serif',fontsize='12',fontstyle='normal'):
        """
        family                [ 'serif' | 'sans-serif' | 'cursive' | 'fantasy' | 'monospace' ]
          size or fontsize    [ size in points | relative size eg 'smaller', 'x-large' ]
          style or fontstyle    [ 'normal' | 'italic' | 'oblique']
        """
        self._ax1.set_xlabel('(R.A. J2000)',family=family,fontsize=fontsize,fontstyle=fontstyle)
        self._ax1.set_ylabel('(Dec. J2000)',family=family,fontsize=fontsize,fontstyle=fontstyle)
        
        if refresh: self.refresh()


class WCSFormatter(mpl.Formatter):
    
    def __init__(self, wcs=False,axist='x'):
        self._wcs = wcs
        self.axist = axist
    
    def __call__(self,x,pos=None):
        'Return the format for tick val x at position pos; pos=None indicated unspecified'
        
        ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
        xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()
        
        if self.axist=='x':
            y = ymin
            x = x
        else:
            y = x
            x = xmin
        
        xw,yw = wcs_util.pix2world(self._wcs,x,y)
        
        if self.axist=='x':
            return "$"+_lon2dms(xw,form=self.axis.apl_label_form)+"$"
        else:
            return "$"+_lat2dms(yw,form=self.axis.apl_label_form)+"$"

def _lat2dms(x,form='dd:mm:ss.ss'):
    
    if x < 0:
        return '-' + _lon2dms(abs(x),form)
    else:
        return '+' + _lon2dms(abs(x),form)

def _lon2dms(x,form='ddd:mm:ss.ss'):
    
    if "hh" in form:
        sep = ["^h","^m","^s"]
#        sep = ["h","m","s"]
        x = x / 15.
    else:
        sep = ["^{\circ}","^{\prime}","^{\prime\prime}"]
#        sep = ["d","'",'"']
    
    # count number of decimal arcseconds or of decimal places to degrees
    if '.s' in form or '.d' in form:
        pos = form.find('.')
        ns = len(form[pos+1:])
        fns = ".%0"+str(ns)+"d"
    
    # If there are decimal places to degrees, conversion is simple
    if '.d' in form:
        
        fd,d = math.modf(x)
        
        part1 = int(d)
        part2 = int(round(fd*10**ns))
        if part2 == 10**ns: part1,part2 = part1+1,0
        
        string = ("%d"+fns) % (part1,part2) + sep[0]
        return string
    
    else:
        
        # use this for dms, hms, and -dms
        
        m,d = math.modf(x)
        s,m = math.modf(m*60.)
        fs,s = math.modf(s*60.)
        
        parts = []
        
        if 'mm' in form:
            parts.append(int(d))
            if 'ss' in form:
                parts.append(int(m))
                if '.s' in form:
                    parts.append(int(s))
                    parts.append(int(round(fs*10**ns)))
                else:
                    parts.append(int(round(s+fs)))
            else:
                parts.append(int(round(m+(s+fs)/60.)))
        else:
            parts.append(int(round(x)))
        
        if len(parts) >= 4 and parts[3] == 10**(ns+2): parts[2],parts[3] = parts[2] + 1, 0
        if len(parts) >= 3 and  parts[2] == 60: parts[1],parts[2] = parts[1] + 1, 0
        if len(parts) >= 2 and  parts[1] == 60: parts[0],parts[1] = parts[0] + 1, 0
        
        if 'hh' in form:
            if parts[0] == 24: parts[0] = 0
        else:
            if parts[0] == 360: parts[0] = 0
        
        string = ""
        
        if len(parts) > 0:
            string = "%d" % parts[0] + sep[0]
            if len(parts) > 1:
                string += "%02d" % parts[1] + sep[1]
                if len(parts) > 2:
                    string += "%02d" % parts[2]
                    if len(parts) > 3:
                        string += fns % parts[3] + sep[2]
                    else:
                        string += sep[2]
        
        return string