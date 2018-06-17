from __future__ import absolute_import, print_function, division

import numpy as np

from .helpers import ASTROPY_LT_31

__all__ = ['WCSAxes']

# This is a backport of a change in Astropy 3.1 that makes contour drawing
# much faster - without this drawing contours is far too slow.

if ASTROPY_LT_31:

    def transform_contour_set_inplace(cset, transform):
        """
        Transform a contour set in-place using a specified
        :class:`matplotlib.transform.Transform`

        Using transforms with the native Matplotlib contour/contourf can be
        slow if the transforms have a non-negligible overhead (which is the
        case for WCS/Skycoord transforms) since the transform is called for
        each individual contour line. It is more efficient to stack all the
        contour lines together temporarily and transform them in one go.
        """

        # The contours are represented as paths grouped into levels. Each can
        # have one or more paths. The approach we take here is to stack the
        # vertices of all paths and transform them in one go. The pos_level
        # list helps us keep track of where the set of segments for each
        # overall contour level ends. The pos_segments list helps us keep track
        # of where each segment ends for each contour level.
        all_paths = []
        pos_level = []
        pos_segments = []

        for collection in cset.collections:

            paths = collection.get_paths()
            all_paths.append(paths)

            # The last item in pos isn't needed for np.split and in fact causes
            # issues if we keep it because it will cause an extra empty array
            # to be returned.
            pos = np.cumsum([len(x) for x in paths])
            pos_segments.append(pos[:-1])
            pos_level.append(pos[-1])

        # As above the last item isn't needed
        pos_level = np.cumsum(pos_level)[:-1]

        # Stack all the segments into a single (n, 2) array
        vertices = np.vstack(path.vertices for paths in all_paths for path in paths)

        # Transform all coordinates in one go
        vertices = transform.transform(vertices)

        # Split up into levels again
        vertices = np.split(vertices, pos_level)

        # Now re-populate the segments in the line collections
        for ilevel, vert in enumerate(vertices):
            vert = np.split(vert, pos_segments[ilevel])
            for iseg in range(len(vert)):
                all_paths[ilevel][iseg].vertices = vert[iseg]

    from astropy.visualization.wcsaxes import WCSAxes as _WCSAxes

    class WCSAxes(_WCSAxes):

        def contour(self, *args, **kwargs):

            # In Matplotlib, when calling contour() with a transform, each
            # individual path in the contour map is transformed separately.
            # However, this is much too slow for us since each call to the
            # transforms results in an Astropy coordinate transformation, which
            # has a non-negligeable overhead - therefore a better approach is
            # to override contour(), call the Matplotlib one with no transform,
            # then apply the transform in one go to all the segments that make
            # up the contour map.

            transform = kwargs.pop('transform', None)

            cset = super(WCSAxes, self).contour(*args, **kwargs)

            if transform is not None:
                # The transform passed to self.contour will normally include a
                # transData component at the end, but we can remove that since
                # we are already working in data space.
                transform = transform - self.transData
                cset = transform_contour_set_inplace(cset, transform)

            return cset

        def contourf(self, *args, **kwargs):

            # See notes for contour above.

            transform = kwargs.pop('transform', None)

            cset = super(WCSAxes, self).contourf(*args, **kwargs)

            if transform is not None:
                # The transform passed to self.contour will normally include a
                # transData component at the end, but we can remove that since
                # we are already working in data space.
                transform = transform - self.transData
                cset = transform_contour_set_inplace(cset, transform)

            return cset

else:

    from astropy.visualization.wcsaxes import WCSAxes
