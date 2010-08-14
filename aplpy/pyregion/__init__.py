from ds9_region_parser import RegionParser
from wcs_helper import check_wcs as _check_wcs
from itertools import cycle, izip

try: # need to set _open_builtin to the original built-in open function
    # however, if you "reload pyregion", it will lead to infinite recursion
    if (_open_builtin == open):
        pass
except NameError:
    _open_builtin = open

class ShapeList(list):
    def __init__(self, *ka, **kw):
        self._comment_list = kw.pop("comment_list", None)
        list.__init__(self, *ka, **kw)

    def check_imagecoord(self):
        if [s for s in self if s.coord_format != "image"]:
            return False
        else:
            return True

    def as_imagecoord(self, header):
        """
        Return a new ShapeList where the coordinate of the each shape
        is converted to the image coordinate using the given header
        information
        """

        comment_list = self._comment_list
        if comment_list is None:
            comment_list = cycle([None])

        r = RegionParser.sky_to_image(izip(self, comment_list),
                                      header)
        shape_list, comment_list = zip(*list(r))
        return ShapeList(shape_list, comment_list=comment_list)


    def get_mpl_patches_texts(self, properties_func=None, text_offset=5.0):
        from mpl_helper import as_mpl_artists
        patches, txts = as_mpl_artists(self, properties_func, text_offset)

        return patches, txts

    def get_filter(self, header=None):
        from region_to_filter import as_region_filter

        if header is None:
            if not self.check_imagecoord():
                raise RuntimeError("the region has non-image coordinate. header is required.")
            reg_in_imagecoord = self
        else:
            reg_in_imagecoord = self.as_imagecoord(header)

        region_filter = as_region_filter(reg_in_imagecoord)

        return region_filter


    def get_mask(self, hdu=None, header=None, shape=None):
        """
        creates a 2-d mask.

        get_mask(hdu=f[0])
        get_mask(shape=(10,10))
        get_mask(header=f[0].header, shape=(10,10))
        """

        if hdu and header is None:
            header = hdu.header
        if hdu and shape is None:
            shape = hdu.data.shape

        region_filter = self.get_filter(header=header)
        mask = region_filter.mask(shape)

        return mask

    def write(self,outfile):
        """ Writes the current shape list out as a region file """
        
        myopen = _open_builtin
        outf = myopen(outfile,'w')

        attr0 = self[0].attr[1]
        defaultline = " ".join(["%s=%s" % (a,attr0[a]) for a in attr0 if a!='text'])

        # first line is globals
        print >>outf,"global",defaultline
        # second line must be a coordinate format
        print >>outf,self[0].coord_format

        for shape in self:
            text_coordlist = ["%f" % f for f in shape.coord_list]
            print >>outf, \
                shape.name + "(" + ",".join(text_coordlist) + ") # " + shape.comment

        outf.close()


def parse(region_string):
    """
    Parse the input string of a ds9 region definition.
    Returns a list of Shape instances.
    """
    rp = RegionParser()
    ss = rp.parse(region_string)
    sss1 = rp.convert_attr(ss)
    sss2 = _check_wcs(sss1)

    shape_list, comment_list = rp.filter_shape2(sss2)
    return ShapeList(shape_list, comment_list=comment_list)

def open(fname):
    region_string = _open_builtin(fname).read()
    return parse(region_string)


# def parse_deprecated(region_string):
#     rp = RegionParser()
#     return rp.parseString(region_string)


def read_region(s):
    rp = RegionParser()
    ss = rp.parse(s)
    sss1 = rp.convert_attr(ss)
    sss2 = _check_wcs(sss1)

    return rp.filter_shape(sss2)


def read_region_as_imagecoord(s, header):
    rp = RegionParser()
    ss = rp.parse(s)
    sss1 = rp.convert_attr(ss)
    sss2 = _check_wcs(sss1)
    sss3 = rp.sky_to_image(sss2, header)

    return rp.filter_shape(sss3)



def get_mask(region, hdu):
    """
    f = pyfits.read("test.fits")
    reg = read_region_as_imagecoord(s, f[0].header)
    mask = get_mask(reg, f[0])
    """

    from pyregion.region_to_filter import as_region_filter

    data = hdu.data
    header = hdu.header

    region_filter = as_region_filter(region)

    mask = region_filter.mask(data)

    return mask


if __name__ == '__main__':
    #reg = pyregion.open("../mos_fov.reg")
    import pyregion
    proposed_fov = 'fk5;circle(290.96388,14.019167,843.31194")'
    reg = pyregion.parse(proposed_fov)
    reg_imagecoord = reg.as_imagecoord(header)
    patches, txts = reg.get_mpl_patches_texts()
    m = reg.get_mask(hdu=f[0])

