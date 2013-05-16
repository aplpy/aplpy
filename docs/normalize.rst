APLpy Normalizations
====================

APLpy uses a different set of normalization techniques than other image
display tools. The default options available for the ``stretch`` argument are
``linear``, ``sqrt``, ``power``, ``log``, and ``arcsinh``.

In all cases, the transformations below map the values from the image onto a
scale from 0 to 1 which then corresponds to the endpoints of the colormap
being used.

Log Scale
---------

APLpy defines the log scale with a ``vmid`` parameter such that

.. math::
    y = \frac{\log_{10}(x \cdot (m-1) + 1)}{\log_{10}(m)}

where:

.. math::
    m = \frac{v_{\rm max} - v_{\rm mid}}{v_{\rm min}-v_{\rm mid}}

and:

.. math::
    x=\frac{v-v_{\rm min}}{v_{\rm max}-v_{\rm min}}

and :math:`v` is the image pixel values. Note that :math:`v_{\rm mid}` should
be smaller than :math:`v_{\rm min}`, which means that :math:`m` will always be
larger than one. By default, :math:`v_{\rm mid}=0` and :math:`v_{\rm min}` is
therefore required to be positive (but negative values of :math:`v_{\rm min}`
are allowed if :math:`v_{\rm mid}` is specified).

For reference, in the FITS display program `ds9 <http://hea-www.harvard.edu/RD/ds9/>`_, the
log scale is defined by

.. math::
    y = \frac{\log_{10}(ax+1)}{\log_{10}(a)}

where :math:`a` defaults to 1000 and recommended values are from 100-10000 (see
`here <http://hea-www.harvard.edu/RD/ds9/ref/how.html>`_).

The two stretches are *nearly* (but not completely) identical for :math:`m
\approx a+1`. If you want to convert from the ds9 :math:`a` parameter to
APLpy's :math:`v_{\rm mid}`, you can use this formula:

.. math::
    v_{\rm mid} = \frac{m \cdot v_{\rm min}-v_{\rm max}}{m-1} \approx \frac{(a+1) \cdot v_{\rm min} - v_{\rm max}}{a}


Arcsinh Scale
-------------

The arcsinh scale is defined by

.. math::
    y = \frac{\textrm{asinh}(x/m)}{\textrm{asinh}(1/m)}

where

.. math::
    m = \frac{v_{\rm mid} - v_{\rm min}}{v_{\rm max}-v_{\rm min}}

By default, :math:`v_{\rm mid}` is chosen such that :math:`1/m=-30`.

For reference, the ds9 definition is simply

.. math::
    y = \frac{\textrm{asinh}(10x)}{3}

Linear Scale
------------

The linear scale is only concerned with the ``vmin`` and ``vmax`` keywords:

.. math::
    y=\frac{x-v_{\rm min}}{v_{\rm max}-v_{\rm min}}

Square Root Scale
-----------------

The square root scale is given by

.. math::
    y=\sqrt{\frac{x-v_{\rm min}}{v_{\rm max}-v_{\rm min}}}

Power Scale
-----------

The power root scale is

.. math::
    y=\left[\frac{x-v_{\rm min}}{v_{\rm max}-v_{\rm min}}\right]^a

where :math:`a` is passed in as the ``exponent`` keyword.
