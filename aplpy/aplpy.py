from distutils import version
import os

try:
    import matplotlib
    import matplotlib.pyplot as mpl
except ImportError:
    raise Exception("matplotlib is required for APLpy")

if version.LooseVersion(matplotlib.__version__) < version.LooseVersion('0.98.5.2'):
    raise Exception("matplotlib >= 0.98.5.2 is required for APLpy")

try:
    import pyfits
except ImportError:
    raise Exception("pyfits is required for APLpy")

try:
    import pywcs
except ImportError:
    raise Exception("pywcs is required for APLpy")

import contour_util

import montage
import image_util
import header

from layers import Layers
from grid import Grid
from ticks import Ticks
from labels import Labels


class FITSFigure(Layers,Grid,Ticks,Labels):
    
    "A class for plotting FITS files."
    
    def __init__(self,filename,hdu=0,downsample=False,north=False,**kwargs):
        
        # Open the figure
        self._figure = mpl.figure(**kwargs)
        
        # Read in FITS file
        try:
            self._hdu = pyfits.open(filename)[hdu]
        except:
            raise Exception("An error occured while reading the FITS file")
        
        # Reproject to face north if requested
        if north:
            self._hdu = montage.reproject_north(self._hdu)
        
        # Check header
        self._hdu.header = header.check(self._hdu.header)
        
        # Parse WCS info
        try:
            self._wcs = pywcs.WCS(self._hdu.header)
        except:
            raise Exception("An error occured while parsing the WCS information")
        
        # Downsample if requested
        if downsample:
            naxis1_new = self._wcs.naxis1 - np.mod(wcs.naxis1,downsample)
            naxis2_new = self._wcs.naxis2 - np.mod(wcs.naxis2,downsample)
            self._hdu.data = self._hdu.data[0:naxis2_new,0:naxis1_new]
            self._hdu.data = resample(self._hdu.data,downsample)
            self._wcs.naxis1,self._wcs.naxis2 = naxis1_new,naxis2_new
        
        # Create the two set of axes
        self._ax1 = self._figure.add_subplot(111)
        self._ax2 = self._ax1.figure.add_axes(self._ax1.get_position(True),frameon=False,aspect='equal')
        
        # Turn off autoscaling
        self._ax1.set_autoscale_on(False)
        self._ax2.set_autoscale_on(False)
        
        # Store WCS in axes
        self._ax1.apl_wcs = self._wcs
        self._ax2.apl_wcs = self._wcs
        
        # Set view to whole FITS file
        self._initialize_view()
        
        # Initialize ticks
        self._initialize_ticks()
        
        # Initialize grid
        self._initialize_grid()
        
        # Initialize labels
        self._initialize_labels()
        
        # Initialize layers list
        self._initialize_layers()
        
        # Find generating function for vmin/vmax
        self._auto_v = image_util.percentile_function(self._hdu.data)
        
        # Set image holder to be empty
        self.image = None
        
        # Set default theme
        self.set_theme(theme='pretty',refresh=False)
    
    def show_grayscale(self,invert='default',**kwargs):
        
        if invert=='default':
            invert = self._get_invert_default()
        
        if invert:
            cmap = 'gist_yarg'
        else:
            cmap = 'gray'
        
        self.show_colorscale(cmap=cmap,**kwargs)
    
    def show_colorscale(self,stretch='linear',exponent=2,vmin='default',vmax='default',cmap='default',interpolation='nearest',labels='auto',smooth=False):
        
        if cmap=='default':
            cmap = self._get_colormap_default()
        
        # The set of available functions
        cmap = mpl.cm.get_cmap(cmap,1000)
        stretched_image = image_util.stretch(self._hdu.data,function=stretch,exponent=exponent)
        
        vmin_auto = image_util.stretch(self._auto_v(0.0025),function=stretch,exponent=exponent)
        vmax_auto = image_util.stretch(self._auto_v(0.9975),function=stretch,exponent=exponent)
        
        vmin_auto,vmax_auto = vmin_auto-(vmax_auto-vmin_auto)/10.,vmax_auto+(vmax_auto-vmin_auto)/10.
        
        if type(vmin) is str:
            vmin=vmin_auto
        
        if type(vmax) is str:
            vmax=vmax_auto
        
        if self.image:
            self.image.set_data(stretched_image)
            self.image.set_clim(vmin=vmin,vmax=vmax)
            self.image.set_cmap(cmap=cmap)
        else:
            self.image = self._ax1.imshow(stretched_image,cmap=cmap,vmin=vmin,vmax=vmax,interpolation=interpolation,origin='lower',extent=self._extent)
        
        self.refresh()
    
    def show_rgb(self,filename):
        pretty_image = flipud(imread(filename))
        self._ax1.imshow(pretty_image,extent=self._extent)
        self.refresh()
    
    def show_contour(self,contour_file,layer=None,levels=5,filled=False, **kwargs):
        '''
        Overlay contours on the current plot
        
        Required Arguments:
        
            *contour_file*:
              The filename of the FITS file to plot the contours of
              
        Optional Arguments:
        
            *layer*:
              The name of the contour layer. This is useful for giving
              custom names to layers (instead of contour_set_n) and for
              replacing existing layers.
              
            *levels*:
              This can either be the number of contour levels to compute
              (if an integer is provided) or the actual list of contours
              to show (if a list of floats is provided) 
              
            *filled*
              Whether to show filled or line contours
                
        '''
        if layer:
            self.remove_layer(layer,raise_exception=False)
        
        if kwargs.has_key('cmap'):
            kwargs['cmap'] = mpl.cm.get_cmap(kwargs['cmap'],1000)
        elif not kwargs.has_key('colors'):
            kwargs['cmap'] = mpl.cm.get_cmap('jet',1000)
        
        hdu_contour = pyfits.open(contour_file)[0]
        hdu_contour.header  = header.check(hdu_contour.header)
        wcs_contour = pywcs.WCS(hdu_contour.header)
        image_contour = hdu_contour.data
        extent_contour = (0.5,wcs_contour.naxis1+0.5,0.5,wcs_contour.naxis2+0.5)
        
        self._name_empty_layers('user')
        
        if filled:
            self._ax1.contourf(image_contour,levels,extent=extent_contour,**kwargs)
        else:
            self._ax1.contour(image_contour,levels,extent=extent_contour,**kwargs)
        
        self._ax1 = contour_util.transform(self._ax1,wcs_contour,self._wcs)
        
        if layer:
            contour_set_name = layer
        else:
            self._contour_counter += 1
            contour_set_name = 'contour_set_'+str(self._contour_counter)
        
        self._name_empty_layers(contour_set_name)
        
        self.refresh()
    
    # This method plots markers. The input should be an Nx2 array with WCS coordinates
    # in degree format.
    
    def show_markers(self,xw,yw,layer=False,**kwargs):
        
        if not kwargs.has_key('c'):
            kwargs.setdefault('edgecolor','red')
            kwargs.setdefault('facecolor','none')
        
        kwargs.setdefault('s',30)
        
        if layer:
            self.remove_layer(layer,raise_exception=False)
        
        self._name_empty_layers('user')
        
        xp,yp = wcs_util.world2pix(wcs,xw,yw)
        self._ax1.scatter(xp,yp,**kwargs)
        
        if layer:
            scatter_set_name = layer
        else:
            self._scatter_counter += 1
            scatter_set_name = 'scatter_set_'+str(self._scatter_counter)
        
        self._name_empty_layers(scatter_set_name)
        
        self.refresh()
    
    def refresh(self):
        self._figure.canvas.draw()
    
    def save(self,saveName,dpi=None,transparent=False):
        
        if dpi == None and os.path.splitext(saveName)[1] in ['.EPS','.eps','.ps','.PS','.Eps','.Ps']:
            width = self._ax1.get_position().width * self._figure.get_figwidth()
            interval = self._ax1.xaxis.get_view_interval()
            nx = interval[1] - interval[0]
            dpi = nx / width
            print "Auto-setting resolution to ",dpi," dpi"
            self._figure.savefig(saveName,dpi=dpi,transparent=transparent)
    
    def _initialize_view(self):
        
        self._ax1.xaxis.set_view_interval(+0.5,self._wcs.naxis1+0.5)
        self._ax1.yaxis.set_view_interval(+0.5,self._wcs.naxis2+0.5)
        self._ax2.xaxis.set_view_interval(+0.5,self._wcs.naxis1+0.5)
        self._ax2.yaxis.set_view_interval(+0.5,self._wcs.naxis2+0.5)
        
        # set the image extent to FITS pixel coordinates
        self._extent = (0.5,self._wcs.naxis1+0.5,0.5,self._wcs.naxis2+0.5)
    
    def _get_invert_default(self):
        return self._figure.apl_grayscale_invert_default
    
    def _get_colormap_default(self):
        return self._figure.apl_colorscale_cmap_default
    
    def set_theme(self,theme='pretty',refresh=True):
        
        if theme=='pretty':
            self.set_frame_color('white',refresh=False)
            self.set_tick_color('white',refresh=False)
            self.set_tick_size(7,refresh=False)
            self._figure.apl_grayscale_invert_default = False
            self._figure.apl_colorscale_cmap_default  = 'jet'
            self.set_grid_color('white')
            self.set_grid_alpha(0.5)
            if self.image:
                self.image.set_cmap(cmap=mpl.cm.get_cmap('jet',1000))
        elif theme=='publication':
            self.set_frame_color('black',refresh=False)
            self.set_tick_color('black',refresh=False)
            self.set_tick_size(7,refresh=False)
            self._figure.apl_grayscale_invert_default = True
            self._figure.apl_colorscale_cmap_default  = 'gist_heat'
            self.set_grid_color('black')
            self.set_grid_alpha(1.0)
            self.image.set_cmap(cmap='jet')
            if self.image:
                self.image.set_cmap(cmap=mpl.cm.get_cmap('gist_yarg',1000))
        
        if refresh: self.refresh()
    
    def set_frame_color(self,color,refresh=True):
        self._ax1.frame.set_edgecolor(color)
        if refresh: self.refresh()