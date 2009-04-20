# Module that looks after plotting a coordinate grid on images

# To improve, create array with e.g. all declination values, insert values which occur at intersections then
# remove all array sections with out of bounds pixel values

from ticks import tick_positions
import numpy as np
from matplotlib.collections import LineCollection

import util

import wcs_util

# can do coarse search to check if any longitude lines are completely contained inside box.
# if not, then has to intersect axis, and so can just do the ones that intersect

class Grid(object):
    
    def _initialize_grid(self):
        
        # Set default parameters for grid
        self._ax1.apl_show_grid = False
        self._ax1.xaxis.apl_grid_spacing = 'auto'
        self._ax1.yaxis.apl_grid_spacing = 'auto'
        
        self._ax1.apl_grid_color = 'white'
        self._ax1.apl_grid_alpha = 0.5
        
        # Set grid event handler
        self._ax1.callbacks.connect('xlim_changed',generate_grid)
        self._ax1.callbacks.connect('ylim_changed',generate_grid)
    
    def set_grid_xspacing(self,xspacing):
        '''
        Set the grid line spacing in the longitudinal direction
        
        Required Arguments:
            
            *xspacing*: [ float | 'auto' ]
                The spacing in the longitudinal direction, in degrees.
                To set the spacing to be automatically determined, set this
                to 'auto'
        '''
        self._ax1.xaxis.apl_grid_spacing = xspacing
        self._ax1 = generate_grid(self._ax1)
        self.refresh()
            
    def set_grid_yspacing(self,yspacing):
        '''
        Set the grid line spacing in the latitudinal direction
        
        Required Arguments:
            
            *yspacing*: [ float | 'auto' ]
                The spacing in the latitudinal direction, in degrees.
                To set the spacing to be automatically determined, set this
                to 'auto'
        '''
        self._ax1.yaxis.apl_grid_spacing = yspacing    
        self._ax1 = generate_grid(self._ax1)
        self.refresh()
        
    def set_grid_color(self,color):
        '''
        Set the color of the grid lines
        
        Required Arguments:
        
            *color*: [ string ]
                The color of the grid lines
        '''
        self._ax1.apl_grid_color = color
        self._ax1 = generate_grid(self._ax1)
        self.refresh()
    
    def set_grid_alpha(self,alpha):
        '''
        Set the alpha (transparency) of the grid lines
        
        Required Arguments:
        
            *alpha*: [ float ]
                The alpha value of the grid. This should be a floating
                point value between 0 and 1, where 0 is completely
                transparent, and 1 is completely opaque.
        '''
        self._ax1.apl_grid_alpha = alpha
        self._ax1 = generate_grid(self._ax1)
        self.refresh()
    
    def show_grid(self):
        '''
        Overlay the coordinate grid
        '''
        
        self._ax1.apl_show_grid = True
        self._ax1 = generate_grid(self._ax1)
        self.refresh()
    
    def hide_grid(self):
        '''
        Hide the coordinate grid
        '''
        
        self._ax1.apl_show_grid = False
        self._ax1 = generate_grid(self._ax1)
        self.refresh()

##########################################################
# plot_grid: the main routine to plot a coordinate grid
##########################################################

def generate_grid(ax):
    
    if ax.apl_show_grid:
        
        wcs = ax.apl_wcs
        
        polygons_out = []
        
        if ax.xaxis.apl_grid_spacing == 'auto':
            xspacing = ax.xaxis.apl_spacing_default
        else:
            xspacing = ax.xaxis.apl_grid_spacing
        
        if ax.yaxis.apl_grid_spacing == 'auto':
            yspacing = ax.yaxis.apl_spacing_default
        else:
            yspacing = ax.yaxis.apl_grid_spacing
        
        # Find longitude lines that intersect with axes
        lon_i,lat_i = find_intersections(wcs,'x',xspacing)
        
        lon_i_unique = np.array(list(set(lon_i)))
        
        # Plot those lines
        for l in lon_i_unique:
            for line in plot_longitude(wcs,lon_i,lat_i,l):
                polygons_out.append(line)
        
        # Find longitude lines that don't intersect with axes
        lon_all = util.complete_range(0.0,360.0,xspacing)
        lon_ni  = np.sort(np.array(list(set(lon_all)-set(lon_i_unique))))
        lat_ni  = np.ones(np.size(lon_ni)) # doesn't matter what value is, is either in or outside
        
        if np.size(lon_ni) > 0:
            
            xpix,ypix = wcs_util.world2pix(wcs,lon_ni,lat_ni)
            
            # Plot those lines
    #        for i in range(0,np.size(lon_ni)):
    #            if(in_plot(wcs,xpix[i],ypix[i])):
    #                print "Inside longitude : "+str(lon_ni[i])
    #                plot_longitude(wcs,np.array([]),np.array([]),lon_ni[i])
            
            # Find latitude lines that intersect with axes
        lon_i,lat_i = find_intersections(wcs,'y',yspacing)
        
        lat_i_unique = np.array(list(set(lat_i)))
        
        # Plot those lines
        for l in lat_i_unique:
            for line in plot_latitude(wcs,lon_i,lat_i,l):
                polygons_out.append(line)
        
        # Find latitude lines that don't intersect with axes
        lat_all = util.complete_range(-90.0,90.0,yspacing)
        lat_ni  = np.sort(np.array(list(set(lat_all)-set(lat_i_unique))))
        lon_ni  = np.ones(np.size(lat_ni)) # doesn't matter what value is, is either in or outside
        
        if np.size(lat_ni) > 0:
            
            xpix,ypix = wcs_util.world2pix(wcs,lon_ni,lat_ni)
            
            # Plot those lines
    #        for i in range(0,np.size(lat_ni)):
    #            if(in_plot(wcs,xpix[i],ypix[i])):
    #                print "Inside latitude : "+str(lat_ni[i])
    #                plot_latitude(wcs,np.array([]),np.array([]),lat_ni[i])
        
        grid_id = -1
        
        for i in range(len(ax.collections)):
            if is_grid(ax.collections[i]):
                grid_id=i
                break
        
        print "Grid ID = "+str(grid_id)
        
        if grid_id >= 0:
            ax.collections[grid_id].set_verts(polygons_out)
            ax.collections[grid_id].set_edgecolor(ax.apl_grid_color)
            ax.collections[grid_id].set_alpha(ax.apl_grid_alpha)
        else:
            c = LineCollection(polygons_out,transOffset=ax.transData,edgecolor=ax.apl_grid_color,alpha=ax.apl_grid_alpha)
            c.grid = True
            ax.add_collection(c,False)
    
    else:
        
        for i in range(len(ax.collections)):
            if is_grid(ax.collections[i]):
                ax.collections.pop(i)
                break
    
    return ax

def is_grid(collection):
    try:
        grid = collection.grid
    except AttributeError:
        return False
    return True

##########################################################
# plot_latitude: plot a single latitude line
##########################################################

def plot_latitude(wcs,lon,lat,lat0,alpha=0.5):
    
    lines_out = []
    
    # Check if the point with coordinates (0,lat0) is inside the viewport
    xpix,ypix = wcs_util.world2pix(wcs,0.,lat0)
    
    if in_plot(wcs,xpix,ypix):
        lon_min = 0.
        inside  = True
    else:
        inside  = False
    
    # Find intersections that correspond to latitude lat0
    index  = np.where(lat==lat0)
    
    # Produce sorted array of the longitudes of all intersections
    lonnew = np.sort(lon[index])
    
    # Cycle through intersections
    for l in lonnew:
        
        # If inside, then current intersection closes arc - plot it
        if(inside):
            lon_max = l
            x_world = util.complete_range(lon_min,lon_max,360) # Plotting every degree, make more general
            y_world = np.ones(len(x_world)) * lat0
            x_pix,y_pix = wcs_util.world2pix(wcs,x_world,y_world)
            lines_out.append(zip(x_pix,y_pix))
            inside = False
        else:
            lon_min = l
            inside = True
    
    # If still inside when finished going through intersections, then close at longitude 360
    if(inside):
        lon_max = 360.
        x_world = util.complete_range(lon_min,lon_max,360)
        y_world = np.ones(len(x_world)) * lat0
        x_pix,y_pix = wcs_util.world2pix(wcs,x_world,y_world)
        lines_out.append(zip(x_pix,y_pix))
        inside = False
    
    return lines_out

##########################################################
# plot_longitude: plot a single longitude line
##########################################################

def plot_longitude(wcs,lon,lat,lon0,alpha=0.5):
    
    lines_out = []
    
    # Check if the point with coordinates (10.,-90.) is inside the viewport
    xpix,ypix = wcs_util.world2pix(wcs,10.,-90.)
    
    if in_plot(wcs,xpix,ypix):
        lat_min = -90.
        inside  = True
    else:
        inside  = False
    # Find intersections that correspond to longitude lon0
    index = np.where(lon==lon0)
    
    # Produce sorted array of the latitudes of all intersections
    latnew = np.sort(lat[index])
    
    # Cycle through intersections
    for l in latnew:
        if(inside):
            lat_max = l
            y_world = util.complete_range(lat_min,lat_max,360)
            x_world = np.ones(len(y_world)) * lon0
            x_pix,y_pix = wcs_util.world2pix(wcs,x_world,y_world)
            lines_out.append(zip(x_pix,y_pix))
            inside = False
        else:
            lat_min = l
            inside = True
    
    if(inside):
        lat_max = 90.
        y_world = util.complete_range(lat_min,lat_max,360)
        x_world = np.ones(len(y_world)) * lon0
        x_pix,y_pix = wcs_util.world2pix(wcs,x_world,y_world)
        lines_out.append(zip(x_pix,y_pix))
        inside = False
    
    return lines_out

##########################################################
# in_plot: whether a given point is in a plot
##########################################################

def in_plot(wcs,x_pix,y_pix):
  return x_pix > +0.5 and x_pix < wcs.naxis1+0.5 and y_pix > +0.5 and y_pix < wcs.naxis2+0.5

##########################################################
# find_intersections: find intersections of a given
#                     coordinate with a all axes.
##########################################################

def find_intersections(wcs,coord,spacing):
    
    # Initialize arrays
    x = []
    y = []
    
    # Bottom X axis
    (labels_x,labels_y,world_x,world_y) = tick_positions(wcs,spacing,'x',coord,farside=False)
    for i in range(0,len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])
    
    # Top X axis
    (labels_x,labels_y,world_x,world_y) = tick_positions(wcs,spacing,'x',coord,farside=True)
    for i in range(0,len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])
    
    # Left Y axis
    (labels_x,labels_y,world_x,world_y) = tick_positions(wcs,spacing,'y',coord,farside=False)
    for i in range(0,len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])
    
    # Right Y axis
    (labels_x,labels_y,world_x,world_y) = tick_positions(wcs,spacing,'y',coord,farside=True)
    for i in range(0,len(world_x)):
        x.append(world_x[i])
        y.append(world_y[i])
    
    return np.array(x),np.array(y)
    
    ##########################################################
        
        
