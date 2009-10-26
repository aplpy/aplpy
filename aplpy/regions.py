try:
    import pyparsing
except ImportError:
    raise Exception("pyparsing is required for pyregions, which is needed for ds9 region parsing")
try:
    import pyregion
except ImportError:
    raise Exception("pyregion is required for regions parsing")

import matplotlib

class Regions:
    """
    Regions sub-class of APLpy

    Used for overplotting various shapes and annotations on APLpy
    fitsfigures
    """

    def __init__(self,ff):
        """
        Initialize a Regions file by passing an aplpy.FITSfigure instance
        """
        self.ff = ff
        pass

    def show_regions(self, regionfile, layer=False, refresh=True, **kwargs):
        """
        Overplot regions as specified in the regionsfile
        """

        PC,TC = ds9( regionfile, self.ff._hdu.header, **kwargs)

        ffpc = self.ff._ax1.add_collection(PC)
        TC.add_to_axes(self.ff._ax1)
        # for a in TC: 
        #     self.ff._ax1.add_artist(a)

        if layer:
            region_set_name = layer
        else:
            self.ff._region_counter += 1
            region_set_name = 'region_set_'+str(self.ff._region_counter)

        self.ff._layers[region_set_name] = ffpc
        self.ff._layers[region_set_name+"_txt"] = TC

        if refresh: self.ff.refresh(force=False)


def ds9(regionfile, header, **kwargs):
    """
    Wrapper to return a PatchCollection given a ds9 region file
    and a fits header.

    Does NOT work for text annotation
    """

    # read region file
    rr = pyregion.open(regionfile)

    # convert coordinates to image coordinates
    rrim = rr.as_imagecoord(header)

    # grab the shapes to overplot
    pp,aa = rrim.get_mpl_patches_texts() 

    PC = matplotlib.collections.PatchCollection(pp, match_original=True)
    #TC =  matplotlib.text.Text(aa) 
    TC = TextCollection(aa)

    return PC,TC

class TextCollection():
    """
    Matplotlib collections can't handle Text.  
    This is a barebones collection for text objects
    that supports removing and making (in)visible
    """
    def __init__(self,textlist):
        """
        Pass in a list of matplotlib.text.Text objects
        (or possibly any matplotlib Artist will work)
        """
        self.textlist = textlist
        pass
    def remove(self):
        for T in self.textlist:
            T.remove()
    def add_to_axes(self,ax):
        for T in self.textlist:
            ax.add_artist(T)
    def get_visible(self):
        visible = True
        for T in self.textlist:
            if not T.get_visible():
                visible = False
        return visible
    def set_visible(self,visible=True):
        for T in self.textlist:
            T.set_visible(visible)
