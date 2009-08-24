from mpl_toolkits.axes_grid.anchored_artists \
    import AnchoredEllipse

import wcs_util


class Beam(object):

    def show_beam(self, major='BMAJ', minor='BMIN', \
        angle='BPA', corner=3, frame=False, **kwargs):

        '''
        Display the beam shape and size for the primary image

        By default, this method will search for the BMAJ, BMIN, and BPA
        keywords in the FITS header to set the major and minor axes and the
        position angle on the sky.

        Optional Keyword Arguments:

            *major*: [ float ]
                Major axis of the beam in degrees (overrides BMAJ if present)

            *minor*: [ float ]
                Minor axis of the beam in degrees (overrides BMIN if present)

            *angle*: [ float ]
                Position angle of the beam on the sky in degrees (overrides
                BPA if present)

            *corner*: [ integer ]
                Where to place the beam. Acceptable values are:
                1: top right
                2: top left
                3: bottom left (default)
                4: bottom right
                5: center right
                6: center left
                7: center right (same as 5)
                8: bottom center
                9: top center

            *frame*: [ True | False ]
                Whether to display a frame behind the beam (default is False)

            Additional arguments can be used to control the appearance of the
            beam (more information soon)

        '''

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
            loc=corner, pad=0.5, borderpad=0.4, frameon=frame)

        self._ax1.add_artist(self._ax1._beam)

        self._ax1._beam.ellipse.set(**kwargs)

        self.refresh()

    def hide_beam(self):
        '''
        Hide the beam
        '''
        try:
            self._ax1._beam.remove()
        except:
            pass

        self.refresh()

    def set_beam_properties(self, refresh=True, **kwargs):

        self._ax1._beam.ellipse.set(**kwargs)
        if refresh:
            self.refresh()
