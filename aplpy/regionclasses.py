import matplotlib

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
