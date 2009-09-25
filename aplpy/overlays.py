from mpl_toolkits.axes_grid.anchored_artists \
    import AnchoredEllipse, AnchoredSizeBar

import wcs_util


class ScaleBar(object):

    def show_scalebar(self, length, label=None, corner=4, frame=False, **kwargs):
        '''
        Display a scalebar

        Required Arguments:

            *length*:[ float ]
                The length of the scalebar, in degrees

        Optional Keyword Arguments:

            *label*: [ string ]
                Label to place above the scalebar

            *corner*: [ integer ]
                Where to place the scalebar. Acceptable values are:
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
                Whether to display a frame behind the scalebar (default is False)

            Additional keyword arguments can be used to control the appearance
            of the scalebar, which is made up of an instance of the matplotlib
            Rectangle class and a an instance of the Text class. For more
            information on available arguments, see

            `Rectangle <http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.patches.Rectangle>`_

            and

            `Text <http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.text.Text>`_`.

            In cases where the same argument exists for the two objects, the
            argument is passed to both the Text and Rectangle instance

        '''

        degperpix = wcs_util.degperpix(self._wcs)

        length = length / degperpix

        try:
            self._ax1._scalebar.remove()
        except:
            pass

        self._ax1._scalebar = AnchoredSizeBar(self._ax1.transData, length, label, corner, \
                              pad=0.5, borderpad=0.4, sep=5, frameon=frame)

        self._ax1.add_artist(self._ax1._scalebar)

        self.set_scalebar_properties(**kwargs)

        self.refresh(force=False)

    def hide_scalebar(self):
        '''
        Hide the scalebar
        '''
        try:
            self._ax1._scalebar.remove()
        except:
            pass

        self.refresh(force=False)

    def set_scalebar_properties(self, **kwargs):
        '''
        Modify the scalebar properties

        All arguments are passed to the scalebar, which is made up of an
        instance of the matplotlib Rectangle class and a an instance of the
        Text class. For more information on available arguments, see

        `Rectangle <http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.patches.Rectangle>`_

        and

        `Text <http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.text.Text>`_`.

        In cases where the same argument exists for the two objects, the
        argument is passed to both the Text and Rectangle instance
        '''

        for kwarg in kwargs:

            args = {kwarg: kwargs[kwarg]}

            try:
                self._ax1._scalebar.size_bar.get_children()[0].set(**args)
            except AttributeError:
                pass

            try:
                self._ax1._scalebar.txt_label.get_children()[0].set(**args)
            except AttributeError:
                pass

        self.refresh(force=False)


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

            Additional keyword arguments can be used to control the appearance
            of the beam, which is an instance of the matplotlib Ellipse class.
            For more information on available arguments, see `Ellipse
            <http://matplotlib.sourceforge.net/api/artist_api.html
            #matplotlib.patches.Ellipse>`_.

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

        self.refresh(force=False)

    def hide_beam(self):
        '''
        Hide the beam
        '''
        try:
            self._ax1._beam.remove()
        except:
            pass

        self.refresh(force=False)

    def set_beam_properties(self, **kwargs):
        '''
        Modify the beam properties

        All arguments are passed to the beam, which is an instance of the
        matplotlib Ellipse class. For more information on available arguments,
        see `Ellipse <http://matplotlib.sourceforge.net/api/artist_api.html
        #matplotlib.patches.Ellipse>`_.
        '''

        self._ax1._beam.ellipse.set(**kwargs)
        self.refresh(force=False)
