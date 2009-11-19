import warnings

try:
    import pyregion
except ImportError:
    raise Exception("could not import the pyregion sub-package")

try:
    import pyregion.pyparsing
except ImportError:
    raise Exception("could not import the pyparsing sub-package")


import matplotlib


class Regions:
    """
    Regions sub-class of APLpy

    Used for overplotting various shapes and annotations on APLpy
    fitsfigures

    Example:
    # DS9 region file called "test.reg"
    # (the coordinates are around l=28 in the Galactic Plane)
    # Filename: test.fits
    fk5
    box(18:42:48.262,-04:01:17.91,505.668",459.714",0) # color=red dash=1
    point(18:42:51.797,-03:59:44.82) # point=x color=red dash=1
    point(18:42:50.491,-04:03:09.39) # point=box color=red dash=1
    # vector(18:42:37.433,-04:02:10.77,107.966",115.201) vector=1 color=red dash=1
    ellipse(18:42:37.279,-04:02:11.92,26.4336",40.225",0) # color=red dash=1
    polygon(18:42:59.016,-03:58:22.06,18:42:58.219,-03:58:11.30,18:42:57.403,-03:58:35.86,18:42:58.094,-03:58:57.69,18:42:59.861,-03:58:41.60,18:42:59.707,-03:58:23.21) # color=red dash=1
    point(18:42:52.284,-04:00:02.80) # point=diamond color=red dash=1
    point(18:42:46.561,-03:58:01.57) # point=circle color=red dash=1
    point(18:42:42.615,-03:58:25.84) # point=cross color=red dash=1
    point(18:42:42.946,-04:01:44.74) # point=arrow color=red dash=1
    point(18:42:41.961,-03:57:26.16) # point=boxcircle color=red dash=1
    # text(18:42:41.961,-03:57:26.16) text={This is text} color=red

    Code:
    import aplpy
    import regions

    ff = aplpy.FITSFigure("test.fits")
    ff.show_grayscale()
    ff.show_regions('test.reg')

    """

    def show_regions(self, regionfile, layer=False, refresh=True, **kwargs):
        """
        Overplot regions as specified in the regionsfile

        Required Arguments:
            *regionfile*: [ string ]
                Path to a ds9 regions file

        Optional Keyword Arguments:

            *layer*: [ string ]
                The name of the layer
            *refresh*: [ bool ]
                Refresh the figure?

        Additional keyword arguments, e.g. zorder, will be passed to the ds9
        call and onto the patchcollections.
        """

        PC, TC = ds9(regionfile, self._hdu.header, **kwargs)

        #ffpc = self._ax1.add_collection(PC)
        PC.add_to_axes(self._ax1)
        TC.add_to_axes(self._ax1)

        if layer:
            region_set_name = layer
        else:
            self._region_counter += 1
            region_set_name = 'region_set_'+str(self._region_counter)

        self._layers[region_set_name] = PC
        self._layers[region_set_name+"_txt"] = TC

        if refresh:
            self.refresh(force=False)


def ds9(regionfile, header, zorder=3, **kwargs):
    """
    Wrapper to return a PatchCollection given a ds9 region file
    and a fits header.

    zorder - defaults to 3 so that regions are on top of contours
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

    if 'text_offset' in kwargs:
        text_offset = kwargs['text_offset']
        del kwargs['text_offset']
    else:
        text_offset = 5.0

    # grab the shapes to overplot
    pp, aa = rrim.get_mpl_patches_texts(text_offset=text_offset)

    PC = ArtistCollection(pp, **kwargs) # preserves line style (dashed)
    TC = ArtistCollection(aa, **kwargs)
    PC.set_zorder(zorder)
    TC.set_zorder(zorder)

    return PC, TC


class ArtistCollection():
    """
    Matplotlib collections can't handle Text.
    This is a barebones collection for text objects
    that supports removing and making (in)visible
    """

    def __init__(self, artistlist):
        """
        Pass in a list of matplotlib.text.Text objects
        (or possibly any matplotlib Artist will work)
        """
        self.artistlist = artistlist

    def remove(self):
        for T in self.artistlist:
            T.remove()

    def add_to_axes(self, ax):
        for T in self.artistlist:
            ax.add_artist(T)

    def get_visible(self):
        visible = True
        for T in self.artistlist:
            if not T.get_visible():
                visible = False
        return visible

    def set_visible(self, visible=True):
        for T in self.artistlist:
            T.set_visible(visible)

    def set_zorder(self, zorder):
        for T in self.artistlist:
            T.set_zorder(zorder)


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
                return 'none'

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
