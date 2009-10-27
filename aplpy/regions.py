try:
    import pyparsing
except ImportError:
    raise Exception("pyparsing is required for pyregions, which is needed for ds9 region parsing")
try:
    import pyregion
except ImportError:
    raise Exception("pyregion is required for regions parsing")

import matplotlib
import numpy

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
    """

    # read region file
    rr = pyregion.open(regionfile)

    # convert coordinates to image coordinates
    rrim = rr.as_imagecoord(header)

    # pyregion and aplpy both correct for the FITS standard origin=1,1
    # need to avoid double-correcting
    for r in rrim:
        r.coord_list[0] += 1
        r.coord_list[1] += 1

    # grab the shapes to overplot
    pp,aa = rrim.get_mpl_patches_texts() 

    PC = PatchCollection2(pp, match_original=True) # preserves line style (dashed)
    TC = ArtistCollection(aa)

    return PC,TC

class ArtistCollection():
    """
    Matplotlib collections can't handle Text.  
    This is a barebones collection for text objects
    that supports removing and making (in)visible
    """
    def __init__(self,artistlist):
        """
        Pass in a list of matplotlib.text.Text objects
        (or possibly any matplotlib Artist will work)
        """
        self.artistlist = artistlist
    def remove(self):
        for T in self.artistlist:
            T.remove()
    def add_to_axes(self,ax):
        for T in self.artistlist:
            ax.add_artist(T)
    def get_visible(self):
        visible = True
        for T in self.artistlist:
            if not T.get_visible():
                visible = False
        return visible
    def set_visible(self,visible=True):
        for T in self.artistlist:
            T.set_visible(visible)

class PatchCollection2(matplotlib.collections.Collection):
    """
    A generic collection of patches.

    This makes it easier to assign a color map to a heterogeneous
    collection of patches.

    This also may improve plotting speed, since PatchCollection will
    draw faster than a large number of patches.
    """

    def __init__(self, patches, match_original=True, **kwargs):
        """
        *patches*
            a sequence of Patch objects.  This list may include
            a heterogeneous assortment of different patch types.

        *match_original*
            If True, use the colors and linewidths of the original
            patches.  If False, new colors may be assigned by
            providing the standard collection arguments, facecolor,
            edgecolor, linewidths, norm or cmap.

        If any of *edgecolors*, *facecolors*, *linewidths*,
        *antialiaseds* are None, they default to their
        :data:`matplotlib.rcParams` patch setting, in sequence form.

        The use of :class:`~matplotlib.cm.ScalarMappable` is optional.
        If the :class:`~matplotlib.cm.ScalarMappable` matrix _A is not
        None (ie a call to set_array has been made), at draw time a
        call to scalar mappable will be made to set the face colors.
        """

        if match_original:
            def determine_facecolor(patch):
                if patch.fill:
                    return patch.get_facecolor()
                return [0, 0, 0, 0]

            facecolors   = [determine_facecolor(p) for p in patches]
            edgecolors   = [p.get_edgecolor() for p in patches]
            linewidths   = [p.get_linewidth() for p in patches]
            linestyles   = [p.get_linestyle() for p in patches]
            antialiaseds = [p.get_antialiased() for p in patches]

            matplotlib.collections.Collection.__init__(
                self,
                edgecolors=edgecolors,
                facecolors=facecolors,
                linewidths=linewidths,
                linestyles=linestyles,
                antialiaseds = antialiaseds)
        else:
            matplotlib.collections.Collection.__init__(self, **kwargs)

        self.set_paths(patches)

    def set_paths(self, patches):
        paths = [p.get_transform().transform_path(p.get_path())
                        for p in patches]
        self._paths = paths
