APLpy Normalizations
====================

APLpy uses a different set of normalization techniques than other image display tools.
The default options available are ``linear``, ``sqrt``, ``power``, ``log``, and ``arcsinh``.  


Log Scale
---------

In the FITS display program `ds9 <http://hea-www.harvard.edu/RD/ds9/>`_, the log scale is defined by 

.. math::

    y = \frac{\log(ax+1)}{\log(a)}

where ``a`` defaults to 1000 and recommended values are from 100-10000 (see
`<http://hea-www.harvard.edu/RD/ds9/ref/how.html>`_).  In both the ds9 and
APLpy formalism, ``x`` is the normalized data in the range [0,1], i.e.
:math:`x=(x_0-vmin)/(vmax-vmin)`.

APLpy defines the log scale with a ``vmid`` parameter such that

.. math::

    m = (vmax - vmid) / (vmin-vmid)
    y = \frac{\log(x * (m-1) + 1)}{\log(m)}

So the midpoint :math:`m \approx a+1`; the two scalings are *nearly* identical
but specified in different ways, i.e. ``a`` can only be specified indirectly in
APLpy. 

If you want to convert from the ds9 ``a`` parameter to APLpy's ``vmid``
parameter, you can use this formula: 
:math:`vmid = (m*vmin-vmax)/(m-1) \approx ((a+1)*vmin - vmax) / a`


Arcsinh Scale
-------------
The arcsinh scale is defined by

.. math::

    m = (vmid - vmin) / (vmax-vmin)
    y = \frac{\textrm{asinh}(x/m)}{\textrm{asinh}(1/m)}

The DS9 definition is simply :math:`y = \frac{\textrm{asinh}(10x)}{3}`.

Linear Scale
------------
The linear scale is only concerned with the ``vmin`` and ``vmax`` keywords:
:math:`y=(x-vmin)/(vmax-vmin)`

Square Root Scale
-----------------
The square root scale is :math:`y=\sqrt{(x-vmin)/(vmax-vmin)}`

Power Scale
-----------
The power root scale is :math:`y=\left[(x-vmin)/(vmax-vmin)\right]^a` between ``vmin`` and ``vmax``, where
``a`` is passed in as the ``exponent`` keyword.
