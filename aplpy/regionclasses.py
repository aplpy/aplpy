

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
