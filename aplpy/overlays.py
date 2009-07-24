try:
    from mpl_toolkits.axes_grid.anchored_artists \
        import AnchoredEllipse
    tk_installed = True
except:
    tk_installed = False
    print "WARNING - mpl_toolkits not installed - beam methods disabled"

import wcs_util


class Beam(object):

    def show_beam(self, major='BMAJ', minor='BMIN', \
        angle='BPA', corner=3, **kwargs):

        if not tk_installed:
            raise Exception("Beam methods disabled since mpl_toolkits is not installed")

        if type(major) == str:
            major = self._hdu.header[major]

        if type(minor) == str:
            minor = self._hdu.header[minor]

        if type(angle) == str:
            angle = self._hdu.header[angle]

        degperpix = wcs_util.degperpix(self._wcs)

        self.minor = minor / degperpix
        self.major = major / degperpix

        try:
            self._ax1._beam.remove()
        except:
            pass

        self._ax1._beam = AnchoredEllipse(self._ax1.transData, \
            width=self.major, height=self.minor, angle=angle, \
            loc=corner, pad=0.5, borderpad=0.4, frameon=False)

        self._ax1.add_artist(self._ax1._beam)

        self.refresh()

    def hide_beam(self):
        try:
            self._ax1._beam.remove()
        except:
            pass

        self.refresh()

    def set_beam_properties(self, refresh=True, **kwargs):

        self._ax1._beam.set(**kwargs)
        if refresh:
            self.refresh()
