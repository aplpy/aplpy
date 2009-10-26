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

        PC = ds9( regionfile, self.ff._hdu.header, **kwargs)

        ffpc = self.ff._ax1.add_collection(PC)

        if layer:
            ds9_set_name = layer
        else:
            self.ff._ds9_counter += 1
            ds9_set_name = 'ds9_set_'+str(self.ff._ds9_counter)

        self.ff._layers[ds9_set_name] = ffpc

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

    return PC

