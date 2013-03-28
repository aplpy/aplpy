Installing Montage
------------------

Montage is a package developed by IPAC designed to handle the
reprojection of FITS files. APLpy relies on Montage for several functions,
such as :func:`~aplpy.rgb.make_rgb_cube` or the ``north=True``
argument in :class:`~aplpy.aplpy.FITSFigure`. To use these features,
Montage needs to be installed.
    
Obtaining and installing Montage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
Montage can be downloaded from
http://montage.ipac.caltech.edu/docs/download.html

Installation instructions are provided at
http://montage.ipac.caltech.edu/docs/build.html

Once Montage is
correctly installed, you are ready to use the Montage-dependent
features of APLpy!
